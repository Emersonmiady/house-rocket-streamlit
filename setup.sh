mkdir -p ~/.streamlit/

echo "\
[general]\n\
email = \"emersonmiady@gmail.com\"\n\
" > ~/.streamlit/credentials.toml

echo "\
[server]\n\
headless = true\n\
enableCORS=false\n\
port = $SPORT\n\
" > ~/.streamlit/config.toml