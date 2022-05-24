
from typing import Optional
import datetime

from pydantic import Field, BaseModel

from ..constants import *


class GlobalAttributes(BaseModel):
    """
    Model for SPIF global attributes.
    Recommended attributes are marked as Optional

    """

    class Config:
        title = 'SPIF Global Metadata Schema'

    Conventions: str = Field(
        description="The conventions followed by this data",
        example=f'SPIF-{SPIF_MAJOR_VERSION}.{SPIF_MINOR_VERSION}'
    )

    title: Optional[str] = Field(
        description='A brief title for the dataset.',
        example='Data from flight a001.'
    )

    comment: Optional[str] = Field(
        description='Any further information pertaining to the production of this dataset.',
        example='This is a comment about the data.'
    )

    institution: Optional[str] = Field(
        description=f'Institution/organisation from where data originated.',
        example=CREATOR_INSTITUTION
    )

    creator_institution: str = Field(
        description=f'Institution/organisation responsible for the creation of the SPIF data file.',
        example=CREATOR_INSTITUTION
    )

    creator_address: str = Field(
        description=f'Address of the creator institution.',
        example=CREATOR_ADDRESS
    )

    creator_type: str = Field(
        description=f'The type of creator. Should be one of {", ".join(CREATOR_TYPES)}.',
        example=CREATOR_TYPES[0]
    )

    creator_name: str = Field(
        description='The name of the person or institution responsible for data.',
        example='A. N. Other'
    )

    creator_email: str = Field(
        description='The email address of the data creator, or a generic institute email.',
        example='a.n.other@faam.ac.uk'
    )

    processing_software: Optional[str] = Field(
        description='Name of software used to generate this SPIF file.',
        example='spif_creator.py'
    )

    processing_software_version: Optional[str] = Field(
        description='Version of processing software.',
        example='v1.2.3'
    )
    processing_software_url: Optional[str] = Field(
        description='URL pointing to processing software source code, if available.',
        example='https://github.com/my-user/spif_creator'
    )

    references: Optional[str] = Field(
        description='References to any documents describing the data and production of this dataset.',
        example='doi:1234'
    )

    time_coverage_start: Optional[datetime.datetime] = Field(
        description='The start time of the data in the file, in ISO8601:2004 format.',
        example='1970-01-01T00:00:00Z'
    )

    time_coverage_end: Optional[datetime.datetime] = Field(
        description='The end time of the data in the file, in ISO8601:2004 format',
        example='1970-01-01T01:00:00Z'
    )

    history: Optional[str] = Field(
        description='Log providing an audit trail of file modifications. It is recommended that each entry is on a new line, is proceeded by a timestamp indicating date and time of file modification, then includes information, username, program and arguments.',
        example='1970-01-01T00:00:00Z A. User, spif_creator.py -i myfile -o myfile'
    )




