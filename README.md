## 前提
・言語：python 3.6.5 

・サーバー：Heroku

・API実装ライブラリ：Flask

・MLロジックファイル：home_recomenndation.py

・学習用データ：homes.csv/rating.csv

・アーキテクチャ：

　① railsアプリ(airbnb)からhomeの名前をパラメータで送る
 
　② 名前に基づいてる類似の商品と類似度を配列で返す
 
　③ railsで受け取った値を正規表現を用いてインスタンス変数に格納
 
　④ railsのviewで表示
