from fastapi import FastAPI
from App.Routes import upload_file, get_image, get_template, get_test


MainApp = FastAPI(title="TABLE-OCR API")
MainApp.include_router(upload_file.router)
MainApp.include_router(get_image.router)
MainApp.include_router(get_template.router)
MainApp.include_router(get_test.router)
