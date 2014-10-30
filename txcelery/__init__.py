#!/usr/bin/env python
from pkg_resources import get_distribution

import defer

__version__ = get_distribution('txcelery').version
