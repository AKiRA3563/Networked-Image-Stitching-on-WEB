import time
import streamlit as st 
import sqlite3

from PIL import Image
from io import BytesIO
from streamlit_extras.grid import grid
from streamlit_image_select import image_select

conn = sqlite3.connect("gallery.db", check_same_thread=False)
c = conn.cursor()

def createTable():
    with conn:
        c.execute("""CREATE TABLE IF NOT EXISTS GALLERY(
                        IMG_ID INTEGER PRIMARY KEY AUTOINCREMENT,
                        IMG_NAME    VARCHAR(50)  NOT NULL UNIQUE,
                        IMG_DATA    BLOB         NOT NULL,
                        DATE        DATE,
                        USER        VARCHAR(50)
                        );""")

def remove_img(app):
    with conn:
        c.execute("DELETE from GALLERY WHERE IMG_DATA = :name", {'name': app})

# def display_image(image, caption):
#     # Display the image
#     img = Image.open(BytesIO(image))
#     st.image(img, caption=caption, width=400, use_column_width=True)

def button_process(image, name):

    buffered = BytesIO()
    image.save(buffered, format="JPEG")
    byte_im = buffered.getvalue() 

    my_grid = grid(6, vertical_align="bottom", )

    btn = {
        "download": my_grid.download_button(
            label="Download", 
            data=byte_im, 
            file_name=f'{name}.png',
            mime="image/png",
            use_container_width=True,
            key="download"
            ),
        "delete": my_grid.button(
            "Delete",
            use_container_width=True,
            key="delete"
            ),
    }

    if st.session_state.get('delete'):
        try:
            sql = f"DELETE FROM GALLERY WHERE IMG_NAME = '{name}'"
            c.execute(sql)
            conn.commit()
            alert = st.success("Image deleted successfully.", icon="✅" )
            sec = 5
        except:
            alert = st.warning('Something went wrong! Try Again.', icon="⚠️")
            sec = 10
        time.sleep(sec) # Wait for x seconds
        alert.empty() # Clear the alert
        st.rerun()

    return btn
  

def main(user):    

    sql = f"SELECT IMG_NAME, IMG_DATA, DATE from GALLERY WHERE USER = '{user}'"
    c.execute(sql)
    data = c.fetchall()

    st.subheader(f"{user}'s Stitched Gallery")  
    if data == []:
        st.text("You're gallery is empty.")
    else:    
        images = []
        caps = []        

        for IMG_NAME, IMG_DATA, DATE in data:
            img = Image.open(BytesIO(IMG_DATA))
            images.append(img)
            caps.append(IMG_NAME)
            
        with st.expander("**Select a image**"):
            imgs = image_select(
                label="",
                images=images,
                captions=caps,
                index=0,
                use_container_width=False,
            )
        
        # edit image_select library on line 108 to return 2 values (images and captions)
        st.image(imgs[0], use_column_width="auto", clamp=True)
        button_process(imgs[0], imgs[1])


