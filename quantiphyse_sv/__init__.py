"""
Quantiphyse - supervoxel clustering package

Copyright (c) 2013-2018 University of Oxford
"""

from .widgets import PerfSlicWidget
from .process import SupervoxelsProcess
from .tests import PerfSlicWidgetTest, SupervoxelsProcessTest

QP_MANIFEST = {
    "widgets" : [PerfSlicWidget],
    "widget-tests" : [PerfSlicWidgetTest,],
    "process-tests" : [SupervoxelsProcessTest,],
    "processes" : [SupervoxelsProcess],
}
