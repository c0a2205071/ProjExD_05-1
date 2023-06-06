# Air-hockey

## 実行環境の必要条件
* python >= 3.10
* pygame >= 2.1

## ゲームの内容
* 1対1の対戦型ホッケーゲーム。相手地点のゴールに入ったら１点とする。

## ゲームの実装
### 共通実装機能
* 1Pの操作に関するクラス
* 背景についての描写
* ホッケーボールに関する描写


### 担当追加機能
* 一つしかなかったプレイヤーの操作するホッケーを二つに増やして移動できるようにした (c0b22128)
* パドルとボールの衝突機能の追加(c0b22076)
* ホッケーの操作機能で自分の陣地を超えないようにした。(c0a22050)
* ゴールの判定機能の追加,得点に関する機能の追加 (c0b22116)
### メモ
* 操作方法
　１PはWASDで、２Pは矢印キーで操作する
　どちらかが先に５点取れば勝ち

* 画像元
　https://github.com/mkfeuhrer/Air-hockey

