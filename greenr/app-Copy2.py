import streamlit as st

import numpy as np
import pandas as pd
import time
import webbrowser
import base64
###########################################
st.beta_set_page_config(
     page_title="Greenr",
     page_icon="🥦",
     layout="centered",
     initial_sidebar_state="collapsed"
 )
###########################################   
st.text('')
st.text('')
st.text('')
st.text('')
st.text('')
st.text('')
st.title('GREENR!')
st.subheader(' A click closer to a greener plate')

###########################################
#Background image

@st.cache(allow_output_mutation=True)
def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

def set_png_as_page_bg(png_file):
    bin_str = get_base64_of_bin_file(png_file)
    page_bg_img = '''
    <style>
    body {
    background-image: url("data:image/png;base64,%s");
    background-size: cover;
    }
    </style>
    ''' % bin_str
    
    st.markdown(page_bg_img, unsafe_allow_html=True)
    return

set_png_as_page_bg('background.png')



###########################################
# Text and page Styleing 
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

#def remote_css(url):
#    st.markdown(f'<link href="{url}" rel="stylesheet">', unsafe_allow_html=True)    

local_css("style.css")

###########################################
#Sidebar
st.sidebar.markdown("Top 5 GHG emitting foods")
st.sidebar.markdown("- Beef(beef herd)")
st.sidebar.markdown("- Lamb and mutton")
st.sidebar.markdown("- Cheese")
st.sidebar.markdown("- Beef(dairy herd)")
st.sidebar.markdown("- Chocolate")

###########################################

selected = st.text_input("", "Paste your bbc.co.uk recipe link here!")
status_text = st.empty()
url = "https://www.google.com.tr/search?q="

if st.button('Go!'):
    progress_bar = st.progress(0)
    
    time.sleep(1.)
    
    for i in range(100):
        progress_bar.progress(i + 1)
    
    time.sleep(1.)    
    
    status_text.text( 
          'Fetching your recipe...')
    
    
    
    webbrowser.open_new_tab(url + selected)
        
#st.error("Oops! That was not a valid recipe. Try again...")       

#st.title(f'This recipe has an estimated environmental impact of {ghg} kilos of CO2')
    



    

