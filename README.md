# AI Data Retrieval Agent

AI Data Retrieval Agent is a web-based tool built with Streamlit, designed to perform web searches and extract relevant information using OpenAI's language model (LLM). The app allows users to input data, perform searches through SerpAPI, and retrieve valuable information related to various sectors and companies. The retrieved data can be downloaded for further analysis.

## Features

- **Data Input**: Upload a CSV file or provide a Google Sheets URL to retrieve data for web searches.
- **Web Search**: Perform web searches using the SerpAPI for entities in the selected dataset.
- **LLM-based Information Extraction**: Use OpenAI's LLM to extract relevant information from web search results.
- **Download Extracted Data**: Download the extracted information in CSV format for further use.

## Prerequisites

Before running the app, you will need to configure a few things:

### 1. **API Keys**:
   - **OpenAI API Key**: For interacting with OpenAI's LLM.
   - **SerpAPI Key**: For performing web searches.
   - **Google Service Account JSON**: For integrating Google Sheets (if using Google Sheets as a data source).

### 2. **Python Environment**:
   - Python 3.x
   - Dependencies listed in the `requirements.txt` file.

## Installation

### Step 1: Clone the repository

Clone this repository to your local machine using the following command:

`git clone https://github.com/your-username/AI_Data_Retrieval.git
cd AI_Data_Retrieval`

### Step 2: Install dependencies

Create a virtual environment (optional but recommended) and install the required packages.

`pip install -r requirements.txt`

### Step 3: Configure API Keys

Create a .env file in the root of the project directory and add the following:
   - `SERPAPI_KEY=your_serpapi_key`
   - `OPENAI_API_KEY=your_openai_api_key`


For Google Sheets integration, ensure you have the Google Service Account JSON file. Update the script with the path to this file.


### Step 4: Run the app

After installing the dependencies and setting up the keys, you can run the Streamlit app:

`streamlit run app.py`




