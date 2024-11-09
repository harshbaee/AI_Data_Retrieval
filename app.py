import streamlit as st
import pandas as pd
from google.oauth2 import service_account
from googleapiclient.discovery import build
import openai
from dotenv import load_dotenv
import os
import requests
import time

#Load environment variables
load_dotenv()
SERPAPI_KEY = os.getenv("SERPAPI_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
openai.api_key = OPENAI_API_KEY

#Initialize session state
if 'search_results_dict' not in st.session_state:
    st.session_state.search_results_dict = {}
if 'extracted_data' not in st.session_state:
    st.session_state.extracted_data = {}

#Function to read data from Google Sheets
def read_google_sheet(sheet_id, sheet_range="Sheet1"):
    credentials = service_account.Credentials.from_service_account_file(
        r"D:\Codings\ai_project\aisheet-441015-22f53733ee54.json",  # Update to your path
        scopes=["https://www.googleapis.com/auth/spreadsheets.readonly"]
    )
    service = build("sheets", "v4", credentials=credentials)
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=sheet_id, range=sheet_range).execute()
    values = result.get("values", [])
    if not values:
        st.write("No data found.")
        return pd.DataFrame()
    data = pd.DataFrame(values[1:], columns=values[0])  # Set headers
    return data

#Function to perform web search using SerpAPI
def search_entity(entity, query_template, num_results):
    entity_str = str(entity) if not pd.isna(entity) else ""
    query = query_template.replace("{company}", entity_str)
    params = {"q": query, "api_key": SERPAPI_KEY, "engine": "google", "num": num_results}
    try:
        response = requests.get("https://serpapi.com/search", params=params)
        response.raise_for_status()
        results = response.json().get("organic_results", [])
    except requests.exceptions.RequestException as req_err:
        st.error(f"Network error for {entity}: {req_err}")
        return []
    except Exception as e:
        st.error(f"Error for {entity}: {e}")
        return []
    return [{"title": res.get("title", "No title"), "link": res.get("link", "No link"), "snippet": res.get("snippet", "No snippet")} for res in results]

#LLM parsing function
def parse_info_with_llm(entity, search_results, query_template):
    formatted_results = "\n".join([f"Title: {result['title']}\nLink: {result['link']}\nSnippet: {result['snippet']}\n" for result in search_results])
    prompt = f"You are an AI assistant. Based on the search results, extract info for '{query_template.replace('{company}', entity)}'.\n\nSearch results:\n{formatted_results}\nExtracted info:"
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )
        extracted_info = response['choices'][0]['message']['content'].strip()
    except openai.error.RateLimitError as e:
        st.error("OpenAI API quota exceeded. Please check your billing details or try again later.")
        return "Rate limit exceeded."
    except Exception as e:
        st.error(f"An error occurred: {e}")
        return "An error occurred during extraction."
    return extracted_info

st.title("AI Data Retrieval Agent")
st.divider()

#Data input options
st.header("Data Input")
uploaded_file = st.file_uploader("Upload a CSV file", type="csv", key="csv_upload")
google_sheet_url = st.text_input("Google Sheet URL", key="sheet_url_input")
data = pd.DataFrame()

#Handle data input
if uploaded_file is not None:
    try:
        data = pd.read_csv(uploaded_file)
        st.write("Uploaded CSV data preview:")
        st.dataframe(data)  # Displays all rows without limiting
    except Exception as e:
        st.error(f"Error reading CSV file: {e}")
elif google_sheet_url:
    try:
        sheet_id = google_sheet_url.split("/")[5]
        data = read_google_sheet(sheet_id)
        if not data.empty:
            st.write("Google Sheets data preview:")
            st.dataframe(data)  # Displays all rows without limiting
        else:
            st.error("No data found in the Google Sheet.")
    except Exception as e:
        st.error(f"Error connecting to Google Sheets: {e}")
        
#Query setup
if not data.empty:
    st.header("Set Information Retrieval Query")
    query_template = st.text_input("Custom prompt", "Get me the email address of {company}", key="query_template_input")
    primary_column = st.selectbox("Entity column:", data.columns, key="primary_column_select")

#User-defined limit for web search results
    num_results = st.slider("Number of search results per entity", min_value=1, max_value=10, value=3)

#Web Search with SERP API
    st.header("Perform Web Search")
    if st.button("Run Web Search"):
        if SERPAPI_KEY and primary_column and query_template:
            st.session_state.search_results_dict = {}
            unique_entities = data[primary_column].dropna().unique()
            total = len(unique_entities)
            progress_bar = st.progress(0)
            for idx, entity in enumerate(unique_entities):
                with st.spinner(f"Searching for '{entity}' ({idx + 1}/{total})..."):
                    search_results = search_entity(entity, query_template, num_results)
                    st.session_state.search_results_dict[entity] = search_results
                    time.sleep(1)  # To respect API rate limits
                progress_bar.progress((idx + 1) / total)
            st.success("Search complete!")
            sample_entities = list(st.session_state.search_results_dict.keys())[:5]
            for entity in sample_entities:
                with st.expander(f"Results for '{entity}'"):
                    results_df = pd.DataFrame(st.session_state.search_results_dict[entity])
                    st.table(results_df.head())
        else:
            st.error("Provide SerpAPI key, select a column, and enter a query template.")

#Information Extraction
    st.header("Extract Information with LLM")
    if st.button("Extract Info"):
        if OPENAI_API_KEY and st.session_state.search_results_dict:
            st.session_state.extracted_data = {}
            for idx, (entity, results) in enumerate(st.session_state.search_results_dict.items()):
                st.write(f"Extracting for {entity}...")
                extracted_info = parse_info_with_llm(entity, results, query_template)
                st.session_state.extracted_data[entity] = extracted_info
            st.success("Extraction complete!")
            st.write("Preview of Extracted Data:")
            st.write(pd.DataFrame.from_dict(st.session_state.extracted_data, orient='index', columns=['Extracted Information']))
        else:
            st.error("Provide OpenAI API key and perform a web search first.")

#Download Extracted Data
    if st.session_state.extracted_data:
        st.header("Download Extracted Data")
        extracted_df = pd.DataFrame.from_dict(st.session_state.extracted_data, orient='index', columns=['Extracted Information'])
        st.download_button("Download CSV", extracted_df.to_csv().encode('utf-8'), "extracted_data.csv", "text/csv")
