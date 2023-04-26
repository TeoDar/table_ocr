import cv2


def gray(img):
    """Преобразует изображение в оттенки серого

    Args:
        img [Array]: Изображение в формате PNG

    Returns:
        [Array]: Изображение в оттенках серого
    """
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    return gray


def thresh(gray):
    """Преобразует изображение в двоичное по пороговому значению с использованием алгоритма OTSU

    Args:
        gray [Array]: Изображение в оттенках серого (обязательно)

    Returns:
        [Array]: Двоичное изображение
    """
    thresh = cv2.threshold(
        gray, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
    return thresh


def adoptThresh(gray, C, d):
    """Преобразует изображение в двоичное по адаптивному пороговому значению

    Args:
        gray [Array]: Изображение в оттенках серого (обязательно)
        C [Int]: Размер квадратной матрицы ядра
        d [Int]: Величина уменьшения порога

    Returns:
        [Array]: Двоичное иображение
    """
    aThresh = cv2.adaptiveThreshold(
        gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, C, d)
    return aThresh


def crop(img, box, plus):
    """Обрезает изображение по координатам из [box] со смещением их от центра [box] на [plus] 

    Args:
        img [Array]: Изображение
        box [Array]: Массив координат вырезаемого прямоугольника
        plus [Int]: Величина смещения координат от центра

    Returns:
        [Array]: Обрезанное изображение
    """
    x0, y0 = box[0]
    x1, y1 = box[1]
    x2, y2 = box[2]
    x3, y3 = box[3]
    minx = min(x0, x1, x2, x3) - plus
    maxx = max(x0, x1, x2, x3) + plus
    miny = min(y0, y1, y2, y3) - plus
    maxy = max(y0, y1, y2, y3) + plus
    croppedImg = img[miny:maxy, minx:maxx]
    return croppedImg
