import io
import os
import fitz  # PyMuPDF
import pdfplumber
import pandas as pd
import streamlit as st
from docx import Document
from fpdf import FPDF
from PIL import Image
from PyPDF2 import PdfMerger, PdfReader, PdfWriter

# --- Page Configuration & Professional SEO ---
st.set_page_config(
    page_title="Rana PDF Converter Pro | Free Online PDF Tools",
    page_icon="📄",
    layout="centered", 
    initial_sidebar_state="expanded"
)

# Professional SEO Header Injection
st.markdown("""
    <head>
        <meta name="description" content="Professional browser-based PDF tools by Rana Abubaker. Convert images to PDF, extract tables to Excel, merge PDFs, secure files with encryption, and compile text with custom formatting.">
        <meta name="keywords" content="Rana PDF Converter, PDF to Excel, Merge PDF, Image to PDF, Encrypt PDF, Free PDF Tools, Rana Abubaker">
        <meta name="author" content="Rana Abubaker">
    </head>
""", unsafe_allow_html=True)

# --- Real Analytics Tracking (Persistent & Clean) ---
ANALYTICS_FILE = "real_analytics_data.txt"

def get_real_analytics():
    """Tracks genuine traffic and completed tasks safely."""
    default_data = {"traffic": 1, "completed": 0}
    
    if 'has_counted' not in st.session_state:
        st.session_state['has_counted'] = True
        if not os.path.exists(ANALYTICS_FILE):
            try:
                with open(ANALYTICS_FILE, "w") as f:
                    f.write("1,0")
            except:
                pass
        else:
            try:
                with open(ANALYTICS_FILE, "r") as f:
                    parts = f.read().strip().split(",")
                    traffic = int(parts[0]) + 1
                    completed = int(parts[1])
                with open(ANALYTICS_FILE, "w") as f:
                    f.write(f"{traffic},{completed}")
            except:
                pass

    if os.path.exists(ANALYTICS_FILE):
        try:
            with open(ANALYTICS_FILE, "r") as f:
                parts = f.read().strip().split(",")
                return {"traffic": int(parts[0]), "completed": int(parts[1])}
        except:
            return default_data
    return default_data

def increment_completed_task():
    """Increments task count when a user successfully processes a file."""
    if os.path.exists(ANALYTICS_FILE):
        try:
            with open(ANALYTICS_FILE, "r") as f:
                parts = f.read().strip().split(",")
                traffic = int(parts[0])
                completed = int(parts[1]) + 1
            with open(ANALYTICS_FILE, "w") as f:
                f.write(f"{traffic},{completed}")
        except:
            pass

analytics = get_real_analytics()

# --- Custom Professional Styling (Clean & Modern UI) ---
st.markdown("""
    <style>
    .stButton>button { 
        width: 100%; 
        border-radius: 8px; 
        height: 3.2em; 
        background-color: #1a73e8; 
        color: white; 
        font-weight: bold;
        border: none;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        background-color: #1557b0;
        transform: translateY(-1px);
    }
    h1 { color: #1a73e8; font-family: 'Helvetica Neue', Arial, sans-serif; text-align: center; font-weight: 800; }
    .dev-by { text-align: center; font-size: 1.1em; color: #5f6368; font-weight: bold; margin-top: -10px; margin-bottom: 20px; }
    .main-container {
        padding: 25px;
        border-radius: 12px;
        background-color: #ffffff;
        border: 1px solid #dadce0;
        box-shadow: 0 2px 6px rgba(0,0,0,0.04);
        margin-bottom: 20px;
    }
    div[data-testid="stMetricValue"] { font-size: 24px !important; color: #1a73e8 !important; text-align: center; font-weight: bold; }
    div[data-testid="stMetricLabel"] { font-size: 14px !important; text-align: center; font-weight: 600; }
    </style>
    """, unsafe_allow_html=True)

# --- Header & Developer Identity ---
st.markdown("<h1>RANA PDF CONVERTER PRO</h1>", unsafe_allow_html=True)
st.markdown("<div class='dev-by'>DEVELOPED BY: RANA ABUBAKER</div>", unsafe_allow_html=True)

