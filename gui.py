import streamlit as st
import numpy as np
import cv2

import stitchers
from output import visualise

def main(user):
    st.sidebar.header('Image Stitching')

    if "file_uploader_key" not in st.session_state:
        st.session_state["file_uploader_key"] = 0

    # Create upload interface for selecting inmages to be uploaded  
    multiple_pngs = st.sidebar.file_uploader(
        "Upload your set of PNG/JPEG images", 
        type=([".png", ".jpeg"]), 
        accept_multiple_files=True,
        key=st.session_state["file_uploader_key"],
    )

    uploaded_images = []

    if multiple_pngs:
        # Clear upload files button
        if st.sidebar.button("Clear uploaded files"):
            st.session_state["file_uploader_key"] += 1
            st.rerun()

    clean_pano = st.sidebar.checkbox('Clean and Crop Result')

    if multiple_pngs:
        # Read and decode the uploaded images and save them to a list
        for file_png in multiple_pngs:
            file_bytes = np.asarray(bytearray(file_png.read()), dtype=np.uint8)
            image = cv2.imdecode(file_bytes, 1)
            uploaded_images.append(image)
        
        st.sidebar.markdown('###')
        st.sidebar.subheader('Status:')
        data_load_state = st.sidebar.text("Processing Images")
        data_load_state.text(f"No. of images uploaded: {str(len(uploaded_images))}")

        # Perform stitching using OpenCV's native stitching function
        st.sidebar.text('Attempting to stitch images...')
        panorama = stitchers.stitcher(uploaded_images, clean_pano)
        
        visualise(panorama, uploaded_images, user)
    else:
        st.subheader("User Guide:")
        st.markdown("""
            1. Upload your images into **File Uploader**.
            2. Mark up on :green[**✅ Clean and Crop Result**] if you want to clean your proccessed image.
            3. Enter the image name into :blue[**📝 Image Description:**] if you want to download/save the image.
            4. Click :red[**Download**] or :red[**Save to Gallery**].
        """)

# if __name__=='__main__':
#     main()