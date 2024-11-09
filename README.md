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

```bash
git clone https://github.com/your-username/AI_Data_Retrieval.git
cd AI_Data_Retrieval
