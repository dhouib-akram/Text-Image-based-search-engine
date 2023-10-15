from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.vgg16 import VGG16, preprocess_input
from tensorflow.keras.models import Model
import numpy as np
import cv2
from skimage import io
from PIL import Image
from io import BytesIO
from joblib import load
import base64

class FeatureExtractor:
    def __init__(self):
        base_model = VGG16(weights='imagenet')
        self.model = Model(inputs=base_model.input, outputs=base_model.get_layer('fc1').output)
        self.pca = load("pca_model20k.pkl")

        

    def _extract(self, img):
        img = cv2.resize(img,(224, 224),interpolation=cv2.INTER_AREA)
        x = image.img_to_array(img)  
        x = np.expand_dims(x, axis=0)
        x = preprocess_input(x)
        feature = self.model.predict(x)[0]
        return feature / np.linalg.norm(feature)
    
    def _run_pca(self, img):
        features = self._extract(img)
        return self.pca.transform(features.reshape(1,-1))[0].tolist()
    
    def get_from_link(self, img_link: str):
        image = io.imread(img_link)
        return self._run_pca(image)
    
    def get_from_image(self, img):
        image_bytes = base64.b64decode(img)
        image_np = np.frombuffer(image_bytes, dtype=np.uint8)
        img = cv2.imdecode(image_np, cv2.IMREAD_COLOR)
        return self._run_pca(img)