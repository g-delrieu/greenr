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
instruct_text = st.empty()

url = inputbar.text_input("", "https://www.bbc.co.uk/food/recipes/caribbean_roast_chicken_45833")

instruct_text.text('Paste any URL to a recipe page on bbc.co.uk (EN), chefkoch.de (DE) or marmiton.org (FR)')

if gobutton.button('Go!'):

    # Cleaning up input elements
    gobutton.empty()
    inputbar.empty()
    instruct_text.empty()

    time.sleep(.1)

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
    out = main_calculation.calculate(url)
    plt = visualizer.waffleplot(out[1], en = out[-1])

    # Cleaning up loading indicators
    load_runner.empty()
    status_text.empty()

    # Showing main result
    if out[-1]:
        st.header(f'**{out[2]}:** {out[0]} kg of CO2 per serving')
    else:
        st.header(f'**Recipe impact:** {out[0]} kg of CO2')

    st.text("")

    plt = plt
    st.pyplot()

    st.markdown(f'<p style = "text-align:center;"> Press [R] to refresh the page and go again! </p>',
        unsafe_allow_html=True,)
