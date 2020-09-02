import streamlit as st

import numpy as np
import pandas as pd
import time
import webbrowser
import base64

import main_calculation

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


#@st.cache(allow_output_mutation=True)
#def get_base64_of_bin_file(bin_file):
#    with open(bin_file, 'rb') as f:
#        data = f.read()
#    return base64.b64encode(data).decode()

#def set_png_as_page_bg(png_file):
#    bin_str = get_base64_of_bin_file(png_file)
#    page_bg_img = '''
#    <style>
#    body {
#    background-image: url("data:image/png;base64,%s");
#    background-size: cover;
#    }
#    </style>
#    ''' % bin_str

#    st.markdown(page_bg_img, unsafe_allow_html=True)
#    return

#set_png_as_page_bg('background.png')
###########################################

def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

#def remote_css(url):
#    st.markdown(f'<link href="{url}" rel="stylesheet">', unsafe_allow_html=True)

local_css("style.css")

###########################################
url = st.text_input("", "Paste your bbc.co.uk recipe link here!")

status_text = st.empty()
if st.button('Go!'):

    with st.spinner('Fetching your recipe...'):
      time.sleep(5)
    st.success('Done!')
    time.sleep(.02)

    ghg = main_calculation.calculate(url)

    st.title(f'This recipe has an estimated environmental impact of {ghg} kilos of CO2')






#st.markdown("https://acegif.com/wp-content/uploads/loading-2.gif")
#st.markdown("![Alt Text](https://media.giphy.com/media/vFKqnCdLPNOKc/giphy.gif)")
