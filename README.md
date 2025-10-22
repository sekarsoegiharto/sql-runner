1. Clone this repository
git clone https://github.com/sekarsoegiharto/sql-runner.git
cd sql-runner

2. Create and activate a virtual environment
python -m venv venv
source venv/bin/activate      # On macOS/Linux
venv\Scripts\activate  

3. Install dependencies
pip install -r requirements.txt

4. Update database credentials
In the script section:

def get_connection():
    conn_str = (
        "DRIVER={ODBC Driver 17 for SQL Server};"
        "SERVER=MSI;"
        "DATABASE=#database_name;"
        "UID=#username;"
        "PWD=#password;"
        "Trusted_Connection=yes;"
    )
    return pyodbc.connect(conn_str)

5. Run the app
streamlit run app.py

💡 How to Use
1. Upload a .sql file (optional) — the contents will appear in the editor.
2. Edit or write your SQL query in the text area.
3. Click "▶️ Run Query" to execute it.
4. View the results directly in Streamlit.
5. Download your query output as Excel or CSV if desired.

🧰 Example Use Cases
- Quickly testing SQL scripts and stored procedures.
- Running ad-hoc analytics queries without opening SQL Server Management Studio.
- Sharing an interactive query tool with non-technical users or analysts.