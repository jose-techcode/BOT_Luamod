# 1. Projeto Lua

O "Projeto Lua" é um bot de discord em que a sua atribuição principal é moderar um servidor, bem como também ter algumas funcionalidades para membros comuns.

# 2. Funcionalidades

I. Membros comuns

- !help — Mostra a lista de comandos.

- !lua — Mostra informações sobre o bot.

- !avatar — Exibe o avatar de um membro.

- !info — Mostra informações do seu perfil.

- !infoserver — Exibe informações do servidor.

II. Moderadores
- !apagar (quantidade) — Apaga mensagens do chat.

- !lentidao (segundos) — Ativa o modo lento no canal.

- !silenciar (membro) (segundos) — Silencia um membro temporariamente.

- !dessilenciar (membro) — Remove o silêncio de um membro.

- !expulsar (membro) — Expulsa um membro do servidor.

- !banir (membro) — Bane um membro do servidor.

- !desbanir (ID) — Remove o banimento de um usuário pelo ID.

- !dm (membro) (mensagem) — Envia uma mensagem privada para um membro.

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
