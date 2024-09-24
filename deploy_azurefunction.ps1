# Variables
$resourceGroupName = "your_resource_group_name"
$location = "your_location"  # e.g., "EastUS"
$appServicePlanName = "your_app_service_plan_name"
$functionAppName = "your_function_app_name"
$storageAccountName = "your_storage_account_name"
$functionAppCodePath = "path\to\your\function\code"

# Create a Resource Group
az group create --name $resourceGroupName --location $location

# Create a Storage Account
az storage account create --name $storageAccountName --location $location --resource-group $resourceGroupName --sku Standard_LRS

# Create an App Service Plan
az appservice plan create --name $appServicePlanName --resource-group $resourceGroupName --location $location --sku B1 --is-linux

# Create a Function App
az functionapp create --name $functionAppName --storage-account $storageAccountName --resource-group $resourceGroupName --plan $appServicePlanName --runtime python --runtime-version 3.8 --functions-version 3

# Deploy code to the Function App
az functionapp deployment source config-zip --name $functionAppName --resource-group $resourceGroupName --src $functionAppCodePath