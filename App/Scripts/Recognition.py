from App.Scripts import *
import App.Scripts.PDFtoPNG as PDFtoPNG
import App.Scripts.ImageProcessing as ImageProcessing
import App.Scripts.LinesSelecting as LinesSelecting
import App.Scripts.TableBorders as TableBorders
import App.Scripts.Rotation as Rotation
import App.Scripts.CellsSelecting as CellsSelecting
import App.Scripts.SortCells as SortCells
import App.Scripts.ToMESAtributes as ToMESAtributes
import App.Scripts.OCR as OCR
import App.Scripts.TextToJSON as TextToJSON

def pdf_to_json(file: bytes, filename:str) -> dict:
    """Обрабатывает PDF файлы и возвращает JSON с распознанным из заданных ячеек текстом    

    Args:
        file
    Returns:
        JSON
    """

    textFromCells = {}

    # Преобразуем исходные сканы в формате PDF в изображения PNG
    pngPages = PDFtoPNG.extraction_images(file, filename)
    # Проходимся по каждому изображению полученному из PDF файла
    for id, img in enumerate(pngPages):

        # Получение изображения в серых тонах
        gray = ImageProcessing.gray(img)

        # Выделение вертикальных и горизонтальных линий таблиц
        tableLines = LinesSelecting.GetLines(gray)
        # Выделение Максимального контура для избавления от паразитных линий по краям скана
        tableBox = TableBorders.findContour(tableLines)

        # Приведение изображения и контуров таблицы к вертикали
        rotation = Rotation.deskew(img, tableBox, tableLines, id)
        # Разделение повёрнутых результатов
        rotatedImg, rotatedTableLines, angle = rotation
        # Нахождение повёрнутого Box для таблицы и его отрисовка
        rotatedTableBox = TableBorders.findContour(rotatedTableLines)
        TableBorders.paintContour(rotatedTableLines, rotatedTableBox)

        # Обрезка изображения по границам таблицы
        croppedTableLines = ImageProcessing.crop(rotatedTableLines, rotatedTableBox, INDENT)
        # Последняя цифра это значение добавочных пикселей к краям обрезк
        croppedImg = ImageProcessing.crop(rotatedImg, rotatedTableBox, INDENT)

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

