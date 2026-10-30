"""praproses.py: rangkaian praproses SIMUTEH (dipakai ulang mulai P5)."""
import json
import cv2
import numpy as np

PARAM_BAWAAN = {
    "lebar": 640,
    "gamma": 1.0,
    "clahe_clip": 2.0,
    "clahe_tile": 8,
    "penapis": "median",
    "kernel": 3,
    "sigma": 1.0,
    "tajam_k": 0.0,
}


def praproses(img_bgr, p=None):
    """Urutan: ubah ukuran -> gamma -> CLAHE kanal V -> redam derau -> tajamkan."""
    p = {**PARAM_BAWAAN, **(p or {})}

    # TODO 1: ubah ukuran
    h, w = img_bgr.shape[:2]
    tinggi = round(h * p["lebar"] / w)
    ukuran = (p["lebar"], tinggi)
    img = cv2.resize(img_bgr, ukuran, interpolation=cv2.INTER_AREA)

    # TODO 2: koreksi gamma
    if p["gamma"] != 1:
        g = p["gamma"]
        lut = np.array([255 * (i / 255) ** g for i in range(256)])
        lut = lut.clip(0, 255).astype(np.uint8)
        img = cv2.LUT(img, lut)

    # TODO 3: CLAHE kanal V
    if p["clahe_clip"] > 0:
        t = int(p["clahe_tile"])
        clahe = cv2.createCLAHE(clipLimit=p["clahe_clip"], tileGridSize=(t, t))
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        hsv[:, :, 2] = clahe.apply(hsv[:, :, 2])
        img = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)

    # TODO 4: redam derau
    k = int(p["kernel"])
    if p["penapis"] == "rerata":
        img = cv2.blur(img, (k, k))
    elif p["penapis"] == "gaussian":
        img = cv2.GaussianBlur(img, (k, k), p["sigma"])
    elif p["penapis"] == "median":
        img = cv2.medianBlur(img, k)

    # TODO 5: unsharp masking
    if p["tajam_k"] > 0:
        kk = p["tajam_k"]
        blur = cv2.GaussianBlur(img, (5, 5), 1.0)
        img = cv2.addWeighted(img, 1 + kk, blur, -kk, 0)

    return img


def simpan_param(p, path="../hasil/param_praproses.json"):
    with open(path, "w") as f:
        json.dump({**PARAM_BAWAAN, **p}, f, indent=2)
