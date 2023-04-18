import os
from fastapi import FastAPI, UploadFile, File, Response, HTTPException
from hashlib import md5
import base64
from Recognition import pdf_to_json
from PDFtoPNG import *


USERPROFILE = os.environ['USERPROFILE'].replace('\\', '/')
root_path = f'D:/Users/Teos/Documents/OCR/Uploads'
os.makedirs(os.path.dirname(root_path+'/'), exist_ok=True)

app = FastAPI()
base_url = '/api/2.0'


@app.post(f'{base_url}/faultreport')
async def KAN_to_pdf(file: UploadFile = File()):
    '''API для полного преобразования PDF сканированных КАНов в атрибуты MES'''
    json = pdf_to_json(file.file.read())
    return Response(content=json, media_type='application/json')


@app.post(f'{base_url}/upload_file')
async def upload_file(file: UploadFile):
    '''Загрузка выбранного файла на сервер'''
    file_bytes: bytes = file.file.read()
    file_name: str = file.filename
    file_hash: str = md5(file_bytes).hexdigest()

    # Проверка на существование такого-же файла
    if file_hash in os.listdir(root_path):
        extracted_images_hashes = [_[:-4] for _ in os.listdir(root_path+f'/{file_hash}')]
        if extracted_images_hashes:
            return {"file_hash": file_hash,"extracted_images_hashes": extracted_images_hashes}
    
    # Извлечение изображения
    images:list = extraction_images(file=file_bytes, filename=file_name)
    # Проверка на существование папки для сохранения
    file_path:str = f'{root_path}/{file_hash}/'
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    try: extracted_images_hashes:list = save_images_from_bytes(file_path, images)
    except: os.removedirs(os.path.dirname(file_path))
    # Вычисление md5
    return {"file_hash": file_hash, "extracted_images_hashes": extracted_images_hashes}


@app.get(f'{base_url}/get_image/'+'{file_hash}/'+'{img_hash}')
async def get_image(file_hash:str, img_hash:str):
    try:
        with open(f'{root_path}/{file_hash}/{img_hash}.png', 'rb') as img:
            return Response(content=base64.b64encode(img.read()), media_type="image/png")
    except: raise HTTPException(status_code=404, detail='Файл изображения не найден. Попробуйте загрузить файл заного.')

#@app.get(f'{base_url}/get_image/'+'{file_hash}/'+'{img_hash}')
