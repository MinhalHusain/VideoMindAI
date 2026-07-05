"""API routes for workspace retrieval."""

import json
from fastapi import APIRouter, HTTPException, status

from app.services.workspace_service import WorkspaceService

router = APIRouter(prefix="/api/v1/workspaces", tags=["Workspaces"])
workspace_service = WorkspaceService()

@router.get(
    "/{workspace_id}/transcript",
    status_code=200,
    summary="Get workspace transcript",
)
async def get_transcript(workspace_id: str):
    """Retrieve the transcript for a processed video workspace."""
    try:
        workspace_path = workspace_service.get_workspace_path(workspace_id)
        transcript_path = workspace_path / "transcript.json"
        
        if not transcript_path.exists():
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Transcript not found for this workspace."
            )
            
        with transcript_path.open("r", encoding="utf-8") as f:
            return json.load(f)
    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(exc)
        )

@router.get(
    "/{workspace_id}/knowledge",
    status_code=200,
    summary="Get workspace knowledge",
)
async def get_knowledge(workspace_id: str):
    """Retrieve the full knowledge base for a processed video workspace."""
    try:
        workspace_path = workspace_service.get_workspace_path(workspace_id)
        knowledge_path = workspace_path / "knowledge.json"
        
        if not knowledge_path.exists():
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Knowledge base not found for this workspace."
            )
            
        with knowledge_path.open("r", encoding="utf-8") as f:
            return json.load(f)
    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(exc)
        )
