import os
from traceback import format_exc as exc

os.environ['TESSDATA_PREFIX'] = 'C:/Program Files/Tesseract-OCR/tessdata'
os.environ['TESSERACT_CMD'] = 'C:/Program Files/Tesseract-OCR/tesseract.exe'

POPPLER = 'D:/Program Files/poppler-0.68.0/bin'
if not os.path.exists(POPPLER): raise Exception('Для извлечения изображений нужен poppler')

ROOT_PATH = F'D:/Users/{os.environ["USERNAME"]}/Documents/OCR/Uploads'
if not os.path.exists(ROOT_PATH): os.makedirs(ROOT_PATH)

HOST = "127.0.0.1"
PORT = 8000
