mkdir -p ~/.streamlit/

echo $PORT

echo "\
[general]\n\
email = \"georges.delrieu@laposte.net\"\n\
" > ~/.streamlit/credentials.toml

echo "\
[server]\n\
headless = true\n\
enableCORS=false\n\
port = $PORT\n\
" > ~/.streamlit/config.toml
