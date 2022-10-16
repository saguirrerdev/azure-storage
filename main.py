import getopt
import sys
import os
from typing import List
from dotenv import load_dotenv

from azure.storage.blob import ContainerClient, BlobClient


def upload_blob(blob_client: BlobClient, file_url: str = "data.csv") -> None:
    """upload_blob(blob_client: BlobClient, file_url: str = "data.csv") -> None

    Upload the :file_url to the :blob_client

    :blob_client: BlobClient -> BlobClient to manage the file to be uploaded

    :file_url: str -> Path to the file to be uploaded

    Raise a FileNotFoundError if the current :file_url it's no valid
    """

    try:
        print("Uploading file")
        with open(file_url, "rb") as data:
            blob_client.upload_blob(data)
    except FileNotFoundError:
        raise "File not found"


def create_blob_client(connection_string: str, container_name: str, file_name: str) -> BlobClient:
    """create_blob_client(connection_string: str, container_name: str, file_name: str) -> BlobClient

    Creates a new BlobClient

    :connection_string: str -> Azure Storage connection string

    :container_name: str -> Container name where the blop is uploaded

    :file_name: srt -> Name of the blob in the container

    Returns BlobClient    
    """

    print(f'Creating blob client')
    return BlobClient.from_connection_string(conn_str=connection_string, container_name=container_name, blob_name=file_name)


def create_container_client(connection_string: str, container_name: str = "testcontainer") -> None:
    """create_container_client(connection_string: str, container_name: str = "testcontainer") -> None

    :connection_string: str Azure Storage connection string

    :container_name: str Container name to be created in the azure storage account

    Creates or verify if the container with :container_name exists
    """

    print(f'Creating container {container_name}')

    container_client = ContainerClient.from_connection_string(
        conn_str=connection_string,
        container_name=container_name
    )

    if not container_client.exists():
        container_client.create_container()
        return

    print(f'The container {container_name} already exists')


def create_connection_string() -> str:
    """create_connection_string() -> str

    Reads the env vars
        - AZURE_STORAGE_ACCOUNT_NAME
        - AZURE_STORAGE_ACCOUNT_KEY

    Returns azure storage connection string
    """

    print("Creating connection string")
    try:
        storage_account_name = os.environ["AZURE_STORAGE_ACCOUNT_NAME"]
        if not storage_account_name:
            raise "Storage account no valid"

        storage_account_key = os.environ["AZURE_STORAGE_ACCOUNT_KEY"]
        if not storage_account_key:
            raise "Storage account key no valid"
    except KeyError as err:
        raise err

    return f'DefaultEndpointsProtocol=https;AccountName={storage_account_name};AccountKey={storage_account_key};EndpointSuffix=core.windows.net'


def read_args() -> List:
    """read_args() -> List

    Parses command line options and parameters list

    Expect to read the next params:
        - -c --container_name
        - -f --file_url
        - -n --container_name

    Returns a list with [container_name, file_url, file_name]
    """

    try:
        opts, args = getopt.getopt(sys.argv[1:], "c:f:n", [
                                   "container_name=", "file_url=", "file_name="])
    except getopt.GetoptError as err:
        print(err)
        opts = []

    file_url = "data.csv"
    container_name = "testcontainer"
    file_name = "data.csv"

    for opt, arg in opts:
        if opt in ['-c', '--container_name']:
            container_name = arg
        elif opt in ['-f', '--file_url']:
            file_url = arg
        elif opt in ['-n', '--file_name']:
            file_url = arg

    return [container_name, file_url, file_name]


def run():
    container_name, file_url, file_name = read_args()

    connection_string = create_connection_string()

    create_container_client(
        connection_string=connection_string, container_name=container_name)

    blob = create_blob_client(connection_string=connection_string,
                              container_name=container_name, file_name=file_name)

    upload_blob(blob, file_url)


if __name__ == "__main__":
    load_dotenv()
    run()
