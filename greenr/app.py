import streamlit as st

import numpy as np
import pandas as pd
import time
import webbrowser
import base64
import app.main_calculation

###########################################
st.text('')
st.text('')
st.text('')
st.title('GREENR!')
st.subheader(' A click closer to a greener plate')

###########################################


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

def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

#def remote_css(url):
#    st.markdown(f'<link href="{url}" rel="stylesheet">', unsafe_allow_html=True)

local_css("style.css")
###########################################

selected = st.text_input("", " ")
progress_bar = st.progress(0)
status_text = st.empty()
url = "https://www.google.com.tr/search?q="


if st.button('Go!'):
    #print('I clicked the button, and I liked it')
    for i in range(100):
        progress_bar.progress(i + 1)
        time.sleep(.02)
    status_text.text(
        'Fetching your recipe...')
    time.sleep(.02)
    webbrowser.open_new_tab(url + selected)







