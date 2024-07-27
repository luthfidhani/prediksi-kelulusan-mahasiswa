import math
from typing import Union

from pydantic import BaseModel, Field, field_validator

import vars


class PredictionRequest(BaseModel):
    nim: Union[int, None] = None
    nama: Union[str, None] = None
    asal_sma: Union[str, None] = None
    penghasilan_orang_tua: int = Field(..., ge=0)
    toefl: int = Field(..., ge=0, le=677)
    prodi: str 
    jalur_masuk: str
    jenis_kelamin: str 
    ip_semester_1: Union[float, None] = None
    ip_semester_2: Union[float, None] = None
    ip_semester_3: Union[float, None] = None
    ip_semester_4: Union[float, None] = None
    ip_semester_5: Union[float, None] = None
    ip_semester_6: Union[float, None] = None
    ip_semester_7: Union[float, None] = None
    ip_semester_8: Union[float, None] = None
    ip_semester_9: Union[float, None] = None
    ip_semester_10: Union[float, None] = None
    ip_semester_11: Union[float, None] = None
    ip_semester_12: Union[float, None] = None
    ip_semester_13: Union[float, None] = None
    ip_semester_14: Union[float, None] = None

    @field_validator('prodi')
    def prodi_must_be_valid(cls, value):
        valid_prodi = list(vars.prodi_dict.keys())
        if value.title() not in valid_prodi:
            raise ValueError(f"Invalid program. Valid programs are: {', '.join(valid_prodi)}")
        return value.title()

    @field_validator('jenis_kelamin')
    def jenis_kelamin_must_be_valid(cls, value):
        valid_jenis_kelamin = ["Laki-Laki", "Perempuan"]
        if value.title() not in valid_jenis_kelamin:
            raise ValueError(f"Invalid gender. Valid genders are: {', '.join(valid_jenis_kelamin)}")
        return value.title()

    @field_validator('jalur_masuk')
    def jalur_must_be_valid(cls, value):
        valid_jalur = list(vars.jalur_dict.keys())
        if value.upper() not in valid_jalur:
            raise ValueError(f"Invalid admission path. Valid paths are: {', '.join(valid_jalur)}")
        return value.upper()

    @property
    def ipk(self) -> float:
        # Mengambil semua nilai IP semester yang ada
        ip_values = [getattr(self, f'ip_semester_{i}', None) for i in range(1, 15)]
        # Menyaring nilai-nilai IP yang tidak None
        valid_ip_values = [ip for ip in ip_values if not (math.isnan(ip) or ip == 0)]
        if valid_ip_values:
            return sum(valid_ip_values) / len(valid_ip_values)
        return 0.0

    @property
    def jumlah_semester(self) -> int:
        # Mengambil semua nilai IP semester yang ada
        ip_values = [getattr(self, f'ip_semester_{i}', None) for i in range(1, 15)]
        return len([ip for ip in ip_values if not (math.isnan(ip) or ip == 0)])

    @property
    def prodi_code(self) -> int:
        return vars.prodi_dict.get(self.prodi, {}).get("code", None)

    @property
    def jalur_code(self) -> int:
        return vars.jalur_dict.get(self.jalur_masuk, None)

    @property
    def jenis_kelamin_code(self) -> int:
        return 0 if self.jenis_kelamin == "Laki-Laki" else 1


class PredictionResponse(PredictionRequest):
    prediction:  str
