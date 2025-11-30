"""
The **Ovi Board** displays Ovechkin goal count, expected goals, and points.
"""
import json
from pathlib import Path

# Expose metadata as module variables (backward compatibility)
__plugin_id__ = "ovi_goal_tracker_board"
__version__ = "2025.11.05"
__description__ = "Ovi Goal and Point Tracker Board"
__board_name__ = "Ovi Goals"
__author__ = "tsmooth3"
__requirements__ = ["requests"]
