from app.models_management.model_loader import ModelSingleton

SCORES_MAPPING = {
    "sexual": "S",
    "hate": "H",
    "violence": "V",
    "harassment": "HR",
    "self-harm": "SH",
    "sexual/minors": "S3",
    "hate/threatening": "H2",
    "violence/graphic": "V2",
    "OK": "OK",
}


def predict_moderation(text: str) -> dict:
    """Predict moderation score for the input text.

    Args:
        text (str): The input text for prediction.

    Returns:
        dict: A dictionary containing the text and its associated moderation category and confidence.
            - 'text' (str): The input text for prediction.
            - 'category' (str): The moderation category (e.g., 'sexual', 'hate', 'OK').
            - 'confidence' (float): The confidence score of the prediction, rounded to 4 decimal places.
    """
    model = ModelSingleton.get_model()
    result = model(text)
    prediction = result[0]

    score = round(prediction.get('score', 0), 4)
    category = SCORES_MAPPING.get(prediction['label'], 'unknown')

    return {"text": text, "category": category, "confidence": score}
