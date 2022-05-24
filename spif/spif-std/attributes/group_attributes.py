
from typing import Optional
import datetime

from pydantic import Field, BaseModel

from ..constants import *


class GroupAttributes(BaseModel):
    """
    Model for SPIF group attributes.
    Recommended attributes are marked as Optional

    """
    class Config:
        title = 'SPIF Instrument Group Attributes'

    instrument_name: str = Field(
        description='Short name of instrument, may be the same as the group name.',
        example='Some instrument'
    )

    instrument_long_name: str = Field(
        description='Full descriptive name of instrument.',
        example='Fab_OAP X, ver 2. Electronics package Y.'
    )

    instrument_manufacturer: Optional[str] = Field(
        description='Name of instrument manufacturer.',
        example='Fab Instrument Manufacturing Ltd.'
    )

    instrument_serial_number: Optional[str] = Field(
        description='Instrument serial number or unique identifier.',
        example='SN123'
    )

    instrument_software: Optional[str] = Field(
        description='Name of data acquisition software interfacing with instrument. This may be installed on the instrument itself or separately on a remote data acquisition computer.',
        example='Instrument software name'
    )

    instrument_software_version: Optional[str] = Field(
        description='Version of data acquisition software.',
        example='v1.2.3'
    )

    instrument_firmware: Optional[str] = Field(
        description='Firmware installed on instrument.',
        example='Instrument firmware'
    )

    instrument_firmware_version: Optional[str] = Field(
        description='Version of Firmware installed on instrument.',
        example='v1.2.3'
    )

    platform: Optional[str] = Field(
        description=f'Name or description of platform the instrument is mounted on.',
        example=PLATFORM
    )

    raw_filenames: Optional[str] = Field(
        description=f'Raw data filename(s) used to generate the current instrument dataset.',
        example='02InstrFab19700101120000.csv, 02InstrFab19700101120530.csv'
    )

    references: Optional[str] = Field(
        description='Link to webpage, published paper, or other document reference describing instrument.',
        example='doi:1234'
    )

    comment: Optional[str] = Field(
        description='Any further notes about instrument, platform, location, orientation, etc.',
        example='This is a comment about the instrument.'
    )
