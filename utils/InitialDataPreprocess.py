# Import the configuration variables from the 'config' module
import config
import pandas as pd
import ast



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
    merged_df.to_csv(config.merged_df_path, index=False)
    return

def transform_labels_to_tag(df):
    """
    Transform LabelNames to human-readable Tags and save the processed data.

    Args:
    merged_df (pd.DataFrame): Merged DataFrame with LabelNames to be transformed.

    """
    # Read the merged data from the saved CSV file with 'LabelName' as a list
    new = pd.read_csv(config.merged_df_path, converters={'LabelName': ast.literal_eval}, index=False)

    # Create a dictionary to map LabelName to human-readable tags (customize this part)
    labels = df.set_index("/m/0100nhbf")["Sprenger's tulip"].to_dict()

    # Apply the mapping to the 'LabelName' column and create a new 'Tags' column
    new['Tags'] = new['LabelName'].apply(lambda x: [labels.get(label, label) for label in x])

    # Drop the 'LabelName' column
    new.drop(axis=1, columns='LabelName', inplace=True)
    return

if __name__ == "__main__":
    df = pd.read_csv(config.class_description_path)
    df_annot = pd.read_csv(config.annotations_path, usecols=['ImageID', 'LabelName', 'Confidence'])
    df_img = pd.read_csv(config.images_path, usecols=['OriginalURL', 'ImageID', 'Author', 'Title'])
    create_merged_dataframe(df_img, df_annot)
    transform_labels_to_tag(df)
    final = pd.read_csv(config.final_path, usecols=['ImageID', 'OriginalURL', 'Tags', 'Author', 'Title'])

