from App.Routes import *
from App.Scripts.PDFtoPNG import extraction_images, save_images

router = APIRouter()

@router.post('/upload_file')
async def upload_file(file: UploadFile):
    '''Загрузка выбранного файла на сервер'''
    file_bytes: bytes = file.file.read()
    file_name: str = file.filename
    file_hash: str = md5(file_bytes).hexdigest()

    # Проверка на существование такого-же файла
    extracted = None
    if file_hash in os.listdir(ROOT_PATH):
        print('[File already exits]')
        extracted = [_[:-4] for _ in os.listdir(ROOT_PATH+f'/{file_hash}') if 'cropped' not in _]
    if not extracted:
        # Извлечение и сохранение изображения
        try: images:list = extraction_images(file=file_bytes, filename=file_name)
        except: raise HTTPException(status_code=500, detail=f'Не удалось извлечь изображения: {exc()}')
        extracted:list = save_images(path=f'{ROOT_PATH}/{file_hash}/', images=images)
    return {"file_hash": file_hash, "extracted": extracted}
