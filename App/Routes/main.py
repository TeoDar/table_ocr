from fastapi import FastAPI
from App.Routes import upload_file, get_image, get_template


MainApp = FastAPI(title="TABLE-OCR API")
MainApp.include_router(upload_file.router, prefix="/upload_file")
MainApp.include_router(get_image.router, prefix="/get_image")
MainApp.include_router(get_template.router, prefix="/get_template")
