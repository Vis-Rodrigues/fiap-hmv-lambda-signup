# fiap-hmv-lambda-signup
[![Generic badge](https://img.shields.io/badge/Linguagem-Python-orange.svg)](https://www.python.org/)

Projeto que expõe APIs para cadastrar os usuários na aplicação do HMV. O serviço está exposto por um AWS Lambda.

Para instalar as dependências:
> pip install -r requirements.txt

### :exclamation: Atualizar o código no lambda
Execute o comando abaixo para gerar o .zip e depois faça o upload no lambda pelo console da AWS
> zip -r hmv-signup.zip * -x ".git*" -x "README.md" -x coverage.xml -x "venv/*" -x ./package -x "tests/*" -x "test/*" -x Dockerfile -x docker-compose.yml -x ./examples -x functions.json -x package.json -x package-lock.json -x rede.yml

