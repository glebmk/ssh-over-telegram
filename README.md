telegram_ssh is a self-hosted telegram bot that enables working on your server via telegram.

Please, follow the provided instruction in order to set-up the bot.

#### Setting-up bot

Create personal bot:
1. Talk to BotFather and create a bot. You will need a token for your bot. 
For more instructions, look [here](https://core.telegram.org/bots#6-botfather).

Start bot code on the host of your choice:
1. Run `git clone https://github.com/glebmak/telegram_ssh.git`
1. Create `config` file and place it in the folder with repository. 
Find more instruction on this below.
1. Install all requirements needed to run the code `pip install -r requirements.py`
1. Start server `python server.py`. Note that files will be saved to the directory from which you run this command.

Talk to bot:
1. Send a `/start` message and you will receive the instructions on how to 
setup ssh connection between the bot and server.



#### About config file

Config file should contain three fields:
* tg_username: should be equal to your telegram username. 
For security reasons, your bot will answer to you only and 
this field is how bot knows who is it's only client.
* tg_bot_token: token provided to you by BotFather
* hostname: hostname of the server your bot should ssh into.

For the example, consult `config_example`. 
**Be careful not to post your config file anywhere as it will 
compromise your bot and potentially server.**
