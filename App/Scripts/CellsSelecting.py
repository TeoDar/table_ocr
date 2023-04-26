import numpy as np
import cv2




def coordSort(box, z):
    """Функция, сортирующая координаты полученных ячеек по часовой стрелке. Первая координата левая верхняя вершина ячейки

    Args:
        box (Array): Массив массивов с координатами ячеек
        z (int): Величина смещения координат относительно центра ячейки (для увеличения или уменьшения ячейки)

    Returns:
        Array: Массив массивов отсортированных ячеек
    """
    x0, y0 = box[0]
    x1, y1 = box[1]
    x2, y2 = box[2]
    x3, y3 = box[3]
    minx = round(min(x0, x1, x2, x3))
    maxx = round(max(x0, x1, x2, x3))
    miny = round(min(y0, y1, y2, y3))
    maxy = round(max(y0, y1, y2, y3))
    sortedBox = [[minx + z, miny + z],[maxx - z, miny + z],[maxx - z, maxy - z],[minx + z, maxy - z]]
    return sortedBox

def divideTable(croppedTableLines):
    """Функция распознающая контуры ячеек на выделенных линиях скана. Также отделяет лишние контуры с отличными от ячеек размерностями

    Args:
        croppedTableLines (Bitmap Image Array): Вырезанные со скана отдельные вертикатьные и горизонтальные линии

    Returns:
        Array: Массив массивов координат вершин распознанных ячеек
    """
    contours, hierarchy = cv2.findContours(croppedTableLines, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_TC89_L1)
    cells = []
    z = 1
    idCont = 0
    for contour in contours:        
        Area = int(cv2.contourArea(contour))
        if Area>500 and Area<500000:
            cell = cv2.minAreaRect(contour)
            box = cv2.boxPoints(cell)
            box = coordSort(box, z)
            # Если размеры коробки ширина и высота адекватные для ячейки и по иерархии ячейка отдельная от остальных
            if abs(box[0][1]-box[2][1]) > 5 and abs(box[0][0]-box[2][0]) > 10 and hierarchy[0][idCont][3] != -1:
                cells.append(box)
        idCont = idCont + 1
    return cells
