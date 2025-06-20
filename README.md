# 1. Bot Lua

O "Bot Lua" é um bot de discord em que a sua atribuição principal é moderar um servidor, bem como também ter algumas funcionalidades para membros comuns.

# 2. Funcionalidades

I. Membros comuns

- help — Mostra a lista de comandos.

- lua — Mostra um easter egg do bot.

- avatar (pessoa) — Exibe o avatar de um membro.

- infobot — Mostra informações do seu perfil.

- infouser (pessoa) - Mostra as informações do usuário.

- infoserver — Exibe informações do servidor.

II. Moderadores

- avisar (usuário) (motivo) - Avisa um usuário.

- desavisar (usuário) - Retira todos os avisos do usuário.

- avisos (usuário) - Vê a quantidade e o(s) motivo(s) do(s) aviso(s) de um usuário.

- listaavisos - Vê o(s) usuário(s) avisado(s) e a quantidade de aviso(s) que cada um tem.

- apagar (quantidade) — Apaga mensagens do chat.

- lentear (segundos) — Ativa o modo lento no canal.

- trancar - Tranca um canal.

- destrancar - Destranca um canal que estava trancado.

- silenciar (membro) (minutos) — Silencia um membro temporariamente.

- dessilenciar (membro) — Remove o silêncio de um membro.

- expulsar (membro) — Expulsa um membro do servidor.

- banir (membro) — Bane um membro do servidor.

- desbanir (ID) — Remove o banimento de um usuário pelo ID.

III. Desenvolvedores

- reiniciar - Reinicia o bot.

- desligar - Desliga o bot.

- verlog - Vê o histórico de logs do bot.

- limparlog - Limpa o histórico de logs do bot.

# 3. Tecnologias

- Linguagem: Python
- Biblioteca: Discord.py
- Ambiente: Linux
- Banco De Dados: Json
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

No mesmo arquivo .env, se for criar comandos específicos para somente o desenvolvedor do bot usar, adicione:

DEV_ID=seu_id

Esses arquivos não devem ser enviados para o Github, pois contém informações sensíveis. Então, devem ser incluídos no .gitignore.

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
