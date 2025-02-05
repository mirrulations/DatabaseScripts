# DatabaseScripts

The [`CheckS3Existance.py`](CheckS3Existance.py) and the[`CopyS3ToNewBucket.py`](CopyS3ToNewBucket.py) scripts are used to check if a file exists in an S3 bucket.

This is useful for copying files from one bucket to another, or for checking if a file exists before downloading it. You can also use these scripts to move dockets to smaller bucket when ingesting data into OpenSearch.

## Usage

To copy a file from one bucket to another, call the ```copy_s3_folder_boto3(folder)``` function in the `CopyS3ToNewBucket.py` script. This function takes the name of the folder you want to copy as an argument. Please note that script will only copy files from the mirrulations bucket to the new bucket.

Example:

```python
copy_s3_folder_boto3('ACUS-2010-0001')
```

To check if a file exists in an S3 bucket, call the `check_s3_file_exists(bucket, key)` function in the `CheckS3Existance.py` script. This function takes the name of the bucket and the key of the file you want to check as arguments.

Example:

```python
check_s3_file_exists('mirrulations', 'ACUS-2010-0001/')
```

## Our technology stack
    * Python 3.13
    * Boto3
    * AWS S3
