import os
import sys
import json
import re
import PyPDF2
from pdfparser import PdfParser

with open('./password.json', 'r') as f:
    obj = json.load(f)
    PASSWORD = obj['pass']

OUTPUT_PATH = './pdf_decrypted/201910-decrypted.pdf'

if __name__ == '__main__':
    
    if len(sys.argv) < 2:
        print('Usage: python main.py target.py')
        sys.exit()
    
    file_path = sys.argv[1]
    if not os.path.isfile(file_path):
        print('failed to open: {0}'.format(file_path))
        sys.exit()

    with open(file_path, mode='rb') as f:
        reader = PyPDF2.PdfFileReader(f)

        # 暗号化されていたら解除する
        if reader.isEncrypted:
            print("isEncrypted")
            try:
                reader.decrypt(PASSWORD)
            except NotImplementedError:
                pattern = r'\.pdf$'
                output_path = re.sub(pattern, '-decrypted.pdf', file_path)
                command = "qpdf --password={0} --decrypt {1} {2}".format(
                    PASSWORD,
                    file_path,
                    output_path
                )
                os.system(command)
        else:
            print("Not encrypted")
            print(reader.getNumPages())
            parser = PdfParser(file_path)
            parser.parse()
            sys.exit()
            
    parser = PdfParser(output_path)
    parser.parse()