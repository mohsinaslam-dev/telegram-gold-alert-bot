"""Telegram price-alert bot: sends a message when a symbol crosses your levels."""
import argparse
import os
import time

import requests


def get_price(symbol):
    import yfinance as yf
    return float(yf.Ticker(symbol).fast_info["last_price"])


def check_levels(price, above, below, fired):
    """Return alert messages. `fired` is a set that stops repeat alerts until price re-arms."""
    msgs = []
    if above is not None and price >= above and "above" not in fired:
        fired.add("above")
        msgs.append(f"Price {price:.2f} is ABOVE your level {above:.2f}")
    if below is not None and price <= below and "below" not in fired:
        fired.add("below")
        msgs.append(f"Price {price:.2f} is BELOW your level {below:.2f}")
    if above is not None and price < above:
        fired.discard("above")
    if below is not None and price > below:
        fired.discard("below")
    return msgs


def send_telegram(token, chat_id, text):
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    r = requests.post(url, json={"chat_id": chat_id, "text": text}, timeout=15)
    r.raise_for_status()


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--symbol", default="GC=F", help="Yahoo Finance symbol (GC=F is gold futures)")
    p.add_argument("--above", type=float)
    p.add_argument("--below", type=float)
    p.add_argument("--interval", type=int, default=60, help="seconds between checks")
    p.add_argument("--once", action="store_true")
    p.add_argument("--dry-run", action="store_true", help="print instead of sending")
    a = p.parse_args()
    token, chat = os.environ.get("TELEGRAM_BOT_TOKEN"), os.environ.get("TELEGRAM_CHAT_ID")
    if not a.dry_run and not (token and chat):
        raise SystemExit("Set TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID (or use --dry-run)")
    fired = set()
    while True:
        price = get_price(a.symbol)
        print(f"{a.symbol}: {price:.2f}")
        for m in check_levels(price, a.above, a.below, fired):
            print("ALERT:", m) if a.dry_run else send_telegram(token, chat, m)
        if a.once:
            break
        time.sleep(a.interval)


if __name__ == "__main__":
    main()
