mkdir -p conf
if [[ ! -f conf/client.crt || ! -f conf/client-key.key  ]] ; then
    openssl req -x509 -newkey rsa:4096 -out conf/client.crt -keyout conf/client-key.key  -days 31 -nodes -sha256 -subj "/C=US/ST=Dresden/L=Saxony/O=Scontain/OU=Org/CN=www.scontain.com" -reqexts SAN -extensions SAN -config <(cat /etc/ssl/openssl.cnf \
<(printf '[SAN]\nsubjectAltName=DNS:www.scontain.com'))
fi
