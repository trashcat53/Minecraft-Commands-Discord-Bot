Simple Python script that allows a server owner to easily control simple minecraft server actions from a bot in their discord server.

**Capabilities:**
- Whitelist users
- Manually start server
- Manually restart server

I have only needed to use these three functions fo rmy own server. If you require a function is missing from the list please submit a pull request.


**HOW TO USE: (Linux servers only)**
1) Follow steps 1-3 of erdbeerbaerlp's guide to set up a discord bot: [https://erdbeerbaerlp.de/projects/discord-integration/quick-setup](url)
   If you want the additional functions of erdbeerbaerlp's Discord Integrations mod follow steps 1-5
   link to Discord Integrations mod: [https://modrinth.com/mod/dcintegration](url)
3) Download serverbot.py and place the file in your minecraft server's directory
4) In your terminal run the following commands (installation commands will vary slightly depending on your linux distrobution. The one used here is for Debian):
```
chmod +x serverbot.sh
sudo apt install -y python3 pip
pip install discord.py aiohttp
```
5) Open serverbot.py and follow instructions 1-11 located in ***SETUP VARIABLES***
6) Manually start your server by running the following command in the directory of your server:
```
./serverbot.sh
```
