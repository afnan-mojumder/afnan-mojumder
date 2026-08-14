#!/usr/bin/env python3
"""
render_heatmap_svg.py
Renders data/contributions.json as a classic 53-week x 7-day calendar of
rounded boxes, using a GitHub-ish green ramp. Reveals once with a diagonal
line-after-line slide-down (CSS keyframes that play on load, then freeze —
no looping), and adds a legend + stats footer.

No JavaScript — the animation is pure CSS keyframes embedded in <style>
inside the SVG, which GitHub renders fine for <img>-embedded SVGs.
"""
import json
import os
from datetime import date, datetime, timedelta

DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "contributions.json")
OUT_PATH = os.path.join(os.path.dirname(__file__), "..", "contrib-heatmap.svg")

# level 0 (none) -> level 4 (most)
PALETTE = ["#161b22", "#0e4429", "#006d32", "#26a641", "#39d353"]
BG = "#0d1117"
TEXT = "#8b949e"
TEXT_BRIGHT = "#c9d1d9"

CELL = 11
GAP = 3
STEP = CELL + GAP
LEFT_PAD = 30       # room for day labels
TOP_PAD = 34         # room for month labels
RIGHT_PAD = 16
BOTTOM_PAD = 46      # room for legend + stats line

DAY_LABELS = {1: "Mon", 3: "Wed", 5: "Fri"}  # sparse labels like GitHub


def load_data():
    with open(DATA_PATH) as f:
        return json.load(f)


def build_weeks(days):
    """Group the flat day list into calendar weeks (columns), Sunday-start,
    matching GitHub's own layout."""
    by_date = {d["date"]: d for d in days}
    if not days:
        return []

    last_date = datetime.strptime(days[-1]["date"], "%Y-%m-%d").date()
    # Walk back to the most recent Saturday (end of a week column) then
    # forward 53 weeks worth of Sundays to find the grid start.
    end = last_date
    while end.weekday() != 5:  # 5 = Saturday
        end += timedelta(days=1)
    start = end - timedelta(weeks=52, days=6)
    while start.weekday() != 6:  # 6 = Sunday
        start -= timedelta(days=1)

    weeks = []
    cur = start
    week = []
    while cur <= end:
        key = cur.isoformat()
        cell = by_date.get(key, {"date": key, "count": 0, "level": 0})
        week.append(cell)
        if cur.weekday() == 6 and week and len(week) == 1:
            pass
        if cur.weekday() == 5:  # Saturday closes the week
            weeks.append(week)
            week = []
        cur += timedelta(days=1)
    if week:
        weeks.append(week)
    return weeks


def month_label_positions(weeks):
    """Return {week_index: 'Jan'} for the first week each month appears in."""
    labels = {}
    seen_months = set()
    for i, week in enumerate(weeks):
        for cell in week:
            d = datetime.strptime(cell["date"], "%Y-%m-%d").date()
            key = (d.year, d.month)
            if key not in seen_months and d.day <= 7:
                seen_months.add(key)
                labels[i] = d.strftime("%b")
                break
    return labels


def render(payload):
    days = payload["days"]
    stats = payload["stats"]
    username = payload["username"]
    weeks = build_weeks(days)
    n_weeks = len(weeks)

    width = LEFT_PAD + n_weeks * STEP + RIGHT_PAD
    height = TOP_PAD + 7 * STEP + BOTTOM_PAD

    svg_parts = []
    svg_parts.append(
        f'<svg viewBox="0 0 {width} {height}" width="{width}" height="{height}" '
        f'xmlns="http://www.w3.org/2000/svg" font-family="-apple-system, Segoe UI, Helvetica, Arial, sans-serif">'
    )

    # Background
    svg_parts.append(f'<rect x="0" y="0" width="{width}" height="{height}" rx="8" fill="{BG}"/>')

    # Style block: diagonal reveal, then freeze. Each cell's delay is a
    # function of (week_index + day_index) so the wipe travels diagonally.
    svg_parts.append("<style>")
    svg_parts.append(
        ".cell{opacity:0;animation:reveal .5s ease-out forwards;}"
        "@keyframes reveal{from{opacity:0;transform:scale(.4);}to{opacity:1;transform:scale(1);}}"
        ".cell{transform-box:fill-box;transform-origin:center;}"
    )
    svg_parts.append("</style>")

    # Month labels
    for week_idx, label in month_label_positions(weeks).items():
        x = LEFT_PAD + week_idx * STEP
        svg_parts.append(f'<text x="{x}" y="{TOP_PAD - 10}" font-size="10" fill="{TEXT}">{label}</text>')

    # Day-of-week labels
    for dow, label in DAY_LABELS.items():
        y = TOP_PAD + dow * STEP + CELL - 1
        svg_parts.append(f'<text x="0" y="{y}" font-size="9" fill="{TEXT}">{label}</text>')

    # Cells, diagonal delay
    max_delay_steps = n_weeks + 6
    for wi, week in enumerate(weeks):
        for di in range(7):
            if di >= len(week):
                continue
            cell = week[di]
            level = min(max(cell.get("level", 0), 0), 4)
            color = PALETTE[level]
            x = LEFT_PAD + wi * STEP
            y = TOP_PAD + di * STEP
            delay = (wi + di) * (0.9 / max_delay_steps)
            title = f'{cell["count"]} contribution{"s" if cell["count"] != 1 else ""} on {cell["date"]}'
            svg_parts.append(
                f'<rect class="cell" x="{x}" y="{y}" width="{CELL}" height="{CELL}" rx="2.5" ry="2.5" '
                f'fill="{color}" style="animation-delay:{delay:.3f}s"><title>{title}</title></rect>'
            )

    # Legend (bottom-left): Less [boxes] More
    legend_y = height - BOTTOM_PAD + 20
    lx = LEFT_PAD
    svg_parts.append(f'<text x="{lx}" y="{legend_y + 8}" font-size="9" fill="{TEXT}">Less</text>')
    lx += 26
    for lvl, color in enumerate(PALETTE):
        svg_parts.append(f'<rect x="{lx}" y="{legend_y}" width="{CELL}" height="{CELL}" rx="2.5" fill="{color}"/>')
        lx += STEP
    svg_parts.append(f'<text x="{lx + 4}" y="{legend_y + 8}" font-size="9" fill="{TEXT}">More</text>')

    # Stats footer (bottom-right)
    total = stats["total_last_year"]
    streak = stats["longest_streak"]
    footer = f'{total} contribution{"s" if total != 1 else ""} in the last year · longest streak {streak} day{"s" if streak != 1 else ""}'
    svg_parts.append(
        f'<text x="{width - RIGHT_PAD}" y="{legend_y + 8}" font-size="9" fill="{TEXT_BRIGHT}" text-anchor="end">{footer}</text>'
    )

    svg_parts.append("</svg>")
    return "\n".join(svg_parts)


def main():
    payload = load_data()
    svg = render(payload)
    with open(OUT_PATH, "w") as f:
        f.write(svg)
    print(f"Wrote {OUT_PATH}")


if __name__ == "__main__":
    main()
