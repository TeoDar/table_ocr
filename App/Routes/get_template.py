from App.Routes import *

from App.Scripts.Template import Template

router = APIRouter()

@router.get(f'/get_template/'+'{file_hash}/'+'{img_hash}')
async def get_image(file_hash:str, img_hash:str):
    '''Получение изображения по hash загруженного файла'''
    cropped_hash = Template.get_cropped_template(file_hash, img_hash)
    if not cropped_hash: raise HTTPException(status_code=500, detail=f'Не удалось извлечь изображения: {exc()}')
    else: return FileResponse(f'{ROOT_PATH}/{file_hash}/{cropped_hash}.png')