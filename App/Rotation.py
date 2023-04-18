import numpy as np
import cv2

def deskew(img, tableBox, tableLines, iter):
    # Изначальная версия получения угла
    # Вычисление координат участков изображения с положительным порогом
    #coords = np.column_stack(np.where(lines>0))
    #angle = cv2.minAreaRect(coords)[-1]

    angle = 0
    x1, y1 = tableBox[0]
    x2, y2 = tableBox[3]
    try:
        angle = np.arctan((y2-y1)/(x2-x1))*180/np.pi
    except:
        angle = np.sign(y2-y1) * np.pi/2
    # Такие сложные преобразования нужны из-за особенностей работы warpAffine и получаемого угла
    if angle > 45:
        angle = angle - 90
    if angle == 90:
        angle = 0
    angle = round(angle, 4)
    # Поворот изображения до вертикали
    (h, w) = img.shape[:2]
    center = (w // 2, h // 2) # Поворот относительно центра
    rotationMatrix = cv2.getRotationMatrix2D(center, angle, 1.0)
    # Поворот изначального изображения
    rotatedImg = cv2.warpAffine(img, rotationMatrix, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
    # Поворот сетки таблицы
    rotatedLines = cv2.warpAffine(tableLines, rotationMatrix, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
    # Можно нарисовать угол изменения прям на изображении
    #cv2.putText(rotated, f'Angle: {angle} degrees', center, cv2.FONT_ITALIC, 1, (0, 0, 180), 2)
    print(f'[INFO] page №{iter}\n  Deskewing angle: {round(angle)}')
    return [rotatedImg, rotatedLines, angle]