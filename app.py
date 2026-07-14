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

# --- Traffic Counter Configuration ---
COUNTER_FILE = "visitor_count.txt"

def get_visitor_count():
    """Tracks and increments the live visitor count using a local file."""
    if not os.path.exists(COUNTER_FILE):
        with open(COUNTER_FILE, "w") as f:
            f.write("1")
        return 1
    else:
        try:
            with open(COUNTER_FILE, "r+") as f:
                count = int(f.read().strip())
                new_count = count + 1
                f.seek(0)
                f.write(str(new_count))
                f.truncate()
                return new_count
        except:
            return 1

# Fetch traffic analytics safely
current_traffic = get_visitor_count()

# --- Page Configuration & SEO Settings ---
st.set_page_config(
    page_title="Rana PDF Converter Pro | Free Online PDF Tools",
    page_icon="📄",
    layout="centered", 
    initial_sidebar_state="expanded"
)

# --- Custom Professional UI Styling ---
st.markdown("""
    <style>
    .main { text-align: center; }
    .stButton>button { 
        width: 100%; 
        border-radius: 8px; 
        height: 3em; 
        background-color: #1a73e8; 
        color: white; 
        font-weight: bold;
        border: none;
        transition: background-color 0.3s ease;
    }
    .stButton>button:hover {
        background-color: #1557b0;
    }
    h1 { color: #1a73e8; font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; }
    h2 { color: #202124; font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; }
    div[data-testid="stMetricValue"] { font-size: 26px; color: #188038; text-align: center; font-weight: bold; }
    div[data-testid="stMetricLabel"] { font-size: 14px; text-align: center; }
    .hero-container {
        padding: 20px;
        border-radius: 10px;
        background-color: #f8f9fa;
        border: 1px solid #dadce0;
        margin-bottom: 25px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- Sidebar / Navigation ---
st.sidebar.title("🛠️ Navigation Menu")
st.sidebar.markdown("Choose a tool below to get started:")
option = st.sidebar.selectbox(
    'Select a PDF Tool:',
    [
        "Home / About",
        "Image to PDF", 
        "Text to PDF", 
        "PDF to Excel/Word", 
        "PDF Merger", 
        "PDF to Image", 
        "Protect PDF"
    ]
)

st.sidebar.markdown("---")
st.sidebar.write("Developed by: **Rana Abubakar**")

# ==================== HOME / ABOUT PAGE ====================
if option == "Home / About":
    st.markdown("""
    <div class="hero-container">
        <h1 style="text-align: center; margin-bottom: 10px;">📄 Rana PDF Converter Pro</h1>
        <p style="text-align: center; font-size: 1.1em; color: #5f6368;">
            Your fast, reliable, and entirely secure cloud-based document processor.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    ### Welcome to Rana PDF Converter Pro
    This platform offers a comprehensive suite of digital document utilities designed to optimize your workflow. No installations, no subscription fees, and no data tracking.
    
    #### **Key Features:**
    * **📸 High-Quality Image to PDF:** Convert your JPG, JPEG, and PNG images into high-resolution PDF documents.
    * **✍️ Dynamic Text Compiler:** Seamlessly convert plain text files or copy-pasted contents into formatted PDFs.
    * **🔄 Advanced Data Extraction:** Export tables directly to **Excel** spreadsheets or extract text layouts to **Word** documents.
    * **🔗 Instant PDF Merger:** Combine multiple PDF files into a single, cohesive document in seconds.
    * **🖼️ PDF to Image Renderer:** Convert specific PDF pages back into web-ready PNG images.
    * **🔒 Enterprise-Grade Encryption:** Secure your intellectual property and confidential files using robust user password protection.
    
    *Please select a utility from the sidebar menu on the left to begin.*
    """)

# ==================== 1. IMAGE TO PDF ====================
elif option == "Image to PDF":
    st.header("📸 Image to PDF Converter")
    st.write("Convert your PNG, JPG, or JPEG images into a single professional PDF document.")
    
    uploaded_images = st.file_uploader("Upload your images", type=['jpg', 'jpeg', 'png'], accept_multiple_files=True)
    
    if uploaded_images:
        if st.button("Convert to PDF"):
            with st.spinner("Compiling images into PDF..."):
                img_list = []
                for img in uploaded_images:
                    try:
                        image = Image.open(img).convert('RGB')
                        img_list.append(image)
                    except Exception as e:
                        st.error(f"Error processing image {img.name}: {e}")
                
                if img_list:
                    pdf_output = io.BytesIO()
                    img_list[0].save(pdf_output, format="PDF", save_all=True, append_images=img_list[1:])
                    st.success("Conversion successful!")
                    st.download_button(
                        label="📥 Download PDF Document", 
                        data=pdf_output.getvalue(), 
                        file_name="Rana_Images.pdf",
                        mime="application/pdf"
                    )
    else:
        st.info("Please upload one or more image files to activate the converter.")

# ==================== 2. TEXT TO PDF ====================
elif option == "Text to PDF":
    st.header("✍️ Text to PDF Converter")
    st.write("Type, paste, or upload plain text to generate a clean, readable PDF file.")
    
    text_input = st.text_area("Type or paste your text content below:", height=200)
    uploaded_txt = st.file_uploader("Or upload a .txt file", type=['txt'])
    
    if st.button("Convert to PDF"):
        final_text = ""
        if uploaded_txt:
            final_text = uploaded_txt.read().decode("utf-8", errors="ignore")
        elif text_input:
            final_text = text_input
            
        if final_text.strip():
            with st.spinner("Generating PDF layout..."):
                try:
                    pdf = FPDF()
                    pdf.add_page()
                    pdf.set_font("Arial", size=12)
                    
                    for line in final_text.split('\n'):
                        # Ensure compatibility with ISO-8859-1 encoding to prevent crashes
                        clean_line = line.encode('latin-1', 'replace').decode('latin-1')
                        pdf.cell(200, 10, txt=clean_line, ln=1)
                        
                    pdf_output = pdf.output(dest='S').encode('latin-1')
                    st.success("Conversion successful!")
                    st.download_button(
                        label="📥 Download PDF Document", 
                        data=pdf_output, 
                        file_name="Rana_Text.pdf", 
                        mime="application/pdf"
                    )
                except Exception as e:
                    st.error(f"An error occurred while compiling PDF: {e}")
        else:
            st.warning("Input required. Please enter text or upload a .txt file first.")

# ==================== 3. PDF TO EXCEL/WORD ====================
elif option == "PDF to Excel/Word":
    st.header("🔄 PDF to Data Extractor")
    st.write("Extract tabular data directly to Excel worksheets, or structured text layouts to editable Word documents.")
    
    uploaded_pdf = st.file_uploader("Upload your PDF document", type=['pdf'])
    format_type = st.radio("Choose output target format:", ["Excel", "Word"])
    
    if uploaded_pdf:
        if st.button("Extract Data"):
            with st.spinner('Extracting document structures...'):
                if format_type == "Excel":
                    try:
                        with pdfplumber.open(uploaded_pdf) as pdf:
                            all_tables = []
                            for page in pdf.pages:
                                table = page.extract_table()
                                if table:
                                    all_tables.append(pd.DataFrame(table))
                            if all_tables:
                                df = pd.concat(all_tables)
                                output = io.BytesIO()
                                df.to_excel(output, index=False, engine='openpyxl')
                                st.success("Tabular extraction completed!")
                                st.download_button(
                                    label="📥 Download Excel Spreadsheet", 
                                    data=output.getvalue(), 
                                    file_name="extracted_data.xlsx",
                                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                                )
                            else:
                                st.warning("No structured data tables were identified on any page of this PDF.")
                    except Exception as e:
                        st.error(f"Excel conversion failure: {e}")
                
                elif format_type == "Word":
                    try:
                        doc = Document()
                        with pdfplumber.open(uploaded_pdf) as pdf:
                            for page in pdf.pages:
                                text = page.extract_text()
                                if text: 
                                    doc.add_paragraph(text)
                        output = io.BytesIO()
                        doc.save(output)
                        st.success("Text extraction completed!")
                        st.download_button(
                            label="📥 Download Word Document", 
                            data=output.getvalue(), 
                            file_name="extracted_document.docx",
                            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                        )
                    except Exception as e:
                        st.error(f"Word conversion failure: {e}")
    else:
        st.info("Please upload a PDF document to activate extraction.")

# ==================== 4. PDF MERGER ====================
elif option == "PDF Merger":
    st.header("🔗 PDF Document Merger")
    st.write("Combine multiple PDF files sequentially into a single consolidated PDF.")
    
    merge_files = st.file_uploader("Upload 2 or more PDF documents", type=['pdf'], accept_multiple_files=True)
    
    if merge_files and len(merge_files) >= 2:
        if st.button("Merge Documents"):
            with st.spinner("Merging document streams..."):
                try:
                    merger = PdfMerger()
                    for pdf in merge_files:
                        merger.append(pdf)
                    output = io.BytesIO()
                    merger.write(output)
                    st.success("PDF documents merged successfully!")
                    st.download_button(
                        label="📥 Download Merged PDF", 
                        data=output.getvalue(), 
                        file_name="Rana_Merged.pdf",
                        mime="application/pdf"
                    )
                except Exception as e:
                    st.error(f"An error occurred during file merging: {e}")
    elif merge_files and len(merge_files) < 2:
        st.info("A minimum of 2 PDF files are required for compilation.")
    else:
        st.info("Please upload your PDF documents to continue.")

# ==================== 5. PDF TO IMAGE ====================
elif option == "PDF to Image":
    st.header("🖼️ PDF to Image Converter")
    st.write("Render specific pages of a PDF document back into individual high-definition PNG images.")
    
    uploaded_pdf = st.file_uploader("Upload your PDF source file", type=['pdf'])
    
    if uploaded_pdf:
        try:
            pdf_bytes = uploaded_pdf.read()
            doc = fitz.open(stream=pdf_bytes, filetype="pdf")
            total_pages = len(doc)
            
            st.info(f"Target document successfully loaded. Total page count: {total_pages}")
            page_num = st.number_input("Target Page Number:", min_value=1, max_value=total_pages, value=1, step=1)
            
            if st.button("Render Page"):
                with st.spinner("Rendering vector graphics to raster..."):
                    page = doc.load_page(page_num - 1)
                    pix = page.get_pixmap()
                    img_data = pix.tobytes("png")
                    
                    st.image(img_data, caption=f"Page {page_num} Visual Preview", use_container_width=True)
                    st.download_button(
                        label=f"📥 Download Page {page_num} as PNG",
                        data=img_data,
                        file_name=f"Rana_Page_{page_num}.png",
                        mime="image/png"
                    )
        except Exception as e:
            st.error(f"Could not parse the selected PDF file: {e}")
    else:
        st.info("Upload a PDF document to extract a page layout as an image.")

# ==================== 6. PROTECT PDF ====================
elif option == "Protect PDF":
    st.header("🔒 File Security & Encryption")
    st.write("Encrypt your sensitive PDFs with strong owner-level user passwords.")
    
    uploaded_pdf = st.file_uploader("Upload your PDF source file", type=['pdf'])
    password = st.text_input("Assign a security password:", type="password")
    
    if uploaded_pdf and password:
        if st.button("Encrypt & Secure File"):
            with st.spinner("Configuring cryptographic locks..."):
                try:
                    reader = PdfReader(uploaded_pdf)
                    writer = PdfWriter()
                    
                    for page in reader.pages:
                        writer.add_page(page)
                        
                    writer.encrypt(password)
                    
                    output = io.BytesIO()
                    writer.write(output)
                    
                    st.success("Your document has been successfully encrypted!")
                    st.download_button(
                        label="📥 Download Encrypted PDF",
                        data=output.getvalue(),
                        file_name="Rana_Protected.pdf",
                        mime="application/pdf"
                    )
                except Exception as e:
                    st.error(f"Failed to encrypt file stream: {e}")
    elif uploaded_pdf and not password:
        st.warning("A security password must be declared to perform document encryption.")
    else:
        st.info("Upload a PDF file and specify a strong password to lock your file.")

# --- Real-Time Visitor Metrics Layout ---
st.markdown("---")
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.metric(label="👥 Live Platform Visits Tracking", value=f"{current_traffic:,} Sessions 🚀")
