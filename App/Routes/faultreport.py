from .._imports import *
from Scripts.Recognition import pdf_to_json

router = APIRouter()

@router.post(f'/faultreport')
async def KAN_to_pdf(file: UploadFile):
    '''API для полного преобразования PDF сканированных КАНов в атрибуты MES'''
    file_bytes: bytes = file.file.read()
    file_name: str = file.filename
    json = pdf_to_json(file_bytes, file_name)
    return Response(content=json, media_type='application/json')