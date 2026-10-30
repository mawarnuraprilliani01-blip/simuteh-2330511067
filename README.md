# SIMUTEH-2330511067: Praproses Citra Daun Teh (Evaluasi P1-P4)

Sistem Pemeriksaan Mutu Daun Teh berbasis citra untuk kelompok tani teh rakyat
di Kabupaten Sukabumi. Repository ini berisi tahap akuisisi dan praproses
(Computer Vision, Teknik Informatika UMMI, TA 2026/2027).

- Nama: Mawar Nur April Liani
- NIM: 2330511067
- Kelas: B
- SEED dataset: **1067** (4 digit terakhir NIM)
- Repository: https://github.com/mawarnuraprilliani01-blip/simuteh-2330511067

## Cara menjalankan
1. Pasang pustaka: `pip install -r requirements.txt`
2. Bangkitkan dataset dari folder utama repository:
   `python src/buat_dataset_sintetis.py` (hasil: 60 citra di `data/sintetis/`)
3. Jalankan notebook di folder `notebook/` berurutan dengan Restart & Run All:
   B1_lingkungan -> B2_citra_warna -> B3_histogram -> B4_penapisan -> B5_praproses
4. Modul yang dipakai ulang pada Pertemuan 5: `src/praproses.py` dan
   `hasil/param_praproses.json`.

## Struktur
`data/sintetis/` (dibangkitkan skrip) | `notebook/` | `src/` | `hasil/` | `laporan/`

## Parameter final praproses
| Langkah | Nilai |
|---|---|
| Ubah ukuran | lebar 640 px |
| Koreksi gamma | 1,0 (nonaktif) |
| CLAHE kanal V | clip 1,0; tile 8 |
| Redam derau | median, kernel 5 |
| Tajamkan | nonaktif (k = 0) |

Kanal terpilih untuk pengukuran KB: R (indeks BGR 2).

## Ringkasan hasil
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

## Keterbatasan
- Sebagian kenaikan KB berasal dari simpangan baku daun yang mengecil, bukan
  hanya bercak yang lebih terpisah.
- Selisih rerata (dI) bercak ringan turun 8,5% (62,26 -> 56,94) akibat median
  kernel 5.
- Uji bercak palsu hanya memakai 4 citra sehat per kondisi, dan ambang titik
  terang (selisih 30, luas >= 5 piksel) dipilih sendiri.
- Parameter dipilih pada data yang sama dengan evaluasi, sehingga hasil
  cenderung optimistis.
- Dataset sintetis, tidak dimaksudkan sebagai acuan diagnosis penyakit tanaman.

## Versi
Tag: `v0.1-praproses`. Versi pustaka: lihat `requirements.txt`.


