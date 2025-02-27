from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from fastapi.responses import JSONResponse

from app.models_management.predictor import predict_moderation

MAX_INPUT_LENGTH = 1000

router = APIRouter()


class TextModerationRequest(BaseModel):
    text: str


@router.post("/moderate")
def moderate_text(request: TextModerationRequest):
    """Text Moderation endpoint.

    Note:
        - Authentication is currently not implemented. In a production setting, I would add authentication (e.g., JWT tokens)
            to ensure that only authorized users can access this endpoint.
    """
    text = request.text

    if len(text) > MAX_INPUT_LENGTH:  # example limit, adjust based on requirements
        raise HTTPException(status_code=400,
                            detail=f"Text too long. Please limit your input to a maximum of {MAX_INPUT_LENGTH} characters.")

    try:
        # Doing this synchronously for now as a proof of concept.
        # In production, I would use a message broker (e.g., Celery + RabbitMQ)
        # to handle background processing, especially for high request volumes and more complex tasks.
        result = predict_moderation(text)
        return JSONResponse(content=result, status_code=200)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")
