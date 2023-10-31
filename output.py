import time
import streamlit as st
from io import BytesIO
from PIL import Image
from streamlit_extras.grid import grid

import sqlite3
conn = sqlite3.connect("gallery.db", check_same_thread=False)
c = conn.cursor()

def visualise(panorama, uploaded_images, user):
    # Display the resulting panorama
    if panorama is not None:
        st.sidebar.text('Stitching Successful!')

        # Display resulting panorama
        st.subheader('Stitching Result')
        st.image(panorama, use_column_width=True)

        # Get a description for the image
        description = st.text_input("Image Description:")

        # process button 
        button_process(panorama, user, description)
        
        st.markdown("#")
        st.subheader('Uploaded Images (Displayed in the order of upload)')
        st.image(uploaded_images, width=200, channels="BGR")

    else:
        st.markdown("Insufficient data, please use more input images \
                    or ensure the images have overlapping features...")
        st.sidebar.text("Unable to stitch images...")


# def get_image_download_link(image):
def button_process(image, user, description):

    result = Image.fromarray(image)
    buffered = BytesIO()
    result.save(buffered, format="JPEG")
    byte_im = buffered.getvalue() 

    my_grid = grid(6, vertical_align="bottom", )

    btn = {
        "download": my_grid.download_button(
            label="Download", 
            data=byte_im, 
            file_name=f'{description}.png' if description else 'stitching.png',
            mime="image/png",
            use_container_width=True,
            key="download"
            ),
        "save": my_grid.button(
            "Save to Gallery",
            use_container_width=True,
            key="save"
            ),
    }
    
    if st.session_state.get('download'):
        alert = st.success("Downlaod Complete.")
        time.sleep(5) # Wait for 3 seconds
        alert.empty() # Clear the alert
    if st.session_state.get('save'):
        if user is ' ':
            alert = st.warning('Please login in before saveing image.')
            time.sleep(10) # Wait for 3 seconds
            alert.empty() # Clear the alert
        else:
            if description == '':
                alert = st.warning('Please enter a name for your image before saving.', icon="⚠️")
                sec = 5
            else:
                try:
                    c.execute("INSERT INTO GALLERY (IMG_NAME, IMG_DATA, DATE, USER) VALUES (?, ?, date('now'), ?)", (description, byte_im, user))
                    conn.commit()
                    alert = st.success("Image is added to the Gallery!", icon="✅" )
                    sec = 5
                except sqlite3.Error as e:
                    # alert = st.warning('Something went wrong! Try Again.', icon="⚠️")
                    # print(type(str(e)))
                    # print(str(e))
                    if 'UNIQUE' in str(e):
                        alert = st.warning("You already have a image with this name. Please try another name.", icon="⚠️")
                    else:
                        alert = st.warning('Something went wrong! Try Again.', icon="⚠️")
                    sec = 10
            time.sleep(sec) # Wait for x seconds
            alert.empty() # Clear the alert
        

    return btn


def simplified_output(uploaded_images):
    # Display uploaded images as is with no modifications
    st.subheader('Uploaded Images (Displayed in the order of upload)')
    st.image(uploaded_images, width=200, channels="BGR")


# def verbose_output(uploaded_images):
#     # Displays the individual images including the following information:
#     # 1- Images with their corresponding features
#     #    detections and matches with found by OpenCV
#     # 2- Ground truth feature locations

#     st.header('Uploaded Images w/ detected feature \
#               annotations (Displayed in the order of upload)')
#     uploaded_images = traditional_stitcher(uploaded_images)
#     # TODO Add feature matching indicators if applicable
#     st.image(uploaded_images, width=400, channels="BGR")
