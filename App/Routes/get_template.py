from App.Routes import *
from App.Scripts.Template import get_template_html

router = APIRouter()

@router.get('/get_template/'+'{file_hash}/'+'{img_hash}')
async def get_template(file_hash: str, img_hash: str):
    '''Получение сформированного html с наложенными ячейками на выделенное из файла изображение'''
    image_path = f'{ROOT_PATH}/{file_hash}/{img_hash}.png'
    template_html = get_template(image_path, img_hash)
    return FileResponse(template_html)
    
