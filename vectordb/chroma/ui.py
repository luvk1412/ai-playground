import pandas as pd
import streamlit as st


@st.cache_resource
def get_sentence_transformer():
    print('transformer loaded')
    # importing here as this import takes time and streamlit run full code again and again
    from sentence_transformers import SentenceTransformer
    model = SentenceTransformer('all-MiniLM-L6-v2')
    return model


@st.cache_resource
def get_vector_collections():
    from chromadb.config import Settings
    import chromadb
    print('got vector collections')
    client = chromadb.Client(
        Settings(chroma_db_impl="duckdb+parquet", persist_directory="db_persist"))
    collection = client.create_collection("luv_emails", get_or_create=True)
    return collection


@st.cache_resource
def get_email_dicts():
    import pickle
    print('got email dicts loaded')
    with open('email_dicts_74025.pkl', 'rb') as f:
        email_dicts = pickle.load(f)
    return email_dicts


@st.cache_resource
def vector_search(query):
    # Function that uses Sentence Transformers and vector db to return a list of emails (as dictionaries)
    # Return should be: [{date, subject, body, from, to}]
    query_embeddings = get_sentence_transformer().encode([query])
    result = get_vector_collections().query(
        query_embeddings=query_embeddings.tolist(),
        n_results=20
    )
    emails = []
    for mids in result['ids']:
        for mid in mids:
            emails.append(get_email_dicts()[mid])
    return emails
    # return [{'date': 'abc', 'from': 'luv', 'to': 'dishant', 'subject': 'subject', 'body': 'body is ur'}, {'date': 'abc', 'from': 'luv', 'to': 'dishant', 'subject': 'subject2', 'body': 'body is ur'}]


def get_email_mark_down_text(email_content):
    return f"""
| **Subject** | {email_content['subject']} |
| --- | --- |
| **Date** | {email_content['date']} |
| **From** | {email_content['from']} |
| **To** | {email_content['to']} |

{email_content['body']}
"""


def main():
    st.title("Email Search")
    # Custom CSS to remove button borders

    # Create a text input for the search query
    query = st.text_input("Search", "")

    # When the search button is pressed, perform the vector search
    # if st.button('Search'):

    # Perform the vector search when there's a query
    if query:
        # Perform the vector search
        results = vector_search(query)
        # Create two columns for the email list and the email content
        col1, col2 = st.columns(2)

        for idx, row in enumerate(results):
            if col1.button(row['subject'], key=idx, use_container_width=True):
                # When a button is clicked, display its corresponding email content in the second column
                markdown_email = get_email_mark_down_text(row)

                col2.markdown(markdown_email)


if __name__ == "__main__":
    main()
