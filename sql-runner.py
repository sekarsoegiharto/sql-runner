import pyodbc
import pandas as pd
import streamlit as st
import io

st.set_page_config(page_title="SQL Runner", layout="wide")

# =========================
# Connection
# =========================
def get_connection():
        conn_str = (
            "DRIVER={ODBC Driver 17 for SQL Server};"
            "SERVER=MSI;"
            "DATABASE=klaimintern;"
            "UID=sekar1505;"
            "PWD=123456;"
            "Trusted_Connection=yes;"
        )
    return pyodbc.connect(conn_str)

# Untuk query SELECT / EXEC yang return tabel
def run_sql(sql: str) -> pd.DataFrame:
    cnxn = get_connection()
    try:
        df = pd.read_sql(sql, cnxn)
        return df
    finally:
        cnxn.close()

# Untuk query non-SELECT (CREATE PROC, DROP, INSERT, UPDATE, DELETE, dll)
def execute_sql(sql: str):
    cnxn = get_connection()
    try:
        cursor = cnxn.cursor()
        cursor.execute(sql)
        cnxn.commit()
    finally:
        cnxn.close()

# =========================
# Download buttons
# =========================
def download_csv_button(df: pd.DataFrame, filename="query_result.csv"):
    st.download_button(
        label="📥 Download Hasil (CSV)",
        data=df.to_csv(index=False).encode('utf-8'),
        file_name=filename,
        mime="text/csv",
        use_container_width=True
    )

def download_excel_button(df: pd.DataFrame, filename="query_result.xlsx"):
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
        df.to_excel(writer, index=False, sheet_name="Data")
        ws = writer.sheets["Data"]
        for i, c in enumerate(df.columns):
            width = max(10, min(40, df[c].astype(str).map(len).max() if not df.empty else 10))
            ws.set_column(i, i, width)
    output.seek(0)
    st.download_button(
        "⬇️ Download Excel",
        data=output,
        file_name=filename,
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        use_container_width=True
    )

# =========================
# UI
# =========================
st.title("🧰 SQL Runner (SQL Server)")
st.caption("Upload file `.sql`, edit query sebelum & sesudah run → lihat hasil → download Excel/CSV.")

# STEP 1: Upload File
uploaded_file = st.file_uploader("Upload file SQL", type=["sql"])

if uploaded_file:
    uploaded_sql = uploaded_file.read().decode("utf-8")
    st.subheader("✏️ Edit Sebelum Run (from file)")
    pre_edit_sql = st.text_area("Query dari file", value=uploaded_sql, height=200, key="pre_sql")
else:
    pre_edit_sql = ""

# STEP 2: Editor untuk query yang akan dieksekusi (editable terus)
st.subheader("⚙️ Query Aktif (bisa diedit sebelum/ sesudah run)")
sql = st.text_area("Query untuk dijalankan", value=pre_edit_sql, height=200, key="exec_sql")

# STEP 3: Tombol Run
col1, col2 = st.columns([1,2])
with col1:
    run_btn = st.button("▶️ Run Query", use_container_width=True)

# STEP 4: Jalankan
if run_btn:
    if not sql.strip():
        st.warning("SQL kosong.")
    else:
        try:
            with st.spinner("Menjalankan query..."):
                # deteksi apakah query SELECT/EXEC atau DDL/DML
                if sql.strip().lower().startswith(("select", "exec")):
                    df = run_sql(sql)
                    st.success(f"Sukses: {len(df)} baris.")
                    st.dataframe(df, use_container_width=True, height=500)
                    if not df.empty:
                        download_excel_button(df, "query_result.xlsx")
                        download_csv_button(df, "query_result.csv")
                else:
                    execute_sql(sql)
                    st.success("✅ Query berhasil dieksekusi (tidak ada hasil tabel).")
        except pyodbc.Error as ex:
            st.error(f"❌ Koneksi/Query gagal: {ex}")
        except Exception as e:
            st.error(f"❌ Error: {e}")
