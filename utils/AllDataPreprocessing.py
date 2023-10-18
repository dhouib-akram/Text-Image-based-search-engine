# Import the configuration variables from the 'config' module
import config_utils
import pandas as pd
import ast
import numpy as np 
from multiprocessing import Pool
import requests

from concurrent.futures import ThreadPoolExecutor
from tqdm import tqdm
import feature_extractor , config_utils
from sklearn.decomposition import PCA
from joblib import dump
import json
from joblib import load

def create_merged_dataframe(df_img, df_annot):
    """
    Create a merged DataFrame where each ImageID has a list of LabelNames.

    Args:
    df_img (pd.DataFrame): DataFrame containing image data.
    df_annot (pd.DataFrame): DataFrame containing annotation data.

    Returns:
    pd.DataFrame: Merged DataFrame with labels as a list for each ImageID.
    """
    df_annot = df_annot[df_annot['Confidence'] == 1]
    df_annot_grb = df_annot.groupby('ImageID')['LabelName'].agg(list)
    merged_df = pd.merge(df_img, df_annot_grb, on='ImageID', how='inner')
    merged_df.to_csv(config_utils.merged_df_path, index=False)
    return merged_df

def transform_labels_to_tag(df):
    """
    Transform LabelNames to human-readable Tags and save the processed data.

    Args:
    merged_df (pd.DataFrame): Merged DataFrame with LabelNames to be transformed.

    """
    # Read the merged data from the saved CSV file with 'LabelName' as a list
    new = pd.read_csv(config_utils.merged_df_path, converters={'LabelName': ast.literal_eval}, index=False)

    # Create a dictionary to map LabelName to human-readable tags (customize this part)
    labels = df.set_index("/m/0100nhbf")["Sprenger's tulip"].to_dict()

    # Apply the mapping to the 'LabelName' column and create a new 'Tags' column
    new['Tags'] = new['LabelName'].apply(lambda x: [labels.get(label, label) for label in x])

    # Drop the 'LabelName' column
    new.drop(axis=1, columns='LabelName', inplace=True)
    return new
# Function to check if a URL is working
def is_url_working(url: str):
    try:
        response = requests.get(url)
        return (response.status_code != 404 and response.status_code != 410)
    except requests.exceptions.RequestException:
        return False
def check_url(url: str):
    return url, is_url_working(url)
def clean_based_on_url(df):
    with Pool(processes=config_utils.num_processes) as pool:

        results = list(pool.imap(check_url, df.OriginalURL[config_utils.start:config_utils.end]), total=config_utils.end-config_utils.start)
        results_df = pd.DataFrame(results, columns=['OriginalURL', 'IsWorking'])

        # Merge the two DataFrames based on the 'OriginalURL' column
        merged_df = pd.merge(df, results_df, on='OriginalURL', how='inner')

        # Filter the rows where 'IsWorking' is True
        filtered_df = merged_df[merged_df['IsWorking']]
        
    return filtered_df[['OriginalURL',"Author","Title","Tags","ImageID"]]

def extract_features(df,new_data_path:str,start: int, end: int):
    fe=feature_extractor.FeatureExtractor()


    # Function to extract features from a URL
    def extract_features_from_url(url):
        try:
            return url, fe.get_features_from_link(url)
        except Exception as e:
            print(f"Error processing URL {url}: {e}")
            return None

    # Number of threads you want to use for parallel processing
    num_threads = 4  # You can adjust this number

    # Create a ThreadPoolExecutor
    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        pbar = tqdm(total=len(df[start:end]), desc="Extracting Features")

        # Submit tasks for each URL to be processed
        futures = [executor.submit(extract_features_from_url, url) for url in df['OriginalURL'][start:end]]

        extracted_features95 = {}

        # Iterate over completed futures
        for future in futures:
            result = future.result()
            if result is not None:
                url, features = result
                extracted_features95[url] = features
            pbar.update(1)

    # Create a list of dictionaries excluding None values
    data = [{'OriginalURL': url, 'FeatureVector': json.dumps(feature_vector.tolist())} for url, feature_vector in extracted_features95.items()]
    new=pd.DataFrame(data)
    new.to_csv(new_data_path,index=False)
    return 
def read_df(path):
    df=pd.read_csv(path)
    df['FeatureVector'] = df['FeatureVector'].apply(lambda x: np.array(json.loads(x)))
    return df
def save_pca_model(pca,pca_path):
    dump(pca, pca_path)
def read_pca(pca_path):
    return load(pca_path)
def fit_pca(data):

    n_components = 786
    pca = PCA(n_components=n_components)

    # Fit the PCA model to your data
    pca.fit(data)
    return pca

def reduce_features(df,fit_pca=False):
    data=df['FeatureVector'].values
    flattened_data = np.array([x.flatten() for x in data])
    if fit_pca:
        pca=fit_pca(flattened_data)
        save_pca_model(pca,config_utils.pca_path)
    else:
        pca=read_pca(config_utils.pca_path)
    df['FeatureVector'] = df['FeatureVector'].apply(lambda x: pca.transform(x.reshape(1, -1))[0])
    return df

if __name__ == "__main__":
    df = pd.read_csv(config_utils.class_description_path)
    df_annot = pd.read_csv(config_utils.annotations_path, usecols=['ImageID', 'LabelName', 'Confidence'])
    df_img = pd.read_csv(config_utils.images_path, usecols=['OriginalURL', 'ImageID', 'Author', 'Title'])
    merged_df= create_merged_dataframe(df_img, df_annot)
    final= transform_labels_to_tag(df)
    final=clean_based_on_url(final)
    final=extract_features(final,config_utils.data_with_features_path,config_utils.start,config_utils.end)
    perfect=read_df(config_utils.data_with_features_path)
    perfect_reduced=reduce_features(perfect)



