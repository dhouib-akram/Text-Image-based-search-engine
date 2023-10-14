from concurrent.futures import ThreadPoolExecutor
from tqdm import tqdm
import pandas as pd 
df=pd.read_csv("C:\content-based-search-engine\Text-Image-based-search-engine\perfect90k.csv",usecols=['ImageID','OriginalURL','Tags', 'Author','Title'])

from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.vgg16 import VGG16, preprocess_input
from tensorflow.keras.models import Model
import numpy as np
import cv2
from skimage import io
import requests
import pandas as pd
import feature_extractor


fe=feature_extractor.FeatureExtractor()
# Function to extract features from a URL
def extract_features_from_url(url):
    try:
        return url, list(fe.get_features_from_link(url))
    except Exception as e:
        print(f"Error processing URL {url}: {e}")
        return url, []

# Number of threads you want to use for parallel processing
num_threads = 4  # You can adjust this number

# Create a ThreadPoolExecutor
with ThreadPoolExecutor(max_workers=num_threads) as executor:
    pbar = tqdm(total=len(df[5000:7000]), desc="Extracting Features")

    # Submit tasks for each URL to be processed
    futures = [executor.submit(extract_features_from_url, url) for url in df['OriginalURL'][:20000]]

    extracted_features = {}

    # Iterate over completed futures
    for future in futures:
        url, features = future.result()
        extracted_features[url] = features
        pbar.update(1)

# Combine the extracted features into a NumPy array
# extracted_features will contain the results