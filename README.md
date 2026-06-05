# Desafio Técnico — Cadastro de Pessoas
Esta é uma solução full-stack para o case de cadastro de pessoas, desenvolvida em uma arquitetura microsserviços no backend e uma interface simples no frontend.


# Arquitetura do Sistema

1. Frontend (React + TS + Vite): Interface de usuário com formulário simples de cadastro, máscaras nos inputs e validação.
2. Person Service (Backend - FastAPI): Microsserviço responsável pelas regras de cadastro de pessoas, validação dos inputs (CPF, data de nascimento e formato do nome) e integração de CEP.
3. Login Service (Backend - FastAPI): Microsserviço responsável pela geração e reserva de logins únicos.
4. Banco de Dados (PostgreSQL 16): Banco relacional com dois schemas isolados (`person_db` e `login_db`).

# Tecnologias Utilizadas

# Backend
- FastAPI: Framework Python para construção de APIs.
- Pydantic v2: Validação de esquemas e tipos de dados.
- SQLAlchemy: ORM para manipulação e mapeamento do banco de dados.
- Alembic: Gerenciamento de migrations do banco de dados.
- Httpx: Cliente HTTP assíncrono para comunicação entre serviços.

# Frontend
- React + TypeScript: Biblioteca para a construção da interface.
- Vite: Ferramenta de build rápida para o desenvolvimento frontend.

# Infraestrutura
- Docker & Docker Compose: Containerização e orquestração de todo o ambiente de desenvolvimento.

# Lógica de Geração e Garantia de Unicidade do Login

Para cumprir todos os requisitos do case, a geração do login segue o seguinte fluxo:

1. O nome é limpo de espaços extras, caracteres especiais ou acentos, sendo convertido para letras minúsculas.
2. O nome é separado em primeiro nome e outros nomes
3. É aplicado 4 lógicas para geração de logins
  - primeiro nome + cada um dos outros nomes
  - primeiro nome + iniciais dos outros
  - primeiro nome + complmento dos outros
  - iniciais dos primeiros nomes + último sobrenome
4. As funções `add` e `completa_login` servem para controlar repetições, tamanho e preenchimento usando `itertools.cycle` com as letras dos nomes da pessoa.
5. Retorna uma lista de candidatos a login

# Regras de Validação Implementadas

# Nome Completo
- Obrigatório.
- Apenas letras de `A-Z` (sem caracteres especiais, til, cedilhas ou acentos).
- Espaços nas extremidades são removidos.
- É obrigatório informar pelo menos nome e sobrenome (mínimo de 2 nomes).

# CPF (Documento Escolhido)
- Obrigatório.
- Remoção automática de pontuações (`.` e `-`) para persistência limpa de 11 dígitos.
- Validação matemática completa utilizando o algoritmo oficial da Receita Federal (validação do primeiro e do segundo dígito verificador).
- Bloqueio automático de sequências inválidas conhecidas (como `111.111.111-11`).

# E-mail
- Obrigatório.
- Validação estrutural pelo Pydantic (`EmailStr`).

# Data de Nascimento
- Obrigatório.
- Conversão segura para objeto de data.
- Impedimento de inserção de datas no futuro (limite máximo igual a `date.today()`).

# CEP e Endereço
- O CEP limpa caracteres especiais e valida se possui exatamente 8 dígitos.
- Autopreenchimento de Endereço, Cidade, Bairro e Estado consultando de forma assíncrona a API pública do ViaCEP.
- Permissão para o usuário inserir o número da residência.

# Como Executar o Projeto

A maneira recomendada de executar todo o ecossistema é usando o Docker Compose.

# Pré-requisitos
- [Docker](https://www.docker.com/products/docker-desktop/) instalado.

# Executar o Docker Compose
Na raiz do projeto, execute o comando abaixo para construir e iniciar todos os serviços (Frontend, Backend Services e PostgreSQL):

`  docker compose up --build  `

Os seguintes serviços estarão disponíveis:
- Frontend: `http://localhost:5173`
- Person Service (API): `http://localhost:8000`
- Person Service (API DOCS): `http://localhost:8000/docs`
- Login Service (API): `http://localhost:8001`
- Login Service (API DOCS): `http://localhost:8001/docs`
- Banco de Dados (Postgres): Porta `5432`
