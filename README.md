# Lunchbot

Insbired by [https://github.com/hugovk/lunchbot](https://github.com/hugovk/lunchbot)

Checks what's available at the local lunch places and prints them to HipCHat.

## Setup

```bash
pipenv install
```

To post to HipChat, get a [token](https://developer.atlassian.com/hipchat/guide/hipchat-rest-api/api-access-tokens) (or from your local install) and save it in the `LUNCHBOT_TOKEN` environment variable (or .env file in project root).

## Configuration

Configure your environment variables to the .env file in project root. Lunchbot will read the .env file and use these values as defaults.

.env file
```bash
LUNCHBOT_TOKEN = "LUNCHBOT_TOKEN"
LUNCHBOT_TARGET = "LUNCHBOT_TARGET"
LUNCHBOT_HOST = "LUNCHBOT_HOST"
```

## Usage

```
lunchbot.py [-h] [-r ROOM] [-n] [-o HOST] [-t TOKEN]

optional arguments:
  -h, --help                show this help message and exit
  -r ROOM, --room ROOM      Send to this Hipchat room number 
                            instead of default one
  -n, --dry-run             Don't post to Hipchat
  -o HOST, --host HOST      Location of your self hosted hipchat
  -t TOKEN, --token TOKEN   HipChat token
```

```bash
# Just print out but don't post
python lunchbot.py --dry-run

# Post to default configured HipChat room
python lunchbot.py

# Post to different room with a different token
python lunchbot.py --room roomID --token TOKEN
```