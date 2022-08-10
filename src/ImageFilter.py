import pathlib
import numpy as np
import cv2


class ImageFilter:
    __image_path = None
    __input_image = None
    __window_name = "Select which filter(s) you would like to apply"
    __sepia = False
    __vignette = False
    __bw = False
    __pskt = False

    def __init__(self, image_path):
        self.__image_path = image_path
        self.__input_image = cv2.imread(self.__image_path, cv2.IMREAD_COLOR)
    
    def run(self):
        try:
            downsized_img = cv2.resize(self.__input_image,None,fx=0.8,fy=0.8) #Downsized copy of the images just to show the results
            downsized_sepia = self.__sepiaFilter(downsized_img)
            downsized_vignette = self.__vignetteFilter(downsized_img)
            downsized_black_and_white = self.__blackAndWhiteFilter(downsized_img)
            downsized_pencil_sketch = self.__pencilSketchFilter(downsized_img)

            upper_filters = cv2.hconcat([downsized_sepia, downsized_vignette])
            bottom_filters = cv2.hconcat([downsized_black_and_white, downsized_pencil_sketch])
            select_window = cv2.vconcat([upper_filters, bottom_filters])

            print("[INFO] Close the window to proceed with your selection...")

            cv2.imshow(self.__window_name, select_window)
            cv2.setMouseCallback(self.__window_name, self.__mouseHandlerCallback, select_window.copy())
            cv2.waitKey(0)
            cv2.destroyAllWindows()

            print("[INFO] Correctly executed program. Saving and finishing...")

            self.__applyAndSave()
        except:
            print('[ERROR] An error occurred. Finishing execution.')
    
    def __applyAndSave(self):
        if self.__sepia:
            full_img_sepia = self.__sepiaFilter(self.__input_image)
            sepia_path = str(pathlib.Path(self.__image_path).with_suffix('')) + '-sepia.jpg'
            cv2.imwrite(sepia_path, full_img_sepia)
            print("Saved", sepia_path)
        if self.__bw:
            full_img_bw = self.__blackAndWhiteFilter(self.__input_image)
            bw_path = str(pathlib.Path(self.__image_path).with_suffix('')) + '-bw.jpg'
            cv2.imwrite(bw_path, full_img_bw)
            print("Saved", bw_path)
        if self.__vignette:
            full_img_vignette = self.__vignetteFilter(self.__input_image)
            vignette_path = str(pathlib.Path(self.__image_path).with_suffix('')) + '-vignette.jpg'
            cv2.imwrite(vignette_path, full_img_vignette)
            print("Saved", vignette_path)
        if self.__pskt:
            full_img_pskt = self.__pencilSketchFilter(self.__input_image)
            pskt_path = str(pathlib.Path(self.__image_path).with_suffix('')) + '-pskt.jpg'
            cv2.imwrite(pskt_path, full_img_pskt)
            print("Saved", pskt_path)
    
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
        img_bw = cv2.cvtColor(img_bw, cv2.COLOR_GRAY2BGR) #It needs to be converted back into a three channels image

        return img_bw
    
    def __pencilSketchFilter(self, img):
        img_psk = img.copy()
        img_psk = cv2.GaussianBlur(img_psk, (5,5), 0, 0)
        img_psk_gray, img_psk_colour = cv2.pencilSketch(img_psk)

        return img_psk_colour

    def __mouseHandlerCallback(self, event, x, y, flags, img):
        if event == cv2.EVENT_LBUTTONDOWN:
            # Remark the selected filter(s) with a red rectangle
            final_img = self.__getSelectedFilter(x, y, img.copy())
            cv2.imshow(self.__window_name, final_img)

    def __remarkSelected(self, img):
        if self.__sepia:
            upper_left = np.array([0,0], dtype=int)
            bottom_right = np.array([img.shape[1]/2, img.shape[0]/2], dtype=int)
            cv2.rectangle(img, upper_left, bottom_right, (0,0,255), 1)
        if self.__bw:
            upper_left = np.array([0, img.shape[0]/2], dtype=int)
            bottom_right = np.array([img.shape[1]/2, img.shape[0]-1], dtype=int)
            cv2.rectangle(img, upper_left, bottom_right, (0,0,255), 1)
        if self.__vignette:
            upper_left = np.array([img.shape[1]/2,0], dtype=int)
            bottom_right = np.array([img.shape[1]-1, img.shape[0]/2], dtype=int)
            cv2.rectangle(img, upper_left, bottom_right, (0,0,255), 1)
        if self.__pskt:
            upper_left = np.array([img.shape[1]/2, img.shape[0]/2], dtype=int)
            bottom_right = np.array([img.shape[1]-1, img.shape[0]-1], dtype=int)
            cv2.rectangle(img, upper_left, bottom_right, (0,0,255), 1)
        
        return img

    def __getSelectedFilter(self, x, y, img):
        if x>=0 and x<=int(img.shape[1]/2):
            if y>=0 and y<=int(img.shape[0]/2): #Selected the top-left corner (Sepia)
                if not self.__sepia:
                    self.__sepia = True
                else:
                    self.__sepia = False
            else: #Selected the bottom-left corner(Black and white)
                if not self.__bw:
                    self.__bw = True
                else:
                    self.__bw = False
        else:
            if y>=0 and y<=int(img.shape[0]/2): #Selected the top-right corner (Vignette)
                if not self.__vignette:
                    self.__vignette = True
                else:
                    self.__vignette = False
            else: #Selected the bottom-right corner (Pencil sketch)
                if not self.__pskt:
                    self.__pskt = True
                else:
                    self.__pskt = False

        after_selection_img = self.__remarkSelected(img)

        return after_selection_img



if __name__ == "__main__":
    imageFilter_obj = ImageFilter(input("Enter the image path: "))
    imageFilter_obj.run()