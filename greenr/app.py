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
#st.subheader('*A click closer to a greener plate*')

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

url = inputbar.text_input("", "")

instruct_text.text('Paste any URL to a recipe page on bbc.co.uk (EN), chefkoch.de (DE) or marmiton.org (FR),\ne.g.: https://www.bbc.co.uk/food/recipes/salmonburgerswithbas_86430')

if url:

    # Cleaning up input elements
    instruct_text.empty()
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

    # Try/except to catch errors
    try:

        # Calling main calculation function & fetching chart
        out = main_calculation.calculate(url.strip())
        chart = visualizer.waffleplot(out[1], en = out[-1])

        # Cleaning up loading indicators
        load_runner.empty()
        status_text.empty()

        # Showing main result
        if out[-1]:
            st.header(f'**{out[2]}:** {out[0]} kg of CO2 per serving')
        else:
            st.header(f'**Recipe impact:** {out[0]} kg of CO2')

        st.text("")

        st.altair_chart(chart, use_container_width=True)

        st.markdown(f'<p style = "text-align:center" color="pink"> \
            Offset the carbon impact of your recipe by donating to www.coolearth.org.\n \
            To try another recipe, press [R] to refresh the page. \
            </p>',
            unsafe_allow_html=True,)

        st.markdown(f'<p style = "text-align:center" color="pink">\
          Credit: Georges Delrieu, Yannick Louwerse, Nick Pinaire & Florencia Rimanoczy  </p>', unsafe_allow_html=True)

    except:

        # Cleaning up loading indicators
        load_runner.empty()
        status_text.empty()

        # Message
        st.text('Something went wrong! Please press [R] to refresh, make sure your pasted url comes from\na supported recipe site and try again!')

        # Gif
        file_ = open("error.gif", "rb")
        contents = file_.read()
        data_url = base64.b64encode(contents).decode("utf-8")
        file_.close()
        load_runner = st.markdown(
            f'<p style="text-align:center;"> <img src="data:image/gif;base64,{data_url}"> </p>',
            unsafe_allow_html=True,
            )

