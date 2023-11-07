import base64

from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.mobilenet import MobileNet, preprocess_input
from tensorflow.keras.models import Model

import numpy as np
import cv2
from skimage import io


class FeatureExtractor:
    def __init__(self):
        base_model = MobileNet(weights='imagenet', include_top=False)
        layer_name = 'conv_pw_13_relu'
        selected_layer = base_model.get_layer(layer_name).output
        self.model = Model(inputs=base_model.input, outputs=selected_layer)

    def _extract(self, img):
        img = cv2.resize(img, (224, 224), interpolation=cv2.INTER_AREA)
        x = image.img_to_array(img)
        x = np.expand_dims(x, axis=0)
        x = preprocess_input(x)
        feature = self.model.predict(x)
        feature = np.mean(feature, axis=(1, 2))
        return (feature / np.linalg.norm(feature))[0]

    def get_from_link(self, img_link: str):
        image = io.imread(img_link)
        return self._extract(image)

    def get_from_image(self, img):
        image_bytes=base64.b64decode(img)
        image_np=np.frombuffer(image_bytes,dtype=np.uint8)
        img=cv2.imdecode(image_np,cv2.IMREAD_COLOR)
        return self._extract(img)