# DocBot — Capillary Documentation Chatbot Instructions

## Step 1: Clone the Repository
```bash
git clone https://github.com/YourUsername/Capillary_assement.git
cd Capillary_assement
```

## Step 2: Create a Virtual Environment
**Windows:**
```bash
python -m venv myenv
myenv\Scripts\activate
```
**macOS/Linux:**
```bash
python3 -m venv myenv
source myenv/bin/activate
```

## Step 3: Install Dependencies
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

## Step 4: Set OpenAI API Key (Environment Variable)
**Windows:**
```bash
setx OPENAI_API_KEY "your_openai_api_key_here"
```
**macOS/Linux:**
```bash
export OPENAI_API_KEY="your_openai_api_key_here"
```
> Optionally, create a `.env` file and load it using `python-dotenv`:
```python
from dotenv import load_dotenv
import os
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
```

## Step 5: Scrape or Generate Documentation JSON File
- Run your scraping script (if available):
```bash
python scraper.py
```
- Ensure `docs_content.json` is generated with structure:
```json
[
  {
    "title": "Audit Logs API",
    "text": "Provides detailed records of user actions and events...",
    "url": "https://docs.capillarytech.com/reference/audit-logs"
  },
  {
    "title": "Transaction APIs",
    "text": "Retrieve customer transactions, including purchases and returns...",
    "url": "https://docs.capillarytech.com/reference/transaction_apis"
  }
]
```
- Place the JSON file in the root folder or update the code path:
```python
retriever = Retriever("docs_content.json")
```

## Step 6: Run the Streamlit App
```bash
streamlit run app.py
```
- Ask questions about the Capillary documentation.


