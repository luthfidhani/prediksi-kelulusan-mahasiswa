import joblib
import pandas as pd
from config import Config
from models import PredictionRequest, PredictionResponse


class Predictor:
    def __init__(self):
        self.model = joblib.load(Config.MODEL_PATH)

    def predict(self, request_data: PredictionRequest) -> PredictionResponse:
        if request_data.ipk <= 2:
            return PredictionResponse(prediction="Tidak tepat waktu")

        df = pd.DataFrame({
            "n_toefl": [request_data.n_toefl],
            "ipk": [request_data.ipk],
            "jumlah_semester": [request_data.jumlah_semester],
            "prodi_code": [request_data.prodi_code],
            "jenis_kelamin_code": [request_data.jenis_kelamin_code],
            "jalur_code": [request_data.jalur_code],
            "penghasilan_orang_tua": [request_data.penghasilan_orang_tua],
        })

        prediction = self.model.predict(df)[0]
        print(prediction)
        print(prediction)
        print(prediction)
        print(prediction)
        print(prediction)
        print(prediction)
        print(prediction)
        print(prediction)
        print(prediction)
        print(prediction)
        print(prediction)
        return PredictionResponse(prediction=prediction)
