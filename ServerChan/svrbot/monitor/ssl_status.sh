#!/bin/bash

# ambition: check letsencrypt status
# location: crontab
# mode: change mode to 755
# reference: https://community.letsencrypt.org/t/it-there-a-command-to-show-how-many-days-certificate-you-have/11351/2

tg_bot_token=your-bot-token
chat_id=your-chat-id

domains=("example.com" "i.example.com")

for domain in "${domains[@]}"; do
    message=$(echo | openssl s_client -connect "${domain}":443 2>/dev/null | openssl x509 -noout -dates | grep -i "notafter" | cut -f 2 -d=)
    curl -s "https://api.telegram.org/bot${tg_bot_token}/sendMessage?chat_id=${chat_id}" --data-binary "&text='${domain}' is in valid after ${message}." >> /dev/null
done