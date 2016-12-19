#!/usr/bin/env python
from pkg_resources import require

from . import defer

__version__ = require('txcelery-py3')[0].version
