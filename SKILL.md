---
name: owqat-skill
description: Fetch current local prayer times, sunrise, sunset, and Gregorian, Solar Hijri, and lunar Hijri dates for a named city. Use for owqat-skill <city>, $owqat-skill <city>, or requests for a bilingual Persian and English اوقات شرعی card.
---

# City prayer times

- Parse the city after the skill name. Resolve its country and local date before searching, using the city's time zone. Ask only if the intended city cannot be resolved from context. Use a requested date if supplied.
- Browse for the city and exact date on every invocation. For Iran, start with [Makanet](https://makanet.ir/time/) or [Azanyar](https://azanyar.com/) and use the city page. For other countries prefer a local authority or a prayer timetable with a regionally appropriate calculation method. Verify the date of the row rather than relying on the page's “today” heading.
- Capture Fajr, Dhuhr, Maghrib, sunrise, and sunset as separate fields. Add Asr, Isha, and religious midnight when published. Leave unavailable values blank. Use local 24-hour times. Keep a coherent set of prayer times and cite all sources used in the card. Include the calculation method when verified, and note material discrepancies between consulted sources. For lunar Hijri, identify the calendar or provider. Verify Solar Hijri separately if the prayer source only carries Gregorian and lunar Hijri dates.
- Render the bilingual card using `python3 scripts/render.py DATA.json OUTPUT.html` with paths resolved relative to this skill for the script, and the user's workspace for input and output. The script uses `assets/card.html`. Save the card to the workspace output directory and link it in the reply.
- DATA.json is an object with `city` (localized city), `gregorian`, `solar`, `lunar` (localized dates, weekday included in Gregorian), optional `note` (localized method, discrepancies or omissions), `times` (object with keys `fajr`, `sunrise`, `dhuhr`, `asr`, `sunset`, `maghrib`, `isha`, `midnight` and HH:MM strings), and `sources` (array of objects with `url` and localized `label`). Each localized value is an object with `fa` and `en` text. Put the actual local calendar dates in both languages. Empty values produce a dash.
