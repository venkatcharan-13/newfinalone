from django.shortcuts import render
import os
from urllib import response 
from django.core.files.storage import FileSystemStorage
import requests
from utility import upload_util
from django.conf.global_settings import MEDIA_URL

# Create your views here.
def upload(request):
    APP_ID = '3228a1c7-6d67-4285-be4a-65762e867252'

    SCOPES = ['Files.ReadWrite']

    access_token = upload_util.generate_access_token(APP_ID,SCOPES)
    headers = {
        'Authorization': 'Bearer {}'.format(access_token['access_token'])
    }
    parent_folder_id = 'Samarth' # we have to get the proper parent id from the database
    folder_name_search_endpoint = f"me/drive/root/search(q='{parent_folder_id}')"
    folder_id_response = requests.get(upload_util.GRAPH_API_ENDPOINT + folder_name_search_endpoint, headers=headers)
    values_of_folder_id_response = folder_id_response.json()['value']
    parent_folder_id_to_upload_docs = values_of_folder_id_response[0]['id']

    if request.method == 'POST':
        fs = FileSystemStorage()
        for file in request.FILES.getlist('uploaded_files'):
            document = fs.save(file.name, file)
            file_path = str(fs.base_location) + f"\{file.name}"
            with open(file_path, 'rb') as upload:
                media_content= upload.read()
                response=requests.put(upload_util.GRAPH_API_ENDPOINT + f'/me/drive/items/{parent_folder_id_to_upload_docs}:/{file.name}:/content',
                    headers=headers,
                    data=media_content
                )
                if response.status_code==200:
                    print('Success')
                else:
                    print('Hutt')
                    print(response.json())
           
    return render(request, 'upload.html')