# TGBot for analysing nginx log

## Requirements

**Python 3.5.3 or higher**.

```bash
pip install -r requirements.txt
```

## Configuration

### Nginx log format

```text
log_format cust_format '"$remote_addr" "$http_x_forwarded_for" "$remote_user" "$request"'
                        ' "$status" "$connection" "$http_referer" "$http_user_agent" "$time_local" "$request_time"';

```

Add above log format to the http block in `nginx.conf`, and then set the access_log like this:

```text
access_log /path/to/access.log cust_format;
```

### Apply a telegram bot token

[Create a bot and get a bot token](https://core.telegram.org/bots#3-how-do-i-create-a-bot)

```bash

export tg_bot_token=110201543:AAHdqTcvCH1vGWJxfSeofSAs0K5PALDsaw # invalid token
export POSTGRES_DB=set_postgres_db_used
export POSTGRES_USER=set_postgres_user
export POSTGRES_PASSWORD=set_postgres_password
export POSTGRES_HOST=localhost
export POSTGRES_PORT=5432

export REDIS_HOST=localhost
export REDIS_PORT=6379
```

### Start the bot

```bash
python start.py
```

### Set domain and the log file to be analysed

```bash
python commands.py --domain example.com --log_file /path/to/access.log
```

## Supported commands

- /ping
- /start
- /uptime
- /resource
- /load
- /last10mins example.com
- /last24hours example.com
- /today example.com
- /last7days example.com
- /last14days example.com
- /last30days example.com
