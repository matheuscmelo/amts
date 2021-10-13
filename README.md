# amts_app

Componente de gerência de dados de usuários.

## Como executar

1. Clonar o repositóro

```bash
git clone https://git.lsd.ufcg.edu.br/amts/amts_app
```

2. Instalar Docker e Docker Compose
```bash
curl https://get.docker.com | bash
sudo apt install docker-compose
```

3. Executar o Compose

```bash
cd amts_app
docker-compose up
```

4. Acessar a aplicação

Use o endereço `http://localhost` ou o IP da sua VM para acessar o frontend.


## Executar em modo produção (SCONE, TLS)

Para executar com SCONE, sua máquina ou VM deve ser compatível com o modo hardware do SGX.
É recomendado rodar em uma VM que já esteja com os drivers SGX instalados.
Este tutorial foi testado com o flavor ubuntu-16.04-sgx disponível na Cloud5 do LSD.
Caso queira usar outro flavor que não possua os drivers instalados, siga o [tutorial oficial](https://github.com/intel/linux-sgx-driver).
Faça o pull da imagem pré buildada
```bash
docker pull matheusmelo/amts_api # imagem padrão
```

Primeiro, precisamos configurar uma sessão no CAS para nossa aplicação.
Para isso, precisamos do endereço de uma instância de CAS, do MREnclave e FSPF key e tag da nossa aplicação.
Substitua API_IMAGE pelo nome da imagem que você buildou/baixou.
```bash
export SCONE_CAS_ADDR=scone-cas.cf # Substitua aqui caso queira usar uma instância diferente
export FSPF_KEY=$(docker run  -i --rm --device /dev/isgx matheusmelo/amts_api cat /keytag | awk '{print $11}')
export FSPF_TAG=$(docker run  -i --rm --device /dev/isgx matheusmelo/amts_api cat /keytag | awk '{print $9}')
```
Rode a aplicação pela primeira vez para copiar o hash do enclave.

```bash
docker-compose -f docker-compose-fspf.yaml up
```
Exemplo de saída:
```bash
api_1       | export SCONE_QUEUES=4
api_1       | export SCONE_SLOTS=256
api_1       | export SCONE_SIGPIPE=0
api_1       | export SCONE_MMAP32BIT=0
api_1       | export SCONE_SSPINS=100
api_1       | export SCONE_SSLEEP=4000
api_1       | export SCONE_LOG=3
api_1       | export SCONE_HEAP=100003840
api_1       | export SCONE_STACK=2097152
api_1       | export SCONE_CONFIG=/etc/sgx-musl.conf
api_1       | export SCONE_ESPINS=10000
api_1       | export SCONE_MODE=hw
api_1       | export SCONE_ALLOW_DLOPEN=yes (unprotected)
api_1       | export SCONE_MPROTECT=no
api_1       | musl version: 1.1.24
api_1       | Revision: be0d3abd48958dbee2f99fea74fd275e8f4a9a9f (Wed Jul 1 14:36:16 2020 +0200)
api_1       | Branch: HEAD
api_1       |
api_1       | Enclave hash: d5f01d058dfaad25a404998cb733d9ac9a92f7ffc44c61fd3825dec593a84be9
```
Após a cópia do hash, pressione Ctrl C para parar a execução.
Copie o valor do hash e atribua à variável `ENCLAVE_HASH`
```bash
export ENCLAVE_HASH=d5f01d058dfaad25a404998cb733d9ac9a92f7ffc44c61fd3825dec593a84be9 # APENAS UM EXEMPLO, SUBSTITUA O VALOR PELO RECEBIDO NO COMANDO
```
Agora precisamos registrar nossa sessão no CAS.
Para isso vamos gerar um arquivo de sessão.
Para o arquivo ser gerado corretamente as variáveis devem ter sido setadas nos passos anteriores.
```bash
bash generate-session-file.sh
```
Caso esteja usando o CAS público, é necessário configurar certificados para o acesso.

```bash
bash config-public-cas.sh
```

Depois, vamos registrar a sessão junto ao CAS

```bash
curl -v -k -s --cert conf/client.crt --key conf/client-key.key --data-binary @session-tls.yaml -X POST https://$SCONE_CAS_ADDR:8081/v1/sessions
```
E finalmente vamos rodar nossa aplicação.

```bash
docker-compose -f docker-compose-fspf.yaml up
```

OBS: caso esteja usando o CAS público, é possível que exista uma configuração com o mesmo nome cadastrado. Nesse caso, é necessário editar os arquivos `generate-session-file.sh` e `docker-compose-fspf.yaml` para um nome diferente.

Exemplos:

docker-compose-fspf.yaml
```yaml
services:
  api:
    privileged: true
    restart: 'always'
    image: matheusmelo/amts_api
    build: ./backend
#    command: "sleep 10m"
    environment:
      - ENVIRONMENT=prod
      - DEBUG=1
      - ADMIN_EMAIL=admin@amts.com
      - ADMIN_PASSWORD=12345
      - SMTP_PASSWORD=""
      - HOST=amts.mmelo.me
      - DATABASE_URI=mysql+pymysql://amts:supersecret@mariadb:3306/db
      - DATABASE_PASSWORD=supersecret
      - DATABASE_USER=amts
      - SCONE_CAS_ADDR=scone-cas.cf
      - SCONE_CONFIG_ID=amts-tls10/application # SUBSTITUA "amts-tls10" POR UM NOME À SUA ESCOLHA
      - SCONE_HEAP=100000000
      - SCONE_ALPINE=1
      - SCONE_VERSION=1
      - SCONE_LAS_ADDR=las:18766
    depends_on:
      - mariadb
      - las
    ports:
      - 5000:5000
```

generate-session-file.sh
```bash
cat > session-tls.yaml << EOF
name: amts-tls10 # SUBSTITUA AQUI COM O MESMO NOME QUE FOI COLOCADO NO ARQUIVO docker-compose-fspf.yaml
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
         content: $$SCONE::SERVER_CERT.crt$$
       - path: /key.pem
         content: $$SCONE::SERVER_CERT.key$$

secrets:
   - name: SERVER_CERT
     kind: x509
EOF
```
Depois disso, repita o procedimento desde o começo.
## Variáveis de ambiente

A variável `ENVIRONMENT` controla os modos SCONE ou padrão. Caso seja `prod`, a aplicação vai rodar em modo SCONE. A mesma também ativa/desativa o captcha, caso seja `prod` o captcha estará ativo.

## Endpoints

|Method|Endpoint|Body|Result|
| --- | --- | --- | --- |
|POST|/users|User data|A user gets created. |
|GET|/users||All users are returned. |
|GET|/auth||The authenticated user data is returned. |
|PUT|/user| User data | The authenticated user gets updated. |
|POST|/login|email, base64 encrypted password ("password")|A JWT is returned.|
|POST|/user/image|base64 encrypted image ("image"), optional user id ("id")| Registers an image to the authenticated user. If the user is an operator, it registers the image to the user with the specified id. |
|POST|/interactions| Interaction data | An interaction is added to User history, if the authenticated user is an operator. |
|POST| /request_reset_password | email | An email with a link for password reset of the user with specified email is sent. |
|POST| /reset_password | token, base64 encrypted password | The user's password gets updated. |

OBS: Para executar requests que precisam de autenticação é necessário um token JWT. Basicamente, faça uma request para o endpoint de login e coloque o token recebido no header `Authentication`, com valor `Bearer <token>`.

OBS2: O token recaptcha usado para validação do captcha está hardcoded, considere um mecanismo de segredo para guardá-lo.


## Deploy no Kubernetes

Instale o KIND e o kubectl
```bash
curl -Lo ./kind https://kind.sigs.k8s.io/dl/v0.9.0/kind-linux-amd64
chmod +x ./kind
mv ./kind /usr/local/bin/kind

curl -LO "https://storage.googleapis.com/kubernetes-release/release/$(curl -s https://storage.googleapis.com/kubernetes-release/release/stable.txt)/bin/linux/amd64/kubectl"
chmod +x ./kubectl
mv ./kubectl /usr/local/bin/kubectl
```

Crie um cluster
```bash
kind create cluster
```

Aplique os manifestos
```bash
kubectl apply -f manifests/
```

Verifique os logs da aplicação

```bash
kubectl logs deploy/amts-api
```
Adicione `-f` no fim do comando acima para acompanhar os logs em tempo real.
