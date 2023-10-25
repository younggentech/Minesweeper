# Minesweeper Telegram bot
Telegram prod version: [Bot](https://t.me/GameMinesweeperBot) <br>
The project demonstrates the first try of fully object oriented architecture, taking advantage of some design patterns. 
Bot fully supports English and Russian languages.
Tests were written to demonstrate knowledge of pytest parametrize and unittest MagicMock.
<br>
Bot has a small CI building a docker image and running tests.
<br>
**To run the bot, create .env file with field TOKEN=<your_token> and start main.py** <br>
**Known prod issues:**
* Statistics is not showed if you have played zero games. It is fixed in the code, but not deployed.