# Solar Split

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-orange.svg)](https://hacs.xyz/docs/publish/start)

A Home Assistant integration to split sensor readings (e.g., power or energy) between multiple sources like solar and grid.

## Features

- Calculates how much energy or power comes from solar vs grid
- Works with any sensor
- Compatible with Energy Dashboard

## Installation

### Via HACS (Custom Repository)

1. Go to **HACS → Integrations → 3-dot menu → Custom repositories**
2. Add this repo: `https://github.com/yourusername/solar_split`
3. Select category: **Integration**
4. Find and install "Solar Split" in HACS

### Manual Installation

1. Copy `solar_split/` into `custom_components/` directory in Home Assistant config.
2. Restart Home Assistant.

## Configuration

This integration is set up via the Home Assistant UI:

1. Go to **Settings → Devices & Services**
2. Click **+ Add Integration**
3. Search for **Solar Split**
4. Follow the prompts
