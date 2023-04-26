from App.Routes import *
from App.Scripts.PDFtoPNG import extraction_images, save_images_from_bytes

router = APIRouter()

@router.post('/')
async def upload_file(file: UploadFile):
    '''Загрузка выбранного файла на сервер'''
    file_bytes: bytes = file.file.read()
    file_name: str = file.filename
    file_hash: str = md5(file_bytes).hexdigest()

    # Проверка на существование такого-же файла
    # if file_hash in os.listdir(ROOT_PATH):
    #     extracted_images_hashes = [_[:-4] for _ in os.listdir(ROOT_PATH+f'/{file_hash}')]
    #     if extracted_images_hashes:
    #         return {"file_hash": file_hash,"extracted_images_hashes": extracted_images_hashes}
    
    # Извлечение изображения
    images:list = extraction_images(file=file_bytes, filename=file_name)
    # Проверка на существование папки для сохранения
    file_path:str = f'{ROOT_PATH}/{file_hash}/'
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    try: extracted_images_hashes:list = save_images_from_bytes(file_path, images)
    except Exception as e:
        print(e)
        raise HTTPException(status_code=404,
                            detail='Файл изображения не найден. Попробуйте загрузить файл заного.')
    return {"file_hash": file_hash, "extracted_images_hashes": extracted_images_hashes}