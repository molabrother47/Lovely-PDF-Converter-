import streamlit as st
import pandas as pd
from PIL import Image
import numpy as np
import cv2  # Advanced Image Processing
from fpdf import FPDF
import pdfplumber
from PyPDF2 import PdfMerger, PdfReader, PdfWriter
from docx import Document
import fitz  # PyMuPDF
import io
import os
import random

# --- App Page Config ---
st.set_page_config(page_title="Multi-Tool PDF & CamScanner App", layout="wide")

# --- Secure Analytics Tracking ---
ANALYTICS_FILE = "analytics_data.txt"

def get_analytics():
    """Saves and increments traffic, conversions and active sessions safely."""
    default_data = {"traffic": 100, "completed": 45, "users": 3}
    
    if not os.path.exists(ANALYTICS_FILE):
        try:
            with open(ANALYTICS_FILE, "w") as f:
                f.write(f"{default_data['traffic']},{default_data['completed']},{default_data['users']}")
            return default_data
        except Exception:
            return default_data
    else:
        try:
            with open(ANALYTICS_FILE, "r+") as f:
                data_str = f.read().strip()
                if not data_str:
                    parts = ["100", "45", "3"]
                else:
                    parts = data_str.split(",")
                
                traffic = int(parts[0]) + 1
                completed = int(parts[1])
                users = random.randint(2, 8)  # Live dynamic users simulator
                
                f.seek(0)
                f.write(f"{traffic},{completed},{users}")
                f.truncate()
                
            return {"traffic": traffic, "completed": completed, "users": users}
        except Exception:
            return default_data

# Run analytics tracking safely
analytics = get_analytics()

# --- Custom CSS (Yellow Sidebar Navigation & Colorful Service Boxes) ---
st.markdown("""
<style>
    /* Yellow background and bold black text for Home, About, Services in Sidebar */
    .nav-item {
        background-color: #FFD700 !important; /* Premium Gold/Yellow Fill */
        color: #000000 !important;
        font-weight: 900 !important;
        font-size: 16px !important;
        padding: 12px 20px;
        border-radius: 8px;
        text-align: center;
        margin-bottom: 12px;
        display: block;
        box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
        text-transform: uppercase;
        border: 2px solid #E6B800;
    }
    
    /* Services Styling - Horizontal Row alignment */
    .service-box {
        padding: 20px;
        border-radius: 10px;
        font-weight: bold;
        font-size: 18px;
        text-align: center;
        color: white !important;
        margin: 10px 0px;
        box-shadow: 0px 4px 10px rgba(0,0,0,0.15);
        transition: transform 0.2s;
    }
    .service-box:hover {
        transform: scale(1.03);
    }
    .img-to-pdf { background: linear-gradient(135deg, #FF416C, #FF4B2B); } /* Vibrant Red/Pink */
    .txt-to-pdf { background: linear-gradient(135deg, #17EAD9, #6078EA); } /* Cool Blue */
    .excel-to-pdf { background: linear-gradient(135deg, #11998e, #38ef7d); } /* Emerald Green */
</style>
""", unsafe_allow_html=True)

# --- Sidebar ---
st.sidebar.title("Navigation")
st.sidebar.markdown('<div class="nav-item">🏠 HOME</div>', unsafe_allow_html=True)
st.sidebar.markdown('<div class="nav-item">ℹ️ ABOUT</div>', unsafe_allow_html=True)
st.sidebar.markdown('<div class="nav-item">🛠️ SERVICES</div>', unsafe_allow_html=True)

# Analytics display in sidebar
st.sidebar.write("---")
st.sidebar.subheader("Live Stats")
st.sidebar.metric("Active Users 👥", analytics["users"])
st.sidebar.metric("Total Traffic 📈", analytics["traffic"])

# --- Main App Header ---
st.title("📄 Advanced Multi-Tool PDF Editor")
st.write("Professional and high-speed PDF utility software.")

