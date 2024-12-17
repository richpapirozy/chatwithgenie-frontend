import streamlit as st
from api_utils import upload_document, list_documents, delete_document

def display_sidebar():
    # model Selection
    model_options = ['gpt-4o','gpt-4o-mini','gpt-3.5-turbo']
    st.sidebar.selectbox("Select Model", options=model_options, key="model")
    # st.sidebar.selectbox("Select Model", options=model_options, key="model", index=None)

    # upload document
    st.sidebar.header("Upload Document")
    uploaded_file = st.sidebar.file_uploader("choose a file", type=['pdf','docx', 'html'])
    if uploaded_file is not None:
        if st.sidebar.button("Upload"):
            with st.spinner("Uploading..."):
                upload_response = upload_document(uploaded_file)
                if upload_response:
                    st.sidebar.success(f"file '{uploaded_file.name}' uploaded successfully with ID {upload_response['file_id']}.")
                    st.session_state.documents = list_documents() # to refresh the list post upload
    
    # List Documents
    st.sidebar.header("Uploaded Documents")
    if st.sidebar.button("Refresh Document List"):
        with st.spinner("Refreshing..."):
            st.session_state.documents = list_documents()

    # initialize Documents list if not present
    if "documents" not in st.session_state:
        st.session_state.documents = list_documents()

    documents = st.session_state.documents
    if documents:
        for doc in documents:
            st.sidebar.text(f"{doc['filename']} (ID: {doc['id']}, upload: {doc['upload_timestamp']})")

        # Delete Document
        selected_file_id = st.sidebar.selectbox("select a document to delete", options=[doc['id'] for doc in documents], 
        format_func=lambda x: next(doc['filename'] for doc in documents if doc['id'] == x))
        if st.sidebar.button('Delete Selected Document'):
            with st.spinner("Deleting..."):
                delete_response = delete_document(selected_file_id)
                if delete_response:
                    st.sidebar.success(f"Document with ID {selected_file_id} deleted successfully.")
                    st.session_state.documents = list_documents()
                else:
                    st.sidebar.error(f"Failed to delete document with ID {selected_file_id}.")
                    




