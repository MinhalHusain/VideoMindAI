"""Service for managing video workspaces and persisting artifacts."""

import json
from pathlib import Path
from typing import Any, Dict

# Resolve project root dynamically
PROJECT_ROOT: Path = Path(__file__).resolve().parent.parent.parent.parent
DATA_DIR: Path = PROJECT_ROOT / "data" / "videos"


class WorkspaceService:
    """Manages isolated storage workspaces for each video."""

    def __init__(self, data_dir: Path = DATA_DIR) -> None:
        self.data_dir = data_dir
        self.data_dir.mkdir(parents=True, exist_ok=True)

    def get_workspace_path(self, video_id: str) -> Path:
        """Get the workspace directory for a given video ID, creating it if needed."""
        workspace = self.data_dir / video_id
        workspace.mkdir(parents=True, exist_ok=True)
        return workspace

    def get_audio_path(self, video_id: str) -> Path:
        """Get the standardized path for the extracted audio file."""
        return self.get_workspace_path(video_id) / "audio.wav"

    def get_original_video_path(self, video_id: str, extension: str) -> Path:
        """Get the standardized path for the original uploaded video."""
        return self.get_workspace_path(video_id) / f"original{extension}"

    def save_metadata(self, video_id: str, metadata: Dict[str, Any]) -> None:
        """Persist metadata to JSON in the video's workspace."""
        path = self.get_workspace_path(video_id) / "metadata.json"
        with path.open("w", encoding="utf-8") as f:
            json.dump(metadata, f, indent=2)

    def save_transcript(self, video_id: str, transcript: Dict[str, Any]) -> None:
        """Persist transcript to JSON in the video's workspace."""
        path = self.get_workspace_path(video_id) / "transcript.json"
        with path.open("w", encoding="utf-8") as f:
            json.dump(transcript, f, indent=2)
