# Telegram Gold Alert Bot

**Platform:** Telegram Bot API + Yahoo Finance

Sends a Telegram message when a price (default: gold futures) crosses your above/below level. Alerts fire once and re-arm when price moves back.

## Setup
```bash
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env    # then fill in your values
```
Environment variables: TELEGRAM_BOT_TOKEN (from @BotFather), TELEGRAM_CHAT_ID

Load them before running (for example `export $(grep -v '^#' .env | xargs)` on Linux/macOS, or set them in your shell on Windows).

## Usage
```bash
python app.py --symbol GC=F --above 2450 --below 2380 --interval 60
python app.py --above 2450 --once --dry-run
```
Use `--dry-run` where available to see what would happen without calling the real API.

## Tests
The core logic is covered by tests that need no internet or credentials:
```bash
pip install pytest && pytest
```

## License
MIT
