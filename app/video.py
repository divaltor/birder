import uuid
from pathlib import Path
from typing import Self

import yt_dlp
from pydantic import BaseModel


class VideoMetadata(BaseModel):
    height: int | None = None
    width: int | None = None


class VideoInformation(BaseModel):
    file_path: Path
    metadata: VideoMetadata

    @classmethod
    def from_file(cls, file_path: Path) -> Self:
        try:
            metadata = VideoMetadata.model_validate_json(
                file_path.with_suffix('.info.json').read_text(),
            )
        except FileNotFoundError:
            metadata = VideoMetadata()

        return cls(
            file_path=file_path,
            metadata=metadata,
        )


def download_video(url: str, folder: str) -> VideoInformation:
    random_id = str(uuid.uuid4())

    with yt_dlp.YoutubeDL(
        {
            'outtmpl': f'{folder}/{random_id}.mp4',
            'quiet': True,
            'no_warnings': True,
            'no_post_overwrites': True,
            'no_overwrites': True,
            'recode-video': 'mp4',
        },
    ) as ydl:
        ydl.download([url])

    return VideoInformation.from_file(Path(folder, f'{random_id}.mp4'))
