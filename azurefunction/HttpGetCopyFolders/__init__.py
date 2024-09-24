import logging

import azure.functions as func
from azure.storage.filedatalake import DataLakeServiceClient
from azure.identity import DefaultAzureCredential
import json

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    par_storage_account = req.params.get('storage_account')
    par_storage_container = req.params.get('storage_container')

    # Use DefaultAzureCredential to authenticate using Managed Identity
    credential = DefaultAzureCredential()

    # Create a DataLakeServiceClient
    service_client = DataLakeServiceClient(
        account_url=f"https://{par_storage_account}.dfs.core.windows.net",
        credential=credential
    )

    # Get a FileSystemClient to interact with the container
    file_system_client = service_client.get_file_system_client(file_system=par_storage_container)

    def get_folder_size(file_system_client, folder_name):
        total_size = 0
        paths = file_system_client.get_paths(path=folder_name, recursive=True)
        for path in paths:
            if not path.is_directory:
                total_size += path.content_length
        return total_size

    def is_parent_path_in_list(path, path_list):
        # Split the path into components
        components = path.split('/')
    
        # Generate all possible parent paths
        parent_paths = ['/'.join(components[:i]) for i in range(1, len(components))]
    
        # Check if any parent path is in the list
        for parent_path in parent_paths:
            if parent_path in path_list:
                return True
        return False

    # List all directories and calculate their sizes
    folders = file_system_client.get_paths()
    folder_recursive_copy = []

    for folder in folders:
        #print(str(folder.name))
        if folder.is_directory and not is_parent_path_in_list(folder.name, folder_recursive_copy):
            folder_size = get_folder_size(file_system_client, folder.name)
            if folder_size < 5000000000: # if folder size is less than 5GB, then data can be copied recurcively, otherwise nested folders in separate copies
                #print(str(folder.name))
                folder_recursive_copy.append(folder.name) 

    if not folder_recursive_copy:
        # no parallization possible, copy container as a whole
        folder_recursive_copy.append("*") 
    
    folder_recursive_copy_json = [{"name": name} for name in folder_recursive_copy]
    folder_recursive_copy_json_str = json.dumps(folder_recursive_copy_json)

    return func.HttpResponse(folder_recursive_copy_json_str, mimetype="application/json")