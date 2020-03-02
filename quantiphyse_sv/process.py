"""
Quantiphyse - Analysis process for supervoxel clustering

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

import numpy as np

import maskslic

from quantiphyse.processes import Process

class SupervoxelsProcess(Process):
    """
    Process to run 3d supervoxel generation
    """
    PROCESS_NAME = "Supervoxels"

    def __init__(self, ivm, **kwargs):
        Process.__init__(self, ivm, **kwargs)

    def run(self, options):
        data = self.get_data(options)
        roi = self.get_roi(options, data.grid)
        n_supervoxels = options.pop('n-supervoxels')
        recompute_seeds = options.pop('recompute-seeds', True)
        seed_type = options.get('seed-type', 'nplace')
        output_name = options.pop('output-name', "supervoxels")
        ncomp = options.pop('n-components', 3)

        img = data.raw()
        slices = roi.get_bounding_box()
        img = img[slices]
        mask = roi.raw()[slices]

        labels = maskslic.perfslic(img, mask,
                                   n_supervoxels=n_supervoxels,
                                   spacing=data.grid.spacing,
                                   seed_type=seed_type,
                                   recompute_seeds=recompute_seeds,
                                   n_pca_components=ncomp,
                                   **options)
        newroi = np.zeros(data.grid.shape)
        newroi[slices] = np.array(labels, dtype=np.int) + 1
        self.ivm.add(newroi, grid=data.grid, name=output_name, roi=True, make_current=True)
