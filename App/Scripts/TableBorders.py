import cv2
import numpy as np

rand = np.random.random() # Случайное число от 0 до 1

def findContour(tableLines):
    """Функция для отделения наибольшего замкнутого контура на скане (Как правило это край таблицы)

    Args:
        tableLines [Array]: Вычленённые ранее вертикальные и горизонтальные линии

    Returns:
        [Array]: Координаты вершин квадрата в который вписывается этот контур
    """
    # Ищем контуры и складируем их в переменную contours
    contours, hierarchy = cv2.findContours(tableLines, cv2.RETR_TREE, cv2.CHAIN_APPROX_TC89_L1)
    # Находим наиболее большой контур (по идее это контур всей таблицы)
    maxContour = max(contours, key = cv2.contourArea)
    # Найдём квадрат минимальной площади в который впишется наш контур
    minContourBox = cv2.minAreaRect(maxContour)
    box = cv2.boxPoints(minContourBox)
    box = np.int0(box)
    
    return box

def paintContour(img, box):
    """Отрисовать контур на изображении
    """
    cv2.drawContours(img, [box],0,(255,255,255),3)