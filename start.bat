call workon venv & cd C:\PROJECTS\table_ocr\ & streamlit run streamlit_app.py
::powershell -c streamlit run streamlit_app.py
::powershell -c uvicorn App.Routes.main:MainApp --reload