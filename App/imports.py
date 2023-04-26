"""Основные модули работы с файлами для распознавания"""

import os
import cv2
from hashlib import md5

from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())
ROOT_PATH = os.getenv('ROOT_PATH')

INDENT = 5