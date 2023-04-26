from .imports import *

app = FastAPI()

@app.post(f'/faultreport')
async def KAN_to_pdf(file: UploadFile):
    '''API для полного преобразования PDF сканированных КАНов в атрибуты MES'''
    file_bytes: bytes = file.file.read()
    file_name: str = file.filename
    json = Recognition.pdf_to_json(file_bytes, file_name)
    return Response(content=json, media_type='application/json')





@app.get(f'/get_image/'+'{file_hash}/'+'{img_hash}')
async def get_image(file_hash:str, img_hash:str):
    try: return FileResponse(f'{root_path}/{file_hash}/{img_hash}.png')
    except: raise HTTPException(status_code=404, detail='Файл изображения не найден. Попробуйте загрузить файл заного.')


@app.get(f'/get_template/'+'{file_hash}/'+'{img_hash}')
async def get_image(file_hash:str, img_hash:str):
    image_path = f'{root_path}/{file_hash}/{img_hash}.png'
    return FileResponse(get_template(image_path, img_hash, root_path))

#@app.get(f'{base_url}/get_image/'+'{file_hash}/'+'{img_hash}')
