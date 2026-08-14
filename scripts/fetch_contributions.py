#!/usr/bin/env python3
"""
fetch_contributions.py
Fetches the public contribution calendar for a GitHub user with no auth
and no GraphQL token, by scraping the same HTML fragment GitHub's own
profile page loads asynchronously: /users/<username>/contributions

Writes data/contributions.json with:
  - raw daily counts + levels
  - current streak, longest streak
  - best single day
  - monthly totals
  - total contributions in the last year
"""
import json
import os
import re
import sys
from datetime import datetime, date, timezone
from collections import defaultdict

import requests
from bs4 import BeautifulSoup

USERNAME = os.environ.get("GH_USERNAME", "afnan-mojumder")
URL = f"https://github.com/users/{USERNAME}/contributions"
OUT_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "contributions.json")

HEADERS = {
    # A normal browser UA avoids being served a stripped-down fragment
    "User-Agent": "Mozilla/5.0 (compatible; profile-readme-bot/1.0)",
    "Accept": "text/html",
}


def fetch_html(url: str) -> str:
    resp = requests.get(url, headers=HEADERS, timeout=20)
    resp.raise_for_status()
    return resp.text


def parse_calendar(html: str):
    soup = BeautifulSoup(html, "html.parser")

    # GitHub renders each day as a <td> (older markup) or an <rect>/<td> with
    # class "ContributionCalendar-day" carrying data-date, data-level (0-4)
    # and title text with the count. We handle both tag shapes defensively.
    day_cells = soup.select("td.ContributionCalendar-day, rect.ContributionCalendar-day")

    if not day_cells:
        # Fallback: some responses wrap cells differently; try a broader match
        day_cells = soup.select("[data-date]")

    days = []
    for cell in day_cells:
        d = cell.get("data-date")
        if not d:
            continue
        level = cell.get("data-level")
        level = int(level) if level is not None else 0

        # Count comes from the tooltip text ("No contributions on ..." or
        # "N contributions on ..."). GitHub links the tooltip via
        # aria-label on the cell itself in recent markup, or via a
        # <tool-tip>/<span> sibling in older markup.
        label = cell.get("aria-label") or cell.get("title") or ""
        if not label:
            tip_id = cell.get("id")
            if tip_id:
                tip = soup.select_one(f'[for="{tip_id}"], tool-tip[for="{tip_id}"]')
                if tip:
                    label = tip.get_text(strip=True)

        match = re.search(r"([\d,]+)\s+contribution", label)
        if match:
            count = int(match.group(1).replace(",", ""))
        elif "No contributions" in label:
            count = 0
        else:
            count = 0

        days.append({"date": d, "count": count, "level": level})

    days.sort(key=lambda x: x["date"])
    return days


def compute_stats(days):
    total = sum(d["count"] for d in days)

    # Streaks
    longest = current = 0
    running = 0
    today = date.today()
    for d in days:
        if d["count"] > 0:
            running += 1
            longest = max(longest, running)
        else:
            running = 0
    # current streak = trailing run ending at the last day with data
    for d in reversed(days):
        if d["count"] > 0:
            current += 1
        else:
            break

    best_day = max(days, key=lambda x: x["count"], default=None)

    monthly = defaultdict(int)
    for d in days:
        month = d["date"][:7]  # YYYY-MM
        monthly[month] += d["count"]

    return {
        "total_last_year": total,
        "current_streak": current,
        "longest_streak": longest,
        "best_day": best_day,
        "monthly_totals": dict(sorted(monthly.items())),
    }


def main():
    html = fetch_html(URL)
    days = parse_calendar(html)

    if not days:
        print("WARNING: no day cells parsed — GitHub markup may have changed", file=sys.stderr)

    stats = compute_stats(days)

    payload = {
        "username": USERNAME,
        "generated_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "days": days,
        "stats": stats,
    }

    os.makedirs(os.path.dirname(OUT_PATH), exist_ok=True)
    with open(OUT_PATH, "w") as f:
        json.dump(payload, f, indent=2)

    print(f"Wrote {len(days)} days, {stats['total_last_year']} total contributions -> {OUT_PATH}")


if __name__ == "__main__":
    main()
