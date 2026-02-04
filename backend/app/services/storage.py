from __future__ import annotations

from dataclasses import dataclass
from typing import Optional
import pandas as pd


@dataclass
class DataStore:
    prices: Optional[pd.DataFrame] = None


store = DataStore()
