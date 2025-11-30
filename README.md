# Christmas Counter Downer Board

A **Christmas Countdown Board** for the [NHL LED Scoreboard](https://github.com/falkyre/nhl-led-scoreboard) that displays a countdown to Christmas Day.

This board shows:
- Days remaining until Christmas
- Hours, minutes, and seconds countdown
- Rotating Christmas-themed images (Christmas tree, candy cane)
- Special "Merry Christmas!" scrolling display on Christmas Day

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Configuration](#configuration)
- [Display Modes](#display-modes)
- [How It Works](#how-it-works)

---

## Features

- Real-time countdown to Christmas Day (December 25th)
- Displays days, hours, minutes, and seconds until Christmas
- Rotating Christmas images based on days remaining
- Special Christmas Day celebration mode with scrolling "MERRY CHRISTMAS!" message and sleigh graphic
- Automatically handles year rollover (counts down to next Christmas if past December 25th)
- Extended display time when "almost there" (less than 3 minutes remaining)
- Only displays when 101 days or fewer until Christmas

---

## Installation

1. Use the NHL Led Scoreboard's plugin manager python script to install:

   ```bash
   python plugins.py add https://github.com/tsmooth3/nls-plugin-christmas-board.git
   ```

2. Add `christmas_board` to your NHL-LED-Scoreboard's main configuration:

   ```bash
   nano config/config.json
   ```

   For example, to add it to the off day rotation:

   ```json
   "states": {
       "off_day": [
           "season_countdown",
           "christmas_board",
           "team_summary",
           "scoreticker",
           "clock"
       ]
   }
   ```

   **Note:** You must restart the scoreboard for changes to take effect.

---

## Configuration

To configure the Christmas Counter Downer board, copy the sample config to config.json and edit it:

```bash
cp config.sample.json config.json
nano config.json
```

**Note:** You must restart the scoreboard for changes to take effect.

### Config Fields

- `enabled` → Enable or disable the board (default: true)
- `displayPoints` → Configuration option (default: true)

---

## Display Modes

The board has two main display modes:

### Countdown Mode (Days 101 to 1)

When there are 1-101 days until Christmas, the board displays:
- Days remaining (e.g., "25 days")
- Time remaining in HH:MM:SS format
- Rotating Christmas images:
  - Christmas tree (when days % 3 == 0)
  - Candy cane (when days % 3 == 2)
  - Other image (when days % 3 == 1)
- "'TIL CHRISTMAS" text at the bottom

The board loops for 10 iterations (10 seconds) normally, or 180 iterations (3 minutes) when "almost there" (less than 180 seconds remaining).

### Christmas Day Mode

On December 25th, the board displays:
- Scrolling "MERRY CHRISTMAS!" text in green
- Sleigh graphic following the text
- Continuous scrolling animation for 15 seconds
- Special celebration display

---

## How It Works

1. The board calculates the time remaining until the next Christmas Day (December 25th)
2. It handles year rollover automatically - if the current date is after December 25th, it counts down to next year's Christmas
3. The countdown updates in real-time, showing:
   - Total days remaining
   - Hours, minutes, and seconds remaining
4. When there are 101 days or fewer until Christmas, the countdown display is shown
5. When less than 180 seconds (3 minutes) remain, the board enters "almost there" mode with extended display time
6. On Christmas Day itself, the board switches to celebration mode with scrolling text and graphics
7. The board uses the following fonts from your scoreboard configuration:
   - `font_large_2` for large text
   - `font_medium` for medium text
   - `font_xmas` for scrolling Christmas text

The board automatically updates the countdown each second and refreshes the display accordingly.
