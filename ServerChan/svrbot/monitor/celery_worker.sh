#!/bin/bash

# goal: monitor celery workers status if it is online.
# location: crontab
# mode: change mode to 555

tg_bot_token=your-own-bot-token
chat_id=your-own-chat-id
flower_dashboard_url="127.0.0.1:5555/dashboard?json=1"
http_basic_auth=username:password

message=$(curl -fL -u ${http_basic_auth} "${flower_dashboard_url}" -o - | jq . - | grep -E "status|hostname" | tr -d " ,")
curl -s "https://api.telegram.org/bot${tg_bot_token}/sendMessage?chat_id=${chat_id}" --data-binary "&text=${message}"
