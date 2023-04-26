import numpy as np
import cv2

def GetLines(gray):
    """Извлекает из изображения только вертикальные и горизонтальные линии с помощью морфологических операций

    Args:
        gray [Array]: Изображение в серых тонах

    Returns:
        [Array]: Выделенные вертикальные и горизонтальные линии на двоичном изображении
    """
    # Применение адаптивного порогового значения
    gray = cv2.bitwise_not(gray)
    thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY, 15, -2)
    
    # Применение морфологического закрытия пробелов в ядре
    kernel = np.ones((3, 3), np.uint8)
    thresh = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
    
    # Создание изображений, которые будут использоваться для получения горизонтальных и вертикальных линий
    horizontal = np.copy(thresh)
    vertical = np.copy(thresh)
    
    # Определение размера горизонтальных линий
    cols = horizontal.shape[1]
    horisontalsize = int(cols / 30)
    # Create structure element for extracting horizontal lines through morphology operations
    horizontalStructure = cv2.getStructuringElement(cv2.MORPH_RECT, (horisontalsize, 1))
    # Применение морфологических операций по горизонтали
    horizontal = cv2.erode(horizontal, horizontalStructure)
    horizontal = cv2.dilate(horizontal, horizontalStructure)
    
    # Определение размера вертикальных линий для морфологического вычленения
    rows = vertical.shape[0]
    verticalsize = int(rows / 50)
    # Create structure element for extracting vertical lines through morphology operations
    verticalStructure = cv2.getStructuringElement(cv2.MORPH_RECT, (1, verticalsize))
    # Применение морфологических операций по вертикальной оси
    vertical = cv2.erode(vertical, verticalStructure)
    vertical = cv2.dilate(vertical, verticalStructure)

    # Слияние вертикальных и горизонтальных линий
    lines = cv2.add(vertical, horizontal)
    

    edges = cv2.adaptiveThreshold(lines, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 3, -2)
    kernel = np.ones((4, 4), np.uint8)
    # cv2.namedWindow(f'lines1', cv2.WINDOW_NORMAL)
    # cv2.imshow(f"lines1", edges)
    # cv2.waitKey(0)
    
    # Утолщение полученных линий
    edges = cv2.dilate(edges, kernel)
    smooth = np.copy(lines)
    smooth = cv2.blur(smooth, (2, 2))

    (rows, cols) = np.where(edges != 0)
    lines[rows, cols] = smooth[rows, cols]
    return lines