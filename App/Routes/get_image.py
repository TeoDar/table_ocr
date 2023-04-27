from App.Routes import *

router = APIRouter()

@router.get('/get_image/'+'{file_hash}/'+'{img_hash}')
async def get_image(file_hash:str, img_hash:str):
    '''Получение изображения по hash загруженного файла'''
    try: return FileResponse(f'{ROOT_PATH}/{file_hash}/{img_hash}.png')
    except: raise HTTPException(status_code=404, detail='Файл изображения не найден. Попробуйте загрузить файл заного.')