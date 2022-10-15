# Upload Blob File to Azure

## _This is a little project to upload a blob file in Azure_

### How to run?

> [Note: before run set the env vars in the .env file](#list-of-commands-used-to-get-required-information)

```bash
  python3 main.py
```

The script can read 3 args

| Default | short | long | Description |
| --------|-------|------|-------------|
| testcontainer | -c | --container_name | The container in the Azure Storage Account |
| data.csv | -f | --file_url | Path to the file |
| data.csv | -n | --file_name | Name of the blob,file in the account |

## List of commands used to get required information

This assumes that it's already created an Azure Storage Account

> If you don't want to install the Azure CLI you can get the _account storage name_ and _account storage key_ in the Azure Portal or Azure Cloud Shell

get the resources grups list

```bash
  az group list --query "[].{ResourceGroups:name}" -o table
```

get storage accounts

```bash
  az storage account list -g <ResourceGroup> --query "[].{StorageAccounts:name}" -o table
```

get the storage account access key

```bash
  az storage account keys list -g <ResourceGroup> -n <StorageAccount> -o table
```
