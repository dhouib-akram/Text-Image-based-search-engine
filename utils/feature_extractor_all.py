import numpy as np
import pandas as pd
import feature_extractor

import json
fe=feature_extractor.FeatureExtractor()
df=pd.read_csv("./final.csv",usecols=['ImageID','OriginalURL','Tags', 'Author','Title'])
# Function to extract features from a URL
def extract_features_from_url(url):
    try:
        return url, fe.get_features_from_link(url)
    except Exception as e:
        print(f"Error processing URL {url}: {e}")
        return None
try:
    df10 = pd.read_csv('./saving2.csv')
except FileNotFoundError:
    df10 = pd.DataFrame(columns=['OriginalURL', 'FeatureVector'])

last_processed_index = df10.index.max() if not df10.empty else 0
for i, url in enumerate(df['OriginalURL'][last_processed_index:], start=last_processed_index):
    result = extract_features_from_url(url)
    if result is not None:
        url, features = result
    if df10[df10['OriginalURL'] == url].empty:
        data = {'ImageID':df['ImageID'][i],'Tags':df['Tags'][i], 'Author':df['Author'][i],
            'Title':df['Title'][i],'OriginalURL': url, 'FeatureVector': json.dumps(features.tolist())}
        df10 = df10._append(data, ignore_index=True)

    print(f"Processed URL {i + 1}/{len(df['OriginalURL'][last_processed_index:])}: {url}")
    df10.to_csv('./saving2.csv', index=False)