# TGBot for analysing nginx log

## Requirements

**Python 3.5.3 or higher**.

```bash
pip install -r requirements.txt
```

## Configuration

### Nginx log format

```text
log_format cust_format '$remote_addr $http_x_forwarded_for $remote_user "$request"'
                        ' $status $connection "$http_referer" "$http_user_agent"'
                        ' "$time_local" $request_time';
```

Add above log format to the http block in `nginx.conf`, and then set the access_log like this:

```text
access_log /path/to/access.log cust_format;
```

### Apply a telegram bot token

[Create a bot and get a bot token](https://core.telegram.org/bots#3-how-do-i-create-a-bot)

```bash
export tg_bot_token=110201543:AAHdqTcvCH1vGWJxfSeofSAs0K5PALDsaw # invalid token
export CHAT_ID=12346783  # invalid chat id
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

## Monitor scripts usage

- ssh_login.sh

```bash
$ cd ServerChan
# no output
$ sudo cp svrbot/monitor/ssh_login.sh /etc/profile.d
# no output
$ sudo chmod 755 /etc/profile.d/ssh_login.sh
# no output
```

**NOTE:** For **zsh** users

append following script to `/etc/zsh/zprofile` file.

```shell
if [ -d /etc/profile.d ]; then
  for i in /etc/profile.d/*.sh; do
    if [ -r $i ]; then
      . $i
    fi
  done
  unset i
fi
```

Otherwise the ssh_login.sh will not be effective when zsh is your interactive shell.

Wanting to know more details about zsh initial: [zsh_initial_configuration](https://wiki.archlinux.org/index.php/Zsh#Initial_configuration)
