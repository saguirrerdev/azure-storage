# Upload Blob File to Azure

## This is a little project to upload a blob file in Azure

### How to run?

```bash
  python3 main.py
```

The script can read 3 args

> -c --container_name  | default **"testcontainer"**
> -f --file_url  | default **"./data.csv"**
> -n --file_name  | default **data.csv**

- Path to the file as **./data.csv**

## List of commands used to get required information

This assumes that it's already created an Azure Storage Account

> If you don't want to install the Azure CLI you can get all this information in the Azure Portal or Azure Cloud Shell

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
