"""
Quantiphyse - Widget for data clustering using the Supervoxel method

Copyright (c) 2013-2020 University of Oxford

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

from PySide2 import QtGui, QtCore, QtWidgets

from quantiphyse.gui.widgets import QpWidget, TitleWidget, Citation, OverlayCombo, RoiCombo, NumericOption

from .process import SupervoxelsProcess

CITE_TITLE = "maskSLIC: Regional Superpixel Generation with Application to Local Pathology Characterisation in Medical Images"
CITE_AUTHOR = "Benjamin Irving"
CITE_JOURNAL = "https://arxiv.org/abs/1606.09518v2 (2017)"

class PerfSlicWidget(QpWidget):
    """
    Generates supervoxels using SLIC method
    """
    def __init__(self, **kwargs):
        super(PerfSlicWidget, self).__init__(name="Super Voxels", icon="sv", 
                                             desc="Generate supervoxel clusters", 
                                             group="Clustering", **kwargs)
        
    def init_ui(self):
        layout = QtWidgets.QVBoxLayout()
        self.setLayout(layout)

        title = TitleWidget(self, "Supervoxel Generation", help="sv")
        layout.addWidget(title)
        
        cite = Citation(CITE_TITLE, CITE_AUTHOR, CITE_JOURNAL)
        layout.addWidget(cite)

        hbox = QtWidgets.QHBoxLayout()
        optbox = QtWidgets.QGroupBox()
        optbox.setTitle("Options")
        grid = QtWidgets.QGridLayout()
        optbox.setLayout(grid)
        
        grid.addWidget(QtWidgets.QLabel("Data"), 0, 0)
        self.ovl = OverlayCombo(self.ivm)
        self.ovl.currentIndexChanged.connect(self._data_changed)
        grid.addWidget(self.ovl, 0, 1)
        grid.addWidget(QtWidgets.QLabel("ROI"), 1, 0)
        self.roi = RoiCombo(self.ivm)
        grid.addWidget(self.roi, 1, 1)

        self.n_comp = NumericOption("Number of components", grid, 2, minval=1, maxval=3, default=3, intonly=True)
        self.compactness = NumericOption("Compactness", grid, 3, minval=0.01, maxval=1, step=0.05, default=0.1, intonly=False)
        self.sigma = NumericOption("Smoothing", grid, 4, minval=0, maxval=5, step=0.1, default=1, intonly=False)
        self.n_supervoxels = NumericOption("Number of supervoxels", grid, 5, minval=2, maxval=1000, default=20, intonly=True)

        grid.addWidget(QtWidgets.QLabel("Output name"), 6, 0)
        self.output_name = QtWidgets.QLineEdit("supervoxels")
        grid.addWidget(self.output_name, 6, 1)

        self.gen_btn = QtWidgets.QPushButton('Generate', self)
        self.gen_btn.clicked.connect(self._generate)
        grid.addWidget(self.gen_btn, 7, 0)
        hbox.addWidget(optbox)
        hbox.addStretch(1)
        layout.addLayout(hbox)

        layout.addStretch(1)

    def _data_changed(self, _):
        name = self.ovl.currentText()
        if name:
            ovl = self.ivm.data[name]
            self.n_comp.label.setVisible(ovl.nvols > 1)
            self.n_comp.spin.setVisible(ovl.nvols > 1)

    def batch_options(self):
        options = {
            "data" : self.ovl.currentText(),
            "roi" : self.roi.currentText(),
            "n-components" : self.n_comp.spin.value(),
            "compactness" : self.compactness.spin.value(),
            "sigma" : self.sigma.spin.value(),
            "n-supervoxels" :  self.n_supervoxels.spin.value(),
            "output-name" :  self.output_name.text() 
        }
        return "Supervoxels", options

    def _generate(self):
        process = SupervoxelsProcess(self.ivm, sync=True)
        process.run(self.batch_options()[1])