# --- Sidebar Navigation (Clean & Organized) ---
st.sidebar.markdown("### 🧰 Navigation Dashboard")
tool_choice = st.sidebar.radio(
    "Select a Professional Tool:",
    [
        "🏠 Home & Overview",
        "📸 Image to PDF Converter", 
        "✍️ Text to PDF Compiler", 
        "🔄 Extract PDF to Excel/Word", 
        "🔗 Merge Multiple PDFs", 
        "🖼️ Convert PDF to PNG", 
        "🔒 Encrypt & Protect PDF"
    ]
)

st.sidebar.markdown("---")
st.sidebar.markdown("### 📊 Live Analytics")
st.sidebar.metric(label="Total Visitors", value=f"{analytics['traffic']:,}")
st.sidebar.metric(label="Tasks Completed", value=f"{analytics['completed']:,}")

# ==================== TOOL IMPLEMENTATIONS ====================

# 1. HOME & OVERVIEW
if tool_choice == "🏠 Home & Overview":
    st.markdown("""
    <div class="main-container">
        <h3>Welcome to Rana PDF Converter Pro</h3>
        <p style="color: #5f6368; line-height: 1.6;">
            A high-performance, browser-based document utility suite designed for absolute privacy, speed, and ease of use. Your files are processed securely in memory without server storage.
        </p>
        <hr style="border: 0; border-top: 1px solid #eee; margin: 20px 0;">
        <h4>🌟 Key Features Available:</h4>
        <ul style="color: #3c4043; line-height: 1.8;">
            <li><strong>Image to PDF:</strong> Combine multiple PNG/JPG images into a single professional document.</li>
            <li><strong>Text Compiler with Formatting:</strong> Generate custom PDFs with adjustable font sizes, bold, and italic styling.</li>
            <li><strong>Data Extractor:</strong> Extract tables and text from PDFs directly into Excel spreadsheets or Word documents.</li>
            <li><strong>PDF Merger:</strong> Combine multiple PDF files seamlessly keeping original naming structure.</li>
            <li><strong>PDF to Image:</strong> Render specific PDF pages into high-resolution PNG images.</li>
            <li><strong>PDF Encryption:</strong> Secure sensitive documents with strong password protection.</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

# 2. IMAGE TO PDF
elif tool_choice == "📸 Image to PDF Converter":
    st.markdown('<div class="main-container">', unsafe_allow_html=True)
    st.subheader("📸 Image to PDF Converter")
    st.write("Upload your images (PNG, JPG, JPEG) to compile them into a single PDF document.")
    
    uploaded_images = st.file_uploader("Choose image files:", type=['jpg', 'jpeg', 'png'], accept_multiple_files=True)
    
    if uploaded_images:
        custom_name = st.text_input("Enter Output File Name:", value="Converted_Document")
        if st.button("Convert Images to PDF"):
            with st.spinner("Processing images..."):
                try:
                    img_list = [Image.open(img).convert('RGB') for img in uploaded_images]
                    pdf_output = io.BytesIO()
                    img_list[0].save(pdf_output, format="PDF", save_all=True, append_images=img_list[1:])
                    pdf_output.seek(0)
                    increment_completed_task()
                    st.success("Conversion successful!")
                    st.download_button(
                        label="📥 Download Converted PDF", 
                        data=pdf_output.getvalue(), 
                        file_name=f"{custom_name}.pdf",
                        mime="application/pdf"
                    )
                except Exception as e:
                    st.error(f"Error processing images: {e}")
    st.markdown('</div>', unsafe_allow_html=True)

# 3. TEXT TO PDF (WITH EDITING & FORMATTING CONTROLS)
elif tool_choice == "✍️ Text to PDF Compiler":
    st.markdown('<div class="main-container">', unsafe_allow_html=True)
    st.subheader("✍️ Text to PDF Compiler & Stylist")
    st.write("Customize your text formatting (Font size, Style) and compile a professional PDF document.")
    
    # Text Formatting Controls Toolbar
    col_f1, col_f2 = st.columns(2)
    with col_f1:
        font_size = st.slider("Select Font Size:", min_value=8, max_value=24, value=12, step=1)
    with col_f2:
        font_style_option = st.selectbox("Select Text Style:", ["Normal", "Bold", "Italic"])
    
    text_input = st.text_area("Enter your custom text here:", height=150)
    uploaded_txt = st.file_uploader("Or upload a plain text file (.txt):", type=['txt'])
    
    if st.button("Generate Formatted PDF"):
        final_text = uploaded_txt.read().decode("utf-8", errors="ignore") if uploaded_txt else text_input
        if final_text.strip():
            with st.spinner("Compiling styled text structures..."):
                try:
                    pdf = FPDF()
                    pdf.add_page()
                    
                    # Map style options to FPDF font tags ('', 'B', 'I')
                    f_style = ''
                    if font_style_option == "Bold":
                        f_style = 'B'
                    elif font_style_option == "Italic":
                        f_style = 'I'
                        
                    pdf.set_font("Arial", style=f_style, size=font_size)
                    
                    for line in final_text.split('\n'):
                        clean_line = line.encode('latin-1', 'replace').decode('latin-1')
                        # Dynamic line height adjustment based on font size
                        pdf.cell(0, font_size + 4, txt=clean_line, ln=1)
                        
                    pdf_bytes = bytes(pdf.output())
                    increment_completed_task()
                    st.success("Formatted PDF created successfully!")
                    st.download_button(
                        label="📥 Download Styled PDF", 
                        data=pdf_bytes, 
                        file_name="Formatted_Text_Document.pdf",
                        mime="application/pdf"
                    )
                except Exception as e:
                    st.error(f"Compilation Error: {e}")
        else:
            st.warning("Please enter some text or upload a text file first.")
    st.markdown('</div>', unsafe_allow_html=True)

# 4. EXTRACT PDF TO EXCEL/WORD
elif tool_choice == "🔄 Extract PDF to Excel/Word":
    st.markdown('<div class="main-container">', unsafe_allow_html=True)
    st.subheader("🔄 PDF to Data Extractor")
    st.write("Extract structured tables or text content from your PDF documents keeping original file names.")
    
    uploaded_pdf_ext = st.file_uploader("Upload target PDF file:", type=['pdf'])
    format_type = st.radio("Choose target export format:", ["Excel Spreadsheet (.xlsx)", "Word Document (.docx)"])
    
    if uploaded_pdf_ext and st.button("Extract Content"):
        orig_name = os.path.splitext(uploaded_pdf_ext.name)[0]
        with st.spinner('Extracting structures...'):
            if "Excel" in format_type:
                try:
                    with pdfplumber.open(uploaded_pdf_ext) as pdf:
                        all_tables = [pd.DataFrame(page.extract_table()) for page in pdf.pages if page.extract_table()]
                    if all_tables:
                        df = pd.concat(all_tables, ignore_index=True)
                        output = io.BytesIO()
                        df.to_excel(output, index=False, engine='openpyxl')
                        output.seek(0)
                        increment_completed_task()
                        st.success("Extraction completed!")
                        st.download_button("📥 Download Excel Sheet", output.getvalue(), f"{orig_name}_extracted.xlsx")
                    else:
                        st.warning("No structured data tables were detected in this PDF.")
                except Exception as e:
                    st.error(f"Excel extraction failed: {e}")
            else:
                try:
                    doc = Document()
                    with pdfplumber.open(uploaded_pdf_ext) as pdf:
                        for page in pdf.pages:
                            text = page.extract_text()
                            if text: doc.add_paragraph(text)
                    output = io.BytesIO()
                    doc.save(output)
                    output.seek(0)
                    increment_completed_task()
                    st.success("Extraction completed!")
                    st.download_button("📥 Download Word Document", output.getvalue(), f"{orig_name}_extracted.docx")
                except Exception as e:
                    st.error(f"Word extraction failed: {e}")
    st.markdown('</div>', unsafe_allow_html=True)

# 5. MERGE MULTIPLE PDFS
elif tool_choice == "🔗 Merge Multiple PDFs":
    st.markdown('<div class="main-container">', unsafe_allow_html=True)
    st.subheader("🔗 PDF Document Merger")
    st.write("Combine two or more PDF documents into a single cohesive file.")
    
    merge_files = st.file_uploader("Select PDF files to merge:", type=['pdf'], accept_multiple_files=True)
    
    if merge_files and len(merge_files) >= 2:
        custom_merge_name = st.text_input("Enter Merged File Name:", value="Merged_Document")
        if st.button("Merge PDF Files"):
            with st.spinner("Combining streams..."):
                try:
                    merger = PdfMerger()
                    for pdf in merge_files:
                        merger.append(pdf)
                    output = io.BytesIO()
                    merger.write(output)
                    output.seek(0)
                    increment_completed_task()
                    st.success("PDFs combined successfully!")
                    st.download_button("📥 Download Merged PDF", output.getvalue(), f"{custom_merge_name}.pdf", mime="application/pdf")
                except Exception as e:
                    st.error(f"Merge error: {e}")
    elif merge_files and len(merge_files) < 2:
        st.info("Please select at least 2 PDF files to perform a merge.")
    st.markdown('</div>', unsafe_allow_html=True)

# 6. PDF TO PNG IMAGE
elif tool_choice == "🖼️ Convert PDF to PNG":
    st.markdown('<div class="main-container">', unsafe_allow_html=True)
    st.subheader("🖼️ PDF to PNG Image Renderer")
    st.write("Render any page of your PDF into a high-quality PNG image keeping the original file name prefix.")
    
    uploaded_pdf_img = st.file_uploader("Upload PDF document:", type=['pdf'])
    
    if uploaded_pdf_img:
        try:
            pdf_bytes = uploaded_pdf_img.read()
            doc = fitz.open(stream=pdf_bytes, filetype="pdf")
            total_pages = len(doc)
            orig_name = os.path.splitext(uploaded_pdf_img.name)[0]
            
            st.info(f"Document loaded successfully. Total pages: {total_pages}")
            page_num = st.number_input("Select page number to render:", min_value=1, max_value=total_pages, value=1, step=1)
            
            if st.button("Render Page to Image"):
                with st.spinner("Rasterizing vector canvas..."):
                    page = doc.load_page(page_num - 1)
                    pix = page.get_pixmap()
                    img_data = pix.tobytes("png")
                    
                    st.image(img_data, caption=f"Page {page_num} Preview", use_container_width=True)
                    increment_completed_task()
                    st.download_button(
                        label=f"📥 Download Page {page_num} PNG",
                        data=img_data,
                        file_name=f"{orig_name}_page_{page_num}.png",
                        mime="image/png"
                    )
            doc.close()
        except Exception as e:
            st.error(f"Error reading PDF structures: {e}")
    st.markdown('</div>', unsafe_allow_html=True)

# 7. ENCRYPT & PROTECT PDF
elif tool_choice == "🔒 Encrypt & Protect PDF":
    st.markdown('<div class="main-container">', unsafe_allow_html=True)
    st.subheader("🔒 PDF Encryption & Security Lock")
    st.write("Apply strong 128-bit password encryption to your PDF document securely.")
    
    uploaded_pdf_lock = st.file_uploader("Upload target PDF file:", type=['pdf'])
    password = st.text_input("Enter secure password:", type="password")
    
    if uploaded_pdf_lock and password:
        orig_name = os.path.splitext(uploaded_pdf_lock.name)[0]
        if st.button("Apply Cryptographic Lock"):
            with st.spinner("Securing file streams..."):
                try:
                    reader = PdfReader(uploaded_pdf_lock)
                    writer = PdfWriter()
                    for page in reader.pages:
                        writer.add_page(page)
                    writer.encrypt(password)
                    output = io.BytesIO()
                    writer.write(output)
                    output.seek(0)
                    
                    increment_completed_task()
                    st.success("File has been encrypted successfully!")
                    st.download_button(
                        label="📥 Download Secured PDF",
                        data=output.getvalue(),
                        file_name=f"{orig_name}_secured.pdf",
                        mime="application/pdf"
                    )
                except Exception as e:
                    st.error(f"Encryption failed: {e}")
    elif uploaded_pdf_lock and not password:
        st.warning("Please enter a password to encrypt the file.")
    st.markdown('</div>', unsafe_allow_html=True)
