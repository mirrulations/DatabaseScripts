"""
The purpose of this script is to copy certain dockets from one S3 bucket to another. 

The script will attempt to utlize the sync command to copy the files.
AUTHOR: Yousuf Kanan
"""
import boto3
import sys

def check_s3_folder(bucket_name, folder_path):
    s3 = boto3.client('s3')
    try:
        response = s3.list_objects_v2(Bucket=bucket_name, Prefix=folder_path)
        if 'Contents' in response:
            print(f"Folder '{folder_path}' exists in bucket '{bucket_name}'.")
        else:
            print(f"Folder '{folder_path}' does not exist in bucket '{bucket_name}'.")
    except Exception as e:
        print(f"Error accessing bucket '{bucket_name}': {e}")

def get_parent_folder(folder_path):
    print(folder_path)
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
 

def main(*folder_paths):
    bucket_name = "mirrulations"
    
    for folder_path in folder_paths:
        Parent_Dir = get_parent_folder(folder_path)
        # make it parentdir /childdir
        folder_path2 = Parent_Dir + "/" + folder_path
        print(folder_paths)
        check_s3_folder(bucket_name, folder_path2)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python script.py <folder_path1> <folder_path2> ...")
    else:
        main(*sys.argv[1:])