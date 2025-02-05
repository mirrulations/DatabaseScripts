import pytest
from unittest.mock import patch
import sys
import os

# Add the parent directory (DatabaseScripts) to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# add the src directory to sys.path


from CopyS3ToNewBucket import copy_s3_folder_boto3

@pytest.fixture
def mock_boto3_client():
    """Mock
    the boto3 S3 client."""
    with patch("boto3.client") as mock_client:
        yield mock_client
@pytest.mark.parametrize("folder_name", [
    "ACUS-2010-0001", "ACUS-2010-0002", "ACUS-2010-0003", "ACUS-2010-0004",
    "ACUS-2010-0005", "ACUS-2010-0006", "ACUS-2010-0007", "ASC_FRDOC_0001",
    "ASC-2012-0004", "ASC-2012-0005", "ASC-2012-0007", "ASC-2012-0008",
    "ASC-2012-0009", "ASC-2012-0010"
])
def test_copy_s3_folder_exists(mock_boto3_client, folder_name):
    """Test check_s3_folder when the folder exists in the mirrulations S3 bucket."""
    mock_s3 = mock_boto3_client.return_value
    mock_s3.list_objects_v2.return_value = {"Contents": [{"Key": folder_name}]}

    assert copy_s3_folder_boto3(folder_name) is True

@pytest.mark.parametrize("folder_name", [
    "NONEXISTENT-2023-0001", "RANDOM-2024-0002", "DOES-NOT-EXIST"
])
def test_copy_s3_folder_not_exists(mock_boto3_client, folder_name):
    """Test check_s3_folder when the folder does not exist in the mirrulations S3 bucket."""
    mock_s3 = mock_boto3_client.return_value
    mock_s3.list_objects_v2.return_value = {}

    with pytest.raises(Exception) as e:
        copy_s3_folder_boto3(folder_name)
    assert str(e.value) == f"Folder '{folder_name}' does not exist in bucket 'mirrulations'"

