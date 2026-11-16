# SIMUTEH-2330511067: Praproses, Deteksi Tepi, dan Analisis Bercak Citra Daun Teh (P1-P6)

Sistem Pemeriksaan Mutu Daun Teh berbasis citra untuk kelompok tani teh rakyat
di Kabupaten Sukabumi. Repository ini berisi tahap akuisisi, praproses,
deteksi tepi, dan analisis bercak (Computer Vision, Teknik Informatika UMMI,
TA 2026/2027).

- Nama: Mawar Nur April Liani
- NIM: 2330511067
- Kelas: B
- SEED dataset: **1067** (4 digit terakhir NIM)
- Repository: https://github.com/mawarnuraprilliani01-blip/simuteh-2330511067

## Status versi
| Tag | Isi | Pertemuan |
|---|---|---|
| `v0.1-praproses` | akuisisi dan praproses | P1-P4 |
| `v0.2-tepi` | gradien, operator tepi, Canny | P5 |
| `v0.3-morfologi` | morfologi, komponen terhubung, modul `bercak.py` | P6 |

## Cara menjalankan
1. Pasang pustaka: `pip install -r requirements.txt`
2. Bangkitkan dataset dari folder utama repository:
   `python src/buat_dataset_sintetis.py` (hasil: 60 citra di `data/sintetis/`)
3. Jalankan notebook di folder `notebook/` berurutan dengan Restart & Run All:
   B1_lingkungan -> B2_citra_warna -> B3_histogram -> B4_penapisan -> B5_praproses
   -> P5_tepi -> P6_morfologi
4. Modul yang dipakai ulang: `src/praproses.py` dan `hasil/param_praproses.json`
   (praproses), `src/utils_tepi.py` (evaluasi tepi dan mask awal), dan
   `src/bercak.py` dengan `hasil/param_bercak.json` (analisis bercak).

## Struktur
`data/sintetis/` (dibangkitkan skrip) | `notebook/` | `src/` | `hasil/` | `laporan/`

---

## Bagian 1. Praproses (Evaluasi P1-P4)

### Parameter final praproses
| Langkah | Nilai |
|---|---|
| Ubah ukuran | lebar 640 px |
| Koreksi gamma | 1,0 (nonaktif) |
| CLAHE kanal V | clip 1,0; tile 8 |
| Redam derau | median, kernel 5 |
| Tajamkan | nonaktif (k = 0) |

Kanal terpilih untuk pengukuran KB: R (indeks BGR 2).

### Ringkasan hasil
KB rata-rata kanal R pada 40 citra berbercak (sebelum -> sesudah praproses):

| Kondisi | KB sebelum | KB sesudah |
|---|---|---|
| normal | 8,89 | 12,09 |
| gelap | 8,87 | 17,25 |
| terang | 6,02 | 8,92 |
| kontras_rendah | 3,92 | 7,81 |
| bayangan | 5,00 | 7,82 |

Uji bercak palsu pada 20 citra sehat: simpangan baku area daun turun di semua
kondisi (rasio 0,44 sampai 0,65). Titik terang lokal tidak naik kecuali pada
kondisi normal (3,00 -> 7,25). Pada panel visual, tidak tampak bintik yang
menyerupai bercak di permukaan daun; tambahan titik pada kondisi normal diduga
berasal dari urat daun yang menegas.

Parameter awal (clip 2,0; kernel 3) menghasilkan bercak palsu lebih banyak
(13,00 titik pada bayangan) dan KB kondisi terang turun (6,02 -> 5,86),
sehingga diganti dengan parameter final di atas.

---

## Bagian 2. Deteksi tepi (P5, tag `v0.2-tepi`)

Notebook: `notebook/P5_tepi.ipynb`. Evaluasi memakai presisi, recall, dan F1
tepi dengan toleransi jarak 2 piksel terhadap tepi acuan dari mask daun dan
bercak.

- Operator yang dibandingkan: Sobel, Prewitt, Laplacian of Gaussian (LoG), dan
  Canny, pada kanal Gray dan R, citra mentah dan sesudah praproses
  (`hasil/p5_tabel_tepi.csv`).
- Operator dan kanal terbaik: [ISI: operator, kanal, dan rerata F1 dari Tabel 6].
- Parameter Canny terpilih: [ISI: sigma dan ambang dari Tabel 7].
- Ambang Canny otomatis berbasis median gagal pada citra kontras rendah;
  diperbaiki dengan `canny_persentil` (ambang dari persentil magnitudo gradien).
- Keputusan pemakaian tepi di SIMUTEH: [ISI: ringkasan Tabel 8].

---

## Bagian 3. Morfologi dan analisis bercak (P6, tag `v0.3-morfologi`)

Notebook: `notebook/P6_morfologi.ipynb`. Modul akhir: `src/bercak.py`.

