# gae2-python37

Google App Engine 2 向けの Python 3.7 フレームワークの検証用レポジトリ

# 方針
Flask を利用した軽量フレームワークをベースにしつつ、

- [x] Open API Specification を使った API Request/Response のバリデーションを検証
- [x] Open API Specification を利用して Cloud Endpoints による API 公開の検証 ← まだ早かった
- [ ] 移行を見据えた Python 3.7 での Cloud Datastore の検証
- [ ] ファイルアップロード周りの検証
- [x] Firebase などを利用した Authentication の検証
- [ ] API ベースでのテスト・カバレッジ計測ツールの検証
- [ ] DI コンテナの検証

を行う。

Open API の利用には Flask と相性の良さそうな [flasgger](https://github.com/rochacbruno/flasgger) を利用する。

# 開発

python 3.7 を導入後(pyenv 推奨)、以下のコマンドでサーバーが起動する。

```sh
$ pip install -r requirements.txt

$ python main.py
 * Serving Flask app "main" (lazy loading)
 * Environment: production
 ...
```

`localhost:8080` でアクセスが可能。

また flasgger の機能で `/apidocs` にアクセスすると API Document が閲覧できる。


## Cloud Endpoints

※2018/11 時点では Cloud Endpoints は GAE 2nd に対応していないため利用できない、無念

Cloud Endpoints は Open API 2.0 にしか対応していないため(2018/10)、
3.0 系のスキーマをコンバートしてデプロイしないといけない。

[api-spec-converter](https://github.com/LucyBot-Inc/api-spec-converter)

を利用すると簡単にコンバートが実行できる(他のものは試していない)。

https://openapi.tools/ にもっといいサービスがあるかも。

以下のコマンドで導入し、変換が可能。

```sh
$ yarn global add api-spec-converter

```sh
$ api-spec-converter --from openapi_3 --to swagger_2 --syntax yaml colors.yml > colors.2.yml
```

```sh
$ gcloud endpoints services deploy colors.2.yml --project $PROJECT
```


## 試験

以下のコマンドで API テストが実行できる

```sh
$ pip install -r requirements.testing.txt

$ pytest main_test.py
```

## デプロイ

gloud は python 2 を利用しているため、python 3 系と共存させる場合、`CLOUDSDK_PYTHON` 環境変数で python 2 のバイナリを指定する必要がある

```sh
CLOUDSDK_PYTHON=~/.pyenv/versions/2.7.15/bin/python
```

direnv で `.envrc` に設定を書いておくと楽(.envrc は git から除外する設定になっています)。

# 認証

認証には [Cloud Identity-Aware Proxy](https://cloud.google.com/iap/)(IAP) を利用します。

IAP を利用すると GAE のサービス単位で Google Account によるアクセス制御が可能になります。

パス単位での制御はできないため、認証範囲が異なる場合はサービス単位で分けてください(管理画面などは別サービスとして作る)。
