import sys

from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import LAParams, LTContainer, LTTextBox
from pdfminer.pdfinterp import PDFPageInterpreter, PDFResourceManager
from pdfminer.pdfpage import PDFPage

class PdfParser:
    def __init__(self, filename):
        self.filename = filename

        # Layout Analysisのパラメーターを設定。縦書きの検出を有効にする。
        self.laparams = LAParams(detect_vertical=True)

        # 共有のリソースを管理するリソースマネージャーを作成。
        self.resource_manager = PDFResourceManager()

        # ページを集めるPageAggregatorオブジェクトを作成。
        self.device = PDFPageAggregator(self.resource_manager, laparams=self.laparams)

        # Interpreterオブジェクトを作成。
        self.interpreter = PDFPageInterpreter(self.resource_manager, self.device)

    def find_textboxes_recursively(self, layout_obj):
        """
        再帰的にテキストボックス（LTTextBox）を探して、テキストボックスのリストを取得する。
        """
        # LTTextBoxを継承するオブジェクトの場合は1要素のリストを返す。
        if isinstance(layout_obj, LTTextBox):
            return [layout_obj]

        # LTContainerを継承するオブジェクトは子要素を含むので、再帰的に探す。
        if isinstance(layout_obj, LTContainer):
            boxes = []
            for child in layout_obj:
                boxes.extend(self.find_textboxes_recursively(child))

            return boxes

        return []  # その他の場合は空リストを返す。

    def parse(self):
        with open(self.filename, 'rb') as f:
            # PDFPage.get_pages()にファイルオブジェクトを指定して、PDFPageオブジェクトを順に取得する。
            # 時間がかかるファイルは、キーワード引数pagenosで処理するページ番号（0始まり）のリストを指定するとよい。
            for page in PDFPage.get_pages(f):
                print('\n====== ページ区切り ======\n')
                self.interpreter.process_page(page)  # ページを処理する。
                layout = self.device.get_result()  # LTPageオブジェクトを取得。

                # ページ内のテキストボックスのリストを取得する。
                boxes = self.find_textboxes_recursively(layout)

                # テキストボックスの左上の座標の順でテキストボックスをソートする。
                # y1（Y座標の値）は上に行くほど大きくなるので、正負を反転させている。
                boxes.sort(key=lambda b: (-b.y1, b.x0))

                for box in boxes:
                    print('-' * 10)  # 読みやすいよう区切り線を表示する。
                    # print("x0: {0}, y1: {1}".format(box.x0, box.y1))
                    print(box.get_text().strip())  # テキストボックス内のテキストを表示する。
