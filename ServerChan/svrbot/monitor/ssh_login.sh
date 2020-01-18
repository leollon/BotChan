#!/bin/bash

# ambition: monitor ssh login and send message to telegram.
# location: copy to /etc/profile.d/
# mode: change mode to 555

tg_bot_token=your-own-bot-token
chat_id=your-own-chat-id

message=$(hostname && TZ=UTC-8 date && who && w | awk 'BEGIN{OFS="\t"}{print $1,$8}')
curl -s "https://api.telegram.org/bot${tg_bot_token}/sendMessage?chat_id=${chat_id}" --data-binary "&text=${message}" >> /dev/null