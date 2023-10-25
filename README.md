# [Minesweeper Telegram bot](https://t.me/GameMinesweeperBot)
## Overview
Last prod deploy: 30.08.2023<br>
**Despite production version exists, it is highly recommended to run code locally due to long deploy cycles.**
The project demonstrates the first try of fully object oriented architecture, taking advantage of some design patterns. 
Bot fully supports English and Russian languages.
Tests were written to demonstrate knowledge of pytest parametrize and unittest MagicMock.
<br>
Bot has a small CI building a docker image and running tests.
<br>
## Run bot
### Without docker:
Create .env file with field TOKEN=<your_token> and start main.py
### With docker:
```
docker build --build-arg TOKEN="<your_token>" -t bot .
docker run -t bot
```
## Extras
**Known prod issues:**
* Statistics is not showed if you have played zero games. It is fixed in the code, but not deployed.<br>

Architecture inspired by [Yandex Backend School](https://www.youtube.com/watch?v=Qw-Wj6NZelQ&t=2780s) <br>
Docker and CI ideas inspired by [Tinkoff Backend Academy](https://fintech.tinkoff.ru/academy/backend/)