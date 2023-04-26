from env import *

from hashlib import md5
from fastapi import FastAPI, UploadFile, File, Response, HTTPException
from fastapi.responses import FileResponse


import App.Recognition as Recognition
import App.PDFtoPNG as PDFtoPNG