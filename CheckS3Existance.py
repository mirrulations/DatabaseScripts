"""
The purpose of this script is to check if a docket exists to copy it from one S3 bucket to another. 

The script will attempt to utlize the sync command to copy the files.
AUTHOR: Yousuf Kanan
"""
import boto3
import sys

def check_s3_folder(bucket_name, folder_path):
    """ 
        * This function will check if a folder exists in a given S3 bucket.
        * The function will return True if the folder exists, False otherwise.
        @param bucket_name: The name of the S3 bucket.
        @param folder_path: The folder path.
        @return: True if the folder exists, False
    """
    s3 = boto3.client('s3')
    Parent_Dir = get_parent_folder(folder_path)
    folder_path2 = Parent_Dir + "/" + folder_path

    try:
        response = s3.list_objects_v2(Bucket=bucket_name, Prefix=folder_path2)
        if 'Contents' in response:
            return True
        else:
            return False
    except Exception as e:
        print(f"Error accessing bucket '{bucket_name}': {e}")

def get_parent_folder(folder_path):
    """
        * This function will return the parent folder of a given folder path.
        * The parent folder is the first part of the folder path that is separated by a non-alphanumeric character.
        @param folder_path: The folder path.
        @return: The parent folder of the given folder path.
    """
    # sometimes the folder path is like "ASC_FRDOC_0001/" and sometimes it is like "ASC-2012-0004/"
    if "-" in folder_path:
        return folder_path.split("-")[0]
    elif "_" in folder_path:
        return folder_path.split("_")[0]
    # find the first occurence of an abnoramal character 
    else:
        for i in range(len(folder_path)):
            if not folder_path[i].isalnum():
                return folder_path[:i]
 

