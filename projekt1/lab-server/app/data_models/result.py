from pydantic import BaseModel, create_model
from typing import List

import app.constants as constants

# ResultItem: day + pola P1_ENTRIES, P1_REJECTED, P1_MAX_OCCUPANCY, P1_REVENUE, ..., P5_REVENUE
ResultItem = create_model(
    'ResultItem',
    day=(int, ...),
    **{name: (float, ...) for name in constants.AGGREGATES},
)


class Result(BaseModel):
    ip_addr: str
    port: int
    indeks: int
    aggregates: List[ResultItem]
