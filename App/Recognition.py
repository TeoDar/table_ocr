import ToMESAtributes
import CellsSelecting
import ImageProcessing
import LinesSelecting
import OCR
import PDFtoPNG
import Rotation
import SortCells
import TableBorders
import TextToJSON

import json
import os
if os.name == 'nt':
    os.environ['TESSDATA_PREFIX'] = 'C:/Program Files/Tesseract-OCR/tessdata'
    os.environ['TESSERACT_CMD'] = 'C:/Program Files/Tesseract-OCR/tesseract.exe'

def pdf_to_json(file) -> dict:
    """Обрабатывает PDF файлы и возвращает JSON с распознанным из заданных ячеек текстом    

    Args:
        file
    Returns:
        JSON
    """

    textFromCells = {}
    iter = 0
    indent = 5  # Отступ координат к центру ячейки

    # Преобразуем исходные сканы в формате PDF в изображения PNG
    pngPages = PDFtoPNG.extraction_images(file)
    # Если изображения не были найдены в PDF файле, то вернуть HTML код 400
    if pngPages == []:
        return 400
    # Проходимся по каждому изображению полученному из PDF файла
    for img in pngPages:
        iter += 1   # Счётчик изображений

        # Получение изображения в серых тонах
        gray = ImageProcessing.gray(img)

        # Выделение вертикальных и горизонтальных линий таблиц
        tableLines = LinesSelecting.GetLines(gray)
        # Выделение Максимального контура для избавления от паразитных линий по краям скана
        tableBox = TableBorders.findContour(tableLines)

        # Приведение изображения и контуров таблицы к вертикали
        rotation = Rotation.deskew(img, tableBox, tableLines, iter)
        # Разделение повёрнутых результатов
        rotatedImg, rotatedTableLines, angle = rotation
        # Нахождение повёрнутого Box для таблицы и его отрисовка
        rotatedTableBox = TableBorders.findContour(rotatedTableLines)
        TableBorders.paintContour(rotatedTableLines, rotatedTableBox)

        # Обрезка изображения по границам таблицы
        croppedTableLines = ImageProcessing.crop(rotatedTableLines, rotatedTableBox, indent)
        # Последняя цифра это значение добавочных пикселей к краям обрезк
        croppedImg = ImageProcessing.crop(rotatedImg, rotatedTableBox, indent)

        # Получение вручную определённых координат ячеек
        # coordinates = CellsCoordinates.getCoords(croppedImg, iter)

        # Получение координат ячеек таблицы
        cells = CellsSelecting.divideTable(croppedTableLines)
        # Разделение распознанных ячеек по строкам_____________________________________________Тут отрисовка ячеек
        cellsByRow = SortCells.cellSorting(croppedImg, cells)

        # Словари сопоставления полей КАН в системе номерами заданных ячеек
        atributesToCoordinates = ToMESAtributes.dictKAHatributes(iter, cellsByRow)
        atributes, N_analysresult, N_Events = atributesToCoordinates

        # Получение массива строк текста из ячеек таблицы
        textFromCells = OCR.searchText(croppedImg.copy(), atributes, textFromCells)

    recognized_dict = TextToJSON.finalProcess(textFromCells, N_analysresult, N_Events)
    return recognized_dict
