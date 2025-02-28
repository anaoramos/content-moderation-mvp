from app.utils.predictor import Predictor


class ModerationService:

    @staticmethod
    def predict_moderation(text: str) -> dict:
        """Generate prediction using the Predictor class."""
        if Predictor.model is None or Predictor.tokenizer is None:
            Predictor.load_model()

        return Predictor.predict_moderation(text)
