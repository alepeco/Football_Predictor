# cd model
# python save.py -c '***AZURE_STORAGE_CONNECTION_STRING***'

import os, uuid
from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
import argparse

# https://learn.microsoft.com/en-us/azure/storage/blobs/storage-quickstart-blobs-python?tabs=managed-identity%2Croles-azure-portal%2Csign-in-azure-cli
# Erlaubnis auf eigenes Konto geben :-)

try:
    print("Azure Blob Storage Python quickstart sample")

    parser = argparse.ArgumentParser(description='Upload Model')
    parser.add_argument('-c', '--connection', required=True, help="azure storage connection string")
    args = parser.parse_args()

    blob_service_client = BlobServiceClient.from_connection_string(args.connection)

    account_url = "https://pecorale.blob.core.windows.net"


    exists = False
    containers = blob_service_client.list_containers()
    suffix = 0
    for container in containers:
        existingContainerName = container['name']
        print(existingContainerName)
        if existingContainerName.startswith("footballpredictormodel"):
            parts = existingContainerName.split("-")
            if len(parts) == 3:
                newSuffix = int(parts[-1])
                if newSuffix > suffix:
                    suffix = newSuffix
        suffix += 1
    container_name = f"footballpredictormodel{suffix}"
    print("new container name: ")
    print(container_name)

    if not exists:
        container_client = blob_service_client.create_container(container_name)

    local_file_name = "model.pkl"
    upload_file_path = os.path.join(".", local_file_name)

    blob_client = blob_service_client.get_blob_client(container=container_name, blob=local_file_name)
    print("\nUploading to Azure Storage as blob:\n\t" + local_file_name)

    with open(file=upload_file_path, mode="rb") as data:
        blob_client.upload_blob(data)


except Exception as ex:
    print('Exception:')
    print(ex)
    exit(1)
