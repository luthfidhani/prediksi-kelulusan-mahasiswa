from models import PredictionRequest


def data_validation(request_form):
    data = {
        "nama_sma": request_form["nama_sma"],
        "prodi": request_form["prodi"],
        "penghasilan_orang_tua": int(request_form["penghasilan_orang_tua"]),
        "jalur": request_form["jalur"],
        "ip_semester_1": float(request_form["ip_semester_1"] if request_form["ip_semester_1"] != "" else 0.0),
        "ip_semester_2": float(request_form["ip_semester_2"] if request_form["ip_semester_2"] != "" else 0.0),
        "ip_semester_3": float(request_form["ip_semester_3"] if request_form["ip_semester_3"] != "" else 0.0),
        "ip_semester_4": float(request_form["ip_semester_4"] if request_form["ip_semester_4"] != "" else 0.0),
    }
    return PredictionRequest(**data)


def is_file_allowed(filename):
    return (
        True
        if "prediction_result.xlsx" not in filename.lower()
        and filename.lower().endswith((".xlsx", ".xls"))
        else False
    )
