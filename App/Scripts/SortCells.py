import cv2
import numpy as np


def drawCells(copyImg, row, numRow):
    cnt = np.int0(row)
    color = (round(np.random.random()*255), round(np.random.random()*255), round(np.random.random()*255))
    cv2.drawContours(copyImg, cnt, -1, color, 2, cv2.LINE_AA)
    cv2.putText(copyImg, f'{numRow}', row[0][3], cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2, cv2.LINE_AA)
    for i in range(len(row)):
        cv2.putText(copyImg, f'{i+1}', (row[i][1][0]-15, row[i][1][1]+18), cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2, cv2.LINE_AA)

def cellSorting(img, cells):
    """Функция сортирует полученный массив ячеек по строкам (по уровням ячеек)

    Args:
        cells (Array):

    Returns:
        [Array]:
    """
    
    copyImg = img.copy()
    
    cellsByRow = []
    row = []
    cells = sorted(cells , key=lambda k: [k[3][1], k[3][0]]) # Сортировка сначала по "y" потом по "x"
    prev_y = cells[0][2][1] # Координата "y" первой ячейки
    
    for i, cell in enumerate(cells):
        y = cell[2][1]
        if y>prev_y+5: # Условие начала новой строки
            row = sorted(row, key=lambda k: k[3][0])
            cellsByRow.append(row) # Дополнительная сортировка по х в каждой строке
            
            # Выделить строки разными цветами
            drawCells(copyImg, row, len(cellsByRow))
            
            row = []
        row.append(cell)
        prev_y = y
        

    # cv2.namedWindow(f'rows', cv2.WINDOW_NORMAL)
    # cv2.imshow(f"rows", copyImg)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    print(f'  Number of recognated rows: {len(cellsByRow)}, cells: {i}')
    return cellsByRow