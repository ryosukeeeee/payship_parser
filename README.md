# Payship Parser

## ライブラリ
- PyPDF2
- pdfminer
- qpdf


## setting

```
$ pip install pdfminer.six PyPDF2
$ brew install qpdf
$ mv password-sample.json password.json
```

password.jsonの `pass` にパスワードを入力
```
{
    "pass": "" 
}
```
## example

```
$ python main.py
```

## 参考
- [Python, PyPDF2でPDFのパスワードを設定・解除（暗号化・復号） | note.nkmk.me](https://note.nkmk.me/python-pypdf2-pdf-password/)
- [【PDFMiner】PDFからテキストの抽出 - Qiita](https://qiita.com/mczkzk/items/894110558fb890c930b5)
- [euske/pdfminer: Python PDF Parser](https://github.com/euske/pdfminer)