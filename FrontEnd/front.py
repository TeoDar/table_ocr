import time
import requests
import streamlit as st

fast_api_url = 'http://127.0.0.1:8000/api/2.0'


class Front:
    def __init__(self) -> None:
        st.set_page_config(page_title='Распознавание таблиц', page_icon='📰', layout='wide')
        st.title("Распознавание таблиц")
        with st.sidebar:
            st.header('Загрузите скан:')
            self.uploaded_file = st.file_uploader('Только для типов [PDF] и [PNG]', type=('pdf', 'png'))
        if self.uploaded_file:
            self.upload()
        
    def upload(self):
        with st.sidebar:
            recognize_btn = st.button('Распознать')

        if recognize_btn:
            stage_text = 'Извлечение изображений'
            stage = st.text(stage_text)

            file = {"file": (self.uploaded_file.name, self.uploaded_file.getvalue())}
            response = requests.post(f"{fast_api_url}/upload_file", files=file)

            file_hash: str = response.json()["file_hash"]
            extracted_images_hashes: list = response.json()["extracted_images_hashes"]

            for img_hash in extracted_images_hashes:
                try:
                    img_response = requests.get(f"{fast_api_url}/get_image/{file_hash}/{img_hash}", stream=True)
                    img_response.raise_for_status()
                except requests.exceptions.HTTPError as err:
                    st.write(err.response.status_code, ':', err.response.json()['detail'])
                    continue
                image = img_response.content.decode()
                with st.sidebar:
                    with open('./FrontEnd/button_style.txt')as f:
                        button_style = f.read().format(image=image)
                        button_html = f'<button type="button" style="{button_style}">'
                        st.markdown(button_html, unsafe_allow_html=True,)
                with open('./FrontEnd/image_style.txt')as f:
                    image_style = f.read()
                    image_html = f'<img src="data:image/png;base64,{image}" style="{image_style}">'
                    st.markdown(image_html, unsafe_allow_html = True)
            stage.text('Предобработка и получение сетки таблицы')

# with st.spinner('Wait for it...'):
#     time.sleep(5)
# st.success('Done!')


if __name__=="__main__":
    Front()