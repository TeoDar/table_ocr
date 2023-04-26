from imports import *
import re
import pytesseract
import ImageProcessing


def searchText(img, atributesToCoordinates, textFromCells):
    path = os.getenv("TESSDATA_PREFIX")
    if os.name == 'nt':
        pytesseract.pytesseract.tesseract_cmd = os.getenv("TESSERACT_CMD")
    # Преобразование цветов в серые тона
    gray = ImageProcessing.gray(img)
    # Адаптивное удаление шумов и теней
    aThresh = ImageProcessing.adoptThresh(gray, 21, 10)
    
    for key, value in atributesToCoordinates.items():
        if value == None:
            textFromCells[key] = ''
            continue
        try:
            x1, y1, x2, y2 = value[0][0], value[0][1], value[2][0], value[2][1]
        except:
            x1, y1, x2, y2 = value[0][0][0], value[0][0][1], value[0][2][0], value[0][2][1]
        
        # Обрезка обработанного изображения на ячейкиs
        cellImg = aThresh[y1:y2, x1:x2]
        
        # Получение текста из вырезанной ячейки
        text = pytesseract.image_to_string(
            cellImg, 'rus', f'--tessdata-dir "{path}" --psm 6 --oem 1')
        text = text.replace("\n", " ")
        text = re.sub(r' *[^ \(\)А-Яа-я\d\w\/\\\.\-,:; ]+ *', ' ', text)
        while text.find('  ') != -1:
            text = text.replace('  ', ' ')
        text = text.strip()
        
        #print(text)
        # cv2.namedWindow(f'lines', cv2.WINDOW_NORMAL)
        # cv2.imshow(f"lines", cellImg)
        # cv2.waitKey(0)
        # cv2.destroyWindow(f'lines')
        
        textFromCells[key] = text
    return textFromCells
