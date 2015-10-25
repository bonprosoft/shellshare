ShellShare
==========

## これはなに
複数のシェルの画面をWebサイトからリアルタイムで見れるようにする何かです。  
プログラミング系の勉強会で、コードに関して議論するときにプロジェクタのコネクタを差し替えるのが面倒だから作りました。  
やっていることは単純で、tmuxのpipe-paneを使ってシェルの操作をファイルに書きだし、それをPythonスクリプトで監視して転送しています。  
サーバーと発表者の間はWebSocketを用いて転送しています。  
内部的なプロトコルは[VSShare](http://vsshare.azurewebsites.net/)とほぼ同様のものを使っています。（つまり将来的にはVSShareでホストできるようにしたい）

## つかいかた
### サーバー
#### やくわり
* WebSocketのハブ役

#### 必要な環境
* Python 2.7

#### セットアップ方法
`packages_requirements.txt`を`pip install`にかけてください。  
必要なら`./install.sh`を実行することで、自動的にvirtualenvを作って、その中に環境構築を行ってくれます。

#### 実行方法
`server.py`を実行します。  
`install.sh`を使った場合には、`server`ディレクトリ内に`env`ディレクトリ（virtualenv）を読み込んでから実行してください。
* `source server/env/bin/activate`

### クライアント（発表者）
#### やくわり
* 発表する側（シェルの画面を共有する側）

#### 必要な環境
* Python 2.7
* tmux

#### セットアップ方法
`./install.sh`を実行することで、自動的にvirtualenvを作って、その中に環境構築を行ってくれます。  
もし手動でインストールを行いたい場合には、`packages_requirements.txt`を`pip install`にかけてください。
なお、その場合には`run.sh`の中で、自動的にvirtualenvを読み込むようにしているので、その行を削除するか、パスを変更してください。

#### 実行方法
`./run.sh [UserName]`を実行します。  
* 例： `./run.sh igarashi`

### ビューアー
#### やくわり
* シェアされているコードを見る側

#### 必要な環境
* (環境構築時のみ)npm

#### セットアップ方法
`./setup.sh`を実行することで、自動的に環境構築を行ってくれます。  

#### 実行方法
置くだけです。

## ライセンス
* [The MIT License (MIT)](LICENSE.txt)

