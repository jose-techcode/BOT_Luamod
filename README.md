# 1. Projeto Lua

O "Projeto Lua" é um bot de discord em que a sua atribuição principal é moderar um servidor, bem como também ter algumas funcionalidades para membros comuns.

# 2. Funcionalidades

I. Membros comuns
- !help
- !lua
- !avatar
- !info
- !infoserver

II. Moderadores
- !apagar (quantidade)
- !lentidao (quantidade em segundos)
- !silenciar (membro) (quantidade em segundos)
- !dessilenciar (membro)
- !expulsar (membro)
- !banir (membro)
- !desbanir (ID do membro)
- !dm (membro) (mensagem)

# 3. Tecnologias

- Linguagem: Python
- Biblioteca: Discord.py
- Ambiente: Linux
- Versionamento de código: Git
- Containerização: Docker

# 4. Clone do Repositório

- Bash

Clone o repositório
git clone
link

# 5. Pasta do Projeto

pasta

# 6. Instalação de Dependências

pip install -r requirements.txt

# 7. Execução do Projeto

python bot.py

# 8. Rodar em Docker

I. Build da Imagem
- docker build -t projeto_lua .

II. Rodar o Container
- docker run -d --name lua_bot projeto_lua