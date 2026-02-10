from ..models.timeline_predictor import TimelinePredictor

class InferenceEngine:
    def __init__(self):
        self.model = TimelinePredictor()

    def predict(self, input_data):
        return self.model.predict(input_data)
