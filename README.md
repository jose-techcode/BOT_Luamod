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

- !lento (segundos) — Ativa o modo lento no canal.

- !trancar - Tranca um canal.

- !destrancar - Destranca um canal que estava trancado.

- !silenciar (membro) (minutos) — Silencia um membro temporariamente.

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
git clone https://github.com/jose-techcode/projeto_lua

# 5. Pasta do Projeto

cd projeto_lua

# 6. Instalação de Dependências

pip install -r requirements.txt

# 7. Configuração de Variáveis de Ambiente

Crie um arquivo chamado .env na raiz do projeto e adicione seu token do bot:

DISCORD_TOKEN=seu_token

Esse arquivo não deve ser enviado para o Git, pois contém informações sensíveis. Então, deve ser incluído no .gitignore.

# 8. Execução do Projeto

python bot.py

# 9. Rodar em Docker

I. Build da Imagem
- docker build -t projeto_lua .

II. Rodar o Container
- docker run -it --name lua_bot projeto_lua

# 10. Contribuição

Sinta-se livre para abrir Issues, sugerir melhorias ou enviar Pull Requests.

# 11. Licença

Este projeto está licenciado sob a licença AGPL.
