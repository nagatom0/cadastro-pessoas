# Como Executar o Projeto

# Pré-requisitos
A maneira recomendada de executar todo o projeto é usando o Docker Compose.
- [Docker](https://www.docker.com/products/docker-desktop/) instalado.


# Executar o Docker Compose
Na pasta raiz do projeto, execute o comando abaixo para construir e iniciar todos os serviços:

`  docker compose up --build  `

Os seguintes serviços estarão disponíveis:
- Frontend: `http://localhost:5173`
- Person Service (API): `http://localhost:8000`
- Person Service (API DOCS): `http://localhost:8000/docs`
- Login Service (API): `http://localhost:8001`
- Login Service (API DOCS): `http://localhost:8001/docs`
- Banco de Dados (Postgres): Porta `5432`

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
