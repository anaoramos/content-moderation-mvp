import logging

from app.schemas.moderation import ModerationResponse, ModerationRequest
from app.services.moderation_service import ModerationService

from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse

from app.schemas.metrics import MetricsResponse
from app.services.metrics_service import MetricsService

MAX_INPUT_LENGTH = 1000

router = APIRouter()

logger = logging.getLogger(__name__)


@router.post("/moderate", tags=["Moderation"], response_model=ModerationResponse)
def moderate_text(request: ModerationRequest):
    """Text Moderation endpoint.

    Note:
        - Authentication is currently not implemented. In a production setting, I would add authentication (e.g., JWT tokens)
            to ensure that only authorized users can access this endpoint.
    """
    text = request.text
    logger.info(f"Received request for moderation.")

    try:
        # Doing this synchronously for now as a proof of concept.
        # In production, I would use a message broker (e.g., Celery + RabbitMQ)
        # to handle background processing, especially for high request volumes and more complex tasks.
        result = ModerationService.predict_moderation(text)
        logger.info(f"Moderation completed successfully.")
        return JSONResponse(content=result, status_code=200)

    except Exception as e:
        logger.error(f"Error occurred while processing the request: {str(e)}")
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")


@router.get("/metrics", tags=["Metrics"], response_model=MetricsResponse)
def get_metrics():
    """Metrics endpoint that returns various metrics about requests.

    Note:
    - Authentication is currently not implemented. In a production setting, I would add authentication (e.g., JWT tokens)
        to ensure that only authorized users can access this endpoint.
    """
    try:
        metrics = MetricsService.get_metrics()
        return JSONResponse(content=metrics, status_code=200)
    except Exception as e:
        logger.error(f"Error occurred while processing the request: {str(e)}")
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")
