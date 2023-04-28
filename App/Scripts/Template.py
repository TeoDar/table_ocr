from App.Scripts import *
import App.Scripts.PDFtoPNG as PDFtoPNG
import App.Scripts.ImageProcessing as ImageProcessing
import App.Scripts.LinesSelecting as LinesSelecting
import App.Scripts.TableBorders as TableBorders
import App.Scripts.Rotation as Rotation
import App.Scripts.CellsSelecting as CellsSelecting
import App.Scripts.SortCells as SortCells


class Template:
    @staticmethod
    def get_cropped_template(file_hash:str, img_hash:str)->str:
        '''Возвращает обрезанные изображения и массив ячеек'''
        image_path = f'{ROOT_PATH}/{file_hash}/{img_hash}.png'
        cropped_path = f'{ROOT_PATH}/{file_hash}/'
        cropped_hash = f'cropped_{img_hash}'

        if not os.path.isfile(image_path): raise Exception
        cv_image = cv2.imread(image_path)[...,::-1] # Срез для правильного считывания RGB вместо BRG
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

        # Получение координат ячеек таблицы
        cells = CellsSelecting.divideTable(croppedTableLines)
        # Разделение распознанных ячеек по строкам. Тут отрисовка ячеек
        cellsByRow = SortCells.cellSorting(croppedImg, cells)
        
        # Тестовая отрисовка ячеек поверх основного изображения
        # for id, row in enumerate(cellsByRow):
        #     croppedImg = SortCells.drawCells(croppedImg, row, id)
        if not cellsByRow: return None
        if f'{cropped_hash}.png' in os.listdir(cropped_path):
            print('[Cropped already exits]')
            return cropped_hash
        img_hash = PDFtoPNG.save_images(cropped_path, [croppedImg.copy(order='C')], cropped_hash)
        return img_hash[0]
        
        self.generate_template(croppedImg, cellsByRow)

    def generate_template(self, croppedImg, cellsByRow):
        pass
