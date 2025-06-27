# 1. Bot Lua

O "Bot Lua" é um bot de discord em que a sua atribuição principal é moderar um servidor, bem como também ter algumas funcionalidades para membros comuns e desenvolvedores.

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

# 3. Tecnologias

- Linguagem: Python
- Biblioteca: Discord.py
- Ambiente: Linux
- Banco de dados/formato de arquivo: Json
- Versionamento de código: Git
- Containerização: Docker

# 4. Clone do Repositório

- Bash

Clone o repositório

git clone https://github.com/jose-techcode/Bot_Lua

# 5. Pasta do Projeto

cd projeto_lua

# 6. Instalação de Dependências

pip install -r requirements.txt

# 7. Configuração de Variáveis de Ambiente

Crie um arquivo chamado .env na raiz do projeto e adicione seu token do bot:

DISCORD_TOKEN=seu_token

No mesmo arquivo .env, se for criar comandos específicos para somente o desenvolvedor do bot usar, adicione:

DEV_ID=seu_id

Esses arquivos não devem ser enviados para o Github, pois contém informações sensíveis. Então, devem ser incluídos no .gitignore.

# 8. Execução do Projeto

python bot.py

# 9. Rodar em Docker

I. Build da Imagem

docker build -t projeto_lua .

II. Rodar o Container

docker run -it --name lua_bot projeto_lua

# 10. Contribuição

Sinta-se livre para abrir Issues, sugerir melhorias ou enviar Pull Requests.

# 11. Licença

Este projeto está licenciado sob a licença AGPL.
