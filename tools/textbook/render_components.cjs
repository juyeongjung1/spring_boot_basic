// HTMLカードを行の境界で分割し、文字を保持した個別PDFへ出力する。
const fs = require('node:fs/promises');
const path = require('node:path');
const { chromium } = require('playwright');

const EDGE = 'C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe';
const MAX_HEIGHT = 620;
const PX_PER_PT = 96 / 72;

function documentHtml(body, css, width, height) {
  const pageSize = height === undefined ? '' : `@page { size: ${width}pt ${height}pt; margin: 0; }`;
  return `<!doctype html><html lang="ja"><head><meta charset="utf-8"><style>${css}
    ${pageSize}
    html, body { margin: 0; padding: 0; background: #fff; }
    #component-root { width: ${width}pt; }
    #component-root > .card { width: ${width}pt; margin: 0; box-sizing: border-box; }
    </style></head><body><main id="component-root">${body}</main></body></html>`;
}

async function main() {
  if (process.argv.length !== 3) throw new Error('使用方法: node render_components.cjs 入力JSON');
  const inputPath = path.resolve(process.argv[2]);
  const input = JSON.parse(await fs.readFile(inputPath, 'utf8'));
  if (!input.output_dir || !Array.isArray(input.cards)) throw new Error('output_dir と cards が必要です。');
  const outputDir = path.resolve(input.output_dir);
  await fs.mkdir(outputDir, { recursive: true });
  const css = await fs.readFile(path.join(__dirname, 'components.css'), 'utf8');
  const results = { cards: [] };
  const browser = await chromium.launch({ executablePath: EDGE, headless: true });
  try {
    const page = await browser.newPage();
    await page.emulateMedia({ media: 'print' });
    for (const [index, card] of input.cards.entries()) {
      if (typeof card.id !== 'string' || !card.id || typeof card.html !== 'string'
          || !Number.isFinite(card.width) || card.width <= 0) {
        throw new Error(`カード ${card.id ?? index}: id/html/正のwidthが必要です。`);
      }
      await page.setViewportSize({ width: Math.ceil(card.width * PX_PER_PT), height: 1200 });
      await page.setContent(documentHtml(card.html, css, card.width), { waitUntil: 'load' });
      await page.evaluate(() => document.fonts.ready);
      const fragments = await page.evaluate(({ id, maximum, scale }) => {
        const root = document.querySelector('#component-root');
        const template = root.querySelector('.card');
        if (!template) throw new Error(`カード ${id}: .card がありません。`);
        const rows = element => Array.from(element.querySelectorAll('[data-break-row]'))
          .filter(row => !row.parentElement.closest('[data-break-row]'));
        const originals = rows(template);
        function candidate(start, end, continued, last) {
          const clone = template.cloneNode(true);
          rows(clone).forEach((row, i) => { if (i < start || i >= end) row.remove(); });
          if (!last) clone.querySelectorAll('.card-footer').forEach(footer => footer.remove());
          let continuation = clone.querySelector('.card-header .continuation');
          if (continued && !continuation) {
            continuation = document.createElement('span');
            continuation.className = 'continuation';
            clone.querySelector('.card-header')?.append(continuation);
          }
          if (continuation) continuation.textContent = continued ? '続き' : '';
          root.replaceChildren(clone);
          return { html: clone.outerHTML, height: clone.getBoundingClientRect().height / scale };
        }
        const fits = part => part.height <= maximum;
        const all = candidate(0, originals.length, false, true);
        if (fits(all)) return [all];
        if (!originals.length) throw new Error(`カード ${id}: ${maximum}ptを超えていますが分割できる行がありません。`);
        const parts = [];
        let start = 0;
        while (start < originals.length) {
          const last = candidate(start, originals.length, parts.length > 0, true);
          if (fits(last)) { parts.push(last); break; }
          let low = start + 1, high = originals.length - 1, best = null, bestEnd = start;
          while (low <= high) {
            const middle = Math.floor((low + high) / 2);
            const part = candidate(start, middle, parts.length > 0, false);
            if (fits(part)) { best = part; bestEnd = middle; low = middle + 1; }
            else high = middle - 1;
          }
          if (!best) {
            const row = originals[start];
            const rowId = row.dataset.sourceIds || row.id || `行${start + 1}`;
            throw new Error(`カード ${id} / ${rowId}: 1行が見出し・余白を含めて${maximum}ptに収まりません。`);
          }
          parts.push(best);
          start = bestEnd;
        }
        return parts;
      }, { id: card.id, maximum: MAX_HEIGHT, scale: PX_PER_PT });

      const rendered = { id: card.id, parts: [] };
      const slug = card.id.replace(/[^\p{L}\p{N}_.-]+/gu, '-').slice(0, 100);
      for (const [partIndex, fragment] of fragments.entries()) {
        // Chromiumの用紙寸法の丸めに備え、下端へ1 CSS px分を確保する。
        const height = Math.ceil((fragment.height + .75) * 1000) / 1000;
        await page.setContent(documentHtml(fragment.html, css, card.width, height), { waitUntil: 'load' });
        await page.evaluate(() => document.fonts.ready);
        const measurement = await page.evaluate(({ scale, id }) => {
          const card = document.querySelector('#component-root > .card');
          const origin = card.getBoundingClientRect();
          const anchors = {};
          for (const element of card.querySelectorAll('th, td, pre.source-code')) {
            if (element.scrollWidth > element.clientWidth + 2) {
              const source = element.closest('[data-source-ids]')?.dataset.sourceIds || id;
              throw new Error(`カード ${id} / ${source}: ${element.tagName}の内容が横幅からはみ出しています。`);
            }
          }
          const elements = [card, ...card.querySelectorAll('[data-source-ids]')];
          const pt = value => Math.round(value / scale * 1e6) / 1e6;
          for (const element of elements) {
            const rect = element.getBoundingClientRect();
            if (!rect.width || !rect.height || !element.dataset.sourceIds) continue;
            for (const id of element.dataset.sourceIds.split(',').map(s => s.trim()).filter(Boolean)) {
              const box = { x0: pt(rect.left - origin.left), y0: pt(rect.top - origin.top),
                x1: pt(rect.right - origin.left), y1: pt(rect.bottom - origin.top) };
              const old = anchors[id];
              anchors[id] = old ? { x0: Math.min(old.x0, box.x0), y0: Math.min(old.y0, box.y0),
                x1: Math.max(old.x1, box.x1), y1: Math.max(old.y1, box.y1) } : box;
            }
          }
          return { text: card.innerText, anchors };
        }, { scale: PX_PER_PT, id: card.id });
        const pdf = path.join(outputDir, `${String(index + 1).padStart(4, '0')}-${slug}-${partIndex + 1}.pdf`);
        await page.pdf({ path: pdf, width: `${card.width / 72}in`, height: `${height / 72}in`,
          margin: { top: 0, right: 0, bottom: 0, left: 0 },
          printBackground: true, preferCSSPageSize: true, displayHeaderFooter: false });
        rendered.parts.push({ pdf, width: card.width, height, ...measurement });
      }
      results.cards.push(rendered);
    }
  } finally {
    await browser.close();
  }
  await fs.writeFile(path.join(outputDir, 'results.json'), JSON.stringify(results, null, 2) + '\n', 'utf8');
  console.log(`カード${results.cards.length}件を出力: ${path.join(outputDir, 'results.json')}`);
}

main().catch(error => { console.error(error.stack || error.message); process.exitCode = 1; });
