# Сервис распознавания сканированных таблиц pdf/png.
## Включает в себя streamlit web-интерфейс и fast-api сервер, для обработки запросов распознавания.

Для работы с PDF для библиотеки pdf2image необходим propler
Ещё нужно ядро Tesseract

Для работы на Windows необходимо добавить в переменные среды (пример):
* "TESSDATA_PREFIX": "/tessdata" -> Путь до папки где лежит файл даты для Tesseract (rus.traineddata)
* "TESSERACT_CMD": "C:/Program Files/Tesseract-OCR/tesseract.exe" -> Путь до установленного tesseract.exe

Для быстрого разворачивания запустить expand_enviroment.bat