cat > session-tls.yaml << EOF
name: amts
version: "0.2"

services:
   - name: application
     environment:
         DATABASE_USER: amts
         DATABASE_PASSWORD: supersecret
         ENVIRONMENT: prod
         DEBUG: 1
         ADMIN_EMAIL: admin@amts.com
         ADMIN_PASSWORD: 12345
         SMTP_PASSWORD: ""
         HOST: amts.mmelo.me
     image_name: matheusmelo/amts_api:latest
     mrenclaves: [$ENCLAVE_HASH]
     command: python3 /encrypted-backend/app.py
     pwd: /
     fspf_path: /encrypted-backend/fspf.pb
     fspf_key: $FSPF_KEY
     fspf_tag: $FSPF_TAG

images:
   - name: matheusmelo/amts_api:latest
     injection_files:
       - path:  /cert.pem
         content: \$\$SCONE::SERVER_CERT.crt\$\$
       - path: /key.pem
         content: \$\$SCONE::SERVER_CERT.key\$\$

secrets:
   - name: SERVER_CERT
     kind: x509

EOF
