from typing import List

import numpy as np

from ichor.atoms import ListOfAtoms
from ichor.make_sets.make_set_method import MakeSetMethod


class MinMax(MakeSetMethod):
    @classmethod
    def name(cls) -> str:
        return "min_max"

    @classmethod
    def get_npoints(cls, npoints: int, points: ListOfAtoms) -> int:
        return 2*len(points[0].features)

    def get_points(self, points: ListOfAtoms) -> List[int]:
        features = points.features
        if features.ndim > 2:
            features = features[0]
        elif features.ndim < 2:
            features = features[:, np.newaxis]

        return list(np.argmin(features, axis=0)) + list(
            np.argmax(features, axis=0)
        )
