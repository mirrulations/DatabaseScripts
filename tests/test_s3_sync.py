import pytest
from unittest.mock import patch
import sys
import os

# Add the parent directory (DatabaseScripts) to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# add the src directory to sys.path


from CheckS3Existance import check_s3_folder, get_parent_folder, main

@pytest.fixture
def mock_boto3_client():
    """Mock the boto3 S3 client."""
    with patch("boto3.client") as mock_client:
        yield mock_client

@pytest.mark.parametrize("folder_name", [
    "ACUS-2010-0001/", "ACUS-2010-0002/", "ACUS-2010-0003/", "ACUS-2010-0004/",
    "ACUS-2010-0005/", "ACUS-2010-0006/", "ACUS-2010-0007/", "ASC_FRDOC_0001/",
    "ASC-2012-0004/", "ASC-2012-0005/", "ASC-2012-0007/", "ASC-2012-0008/",
    "ASC-2012-0009/", "ASC-2012-0010/"
])
def test_check_s3_folder_exists(mock_boto3_client, capsys, folder_name):
    """Test check_s3_folder when the folder exists in the mirrulations S3 bucket."""
    mock_s3 = mock_boto3_client.return_value
    mock_s3.list_objects_v2.return_value = {"Contents": [{"Key": folder_name + "file.txt"}]}

    check_s3_folder("mirrulations", folder_name)

    captured = capsys.readouterr()
    assert f"Folder '{folder_name}' exists in bucket 'mirrulations'." in captured.out

@pytest.mark.parametrize("folder_name", [
    "NONEXISTENT-2023-0001/", "RANDOM-2024-0002/", "DOES-NOT-EXIST/"
])
def test_check_s3_folder_not_exists(mock_boto3_client, capsys, folder_name):
    """Test check_s3_folder when the folder does not exist in the mirrulations S3 bucket."""
    mock_s3 = mock_boto3_client.return_value
    mock_s3.list_objects_v2.return_value = {}

    check_s3_folder("mirrulations", folder_name)

    captured = capsys.readouterr()
    assert f"Folder '{folder_name}' does not exist in bucket 'mirrulations'." in captured.out

def test_check_s3_folder_error(mock_boto3_client, capsys):
    """Test check_s3_folder when an error occurs."""
    mock_s3 = mock_boto3_client.return_value
    mock_s3.list_objects_v2.side_effect = Exception("Access Denied")

    check_s3_folder("mirrulations", "ACUS-2010-0001/")

    captured = capsys.readouterr()
    assert "Error accessing bucket 'mirrulations': Access Denied" in captured.out

@pytest.mark.parametrize("folder_path, expected_parent", [
    ("ACUS-2010-0001/", "ACUS"),
    ("ASC_FRDOC_0001/", "ASC"),
    ("ASC-2012-0004/", "ASC"),
    ("ACUS-2010-0007/", "ACUS")
])
def test_get_parent_folder(folder_path, expected_parent):
    """Test get_parent_folder function."""
    assert get_parent_folder(folder_path) == expected_parent

@patch("CheckS3Existance.check_s3_folder")
@patch("CheckS3Existance.get_parent_folder", side_effect=lambda x: x.split("-")[0])
def test_main(mock_get_parent, mock_check_s3, capsys):
    """Test main function with multiple folder paths."""
    main("ACUS-2010-0001/", "ASC-2012-0009/")

    captured = capsys.readouterr()
    assert "ACUS-2010-0001/" in captured.out
    assert "ASC-2012-0009/" in captured.out
    mock_get_parent.assert_any_call("ACUS-2010-0001/")
    mock_get_parent.assert_any_call("ASC-2012-0009/")
    mock_check_s3.assert_any_call("mirrulations", "ACUS/ACUS-2010-0001/")
    mock_check_s3.assert_any_call("mirrulations", "ASC/ASC-2012-0009/")

def test_get_parent_folder_fail():
    """Test get_parent_folder with incorrect assertions to ensure failure."""
    with pytest.raises(AssertionError):
        assert get_parent_folder("ACUS-2010-0001/") == "RANDOM"
    
    with pytest.raises(AssertionError):
        assert get_parent_folder("ASC_FRDOC_0001/") == "FRDOC"
