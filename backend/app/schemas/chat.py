"""Pydantic schemas for the chat endpoint."""

from typing import Any, Dict, List

from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    """Request body for the chat endpoint."""

    workspace_id: str = Field(..., description="UUID of the video workspace to query.")
    question: str = Field(..., description="Natural language question about the video.")

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "workspace_id": "9f2d3e14-acde-4c4d-b1a2-7e8f9a0b1c2d",
                    "question": "What is the main topic of the video?",
                }
            ]
        }
    }


class RetrievedChunk(BaseModel):
    """A single chunk retrieved from the vector index."""

    chunk_id: int | None = Field(default=None, description="The ID of the retrieved chunk.")
    score: float | None = Field(default=None, description="The distance/similarity score.")
    text: str = Field(default="", description="The transcript text of the chunk.")


class ChatResponse(BaseModel):
    """Response body returned by the chat endpoint."""

    answer: str = Field(..., description="The AI-generated answer grounded on video context.")
    retrieved_chunks: List[RetrievedChunk] = Field(
        default_factory=list,
        description="The context chunks used to generate the answer.",
    )

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "answer": "The video discusses machine learning fundamentals.",
                    "retrieved_chunks": [
                        {
                            "chunk_id": 1,
                            "score": 0.4321,
                            "text": "In this lecture we cover the basics of ML...",
                        }
                    ],
                }
            ]
        }
    }
