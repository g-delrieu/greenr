mkdir -p ~/.streamlit/

ls

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

cd greenr
