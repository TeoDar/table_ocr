from App import HOST, PORT
import webbrowser

import requests

import streamlit as st
from streamlit_option_menu import option_menu
from st_click_detector import click_detector

SERVER_URL = f'http://{HOST}:{PORT}'
session = requests.Session()

if 'npage' not in st.session_state:
    st.session_state['npage'] = 0
if 'clicked' not in st.session_state:
    st.session_state['clicked'] = None


def st_request_error_wrapper(func):
        def wrapper(*args, **kwargs):
            try:
                response = func(*args, **kwargs)
                response.raise_for_status()
                return response.json()
            except requests.exceptions.HTTPError as err:
                st.write(err.response.status_code, err.response.json()['detail'])
                st.stop()
        return wrapper

class WebPage:
    '''
    Класс реализующий основное окно приложения
    '''

    def __init__(self) -> None:
        # Задание общих параметров сайта
        st.set_page_config(page_title='Распознавание таблиц', page_icon='📰', layout='wide', )
        # Добавление бокового меню
        with st.sidebar:
            self.draw_side_bar()
        if self.selected in 'Шаблоны':
            st.title("Создание шаблона распознавания")
            uploaded_file = None
            with st.sidebar:
                st.header('Загрузите скан:')
                uploaded_file = st.file_uploader('Только для типов [PDF] и [PNG]', type=('pdf', 'png'))
            if uploaded_file:
                self.upload(uploaded_file)
        if self.selected in 'API Справка':
            webbrowser.open_new_tab('http://127.0.0.1:8000/docs')
        if self.selected in 'Разработчик':
            webbrowser.open_new_tab('https://t.me/TeoDar')
        if self.selected in 'Тест':
            self.test()

    def upload(self, file):
        file = {"file": (file.name, file.getvalue())}
        with st.spinner('Загрузка файла и извлечение изображений'):
            upload_result = self.request(method='file_post', url=f"{SERVER_URL}/upload_file", file=file)
            st.write(upload_result)
    
    @st_request_error_wrapper
    def request(self, method:str, url:str, *args, **kwargs) -> str:
        if method=='file_post':
            return session.post(url, files=kwargs)
        
    def get_view(self, url:str) -> str:
        try:
            response = session.get(url)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as err:
            st.write(err.response.status_code, err.response.json()['detail'])
            st.stop()

    def draw_side_bar(self):
        self.selected = option_menu(
            menu_title="TABLE-OCR",
            options=["Шаблоны", "Распознавание", "API Справка", "Разработчик", "Тест"],
            default_index=0,
            menu_icon="table",
            icons=['border', 'eye', 'book', 'person lines fill'],
            styles={
                #"container": {"background-color": "rgb(14, 17, 23)"},
                # "icon": {"color": "#ffb4b4", "font-size": "25px"},
                "nav-item": {"padding": "2px"},
                "nav-link": {"margin": "0px", "--hover-color": "gray"},
                "nav-link-selected": {"background-color": "gray"},
            })

    def test(self):
        with open('./App/FrontEnd/html/test.html', encoding='utf-8') as f:
            st.session_state.clicked = click_detector(f.read())
            st.write(st.session_state.clicked)
#           <p><a href='#' id='Link 2'>Second link</a></p>

if __name__ == "__main__":
    WebPage()
