"""Render a bilingual prayer timetable from verified source data."""
import argparse
from html import escape
import json
from pathlib import Path
import re
from urllib.parse import urlsplit

EVENTS = {
    "fajr": ("اذان صبح", "Fajr"),
    "sunrise": ("طلوع آفتاب", "Sunrise"),
    "dhuhr": ("اذان ظهر", "Dhuhr"),
    "asr": ("عصر", "Asr"),
    "sunset": ("غروب آفتاب", "Sunset"),
    "maghrib": ("اذان مغرب", "Maghrib"),
    "isha": ("عشاء", "Isha"),
    "midnight": ("نیمه‌شب شرعی", "Religious midnight"),
}
DIGITS = str.maketrans("0123456789", "۰۱۲۳۴۵۶۷۸۹")


def localized(fields, language):
    return escape(fields.get(language) or "—")


def render(data, template):
    values = {
        f"{field}_{language}": localized(data.get(field, {}), language)
        for field in ("city", "solar", "gregorian", "lunar", "note")
        for language in ("fa", "en")
    }
    rows = []
    for event, (fa, en) in EVENTS.items():
        time = data["times"].get(event) or "—"
        if time == "—" and event in {"asr", "isha", "midnight"}:
            continue
        if time != "—" and not re.fullmatch(r"(?:[01][0-9]|2[0-3]):[0-5][0-9]", time):
            raise ValueError(f"{event} requires a local time in HH:MM format")
        row_class = ' class="solar"' if event in {"sunrise", "sunset"} else ""
        rows.append(
            f'<tr{row_class}><th scope="row">{fa}<span class="en" lang="en">{en}</span></th>'
            f'<td><bdi dir="ltr">{time.translate(DIGITS)}</bdi>'
            f'<span class="en" lang="en">{time}</span></td></tr>'
        )
    sources = []
    for source in data["sources"]:
        url = urlsplit(source["url"])
        if url.scheme not in {"http", "https"} or not url.hostname:
            raise ValueError("Sources require HTTP or HTTPS URLs")
        fa = localized(source["label"], "fa")
        en = localized(source["label"], "en")
        sources.append(f'<li><a href="{escape(url.geturl())}">{fa} · <bdi lang="en">{en}</bdi></a></li>')
    values["rows"] = "\n".join(rows)
    values["sources"] = "\n".join(sources)
    return re.sub(r"\{\{(\w+)\}\}", lambda match: values[match[1]], template)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("data", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    template = Path(__file__).resolve().parents[1] / "assets/card.html"
    data = json.loads(args.data.read_text(encoding="utf-8"))
    args.output.write_text(render(data, template.read_text(encoding="utf-8")), encoding="utf-8")