# --- Row of Core Services (Direct Horizontal Presentation) ---
st.write("### Quick Services")
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown('<div class="service-box img-to-pdf">🖼️ Image to PDF</div>', unsafe_allow_html=True)
    # Upload and convert multiple images to PDF
    img_files = st.file_uploader("Upload Images for PDF:", type=["jpg", "png", "jpeg"], accept_multiple_files=True, key="quick_img")
    if img_files:
        if st.button("Convert to PDF 🖼️➡️📄", key="btn_img"):
            pdf = FPDF()
            for img_file in img_files:
                image = Image.open(img_file)
                # Convert to RGB if RGBA
                if image.mode == 'RGBA':
                    image = image.convert('RGB')
                
                # Save temporarily to bytes
                temp_iot = io.BytesIO()
                image.save(temp_iot, format="JPEG")
                temp_iot.seek(0)
                
                # Add page to PDF
                pdf.add_page()
                # Simple full page fit or default positioning
                pdf.image(temp_iot, x=10, y=10, w=190)
            
            pdf_output = pdf.output(dest='S').encode('latin-1')
            st.download_button("📥 Download PDF", data=pdf_output, file_name="images_converted.pdf", mime="application/pdf")
    
with col2:
    st.markdown('<div class="service-box txt-to-pdf">📝 Text to PDF</div>', unsafe_allow_html=True)
    txt_file = st.file_uploader("Upload Text File (.txt):", type=["txt"], key="quick_txt")
    if txt_file:
        if st.button("Convert to PDF 📝➡️📄", key="btn_txt"):
            text_data = txt_file.read().decode("utf-8")
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", size=12)
            # Multi-line text write
            pdf.multi_cell(0, 10, txt=text_data)
            pdf_output = pdf.output(dest='S').encode('latin-1')
            st.download_button("📥 Download PDF", data=pdf_output, file_name="text_converted.pdf", mime="application/pdf")
    
with col3:
    st.markdown('<div class="service-box excel-to-pdf">📊 Excel to PDF</div>', unsafe_allow_html=True)
    excel_file = st.file_uploader("Upload Excel File:", type=["xlsx", "xls"], key="quick_excel")
    if excel_file:
        if st.button("Convert to PDF 📊➡️📄", key="btn_excel"):
            df = pd.read_excel(excel_file)
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", size=10)
            
            # Simple tabular text representation
            table_str = df.to_string()
            pdf.multi_cell(0, 10, txt=table_str)
            
            pdf_output = pdf.output(dest='S').encode('latin-1')
            st.download_button("📥 Download PDF", data=pdf_output, file_name="excel_converted.pdf", mime="application/pdf")


# --- CamScanner Auto-Aligner & Enhancer Section ---
st.write("---")
st.markdown("## 📷 CamScanner Pro (Auto-Align & Scan Optimizer)")
st.info("Directly capture images from your camera or upload files. The system will automatically detect the paper boundaries, auto-align to 90 degrees, and enhance the brightness for clear, readable text.")

# Document Scan State Management
if "camscanner_pages" not in st.session_state:
    st.session_state.camscanner_pages = []

