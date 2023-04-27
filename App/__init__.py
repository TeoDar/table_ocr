import os
from traceback import format_exc as exc

os.environ['TESSDATA_PREFIX'] = 'C:/Program Files/Tesseract-OCR/tessdata'
os.environ['TESSERACT_CMD'] = 'C:/Program Files/Tesseract-OCR/tesseract.exe'

ROOT_PATH = 'D:/Users/Teos/Documents/OCR/Uploads'
HOST = "127.0.0.1"
PORT = 8000
