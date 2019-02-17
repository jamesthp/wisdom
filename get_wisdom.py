#!/usr/bin/env python

import os
import sys

_LAUNCH_DIR = os.path.abspath(os.path.dirname(__file__))
script_loc = os.path.join(_LAUNCH_DIR, 'python')
if not script_loc in sys.path:
    sys.path.append(script_loc)

import wisdom_ui

wisdom_ui.run_get_wisdom()
