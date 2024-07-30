import math
from typing import Union

from pydantic import BaseModel, Field, field_validator

import vars


class PredictionRequest(BaseModel):
    nim: Union[int, None] = None
    nama: Union[str, None] = None
    nama_sma: Union[str, None] = None
    penghasilan_orang_tua: int = Field(..., ge=0)
    prodi: str 
    jalur: str
    ip_semester_1: Union[float, None] = None
    ip_semester_2: Union[float, None] = None
    ip_semester_3: Union[float, None] = None
    ip_semester_4: Union[float, None] = None

    @field_validator("prodi")
    def prodi_must_be_valid(cls, value):
        valid_prodi = list(vars.prodi_dict.keys())
        if value.title() not in valid_prodi:
            raise ValueError(f"Invalid program. Valid programs are: {', '.join(valid_prodi)}")
        return value.title()

    @field_validator("jalur")
    def jalur_must_be_valid(cls, value):
        valid_jalur = list(vars.jalur_dict.keys())
        if value.upper() not in valid_jalur:
            raise ValueError(f"Invalid admission path. Valid paths are: {', '.join(valid_jalur)}")
        return value.upper()

    @property
    def ipk(self) -> float:
        # Mengambil semua nilai IP semester yang ada
        ip_values = [getattr(self, f"ip_semester_{i}", None) for i in range(1, 5)]
        # Menyaring nilai-nilai IP yang tidak None
        valid_ip_values = [ip for ip in ip_values if not (math.isnan(ip) or ip == 0)]
        if valid_ip_values:
            return sum(valid_ip_values) / len(valid_ip_values)
        return 0.0

    @property
    def prodi_code(self) -> int:
        return vars.prodi_dict.get(self.prodi, {}).get("code", None)

    @property
    def jalur_code(self) -> int:
        return vars.jalur_dict.get(self.jalur, None)
    
    @property
    def nama_sma_code(self) -> int:
        list_sma = {k.lower(): v for k, v in vars.nama_sma_dict.items()}
        return list_sma.get(self.nama_sma.lower(), 130)


class PredictionResponse(PredictionRequest):
    prediction:  str
