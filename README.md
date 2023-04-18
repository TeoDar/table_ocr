# Сервис распознавания сканированных таблиц. pdf/png
Для работы на Windows необходимо добавить в переменные среды (пример):
* "FLASK_APP": "/App/app.py",
* "FLASK_ENV": "development",
* "TESSDATA_PREFIX": "/tessdata" -> Путь до папки где лежит файл даты для Tesseract (rus.traineddata)
* "TESSERACT_CMD": "C:/Program Files/Tesseract-OCR/tesseract.exe" -> Путь до установленного tesseract.exe

Для быстрого разворачивания запустить expand_enviroment.bat