### Alur analisis bercak
mask daun awal (Otsu pada kanal S) -> bercak awal (median + k x MAD pada kanal R)
-> opening lalu closing -> komponen terhubung (konektivitas 8) -> penyaringan
luas, kebulatan, dan rasio aspek -> persen bercak dan kelas mutu.

### Parameter final bercak (`hasil/param_bercak.json`)
| Parameter | Nilai |
|---|---|
| kanal | 2 (R) |
| k | 4,0 |
| se_bentuk, se_open, se_close | elips, 5, 5 |
| luas_min | 20 px |
| bulat_min, rasio_maks | 0,5 dan 1,8 |
| batas_ringan, batas_berat | 0,1% dan 2,0% |
| mm_per_px | 0,4375 (jarak 200 mm, lebar kerja 640 px) |

### Hasil penyaringan komponen (rerata galat jumlah bercak per citra)
| Aturan | Berat | Ringan | Sehat | Daun sehat dengan bercak palsu |
|---|---|---|---|---|
| tanpa saring | 2,65 | 2,10 | 3,05 | 11 |
| luas >= 20 | 1,90 | 1,45 | 2,25 | 10 |
| luas + kebulatan | 1,50 | 0,95 | 0,90 | 7 |
| luas + kebulatan + rasio | 1,25 | 0,65 | 0,25 | 4 |

### Evaluasi modul `bercak.py` pada 60 citra
- Galat absolut rerata persen bercak: **0,487**
- Korelasi persen prediksi dan acuan: **0,946**
- Akurasi kelas: **0,833** (50 dari 60 benar)

| Acuan \ Prediksi | Bercak Berat | Bercak Ringan | Sehat |
|---|---|---|---|
| Bercak Berat | 18 | 1 | 1 |
| Bercak Ringan | 0 | 13 | 7 |
| Sehat | 0 | 1 | 19 |

Akurasi per kondisi cahaya: bayangan 1,00 | terang 0,83 | kontras_rendah 0,83 |
gelap 0,75 | normal 0,75.

Kesalahan terbanyak adalah bercak ringan yang dinilai sehat (7 citra), yaitu
bercak terlewat, bukan bercak yang mengada-ada.

## Cara memakai `analisis_daun`
Dari folder utama repository:

```python
import sys, json
sys.path.append("src")
import cv2
from praproses import praproses
import bercak

PARAM = json.load(open("hasil/param_praproses.json"))
img = cv2.imread("data/sintetis/citra/teh_041.png")

hasil = bercak.analisis_daun(praproses(img, PARAM))
print(hasil["jumlah_bercak"], hasil["persen_bercak"], hasil["kelas"])
```

`analisis_daun(img_praproses, p=None)` menerima citra BGR yang sudah
dipraproses dan mengembalikan kamus:

| Kunci | Isi |
|---|---|
| `mask_daun` | mask daun (255 = daun) |
| `mask_bercak` | mask bercak sesudah dibersihkan dan disaring |
| `jumlah_bercak` | jumlah bercak yang lolos penyaringan |
| `persen_bercak` | luas bercak / luas daun x 100 |
| `kelas` | `Sehat`, `Bercak Ringan`, atau `Bercak Berat` |
| `bercak` | daftar ukuran tiap bercak (luas px dan mm2, keliling, kebulatan, rasio aspek, pusat) |

Parameter bawaan ada di `PARAM_BERCAK` pada `src/bercak.py`. Untuk mengganti
sebagian, kirim kamus kedua, misalnya `bercak.analisis_daun(pra, {"se_open": 3})`.

---

## Keterbatasan
- Sebagian kenaikan KB berasal dari simpangan baku daun yang mengecil, bukan
  hanya bercak yang lebih terpisah.
- Selisih rerata (dI) bercak ringan turun 8,5% (62,26 -> 56,94) akibat median
  kernel 5.
- Uji bercak palsu hanya memakai 4 citra sehat per kondisi, dan ambang titik
  terang (selisih 30, luas >= 5 piksel) dipilih sendiri.
- Parameter dan batas kelas (0,1% dan 2,0%) dipilih pada data yang sama dengan
  evaluasi, sehingga akurasi cenderung optimistis.
- Bercak pada dataset sintetis berbentuk lingkaran sempurna, sehingga aturan
  kebulatan dan rasio aspek mungkin terlalu cocok dengan data sintetis dan
  perlu diuji ulang pada foto bercak nyata.
- Konversi 0,4375 mm/px hanya berlaku untuk jarak foto 200 mm.
- Dataset sintetis, tidak dimaksudkan sebagai acuan diagnosis penyakit tanaman.

## Versi
Tag: `v0.1-praproses`, `v0.2-tepi`, `v0.3-morfologi`.
Versi pustaka: lihat `requirements.txt`.
