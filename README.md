# 1. BOT Luamod

The "BOT Luamod" is a Discord bot whose main function is to moderate a server, provide a logging system for monitoring, and offer features for members and developers, including AI commands (chatbot). By cloning the repository, you can enter "developer mode," control the AI, and access a local REST API, provided you configure these elements correctly.

# 2. Features

I. General

- ping - Displays the bot's latency.

- help - Displays the list of commands.

- avatar < member > - Displays a member's avatar.

- userinfo < member > - Displays user information.

- serverinfo - Displays server information.

- botinfo - Displays bot profile information.

II. Moderators

- warn < member > < reason > - Warns a user.

- unwarn < member > - Removes all warnings from the user.

- warnings < member > - Views the number and reason(s) of warnings for a user.

- warninglist - Views the user(s) warned and the number of warnings each has.

- clear < quantity > - Deletes chat messages.

- purge < member > < quantity > - Deletes a member's chat messages.

- slow < seconds > - Activates slow mode in the channel.

- lock - Locks a channel.

- unlock - Unlocks a locked channel.

- lockdown - Locks all channels.

- unlockdown - Unlocks all channels.

- mute < member > < minutes > - Temporarily mutes a member.

- unmute < member > - Removes a member's mute.

- kick < member > - Kicks a member from the server.

- ban < member > - Bans a member from the server.

- unban < ID > - Removes a ban from a user by ID.

- tempban < member > < quantity > - Bans a member from the server for a period of time.

- softban < member > - Bans a member from the server for one second to clear messages.

- setlog < channel > - Sets a channel to receive server action logs.

III. Developers

- restart - Restarts the bot.

- toswitchoff - Turns off the bot.

- log - Views the bot's log history.

- clearlog - Clears the bot's log history.

- reloadcog < cog > - Reloads a specific cog.

- debug - Displays general and technical information about the bot.

IV. AI

- on - Turns on AI chat.

- off - Turns off AI chat.

# 3. Simple API

Simple API built with FastAPI to view the bot's overall status. Localhost.

# 3.5. REST API

Educational and didactic REST API separate from the simple API and also built with FastAPI. Localhost.

- GET - View information.
- POST - Create information.
- PUT - Update information.
- DELETE - Delete information.

# 4. Technologies

- Language: Python
- Framework: FastAPI
- Library: Discord.py & Others
- Environment: Linux
- Files Format: Json & Yaml
- Code Versioning: Git
- Containerization: Docker
- CI/CD: Github Actions

# 5. Clone the Repository

- Bash

git clone https://github.com/jose-techcode/BOT_Luamod

# 6. Project Folder

- Bash

cd BOT_Luamod

# 7. Install Dependencies

pip install -r requirements.txt

# 8. Setting Environment Variables

Create a file called .env in the project root and add your bot token:

DISCORD_TOKEN=your_token

In the same .env file, if you're creating specific commands for only the bot developer to use, add:

DEV_ID=your_id

Also, in the same .env file, if you're creating specific commands for using the bot's AI, add:

API_KEY_OPEN_ROUTER=your_api_key

These files should not be uploaded to Github, as they contain sensitive information. Therefore, they should be included in .gitignore.

# 9. Running the Project

python bot.py

# 10. Running in Docker (lowercase)

I. Building the Image (lowercase)

docker build -t bot_luamod .

II. Running the Container (lowercase)

docker run -it --name container_bot_luamod bot_luamod

# 11. Contribution

Feel free to open Issues or submit Pull Requests.

# 12. License

This project is licensed under the AGPL license.

# 13. Notes

In the future, a SQL database may be added.