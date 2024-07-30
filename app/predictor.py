import os

import joblib
import pandas as pd

from config import Config
from models import PredictionRequest, PredictionResponse

class Predictor:
    def __init__(self):
        self.model = joblib.load(Config.MODEL_PATH)

    def _create_feature_dataframe(self, request_data: PredictionRequest) -> pd.DataFrame:
        """Membuat DataFrame dari data permintaan prediksi."""
        return pd.DataFrame({
            "nama sma": [request_data.nama_sma_code],
            "jalur": [request_data.jalur_code],
            "penghasilan_orang_tua": [request_data.penghasilan_orang_tua],
            "prodi": [request_data.prodi_code],
            "ipk": [request_data.ipk],
        })

    def _handle_prediction_request(self, request_data: PredictionRequest) -> PredictionResponse:
        """Menangani permintaan prediksi individu dan menghasilkan respons."""
        df = self._create_feature_dataframe(request_data)
        prediction = self.model.predict(df)[0]
        return PredictionResponse(prediction=prediction, **request_data.model_dump())

    def predict(self, request_data: PredictionRequest) -> PredictionResponse:
        """Menangani prediksi berdasarkan data permintaan."""
        return self._handle_prediction_request(request_data)

    def _process_batch_prediction(self, df: pd.DataFrame) -> pd.DataFrame:
        """Memproses prediksi batch dan menghasilkan DataFrame hasil prediksi."""
        results = []
        for req in df.to_dict(orient="records"):
            try:
                valid_req = PredictionRequest(**req)
                results.append(self._handle_prediction_request(valid_req).model_dump())
            except ValueError as e:
                try:
                    req["error"] = str(e)
                    results.append(req)
                except Exception as e:
                    raise ValueError("Data does not match the format")
        return pd.DataFrame(results)

    def batch_prediction(self, file) -> str:
        """Menangani prediksi batch dari file Excel dan menyimpan hasilnya."""
        df = pd.read_excel(file)
        result_df = self._process_batch_prediction(df)
        
        output_path = os.path.join("app/static/temp", "prediction_result.xlsx")
        result_df.to_excel(output_path, index=False)
        
        return output_path.replace("app/", "")

