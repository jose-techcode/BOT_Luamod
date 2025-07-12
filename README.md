# 1. Bot Luamod

O "Bot Luamod" é um bot de discord em que a sua atribuição principal é moderar um servidor, bem como ter um sistema de logs para monitoramento, além de suas funcionalidades para membros comuns e desenvolvedores. Ao clonar o repositório, você pode entrar no "modo desenvolvedor", controlar a IA e ter acesso a uma API REST local, desde que configure essas partes corretamente.

# 2. Funcionalidades

I. Gerais

- ping - Mostra a latência do bot.

- ajuda - Mostra a lista de comandos.

- avatar < member > - Exibe o avatar de um membro.

- userinfo < member > - Mostra as informações do usuário.

- serverinfo - Exibe informações do servidor.

- botinfo - Mostra informações do perfil do bot.

II. Moderadores

- warn < member > < reason > - Avisa um usuário.

- unwarn < member > - Retira todos os avisos do usuário.

- warnings < member > - Vê a quantidade e o(s) motivo(s) do(s) aviso(s) de um usuário.

- warninglist - Vê o(s) usuário(s) avisado(s) e a quantidade de aviso(s) que cada um tem.

- clear < quantity > - Apaga mensagens do chat.

- slow < seconds > - Ativa o modo lento no canal.

- lock - Tranca um canal.

- unlock - Destranca um canal que estava trancado.

- mute < member > < minutos > - Silencia um membro temporariamente.

- unmute < member > - Remove o silêncio de um membro.

- kick < member > - Expulsa um membro do servidor.

- ban < member > - Bane um membro do servidor.

- unban < ID > - Remove o banimento de um usuário pelo ID.

- setlog < channel > - Define um canal para receber logs de ações do servidor.

III. Desenvolvedores

- restart - Reinicia o bot.

- toswitchoff - Desliga o bot.

- log - Vê o histórico de logs do bot.

- clearlog - Limpa o histórico de logs do bot.

- reloadcog < cog > - Recarrega uma cog específica.

- debug - Exibe informações gerais e técnicas do bot.

IV. IA

- on - Liga o chat da IA.

- off - Desliga o chat da IA.

# 3. API simples

API simples feita com FastAPI para ver o status geral do bot. 

# 3.5. API REST

API REST educativa e didática separada da API simples e feita com FastAPI também.

GET - Ver informações.
POST - Criar informações.
PUT - Atualizar informações.
DELETE - Deletar informações.

# 4. Tecnologias

- Linguagem: Python
- Framework: FastAPI
- Biblioteca: Discord.py
- Ambiente: Linux
- Formato de arquivo: Json
- Versionamento de código: Git
- Containerização: Docker

# 5. Clone do Repositório

- Bash

Clone o repositório

git clone https://github.com/jose-techcode/Bot_Lua

# 6. Pasta do Projeto

cd Bot_Lua

# 7. Instalação de Dependências

pip install -r requirements.txt

# 8. Configuração de Variáveis de Ambiente

Crie um arquivo chamado .env na raiz do projeto e adicione seu token do bot:

DISCORD_TOKEN=seu_token

No mesmo arquivo .env, se for criar comandos específicos para somente o desenvolvedor do bot usar, adicione:

DEV_ID=seu_id

Também, no mesmo arquivo .env, se for criar comandos específicos para usar a IA do bot, adicione:

API_KEY_OPEN_ROUTER=sua_api_key

Esses arquivos não devem ser enviados para o Github, pois contém informações sensíveis. Então, devem ser incluídos no .gitignore.

# 9. Execução do Projeto

python bot.py

# 10. Rodar em Docker

I. Build da Imagem

docker build -t Bot_Lua .

II. Rodar o Container

docker run -it --name lua_bot Bot_Lua

# 11. Contribuição

Sinta-se livre para abrir Issues, sugerir melhorias ou enviar Pull Requests.

# 12. Licença

Este projeto está licenciado sob a licença AGPL.

# 13. Observações

O sistema de warns do Bot Lua pode ser descontinuado.