def process_camscan(image_bytes):
    """Detects page corners, warps perspective to a clean 90-degree angle, and boosts brightness."""
    # Convert uploaded raw bytes to OpenCV Mat image
    nparr = np.frombuffer(image_bytes, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    original = img.copy()
    
    # Step 1: Pre-processing (Grayscale, Blur & Edge Detection)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    edged = cv2.Canny(blurred, 75, 200)
    
    # Step 2: Find contours to find document boundary
    contours, _ = cv2.findContours(edged.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours, key=cv2.contourArea, reverse=True)[:5]
    
    target_contour = None
    for c in contours:
        perimeter = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.02 * perimeter, True)
        if len(approx) == 4:
            target_contour = approx
            break
            
    # Step 3: Perspective transform to align the sheet to 90 degrees straight
    if target_contour is not None:
        pts = target_contour.reshape(4, 2)
        rect = np.zeros((4, 2), dtype="float32")
        
        # Sort points sequence: Top-Left, Top-Right, Bottom-Right, Bottom-Left
        s = pts.sum(axis=1)
        rect[0] = pts[np.argmin(s)]
        rect[2] = pts[np.argmax(s)]
        
        diff = np.diff(pts, axis=1)
        rect[1] = pts[np.argmin(diff)]
        rect[3] = pts[np.argmax(diff)]
        
        (tl, tr, br, bl) = rect
        width_a = np.sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2))
        width_b = np.sqrt(((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2))
        max_width = max(int(width_a), int(width_b))
        
        height_a = np.sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2))
        height_b = np.sqrt(((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2))
        max_height = max(int(height_a), int(height_b))
        
        dst = np.array([
            [0, 0],
            [max_width - 1, 0],
            [max_width - 1, max_height - 1],
            [0, max_height - 1]], dtype="float32")
        
        transform_matrix = cv2.getPerspectiveTransform(rect, dst)
        warped = cv2.warpPerspective(img, transform_matrix, (max_width, max_height))
    else:
        # Fallback if paper borders are not detected clearly
        warped = original

    # Step 4: CamScanner Brightness & Contrast Enhancer
    # alpha (Contrast): 1.35x for pop out text, beta (Brightness): +20 for removing page shadows
    scanned_effect = cv2.convertScaleAbs(warped, alpha=1.35, beta=20)
    
    # Convert BGR back to PIL RGB format for Streamlit
    color_corrected = cv2.cvtColor(scanned_effect, cv2.COLOR_BGR2RGB)
    return Image.fromarray(color_corrected)

# Interactive Source Picker
input_source = st.radio("Select Image Source:", ["📷 Live Camera Capture", "📁 Upload Local Files"], horizontal=True)
scanned_inputs = []

if input_source == "📷 Live Camera Capture":
    camera_pic = st.camera_input("Snap a paper document:")
    if camera_pic:
        scanned_inputs.append(camera_pic)
else:
    uploaded_pics = st.file_uploader("Upload Pages:", type=["jpg", "png", "jpeg"], accept_multiple_files=True)
    if uploaded_pics:
        scanned_inputs = uploaded_pics

# Trigger Scan Processing
if scanned_inputs:
    if st.button("🪄 Run CamScanner Edge-Correction"):
        with st.spinner("Aligning and enhancing your document..."):
            processed_list = []
            for item in scanned_inputs:
                file_bytes = item.read()
                processed_pil = process_camscan(file_bytes)
                processed_list.append(processed_pil)
            st.session_state.camscanner_pages.extend(processed_list)
            st.success(f"Added {len(processed_list)} page(s) successfully!")

# Display Scanned Queue and compile Multi-page PDF
if st.session_state.camscanner_pages:
    st.write("---")
    st.write("### 📂 Scanned Document Queue")
    
    # Show thumbnails in columns
    thumb_cols = st.columns(min(len(st.session_state.camscanner_pages), 6))
    for idx, img in enumerate(st.session_state.camscanner_pages):
        with thumb_cols[idx % len(thumb_cols)]:
            st.image(img, caption=f"Page {idx+1}", use_container_width=True)
            
    col_act1, col_act2 = st.columns(2)
    
    with col_act1:
        # Build multi-page PDF on the fly
        pdf_io = io.BytesIO()
        first_page = st.session_state.camscanner_pages[0]
        subsequent_pages = st.session_state.camscanner_pages[1:]
        
        first_page.save(pdf_io, format="PDF", save_all=True, append_images=subsequent_pages)
        pdf_io.seek(0)
        
        st.download_button(
            label="📥 Download Compiled PDF Document",
            data=pdf_io,
            file_name="scanned_cam_document.pdf",
            mime="application/pdf"
        )
        
    with col_act2:
        if st.button("🧹 Reset Scanner Queue"):
            st.session_state.camscanner_pages = []
            st.rerun()
    
