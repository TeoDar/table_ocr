from io import BytesIO
import os
import fitz
from PIL import Image
import numpy as np

supported_filetypes = ('pdf', 'png')

# Преобразование PixMap в PNG


def pixtopng(pix):
    im = np.frombuffer(pix.samples, dtype=np.uint8)#.reshape(pix.h, pix.w, pix.n)
    im = np.ascontiguousarray(im[..., [0, 1, 2]])
    return im

# Извлечение файлов из PDF в PixMap с помощью fitz


def extraction_images(file: bytes, filename: str) -> list:
    """Возвращает массив пикселей полученной страницы"""
    # Провера типа файла
    filetype: str = filename[-3:].lower()
    if filetype not in supported_filetypes:
        return None
    elif filetype == 'png':
        return [file]
    else:
        pages = []
        scan = fitz.Document(stream=file, filetype="pdf")
        for i in range(scan.page_count):
            for img in scan.get_page_images(i):
                xref = img[0]
                pix = fitz.Pixmap(scan, xref)
                if pix.n < 5:
                    pages.append(pix.tobytes())
                else:
                    pix1 = fitz.Pixmap(fitz.csRGB, pix)
                    pages.append(pix1.tobytes())
                    pix1 =None
                pix = None
        scan.close()
        return pages


def save_images_from_bytes(path: str, images: list):
    imgs_md5 = []
    from hashlib import md5
    for img in images:
        img_md5 = md5(img).hexdigest()
        imgs_md5.append(img_md5)
        file_path = f'{path}{img_md5}.png'
        img = Image.open(BytesIO(img))
        img.save(file_path, bits=1, optimize=True)
        print(f'[IMAGE SAVED]   {file_path}')
    return imgs_md5


def test():
    test_path = 'C:/PROJECTS/ocr/Other/KAH/'
    if not os.path.exists(f'{test_path}'): os.makedirs(f'{test_path}')
    test_file = '21-4504-021.pdf'
    with open(test_path+test_file, 'rb') as png:
        images = extraction_images(file=png.read(), filename=test_file)
        save_images_from_bytes('C:/PROJECTS/ocr/App/', images)


if __name__ == "__main__":
    test()
    
