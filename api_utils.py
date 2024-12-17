import requests
import streamlit as st

def get_api_response(question, session_id, model):
    headers = {
        "accept": "application/json",
        "Content-Type": "application/json"
    }
    data = {
        "question": question,
        "model": model
    }
    if session_id:
        data["session_id"] = session_id

    try:
        response = requests.post("https://dcb-moses.onrender.com/chat", headers=headers, json=data)
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"API request failed with status code {response.status_code}: {response.text}")
            return None
    except Exception as e:
        st.error(f"An Error occurred: {str(e)}")
        return None



def upload_document(file):
    print("Uploading file...")
    try:
        files = {"file": (file.name, file, file.type)}
        response = requests.post("https://dcb-moses.onrender.com/upload-doc", files=files)
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"failed to upload file. Error: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        st.error(f"An Error occured while uploading the file: {str(e)}")
        return None


def list_documents():
    try:
        response = requests.get("https://dcb-moses.onrender.com/list-docs")
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Failed to fetch document list. Error: {response.status_code} - {response.text}")
            return []
    except Exception as e:
        st.error(f"An Error occured while listing files: {str(e)}")
        return None

def delete_document(file_id):
    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/json'
    }
    data = {"file_id": file_id}

    try:
        response = requests.post("https://dcb-moses.onrender.com/delete-doc", headers=headers, json=data)
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Failed to Delete file. Error: {response.status_code}: {response.text}")
            return None
    except Exception as e:
        st.error(f"An Error occurred: {str(e)}")
        return None

