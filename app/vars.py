jalur = [
    ("PMDK"),
    ("USMI"),
    ("USM2"),
    ("USM3"),
    ("USM"),
    ("USM 1"),
    ("USM 2"),
    ("USM 3"),
    ("USM 2A"),
    ("USM 2B"),
    ("USM 3A"),
    ("USM 3B"),
    ("UTBK"),
]

prodi = [
    ("S1", "Informatika"),
    ("S1", "Sistem Informasi"),
    ("S1", "Teknik Elektro"),
    ("S1", "Manajemen Rekayasa"),
    ("S1", "Teknik Bioproses"),
    ("D4", "Sarjana Terapan Teknologi Rekayasa Perangkat Lunak"),
    ("D3", "Teknologi Informasi"),
    ("D3", "Teknologi Komputer"),
]

jenis_kelamin = [
    ("Laki-Laki"),
    ("Perempuan"),
]


prodi_dict = {
    "Teknologi Informasi": {
        "code": 1,
        "jenjang": "D3",
        "minimum_semester": 4,
    },
    "Sarjana Terapan Teknologi Rekayasa Perangkat Lunak": {
        "code": 2,
        "jenjang": "D4",
        "minimum_semester": 6,
    },
    "Informatika": {
        "code": 3,
        "jenjang": "S1",
        "minimum_semester": 6,
    },
    "Sistem Informasi": {
        "code": 4,
        "jenjang": "S1",
        "minimum_semester": 6,
    },
    "Teknologi Komputer": {
        "code": 5,
        "jenjang": "D3",
        "minimum_semester": 4,
    },
    "Teknik Elektro": {
        "code": 6,
        "jenjang": "S1",
        "minimum_semester": 6,
    },
    "Manajemen Rekayasa": {
        "code": 7,
        "jenjang": "S1",
        "minimum_semester": 6,
    },
    "Teknik Bioproses": {
        "code": 8,
        "jenjang": "S1",
        "minimum_semester": 6,
    }
}

jalur_dict = {
    "PMDK": 1,
    "USMI": 2,
    "USM2": 3,
    "USM3": 4,
    "USM": 5,
    "USM 1": 6,
    "USM 2": 7,
    "USM 3": 8,
    "USM 2A": 9,
    "USM 2B": 10,
    "USM 3A": 11,
    "USM 3B": 12,
    "UTBK": 13,
}

jenis_kelamin_dict = {
    "Laki-Laki": 0,
    "Perempuan": 1
}