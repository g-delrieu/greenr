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
st.title('GREENR!')
st.subheader('*A click closer to a greener plate*')

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

local_css("style.css")
###########################################

inputbar = st.empty()
status_text = st.empty()
gobutton = st.empty()

url = inputbar.text_input("", "https://www.bbc.co.uk/food/recipes/caribbean_roast_chicken_45833")

if gobutton.button('Go!'):

    # Cleaning up input elements
    gobutton.empty()
    inputbar.empty()

    # Indicate progress
    status_text.text(
        'Fetching your recipe...')

    # Add gif
    file_ = open("loading.gif", "rb")
    contents = file_.read()
    data_url = base64.b64encode(contents).decode("utf-8")
    file_.close()

    load_runner = st.markdown(
        f'<p style="text-align:center;"> <img src="data:image/gif;base64,{data_url}"> </p>',
        unsafe_allow_html=True,
        )

    # Calling main calculation function & fetching chart
    ghg_sum, df_parsed = main_calculation.calculate(url)
    plt,debugvalue = visualizer.waffleplot(df_parsed)

    # Cleaning up loading indicators
    load_runner.empty()
    status_text.empty()

    # Showing main result
    st.title(f'This recipe has an estimated environmental impact of {ghg_sum} kilos of CO2 per serving')

    st.text("")

    plt = plt
    st.pyplot(use_container_width= False)

    st.dataframe(df_parsed)
    st.text(debugvalue)
