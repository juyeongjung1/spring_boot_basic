---
header: 演習 3 Spring Data JPA
page: 20
---

# 演習3.1. Entity とRepository の定義

## a. entity.Employee クラスのクラス名の上に適切なアノテーションを付けてください。

- テーブル情報と、テキスト3.2 の【作業手順①～②】を参考にしてください。
- Lombok のライブラリを活用してください。

## b. 4 つのフィールドの上に適切なアノテーションを付けてください。

- テーブル情報と、テキスト3.2 の【作業手順③】を参考にしてください。
- id(社員番号)には、@GeneratedValue アノテーションを付けてください。
- id 以外の列は、制約がありませんので、@Column の引数は今回不要です。

## c. repository.EmpRepository にJpaRepository を適切に継承してください。

- テキスト3.3 の【作業手順④】を参考にしてください。
- \<紐づけたいEntity 名, Entity の主キーの型名>
