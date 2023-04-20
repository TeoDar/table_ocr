import requests
import streamlit as st
from streamlit_option_menu import option_menu
import webbrowser


fast_api_url = 'http://127.0.0.1:8000'


class MainPage:
    '''
    Красс реализующий основное окно приложения
    '''

    def __init__(self) -> None:
        # Задание общих параметров сайта
        st.set_page_config(page_title='Распознавание таблиц', page_icon='📰', layout='wide')
        # Добавление бокового меню
        with st.sidebar:
            self.draw_side_bar()

        if self.selected in 'Шаблоны':
            st.title("Создание шаблона распознавания")
            st.header('Загрузите скан:')
            uploaded_file = st.file_uploader('Только для типов [PDF] и [PNG]', type=('pdf', 'png'))
            if uploaded_file:
                self.upload(uploaded_file)

        if self.selected in 'Связаться с разработчиком':
            webbrowser.open_new_tab('https://t.me/TeoDar')

        if self.selected in 'test':
            # test
            test_file = st.file_uploader('Только для типов [PDF] и [PNG]', type=('pdf', 'png'))
            if test_file:
                try:
                    file = {"file": (test_file.name, test_file.getvalue())}
                    response = requests.post(f"{fast_api_url}/faultreport", files=file)
                    response.raise_for_status()
                    st.write(response.json())
                except requests.exceptions.HTTPError as err:
                    st.write(err.response.status_code, ':', err.response.json()['detail'])
            with open('./FrontEnd/test.html', encoding='utf-8') as f:
                st.markdown(f.read(), unsafe_allow_html=True,)

    def draw_side_bar(self):
        self.selected = option_menu(
            menu_title="TABLE-OCR",
            options=["Шаблоны", "Распознавание", "Справка", "Связаться с разработчиком", "test"],
            default_index=0,
            menu_icon="table",
            icons=['border', 'eye', 'book', 'person lines fill'],
            styles={
                "container": {"background-color": "rgb(14, 17, 23)"},
                # "icon": {"color": "#ffb4b4", "font-size": "25px"},
                "nav-item": {"padding": "2px"},
                "nav-link": {"margin": "0px", "--hover-color": "#eee"},
                "nav-link-selected": {"background-color": "gray"},
            })

    def upload(self, uploaded_file):
        file = {"file": (uploaded_file.name, uploaded_file.getvalue())}
        with st.spinner('Загрузка файла и извлечение изображений'):
            try:
                response = requests.post(f"{fast_api_url}/upload_file", files=file)
                response.raise_for_status()
            except requests.exceptions.HTTPError as err:
                st.write(err.response.status_code, ':', err.response.json()['detail'])
                st.stop()

        file_hash: str = response.json()["file_hash"]
        extracted_images_hashes: list = response.json()["extracted_images_hashes"]

        for img_hash in extracted_images_hashes:
            image_link = f"{fast_api_url}/get_image/{file_hash}/{img_hash}"
            with st.sidebar:
                with open('./FrontEnd/button.html') as f:
                    button_html = f.read().replace('src=""', f'src="{image_link}"')
                    st.markdown(button_html, unsafe_allow_html=True,)
            with open('./FrontEnd/image_style.txt') as f:
                image_style = f.read()
                image_html = f'<img src="{image_link}" style="{image_style}">'
                st.markdown(image_html, unsafe_allow_html=True)


if __name__ == "__main__":
    MainPage()
