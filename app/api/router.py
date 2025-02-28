import logging

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from fastapi.responses import JSONResponse

from app.models_management.predictor import predict_moderation

MAX_INPUT_LENGTH = 1000

router = APIRouter()

logger = logging.getLogger(__name__)


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
    logger.info(f"Received request for moderation.")
    if len(text) > MAX_INPUT_LENGTH:  # example limit, adjust based on requirements
        logger.warning(
            f"Input too long. Request rejected.")  # In a production env, it would be helpful to include a request ID or user identifier for better traceability.

        raise HTTPException(status_code=400,
                            detail=f"Text too long. Please limit your input to a maximum of {MAX_INPUT_LENGTH} characters.")

    try:
        # Doing this synchronously for now as a proof of concept.
        # In production, I would use a message broker (e.g., Celery + RabbitMQ)
        # to handle background processing, especially for high request volumes and more complex tasks.
        result = predict_moderation(text)
        logger.info(f"Moderation completed successfully.")
        return JSONResponse(content=result, status_code=200)

    except Exception as e:
        logger.error(f"Error occurred while processing the request: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")
