latexの自分用の.styファイル

更新したら，mktexlsrをする

## ファイル構成
- `_my_style.sty`: 読み込み用の入口
- `_my_style-packages.sty`: パッケージ読み込みと全体設定
- `_my_style-macros.sty`: 数式用マクロ
- `_my_style-theorems.sty`: 定理環境と参照設定

## gen_cwl.py
- 分割したstyファイルをたどってcwlファイルを生成する
- cwlファイルは，エディタの補完機能を使うためのファイル