# AI_Data_Retrieval
# AI Data Retrieval Agent

This application is a web-based tool built with Streamlit that performs web searches, extracts relevant information using an LLM (Large Language Model), and allows you to download the extracted data. The app is designed to read data from CSV files or Google Sheets, perform searches using the SerpAPI, and then extract useful information using OpenAI's API.

## Features

- **Data Input**: Upload a CSV file or provide a Google Sheet URL to retrieve data.
- **Web Search**: Perform web searches using the SerpAPI for entities in the selected dataset.
- **LLM-based Information Extraction**: Extract useful information from web search results using OpenAI’s LLM.
- **Download Extracted Data**: Download the extracted information as a CSV file.

## Prerequisites

Before running the app, you need to install the necessary dependencies and configure some keys:

1. **API Keys**: 
   - OpenAI API Key
   - SerpAPI Key
   - Google Service Account JSON for Google Sheets integration

2. **Python Environment**:
   - Python 3.x
   - Install dependencies using `pip install -r requirements.txt`

## Installation

### 1. Clone the repository

`bash
git clone https://github.com/your-username/AI_Data_Retrieval.git
cd AI_Data_Retrieval`

### 2.Install dependencies
Create a virtual environment (optional but recommended) and install the required packages.

bash
pip install -r requirements.txt
### 3. Configure API Keys
Create a .env file in the root of the project directory and add the following:
plaintext
SERPAPI_KEY=your_serpapi_key
OPENAI_API_KEY=your_openai_api_key
For Google Sheets integration, ensure you have the Google Service Account JSON file. Update the script with the path to this file.
### 4. Run the app
After installing the dependencies and setting up the keys, you can run the Streamlit app:
bash
streamlit run app.py
Usage
Upload a CSV File or Provide Google Sheet URL:

Upload a CSV containing the entity data you want to search.
Alternatively, provide a Google Sheet URL containing the data.
Enter the Search Query:

Define the custom search query template, such as "List companies in the {sector} sector with the highest P/E ratio".
Select the column containing the entities (e.g., sector names, company names).
Run Web Search:

Click the "Run Web Search" button to perform web searches for each entity in the selected dataset.
Extract Information:

Use OpenAI’s API to extract relevant information from the search results.

