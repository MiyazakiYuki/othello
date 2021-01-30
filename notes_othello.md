# Othello PJ

## Docker  Tutorial
Docker：仮想環境で開発/実行するためのオープンプラットフォーム
* [Dockerインストール方法（Qiita）](https://qiita.com/k5n/items/2212b87feac5ebc33ecb)
* [Dockerコマンド一覧](https://qiita.com/suzukihi724/items/961112f6578a60dd6266)

### 仮想環境の立ち上げ
1. Docker Desktop 起動（docker daemonの起動）
2. Docker Hubにログイン
3. docker run （下記）
    * ID:ymiyamiya、Project:othello、Tag:3.7-alpineのimageを起動
    * -it：Dockerを標準入力で操作するためのコマンド。（必須）
    * --rm：クリーンアップ。コンテナ終了時にファイルシステムを削除する。
    * -p：ポート指定
    * -v：コンテナとホストの間でファイルをやりとりする。コンテナを削除してもホストにデータが残るようになる。
```
docker run -it --rm -p 127.0.0.1:8000:8000 -v ~/Documents/othello:/work ymiyamiya/othello:3.7-alpine /bin/sh
```
* 注意
    * localhostのポート番号と仮想環境のポート番号を対応させる必要がある
    * 仮想OSはAlpine linux

### 仮想環境の環境構築
* [vimのインストール](https://qiita.com/YumaInaura/items/3432cc3f8a8553e05a6e)
```
apk --update add vim 
```
* [numpyのインストール](https://github.com/doccano/doccano/issues/969)
```
apk add -U --no-cache bash python3 python3-dev libpq postgresql-dev unixodbc-dev musl-dev g++ libffi-dev 
&& pip3 install --upgrade --no-cache-dir pip setuptools==49.6.0 
&& pip3 install --no-cache-dir -r requirements.txt 
&& ln -s /usr/bin/python3 /usr/bin/python 
&& apk del --no-cache python3-dev postgresql-dev unixodbc-dev musl-dev g++ libffi-dev
```

### Docker環境の保存
```
docker ps
docker login
docker commit <ContainerID> ymiyamiya/othello:<Tag>
docker push ymiyamiya/othello:latest
```
* [保存方法](https://sagantaf.hatenablog.com/entry/2018/09/04/190801)

## Do

***
## Django Tutorial
Django：Pythonで実装されたWebアプリケーションフレームワーク

### Webサーバの立ち上げ
* djangoの再インストールが必要
* [Django Girls](https://tutorial.djangogirls.org/ja/)
```
cd work/djangogirls
pip install -r requirments.txt
python manage.py migrate
python manage.py runserver 0:8000
```
* http://127.0.0.1:8000 と入力




***
## PythonAnywhere

### PythonAnywhereでのサーバの立ち上げ
* ポート8000が空いてないと言われた場合は8080を使う
* "miyazaki.pythonanywhere.com"とURL欄に打ち込めば入れる
* サーバの停止、削除は
    * python anywhere > Web > Disable Webapp
```
python manage.py runserver 8080
```


***
## GitHub Tutorial
* [GitHub使い方](https://tracpath.com/bootcamp/learning_git_firststep.html)
* 最初にレポジトリをGitHub上で作成しておく
```
git remote add origin https://github.com/MiyazakiYuki/othello.git
git add <filename>
git status
git commit -m "<comments>"
git push origin main
```
* GitHubのデータをローカルに複製する
```
git clone https://github.com/MiyazakiYuki/othello
```
