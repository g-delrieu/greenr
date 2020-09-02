import streamlit as st

import numpy as np
import pandas as pd
import time
import webbrowser
import base64

import main_calculation
import visualizer

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

###########################################

def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

#def remote_css(url):
#    st.markdown(f'<link href="{url}" rel="stylesheet">', unsafe_allow_html=True)

local_css("style.css")
###########################################

url = st.text_input("", "https://www.bbc.co.uk/food/recipes/caribbean_roast_chicken_45833")

status_text = st.empty()

if st.button('Go!'):

    # Progress bar
    progress_bar = st.progress(0)

    for i in range(100):
        progress_bar.progress(i + 1)
    status_text.text(
        'Fetching your recipe...')
    time.sleep(.2)

    # Calling main calculation function
    ghg_sum, df_parsed = main_calculation.calculate(url)

    # Showing main result
    st.title(f'This recipe has an estimated environmental impact of {ghg_sum} kilos of CO2 per serving')

    # Fetching and showing chart
    plt,debugvalue = visualizer.waffleplot(df_parsed)
    st.pyplot(plt, width = 700, height = 700)

    st.dataframe(df_parsed)
    st.text(debugvalue)
