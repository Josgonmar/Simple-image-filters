import cv2
import numpy as np
import streamlit as st
import io
import base64
from PIL import Image

class ImageFilterApp():
    def __init__(self):
        st.title("Simple image filters")

    def run(self):
        uploaded_image_file = st.file_uploader("Upload an image:", type=['png', 'jpg'])

        if uploaded_image_file is not None:
            image = self.__toOpenCV(uploaded_image_file)
            input_col, output_col = st.columns(2)

            with input_col:
                st.header('Original input')
                st.image(image, channels='BGR', use_column_width=True)

            st.header("Filter examples:")
            option = st.selectbox('Select a filter:', ('None','Black and White','Sepia / Vintage','Vignette Effect','Pencil Sketch'))

            self.__setFilterCols(image)
            filtered_img, colour = self.__generateSelection(option, image)

            with output_col:
                if option != 'None':
                    st.header('Output image')
                    st.image(filtered_img, channels=colour)
                    if colour == 'BGR':
                        result = Image.fromarray(filtered_img[:,:,::-1])
                    else:
                        result = Image.fromarray(filtered_img)
                    st.markdown(self.__getDownloadLink(result,'output.jpeg'),
                                unsafe_allow_html=True)
    
    def __toOpenCV(self, src):
        raw_bytes = np.asarray(bytearray(src.read()), dtype=np.uint8)
        dst = cv2.imdecode(raw_bytes, cv2.IMREAD_COLOR)

        return dst
    
    def __getDownloadLink(self, img, filename):
        buffered = io.BytesIO()
        img.save(buffered, format = 'JPEG')
        img_str = base64.b64encode(buffered.getvalue()).decode()
        href = f'<a href="data:file/txt;base64,{img_str}" download="{filename}">Download output</a>'
        return href
    
    def __generateSelection(self, option, img):
        if option == 'None':
            colour = ''
            return img, colour
        elif option == 'Black and White':
            output = self.__blackAndWhiteFilter(img)
            colour = 'GRAY'
        elif option == 'Sepia / Vintage':
            output = self.__sepiaFilter(img)
            colour = 'BGR'
        elif option == 'Vignette Effect':
            level = st.slider('level', 1, 5, 2)
            output = self.__vignetteFilter(img, level)
            colour = 'BGR'
        elif option == 'Pencil Sketch':
            ksize = st.slider('Blur kernel size', 1, 11, 5, step=2)
            output = self.__pencilSketchFilter(img, ksize)
            colour = 'BGR'
        
        return output, colour

    def __setFilterCols(self, image):
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.caption('Black and White')
            st.image(self.__blackAndWhiteFilter(image), channels='GRAY')
        with col2:
            st.caption('Sepia / Vintage')
            st.image(self.__sepiaFilter(image), channels='BGR')
        with col3:
            st.caption('Vignette Effect')
            st.image(self.__vignetteFilter(image), channels='BGR')
        with col4:
            st.caption('Pencil Sketch')
            st.image(self.__pencilSketchFilter(image), channels='BGR')
    
    def __sepiaFilter(self, img):
        img_sepia = img.copy()
        img_sepia = cv2.cvtColor(img_sepia, cv2.COLOR_BGR2RGB)
        img_sepia = cv2.transform(img_sepia, np.matrix([[0.393, 0.769, 0.189],
                                                        [0.349, 0.686, 0.168],
                                                        [0.272, 0.534, 0.131]]))
        img_sepia = np.clip(img_sepia, 0, 255)
        img_sepia = np.array(img_sepia, dtype = np.uint8)
        img_sepia = cv2.cvtColor(img_sepia, cv2.COLOR_RGB2BGR)

        return img_sepia

    def __vignetteFilter(self, img, level=2):
        height, width = img.shape[:2]
        x_kernel = cv2.getGaussianKernel(width, width/level)
        y_kernel = cv2.getGaussianKernel(height, height/level)
        kernel = y_kernel * x_kernel.T

        mask = kernel / kernel.max()
        img_vignette = img.copy()
        for i in range(img_vignette.shape[2]):
            img_vignette[:,:,i] = img_vignette[:,:,i] * mask

        return img_vignette

    def __blackAndWhiteFilter(self, img):
        img_bw = img.copy()
        img_bw = cv2.cvtColor(img_bw, cv2.COLOR_BGR2GRAY)

        return img_bw
    
    def __pencilSketchFilter(self, img, ksize = 5):
        img_psk = img.copy()
        img_psk = cv2.GaussianBlur(img_psk, (ksize, ksize), 0, 0)
        img_psk_gray, img_psk_colour = cv2.pencilSketch(img_psk)

        return img_psk_colour


if __name__ == "__main__":
    ImageFilter_obj = ImageFilterApp()
    ImageFilter_obj.run()