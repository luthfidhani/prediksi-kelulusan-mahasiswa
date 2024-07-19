from pydantic import BaseModel, field_validator
from typing import List


class PredictionRequest(BaseModel):
    asal_sma: str
    penghasilan_orang_tua: int
    n_toefl: int
    ipk: float
    jumlah_semester: int
    prodi_code: int
    jenis_kelamin_code: int
    jalur_code: int
    ips: List[float]

    @field_validator("ipk")
    def ipk_must_be_non_negative(cls, v):
        if v < 0:
            raise ValueError("IPK must be non-negative")
        return v


class PredictionResponse(BaseModel):
    prediction: str
