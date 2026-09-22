# Patttttern

Generates pattern SVG and PDF files.

## Setup

Install dependencies:

```bash
pip install svgwrite python-dotenv
```

## Run Guide

Always run from the project root, using `run.py` — it finds pattern scripts
for you, so you don't need to remember `python -m package.module` paths.

Render everything:

```bash
python run.py
```

Render just one piece — by name, if it's unambiguous:

```bash
python run.py front
```

Or by path/dotted module, when the name alone is ambiguous (there are
several `front.py` files) or you just want to be explicit:

```bash
python run.py aldrich_close_fitting_bodice/base/front.py
python run.py aldrich_close_fitting_bodice.base.front
```

Render several at once:

```bash
python run.py front back
```

See every available target:

```bash
python run.py --list
```

If a name matches more than one target, `run.py` lists the matches so you
can be more specific (e.g. `no_dart_flare_shorts/front` instead of `front`).

## Measurement profiles

Body measurements live in `utils/profiles/<name>.json`, one file per person.
`utils/measurements.py` loads the profile named by the `PATTERN_PROFILE`
environment variable (default `"default"`).

Set which profile to use by default by copying `.env.example` to `.env`
and editing `PATTERN_PROFILE` — `.env` is gitignored, so it's your local
setting only. It can still be overridden per command with `--profile`:

```bash
python run.py --profile <name>
python run.py front --profile <name>
```

Add a new person by copying `utils/profiles/default.json` to
`utils/profiles/<name>.json` and editing the values.

## Scale for Autodesk Fusion 360

After importing the generated svg, scale by `3.77957517575`.