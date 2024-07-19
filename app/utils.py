import numpy as np
from vars import prodi
from models import PredictionRequest


def collect_data_from_form(request_form):
    ips = [float(request_form[f"ip_semester_{i}"]) for i in range(1, 15) if request_form[f"ip_semester_{i}"]]
    ips = np.array(ips, dtype=float)

    data = {
        "asal_sma": request_form["asal_sma"],
        "penghasilan_orang_tua": int(request_form["penghasilan_orang_tua"]),
        "n_toefl": int(request_form["n_toefl"]),
        "ipk": np.mean(ips),
        "jumlah_semester": len(ips),
        "prodi_code": int(request_form["prodi_code"]),
        "jenis_kelamin_code": int(request_form["jenis_kelamin_code"]),
        "jalur_code": int(request_form["jalur_code"]),
        "ips": ips.tolist(),
    }
    return PredictionRequest(**data)


def is_smt_valid(prodi_code, ips):
    for _, kode, minimal_studi in prodi:
        if kode == prodi_code:
            if len(ips) < minimal_studi:
                return False
    return True
