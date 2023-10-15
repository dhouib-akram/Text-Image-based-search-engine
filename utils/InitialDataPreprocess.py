# Import the configuration variables from the 'config' module
import config_utils
import pandas as pd
import ast
import numpy as np 
from multiprocessing import Pool
import requests


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
    return

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
    return
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
        filtered_df[['OriginalURL',"Author","Title","Tags","ImageID"]].to_csv(config_utils.url_filtered_path)
    return



if __name__ == "__main__":
    df = pd.read_csv(config_utils.class_description_path)
    df_annot = pd.read_csv(config_utils.annotations_path, usecols=['ImageID', 'LabelName', 'Confidence'])
    df_img = pd.read_csv(config_utils.images_path, usecols=['OriginalURL', 'ImageID', 'Author', 'Title'])
    create_merged_dataframe(df_img, df_annot)
    transform_labels_to_tag(df)
    final = pd.read_csv(config_utils.final_path, usecols=['ImageID', 'OriginalURL', 'Tags', 'Author', 'Title'])
    clean_based_on_url(final)
    final = pd.read_csv(config_utils.url_filtered_path, usecols=['ImageID', 'OriginalURL', 'Tags', 'Author', 'Title'])



