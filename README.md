# parse_royal_bot

Telegram Bot for parsing chats and customers:
t.me/parse_royal_bot

## Installing using Github

```shell
git clone https://github.com/KirillDrago/parse_royal_bot.git
python3 -m venv venv
source venv/bin/activate (Linux and macOS) or venv\Scripts\activate (Windows)
pip install -r requirements.txt
```
Enter your phone number in the "PHONE" variable


```shell
python3 run main.py
Please enter your phone (or bot token):  <your phone>
Please enter the code you received: <your code from Telegram>
```

## Troubleshooting
If you have:
```shell
ValueError: Could not find the input entity for PeerUser(user_id) (PeerUser). 
```
- just rerun main.py
