# Variables
$resourceGroupName = "your_resource_group_name"
$templateFile = "path\to\ARMTemplateForFactory.json"
$deploymentName = "your_deployment_name"

# Optional: Parameters for the ARM template
$parameters = @{
    factoryName = "test-adf-copy-scale-adf"
    AzureFunction1_functionKey = "your_function_key"
    AzureFunction1_properties_typeProperties_functionAppUrl = "https://test-adf-copy-scale-fun.azurewebsites.net"
    adlsgen2sink_properties_typeProperties_url = "https://testgdpinformationf.dfs.core.windows.net/"
    adlsgen2source_properties_typeProperties_serviceEndpoint = "https://testgdpstor2.blob.core.windows.net/"
    sourcestor_properties_typeProperties_url = "https://your_source_storage_url"
}

# Convert parameters to JSON format
$parametersJson = $parameters | ConvertTo-Json -Compress

# Deploy the ARM template
az deployment group create `
  --name $deploymentName `
  --resource-group $resourceGroupName `
  --template-file $templateFile `
  --parameters $parametersJson