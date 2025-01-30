"""
The purpose of this script is to copy certain dockets from one S3 bucket to another.

The script will attempt to utlize the sync command to copy the files.

AUTHOR: Yousuf Kanan
"""
from CheckS3Existance import check_s3_folder, get_parent_folder
import boto3

def copy_s3_folder_boto3(folder):
    """
        * This function will copy a folder from one S3 bucket to another.
        * The function will first check if the folder exists in the source bucket.
        * If the folder exists, the function will copy the folder to the destination bucket.
        * The function will then check if the folder exists in the destination bucket in 
          order to confirm that the folder was copied successfully.
        @param folder: The folder to copy.
        @return: True if the folder was copied successfully, False otherwise.
    """
    # check if the folder exists
    bucket_name = 'mirrulations'
    if not check_s3_folder(bucket_name, folder):
        raise Exception(f"Folder '{folder}' does not exist in bucket '{bucket_name}'")
 
    parent = get_parent_folder(folder)
    folder2 = parent + "/" + folder

    # copy the folder to the new bucket
    destination_bucket = 'docket-samples'
    s3 = boto3.client('s3')
    response = s3.list_objects_v2(Bucket=bucket_name, Prefix=folder2)
    for obj in response.get('Contents', []):
        key = obj['Key']
        copy_source = {'Bucket': bucket_name, 'Key': key}
        s3.copy_object(CopySource=copy_source, Bucket=destination_bucket, Key=key)

    return check_s3_folder(destination_bucket, folder)
  