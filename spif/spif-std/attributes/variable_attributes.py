
from typing import Optional, Union
import datetime

from pydantic import Field, BaseModel
from vocal.schema_types import Numeric

from ..constants import *


class VariableAttributes(BaseModel):
    """
    Model for SPIF variable attributes.
    Recommended attributes are marked as Optional

    """
    class Config:
        # Configuration options here
        title = 'SPIF Variable Attributes'

    FillValue: Union[int, float] = Field(
        description='The prefill/missing data value',
        alias='_FillValue',
        example=-9999
    )

    coverage_content_type: str = Field(
        description=f'ISO 19115-1 code. One of {", ".join(COVERAGE_CONTENT_TYPES)}',
        example=COVERAGE_CONTENT_TYPES[2]
    )

    long_name: str = Field(
        description='A longer, descriptive name for the variable',
        example='Number of pixels across an image. If fixed size then will be number of pixels, if variable size then use _FillValue.'
    )

    units: str = Field(
        description='Valid UDUNITS unit.',
        example='m'
    )

    # Optional Attributes
    ancillary_variables: Optional[str] = Field(
        description='Names of any ancillary variables e.g. flags, uncertainties',
        example='resolution_error'
    )