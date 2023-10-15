from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.vgg16 import VGG16, preprocess_input
from tensorflow.keras.models import Model
import numpy as np
import cv2
from skimage import io

class FeatureExtractor:
    def __init__(self):
        base_model = VGG16(weights='imagenet')
        self.model = Model(inputs=base_model.input, outputs=base_model.get_layer('fc1').output)
        

    def _extract(self, img):
        img = cv2.resize(img,(224, 224),interpolation=cv2.INTER_AREA)
        x = image.img_to_array(img)  
        x = np.expand_dims(x, axis=0)
        x = preprocess_input(x)
        feature = self.model.predict(x)
        return feature / np.linalg.norm(feature)
    
    def get_features_from_link(self, img_link: str):
        image = io.imread(img_link)
        return self._extract(image)
    
    def get_features_from_image(self, img):
        return self._extract(img)