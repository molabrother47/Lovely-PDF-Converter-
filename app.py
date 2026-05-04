import streamlit as st
import pandas as pd
from PIL import Image
from fpdf import FPDF
import pdfplumber
from PyPDF2 import PdfMerger, PdfReader, PdfWriter
from docx import Document
import fitz  # PyMuPDF
import io
import os

# --- SEO aur Mobile Settings ---
st.set_page_config(
    page_title="Rana PDF Converter Pro | Best Free PDF Tools Online",
    page_icon="📄",
    layout="centered", # Mobile ke liye centered layout behtar hai
    initial_sidebar_state="collapsed"
)

# --- Custom CSS for Styling ---
st.markdown("""
    <style>
    .main { text-align: center; }
    .stButton>button { width: 100%; border-radius: 10px; height: 3em; background-color: #3498db; color: white; }
    h1 { color: #3498db; font-family: 'Roboto', sans-serif; }
    </style>
    """, unsafe_allow_html=True)

# --- Header & SEO Keywords ---
st.title("📄 Rana PDF Converter Pro")
st.markdown("""
**Sabse Tez aur Free PDF Tools!** 
Convert PDF to Excel, Word, Merge PDFs, and Protect Files. 
*Mobile-friendly, No installation required.*
""")

# --- Sidebar / Navigation ---
option = st.sidebar.selectbox(
    'Tool Select Karein:',
    ["Image to PDF", "Text to PDF", "PDF to Excel/Word", "PDF Merger", "PDF to Image", "Protect PDF"]
)

# ---------------- 1. IMAGE TO PDF ----------------
if option == "Image to PDF":
    st.header("📸 Image to PDF")
    uploaded_images = st.file_uploader("Photos select karein", type=['jpg', 'jpeg', 'png'], accept_multiple_files=True)
    
    if uploaded_images and st.button("Convert to PDF"):
        img_list = []
        for img in uploaded_images:
            image = Image.open(img).convert('RGB')
            img_list.append(image)
        
        pdf_output = io.BytesIO()
        img_list[0].save(pdf_output, format="PDF", save_all=True, append_images=img_list[1:])
        st.download_button("📥 Download PDF", data=pdf_output.getvalue(), file_name="Rana_Images.pdf")

# ---------------- 2. PDF TO EXCEL/WORD ----------------
elif option == "PDF to Excel/Word":
    st.header("🔄 PDF to Data")
    uploaded_pdf = st.file_uploader("PDF File upload karein", type=['pdf'])
    format_type = st.radio("Format select karein:", ["Excel", "Word"])
    
    if uploaded_pdf and st.button("Convert"):
        with st.spinner('Processing...'):
            if format_type == "Excel":
                with pdfplumber.open(uploaded_pdf) as pdf:
                    all_tables = []
                    for page in pdf.pages:
                        table = page.extract_table()
                        if table:
                            all_tables.append(pd.DataFrame(table))
                    if all_tables:
                        df = pd.concat(all_tables)
                        output = io.BytesIO()
                        df.to_excel(output, index=False)
                        st.download_button("📥 Download Excel", output.getvalue(), "converted.xlsx")
            
            elif format_type == "Word":
                doc = Document()
                with pdfplumber.open(uploaded_pdf) as pdf:
                    for page in pdf.pages:
                        text = page.extract_text()
                        if text: doc.add_paragraph(text)
                output = io.BytesIO()
                doc.save(output)
                st.download_button("📥 Download Word Doc", output.getvalue(), "converted.docx")

# ---------------- 3. PDF MERGER ----------------
elif option == "PDF Merger":
    st.header("🔗 PDF Merger")
    merge_files = st.file_uploader("2 ya usse zyada PDFs select karein", type=['pdf'], accept_multiple_files=True)
    
    if merge_files and len(merge_files) >= 2:
        if st.button("Merge PDFs"):
            merger = PdfMerger()
            for pdf in merge_files:
                merger.append(pdf)
            output = io.BytesIO()
            merger.write(output)
            st.download_button("📥 Download Merged PDF", output.getvalue(), "merged_rana.pdf")

# ---------------- BAAQI TOOLS ----------------
# Isi tarah aap Protect PDF aur Text to PDF bhi add kar sakte hain logic wahi rahegi bas io.BytesIO() use karna hoga.

st.sidebar.markdown("---")
st.sidebar.write("Developed by: **Rana Abubakar**")