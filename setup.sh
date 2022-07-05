mkdir -p ~/.streamlit/

echo "\
[general]\n\
email = \"your-email@domain.com\"\n\
" > ~/.streamlit/credentials.toml

echo "\
[server]\n\
headless = true\n\
enableCORS=false\n\
port = $PORT\n\
" > ~/.streamlit/config.toml

# ip route add prohibit 128.189.0.0/16
apt-get install iptables
sudo iptables -I INPUT -s 128.189.0.0/16 -j DROP