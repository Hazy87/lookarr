from dataclasses import dataclass
from typing import Type

from infrastructure.interfaces.imedia_server_repository import IMediaServerRepository
from infrastructure.media_type import TMediaType


@dataclass
class MediaServer:
    media_server: IMediaServerRepository
    data_type: Type[TMediaType]
