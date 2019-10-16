from typing import List

import numpy as np
import pandas as pd
import torch

from .slide import Slide

__all__ = ["Dataset"]


class Dataset(torch.utils.data.Dataset):
    """Dataset consisting of multiple instances of :class:`Slide`"""

    def __init__(self, slides: List[Slide], design: pd.DataFrame):
        self.design = design
        self.slides = slides

        self.observations = pd.DataFrame(
            dict(
                sample=np.repeat(range(len(slides)), [len(x) for x in slides]),
                idx=np.concatenate([range(len(x)) for x in slides]),
            )
        )

    def __len__(self):
        return len(self.observations)

    def __getitem__(self, idx):
        slide = self.observations["sample"].iloc[idx]
        return dict(
            **self.slides[slide].__getitem__(
                self.observations["idx"].iloc[idx]
            ),
            effects=torch.tensor(self.design[slide].values),
        )
