"""Java 21/Boot 4.0.2の本文教材アプリを、指定したMySQLに接続してHTTP確認する。"""
from pathlib import Path
import argparse
import http.cookiejar
import json
import os
import re
import subprocess
import shutil
import socket
import uuid
import time
import urllib.error
import urllib.parse
import urllib.request

ROOT=Path(__file__).resolve().parents[2]


def sql(query):
    env=dict(os.environ,MYSQL_PWD=ENV['sample_password'])
    args=[str(MYSQL),'--host='+ENV['mysql_host'],'--port='+str(ENV['mysql_port']),
          '--user='+ENV['sample_user'],'--default-character-set=utf8mb4','--batch','--skip-column-names',ENV['sample_database'],'-e',query]
    return subprocess.check_output(args,env=env,encoding='utf-8',stderr=subprocess.STDOUT).strip()


def delete_created(marker):
    # 生成した一意名とその更新後の名前だけを照合し、作成した行だけを削除する。
    names="'"+marker+"','"+marker+"_UPDATED'"
    for value in sql('SELECT id FROM product WHERE name IN ('+names+')').splitlines():
        sql('DELETE FROM product WHERE id='+str(int(value))+' AND name IN ('+names+')')


def run_app(group,app,port):
    # 使用中の別アプリへ誤ってテスト要求を送らない。
    with socket.socket() as probe:probe.bind(('127.0.0.1',port))
    name=app.name
    log=WORK/(name+'-http.log')
    env=dict(os.environ,SPRING_DATASOURCE_PASSWORD=ENV['sample_password'])
    java=Path(ENV['java_home'])/'bin'/('java.exe' if os.name=='nt' else 'java')
    jar=app/'target'/(name+'-0.0.1-SNAPSHOT.jar')
    args=[str(java),'-Xmx384m','-Dfile.encoding=UTF-8','-Dsun.stdout.encoding=UTF-8','-Dsun.stderr.encoding=UTF-8','-jar',str(jar),'--server.address=127.0.0.1','--server.port='+str(port),
          '--spring.datasource.url=jdbc:mysql://'+ENV['mysql_host']+':'+str(ENV['mysql_port'])+'/'+ENV['sample_database']+'?serverTimezone=Asia/Tokyo',
          '--spring.datasource.username='+ENV['sample_user'],
          '--spring.devtools.restart.enabled=false']
    record={'project':name,'java':'21','spring_boot':'4.0.2','port':port,'requests':[],'passed':False}
    cookie=http.cookiejar.CookieJar()
    opener=urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cookie))
    base='http://127.0.0.1:'+str(port)
    def request(path,form=None,status=200,contains=None):
        data=urllib.parse.urlencode(form).encode() if form is not None else None
        req=urllib.request.Request(base+path,data=data)
        try:
            response=opener.open(req,timeout=20)
        except urllib.error.HTTPError as error:response=error
        body=response.read().decode('utf-8',errors='replace')
        result={'method':'POST' if form is not None else 'GET','path':path,'status':response.code,'expected_status':status}
        result['passed']=response.code==status and (contains is None or contains in body)
        if contains is not None:result['expected_text']=contains
        if not result['passed']:result['body_excerpt']=body[:600]
        record['requests'].append(result)
        assert result['passed'],result
        return body
    started=time.monotonic()
    with log.open('w',encoding='utf-8') as stream:
        process=subprocess.Popen(args,cwd=app,env=env,stdout=stream,stderr=subprocess.STDOUT,
                                 creationflags=subprocess.CREATE_NO_WINDOW if os.name=='nt' else 0)
        try:
            for _ in range(180):
                if process.poll() is not None:raise AssertionError('アプリケーションが起動前に終了しました')
                content=log.read_text(encoding='utf-8',errors='replace')
                if re.search(r'Started \w+Application in',content):break
                time.sleep(1)
            else:raise AssertionError('起動が180秒を超えました')
            assert '(v4.0.2)' in content and 'Java 21.' in content,'実行時バージョンが一致しません'
            record['startup_seconds']=round(time.monotonic()-started,2)
            if name.endswith('_1_3'):
                request('/',status=404,contains='Not Found')
                record['note']='第1章の開始/解答はAppクラスのみの配布状態。標準404で組込サーバー稼働を確認。'
            elif group=='spring_exercise' and name.endswith('_2'):
                request('/',contains='<html')
                request('/login',status=404,contains='Not Found')
                request('/login2',contains='<form')
                request('/login3',contains='<form')
                request('/login2',{'id':'123456','password':'migration21'},contains='<html')
                record['expected_incomplete']=['GET /login','POST /login3']
                record['note']='IndexControllerと/loginのマッピング、/login3のModel設定は受講者の実装課題。課題の未実装を保っています。'
            elif group=='spring_exercise' and name.endswith('_3'):
                request('/product/',contains='<form')
                request('/product/findAll',contains='商品一覧')
                request('/product/findByPrice?price=30000',contains='商品一覧')
                record['expected_incomplete']=['Entity/Repositoryの実装','DB検索結果のModel設定']
                record['note']='Entity/Repository/Modelへの一覧設定が受講者の実装課題。検索画面と空の一覧を確認しています。'
            elif name.endswith('_2'):
                request('/',contains='<html')
                request('/login',contains='<form')
                request('/login2',contains='<form')
                request('/login3',contains='<form')
                request('/login',{'id':'123456','password':'migration21'},contains='<html')
                request('/login3',{'id':'123456','password':'migration21'},contains='123456')
            elif group=='spring_exercise' and name.endswith('_4'):
                for path in ['/','/2','/3']:request(path,contains='<form')
                record['expected_incomplete']=['POST /login','POST /login2','GET /4','POST /login4','GET /5']
                record['note']='ログイン/Session/Validationが受講者の実装課題。/, /2, /3のログイン画面を確認。/4以降はth:object等の課題実装後に確認する画面です。'
            elif group=='spring_exercise' and name.endswith('_5'):
                request('/product/',contains='<form')
                request('/product/findAll',contains='商品一覧')
                request('/product/findByPrice?price=30000',contains='<td>1</td>')
                request('/product/findByNameAndPrice?'+urllib.parse.urlencode({'name':'スマートテレビ','price':'30000'}),contains='<td>1</td>')
                record['expected_incomplete']=['商品名/価格/画像の動的表示','共通レイアウト適用']
                record['note']='商品名/価格/画像の動的出力とレイアウト適用が受講者の課題。空欄を保ち、検索画面・DB由来の商品番号を確認しています。'
            elif name.endswith('_7'):
                for path in ['/7-2','/7-3','/7-4','/7-5','/7-5-2','/7-6','/7-6-2']:request(path,contains='<html')
                if group=='spring_answer':request('/product/findAll',contains='スマートテレビ')
            else:
                if group=='spring_answer' and name.endswith('_4'):
                    request('/login5',{'empId':'123456','password':'pass1234'},contains='山田太郎')
                request('/product/',contains='<form')
                request('/product/findAll',contains='スマートテレビ')
                request('/product/findByPrice?price=30000',contains='スマートテレビ')
                request('/product/findByNameAndPrice?'+urllib.parse.urlencode({'name':'スマートテレビ','price':'30000'}),contains='スマートテレビ')
                if group=='spring_answer' and name.endswith('_3'):
                    request('/product/findById?id=1',contains='スマートテレビ')
                    request('/product/insert',contains='<form')
                    request('/product/update/1',contains='スマートテレビ')
                    for route,label in [('/product/insert','通常登録'),('/product/insert2','ModelMapper登録')]:
                        marker='MIGRATION21_'+uuid.uuid4().hex[:16]
                        assert sql("SELECT COUNT(*) FROM product WHERE name='"+marker+"'")=='0'
                        try:
                            request(route,{'name':marker,'price':'2100'},contains=marker)
                            ident=int(sql("SELECT id FROM product WHERE name='"+marker+"' ORDER BY id DESC LIMIT 1"))
                            request('/product/update',{'id':str(ident),'name':marker+'_UPDATED','price':'4200'},contains=marker+'_UPDATED')
                            assert sql('SELECT price FROM product WHERE id='+str(ident))=='4200'
                            request('/product/delete/'+str(ident),contains='スマートテレビ')
                            assert sql('SELECT COUNT(*) FROM product WHERE id='+str(ident))=='0'
                        finally:delete_created(marker)
                if group=='spring_answer' and name.endswith('_4'):
                    request('/5',contains='<form')
                    request('/login5',{'empId':'','password':''},contains='社員番号を入力してください')
                    request('/login5',{'empId':'123456','password':'wrong'},contains='社員番号またはパスワードが誤っています。')
                    request('/login5',{'empId':'123456','password':'pass1234'},contains='山田太郎')
                    assert any(c.name=='JSESSIONID' for c in cookie),'セッションCookieがありません'
                if group=='spring_answer' and name.endswith('_5'):
                    body=request('/product/findAll',contains='Traino家電商品')
                    assert '/product/findById/1' in body and '/images/product1.png' in body
                    request('/css/layout.css',contains='flex')
                if group=='spring_answer' and name.endswith('_6'):
                    request('/product/findAll',contains='テレビ・モニター')
                    request('/product/findById?id=1',contains='テレビ・モニター')
                    marker='MIGRATION21_'+uuid.uuid4().hex[:16]
                    assert sql("SELECT COUNT(*) FROM product WHERE name='"+marker+"'")=='0'
                    try:
                        request('/product/insert',{'name':marker,'price':'2100','categoryId':'1'},contains='テレビ・モニター')
                        ident=int(sql("SELECT id FROM product WHERE name='"+marker+"' ORDER BY id DESC LIMIT 1"))
                        request('/product/update',{'id':str(ident),'name':marker+'_UPDATED','price':'4200','categoryId':'2'},contains='コンピュータ')
                        assert sql('SELECT category_id FROM product WHERE id='+str(ident))=='2'
                        request('/product/delete/'+str(ident),contains='スマートテレビ')
                    finally:delete_created(marker)
            record['passed']=True
        except Exception as error:
            record['error']=str(error)
            record['log_tail']=log.read_text(encoding='utf-8',errors='replace')[-7000:]
        finally:
            process.terminate()
            try:process.wait(timeout=15)
            except subprocess.TimeoutExpired:process.kill();process.wait(timeout=15)
    record['seconds']=round(time.monotonic()-started,2)
    return record


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--java-home',default=os.environ.get('JAVA_HOME'),help='JDK 21の場所。既定はJAVA_HOME。')
    parser.add_argument('--mysql-host',default='127.0.0.1')
    parser.add_argument('--mysql-port',type=int,default=3306)
    parser.add_argument('--port-start',type=int,default=18100)
    parser.add_argument('--output',type=Path,default=ROOT/'output/verification/spring-http.json')
    parser.add_argument('--group',choices=['spring_answer','spring_exercise','all'],default='all')
    parser.add_argument('--project',help='一つのアプリだけを再確認する場合に指定。')
    options=parser.parse_args()
    if not options.java_home:parser.error('--java-homeまたはJAVA_HOMEにJDK 21を指定してください。')
    options.java_home=str(Path(options.java_home).resolve())
    if not (Path(options.java_home)/'bin'/('java.exe' if os.name=='nt' else 'java')).is_file():parser.error('指定したJDKのjavaが見つかりません。')
    mysql=shutil.which('mysql')
    if not mysql:
        candidates=sorted(Path('C:/Program Files/MySQL').glob('MySQL Server */bin/mysql.exe'))
        if candidates:mysql=str(candidates[-1])
    if not mysql:parser.error('mysqlクライアントをPATHへ追加してください。')
    MYSQL=Path(mysql)
    ENV={'java_home':options.java_home,'mysql_host':options.mysql_host,'mysql_port':options.mysql_port,
         'sample_database':'spring_sample','sample_user':'spring_sample_user',
         'sample_password':os.environ.get('SPRING_SAMPLE_PASSWORD','trainocate')}
    result_path=options.output.resolve()
    result_path.parent.mkdir(parents=True,exist_ok=True)
    WORK=result_path.parent/'logs'
    WORK.mkdir(parents=True,exist_ok=True)
    groups=['spring_answer','spring_exercise'] if options.group=='all' else [options.group]
    report=[]
    for group in groups:
        for index,app in enumerate(sorted((ROOT/'projects'/group).glob('*/pom.xml'))):
            if options.project and app.parent.name!=options.project:continue
            result=run_app(group,app.parent,options.port_start+index+(7 if group=='spring_exercise' else 0))
            report.append(result)
            if options.project and result_path.exists():
                saved=json.loads(result_path.read_text(encoding='utf-8'))
                saved=[r for r in saved if r['project']!=result['project']]+[result]
            else:saved=report
            result_path.write_text(json.dumps(sorted(saved,key=lambda r:r['project']),ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
            print(json.dumps({k:v for k,v in result.items() if k not in ['requests','log_tail']},ensure_ascii=False),flush=True)
    if not report:parser.error('対象プロジェクトが見つかりません。')
    failures=[r['project'] for r in report if not r['passed']]
    print(json.dumps({'projects':len(report),'requests':sum(len(r['requests']) for r in report),'failed':failures},ensure_ascii=False),flush=True)
    if failures:raise SystemExit(1)
