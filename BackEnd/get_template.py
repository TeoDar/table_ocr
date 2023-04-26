from App.imports import *

class Template:
    def get_template(image_path:str, img_hash:str, root_path:str)->str:
        '''Возвращает путь к html'''
        if not path.isfile(image_path): raise HTTPException(status_code=404, detail='Файл изображения не найден. Попробуйте загрузить файл заного.')
        cv_image = cv2.imread(image_path)[...,::-1]
        # Получение изображения в серых тонах
        gray = ImageProcessing.gray(cv_image)
        # Выделение вертикальных и горизонтальных линий таблиц
        tableLines = LinesSelecting.GetLines(gray)
        # Выделение Максимального контура для избавления от паразитных линий по краям скана
        tableBox = TableBorders.findContour(tableLines)
        # Приведение изображения и контуров таблицы к вертикали
        rotation = Rotation.deskew(cv_image, tableBox, tableLines, 0)
        # Разделение повёрнутых результатов
        rotatedImg, rotatedTableLines, angle = rotation
        # Нахождение повёрнутого Box для таблицы и его отрисовка
        rotatedTableBox = TableBorders.findContour(rotatedTableLines)
        TableBorders.paintContour(rotatedTableLines, rotatedTableBox)
        # Обрезка изображения по границам таблицы
        croppedTableLines = ImageProcessing.crop(rotatedTableLines, rotatedTableBox, INDENT)
        # Последняя цифра это значение добавочных пикселей к краям обрезк
        croppedImg = ImageProcessing.crop(rotatedImg, rotatedTableBox, INDENT)
        return croppedImg

        # Получение координат ячеек таблицы
        cells = CellsSelecting.divideTable(croppedTableLines)
        # Разделение распознанных ячеек по строкам. Тут отрисовка ячеек
        cellsByRow = SortCells.cellSorting(croppedImg, cells)
    


if __name__=='__main__':
    image_path:str = "D:/Users/Teos/Documents/OCR/Uploads/59eb1ca5cb3a5cbdd9654656ab8ff8d1/3d5238628c73b9221ba25098b51dc20c.png"
    img_hash:str = "3d5238628c73b9221ba25098b51dc20c"
    root_path:str = "D:/Users/Teos/Documents/OCR/Uploads"
    image = get_template(image_path, img_hash, root_path)
    print(PDFtoPNG.save_images_from_bytes(path="D:/Users/Teos/Documents/OCR/Uploads/59eb1ca5cb3a5cbdd9654656ab8ff8d1/", images=[image], img_md5=f'{img_hash}_cropped'))