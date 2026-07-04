"""API routes for video-aware chat using RAG."""

import logging

from fastapi import APIRouter, HTTPException, status

from app.schemas.chat import ChatRequest, ChatResponse
from app.services.rag_service import RAGService
from app.services.workspace_service import WorkspaceService

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1", tags=["Chat"])

rag_service = RAGService()
workspace_service = WorkspaceService()


@router.post(
    "/chat",
    response_model=ChatResponse,
    status_code=200,
    summary="Ask a question about a video",
    response_description="AI-generated answer grounded on the video's knowledge base.",
)
async def chat(request: ChatRequest) -> ChatResponse:
    """Ask a natural language question about a previously processed video.

    Retrieves relevant context from the video's FAISS index and generates
    an answer using Gemini via Retrieval Augmented Generation.
    """
    workspace_path = workspace_service.get_workspace_path(request.workspace_id)

    # Verify the workspace actually has the required files
    if not (workspace_path / "knowledge.json").exists() or not (workspace_path / "video.index").exists():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Workspace '{request.workspace_id}' not found or not fully processed.",
        )

    try:
        result = rag_service.answer_question(
            workspace_path=workspace_path,
            question=request.question,
            top_k=5,
        )
    except FileNotFoundError as exc:
        logger.error("Workspace files missing: %s", exc)
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc
    except Exception as exc:
        logger.exception("Chat request failed for workspace '%s'.", request.workspace_id)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An internal error occurred while generating the answer.",
        ) from exc

    return ChatResponse(
        answer=result["answer"],
        retrieved_chunks=result["retrieved_chunks"],
    )
