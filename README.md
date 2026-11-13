# Simulasi Jatuh Bebas dan Pantulan Bola

**Tutorial mahasiswa: menjalankan simulasi Pygame dan mengunggahnya ke itch.io.**

Proyek ini mengadaptasi program `Kualitas Bagys.py`. Bola dijatuhkan dari ketinggian 6 meter, memantul, lalu berhenti ketika kecepatan pantulnya cukup kecil. Pengguna dapat mengubah gravitasi dan koefisien restitusi.

Versi ini memakai judul **Simulasi Jatuh Bebas dan Pantulan Bola**, dengan ukuran layar **1000 × 680 piksel**. Kode lengkap tersedia di [game/main.py](game/main.py).

> **Status paket:** kode sudah disesuaikan untuk Pygbag dan diperiksa sintaksnya. Eksekusi grafis serta build web belum terverifikasi karena dependensi/runtime tidak dapat diunduh di lingkungan penyusunan. ZIP paket sumber ini untuk GitHub; ZIP yang dimainkan di itch.io harus dibuat melalui langkah build di bawah.

## Isi panduan

1. [Mengenal program](#1-mengenal-program)
2. [Persiapan dan instalasi](#2-persiapan-dan-instalasi)
   - [2A. Mengubah kode asli agar berjalan di browser](#2a-mengubah-kode-asli-agar-berjalan-di-browser)
   - [2B. Memasukkan gambar, suara, musik, dan font](#2b-memasukkan-gambar-suara-musik-dan-font)
3. [Menjalankan simulasi](#3-menjalankan-simulasi)
4. [Membuat ZIP web](#4-membuat-zip-web)
5. [Upload ke itch.io](#5-upload-ke-itchio)
6. [Menyimpan di GitHub](#6-menyimpan-di-github)
7. [Solusi masalah](#7-solusi-masalah)

## 1. Mengenal program

### Kontrol

| Tombol | Fungsi |
| --- | --- |
| **Space** | Jeda atau lanjutkan simulasi. |
| **R** | Ulangi jatuh dari 6 m; waktu dan hitungan pantulan direset. Gravitasi dan restitusi tetap memakai pengaturan terakhir. |
| **↑ / ↓** | Naikkan/turunkan gravitasi sebesar 0,5 m/s²; batas 0,5–25 m/s². |
| **→ / ←** | Naikkan/turunkan koefisien restitusi sebesar 0,05; batas 0–1. |
| **Esc** | Akhiri program. Di browser, muat ulang halaman untuk memulai kembali. |

Klik area simulasi sebelum menggunakan keyboard. Contoh ini ditujukan untuk laptop/komputer; tombol layar sentuh belum disediakan.

### Besaran yang ditampilkan

| Besaran | Nilai awal / keterangan |
| --- | --- |
| Ketinggian | 6,00 m; dihitung dari posisi kontak dengan lantai. |
| Kecepatan | 0 m/s; positif ke bawah, negatif ketika bola naik. |
| Gravitasi | 9,81 m/s². |
| Koefisien restitusi | 0,78. |
| Pantulan | Jumlah tumbukan yang menghasilkan pantulan di atas ambang. |
| Waktu | Waktu simulasi; berhenti bertambah saat dijeda atau bola berhenti. |

Model mengikuti program asal: selama terbang, tinggi diperbarui dengan `h_baru = h - v*dt - 0.5*g*dt**2` dan kecepatan dengan `v_baru = v + g*dt`. Saat tumbukan, kecepatan pantul bernilai `-e * v_tumbukan`. Bola dihentikan jika besar kecepatan pantul tidak melebihi 0,45 m/s.

Ini model pembelajaran tanpa hambatan udara. Sisa waktu pada frame tumbukan tidak diintegrasikan; hasil waktu/tinggi pantulan memiliki galat langkah waktu. `dt` dibatasi 0,033 s, sehingga pada perangkat lambat waktu simulasi dapat tertinggal dari waktu nyata. Pengaturan `e = 1` tidak kehilangan kecepatan pada aturan tumbukan, tetapi galat numerik tetap mungkin terjadi.

### Penyesuaian untuk browser

- Berkas masuk menjadi `game/main.py`.
- `main()` menjadi `async def main()`.
- Setiap frame menjalankan `await asyncio.sleep(0)`.
- Program dimulai dengan `asyncio.run(main())`.
- Font memakai font bawaan Pygame agar tidak bergantung pada Arial.
- Judul jendela dan judul di layar disamakan dengan nama program.

## 2. Persiapan dan instalasi

Siapkan [Python](https://www.python.org/downloads/), editor seperti VS Code, koneksi internet, dan akun [itch.io](https://itch.io/).

Ekstrak paket sumber ini. Buka folder **`simulasi-jatuh-bebas`** di VS Code, kemudian buka **Terminal → New Terminal** dengan PowerShell. Terminal harus berada pada folder yang berisi README dan `requirements.txt`.

| Berkas/folder | Fungsi |
| --- | --- |
| `README.md` | Tutorial ini. |
| `game/main.py` | Kode simulasi lengkap. |
| `requirements.txt` | Paket Python untuk instalasi. |
| `docs/images/` | Ilustrasi langkah upload, dipakai oleh README. |
| `.gitignore` | Mengecualikan environment dan hasil build dari Git. |

Periksa Python:

```powershell
python --version
```

Jika perintah itu tidak tersedia tetapi `py --version` berhasil, ganti `python` dengan `py` pada perintah pembuatan environment berikut.

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install --upgrade pip
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

Pemanggilan Python lewat `.venv` tidak memerlukan aktivasi PowerShell. Instalasi `pygame-ce` tetap diakses dengan `import pygame` di kode.

## 2A. Mengubah kode asli agar berjalan di browser

**Jika menggunakan `game/main.py` dari paket ini, penyesuaian browser sudah diterapkan.** Bagian ini menjelaskan perubahan dari `Kualitas Bagys.py`, supaya bisa diterapkan pada tugas Pygame lain. Simpan salinan kode asli sebelum mengedit.

Program asal menggambar bola dan lantai dengan `pygame.draw`, sehingga **tidak memerlukan foto, suara, atau berkas font tambahan**. Aset pada bagian 2B bersifat opsional.

### Langkah 1 — Nama berkas dan lokasi

Simpan salinan `Kualitas Bagys.py` sebagai **`main.py`** di dalam folder `game`. Pastikan ekstensi sebenarnya `.py`, bukan `.py.txt`. Folder `game` menjadi folder yang dikemas Pygbag.

### Langkah 2 — Tambahkan asyncio

Pada bagian import, kode asal berisi `import math` dan `import pygame`. Tambahkan satu import sehingga menjadi:

```python
import asyncio
import math
import pygame
```

`asyncio` sudah termasuk pustaka standar Python; tidak perlu menginstalnya dengan pip.

### Langkah 3 — Ubah definisi main

Ganti baris `def main():` menjadi:

```python
async def main():
    tinggi, kecepatan, pantulan, waktu, jeda = reset_simulasi()
```

Cuplikan ini hanya menunjukkan awal fungsi. **Pertahankan seluruh isi fungsi di bawahnya**, termasuk pengaturan gravitasi, restitusi, event keyboard, perhitungan fisika, dan penggambaran.

Fungsi `teks()`, `reset_simulasi()`, `gambar_latar()`, dan `gambar_bola()` tetap menggunakan `def` biasa karena tidak memerlukan `await`.

### Langkah 4 — Beri kesempatan browser bekerja pada setiap frame

Di dalam `while berjalan:`, cari `pygame.display.flip()`. Tambahkan tepat di bawahnya dengan indentasi yang sama:

```python
        pygame.display.flip()
        await asyncio.sleep(0)
```

Baris `await` harus berada **di dalam loop**, bukan setelah loop selesai. Pada kode ini letaknya juga di luar `if not jeda`, sehingga browser tetap menerima input ketika simulasi dijeda. Angka `0` menyerahkan giliran ke browser, bukan menghentikan simulasi selama satu detik. `jam.tick(FPS)` tetap dipakai untuk pengaturan frame desktop dan perhitungan `dt`.

Jika menambahkan loop menu tersendiri, pastikan loop tersebut juga memberi kesempatan browser bekerja. Hindari `time.sleep()` untuk jeda animasi; gunakan penghitung waktu atau `await asyncio.sleep(...)` sesuai kebutuhan.

### Langkah 5 — Ubah pemanggilan terakhir

Pada akhir kode asli:

```python
if __name__ == "__main__":
    main()
```

Ganti menjadi:

```python
if __name__ == "__main__":
    asyncio.run(main())
```

Jangan menambahkan pemanggilan `main()` kedua. Pertahankan `pygame.quit()` **di dalam fungsi `main`, setelah `while` selesai**. Jangan memindahkannya ke bawah `asyncio.run(main())`, karena pada runtime web baris itu dapat dieksekusi sebelum simulasi selesai.

### Langkah 6 — Samakan judul dan pilih font

Versi paket memakai `JUDUL = "Simulasi Jatuh Bebas dan Pantulan Bola"` untuk judul jendela dan tulisan di layar. Judul ini tidak memengaruhi perhitungan fisika.

Pemanggilan `pygame.font.SysFont("arial", ...)` pada kode asli bergantung pada font sistem. Paket memakai `pygame.font.Font(None, ...)` sebagai font bawaan. Jika perlu tampilan huruf tertentu, sertakan berkas TTF seperti pada bagian 2B.

| Bagian kode asli | Yang dilakukan |
| --- | --- |
| Konstanta, skala meter, ukuran layar | Dipertahankan. |
| Rumus tinggi, kecepatan, tumbukan | Dipertahankan. |
| Space, R, panah, Esc | Dipertahankan. |
| Loop utama | Diubah menjadi async dan ditambahkan yield setiap frame. |
| Judul dan font | Disesuaikan untuk nama program serta ketersediaan font browser. |

Setelah penyesuaian, ikuti tes desktop dan browser di bagian 3. **Berhasil di desktop belum membuktikan berhasil di browser.**

## 2B. Memasukkan gambar, suara, musik, dan font

Bagian ini berisi **contoh tambahan**, bukan aset yang sudah disertakan dalam paket. Sediakan berkasnya dahulu. Terapkan hanya contoh yang dibutuhkan; jangan menempel semua potongan sebagai satu program baru.

### 1. Siapkan folder aset

Buat folder `assets` **di dalam `game`**, lalu salin berkas menggunakan File Explorer. Contoh susunannya:

| Lokasi relatif terhadap folder proyek | Kegunaan |
| --- | --- |
| `game/main.py` | Program utama. |
| `game/assets/images/bola.png` | Gambar bola; PNG mendukung latar transparan. |
| `game/assets/images/latar.jpg` | Foto/latar simulasi. |
| `game/assets/audio/pantul.ogg` | Efek suara tumbukan singkat. |
| `game/assets/audio/musik.ogg` | Musik latar. |
| `game/assets/fonts/teks.ttf` | Font pilihan yang boleh dibagikan bersama proyek. |

Gunakan nama sederhana dengan huruf kecil. `bola.png` dan `Bola.png` dapat dianggap berbeda di web. Jangan menggunakan path pribadi seperti `C:/Users/Nama/Downloads/bola.png`.

Untuk target Pygbag, ikuti panduan audionya: gunakan **OGG**, misalnya hasil ekspor Ogg Vorbis. Konversi WAV/MP3 melalui editor/konverter audio; **mengganti nama `.mp3` menjadi `.ogg` bukan konversi**. Simpan berkas audio asli yang tidak digunakan di luar folder `game`.

### 2. Tentukan path berdasarkan lokasi main.py

Tambahkan import berikut di atas kode:

```python
from pathlib import Path
```

Kemudian, setelah bagian import dan sebelum aset dimuat, tambahkan:

```python
FOLDER_GAME = Path(__file__).resolve().parent
FOLDER_ASET = FOLDER_GAME / "assets"
```

Dengan demikian, ketika `main.py` dipanggil dari folder utama proyek, aset tetap dicari dari folder tempat `main.py` berada. Contoh selanjutnya memakai variabel ini.

### 3. Ganti bola lingkaran menjadi gambar

**Muat sekali**, setelah `layar = pygame.display.set_mode((LEBAR, TINGGI))` dan sebelum `main()` dijalankan:

```python
gambar_bola_aset = pygame.image.load(
    str(FOLDER_ASET / "images" / "bola.png")
).convert_alpha()
gambar_bola_aset = pygame.transform.smoothscale(
    gambar_bola_aset, (RADIUS * 2, RADIUS * 2)
)
```

`convert_alpha()` mempertahankan transparansi. Proses konversi dilakukan setelah mode layar dibuat. Diameter gambar mengikuti `RADIUS` agar ukuran visual sesuai bola pada simulasi.

Di fungsi `gambar_bola()`, pertahankan gambar bayangan. **Ganti tiga pemanggilan `pygame.draw.circle(...)`** dengan:

```python
    pusat = (500, int(y_bola))
    posisi_gambar = gambar_bola_aset.get_rect(center=pusat)
    layar.blit(gambar_bola_aset, posisi_gambar)
```

Pusat gambar mengikuti posisi bola. Rumus gerak dan tumbukan tetap menggunakan radius yang sama. Gambar sebaiknya persegi, dengan bola memenuhi area gambar agar tepi transparan tidak membuatnya terlihat melayang.

### 4. Tambahkan foto sebagai latar

Muat dan ubah ukuran sekali setelah mode layar dibuat:

```python
gambar_latar_aset = pygame.image.load(
    str(FOLDER_ASET / "images" / "latar.jpg")
).convert()
gambar_latar_aset = pygame.transform.smoothscale(
    gambar_latar_aset, (LEBAR, TINGGI)
)
```

Di awal fungsi `gambar_latar()`, **ganti** `layar.fill((237, 246, 255))` dengan:

```python
    layar.blit(gambar_latar_aset, (0, 0))
```

Pertahankan baris penggambaran skala dan tanah setelahnya. Latar akan berada di belakang keduanya; area tanah tetap ditutupi warna hijau. Menambahkan gambar sebelum `layar.fill()` tidak efektif karena akan tertutup kembali. Contoh ini meregangkan foto ke ukuran layar; pilih foto berasio serupa agar tidak tampak gepeng.

### 5. Bunyi ketika bola menyentuh tanah

Tambahkan inisialisasi berikut **di dalam `async def main()`, sebelum `while berjalan:`**. Berkas `pantul.ogg` harus sudah tersedia:

```python
    suara_pantul = None
    try:
        if pygame.mixer.get_init() is None:
            pygame.mixer.init()
        suara_pantul = pygame.mixer.Sound(
            str(FOLDER_ASET / "audio" / "pantul.ogg")
        )
        suara_pantul.set_volume(0.5)
    except (pygame.error, OSError) as error:
        print(f"Efek suara tidak tersedia: {error}")
```

Nilai volume berkisar 0–1. Jika pemuatan gagal, contoh ini menampilkan pesan dan tetap menjalankan simulasi tanpa efek suara.

Di kode fisika, cari cabang `if tinggi_baru <= 0:`. Tambahkan pemutaran di **awal cabang tersebut**, sebelum perhitungan `kecepatan_tumbukan`:

```python
            if tinggi_baru <= 0:
                if suara_pantul is not None:
                    suara_pantul.play()
                # Pertahankan perhitungan tumbukan yang sudah ada di sini.
```

Cuplikan ini hanya menunjukkan tempat penyisipan, **jangan menghapus perhitungan tumbukan di bawahnya**. Dengan posisi ini bunyi dipicu pada tumbukan, termasuk tumbukan terakhir. Jangan menaruh `play()` di bagian gambar yang dijalankan setiap frame karena suara akan terus ditumpuk.

### 6. Tambahkan musik latar setelah interaksi pengguna

Tambahkan pemuatan ini **di dalam `main()`, sebelum loop**. Bisa dipakai bersama efek suara atau sendiri:

```python
    musik_siap = False
    musik_dimulai = False
    try:
        if pygame.mixer.get_init() is None:
            pygame.mixer.init()
        pygame.mixer.music.load(
            str(FOLDER_ASET / "audio" / "musik.ogg")
        )
        pygame.mixer.music.set_volume(0.25)
        musik_siap = True
    except (pygame.error, OSError) as error:
        print(f"Musik tidak tersedia: {error}")
```

Lalu sisipkan kondisi berikut **tepat di bawah `for event in pygame.event.get():`, sebelum penanganan event yang sudah ada**. Ini merupakan tambahan, bukan pengganti kontrol Space/R/panah:

```python
            if (
                musik_siap
                and not musik_dimulai
                and (
                    event.type == pygame.MOUSEBUTTONDOWN
                    or (event.type == pygame.KEYDOWN
                        and event.key != pygame.K_ESCAPE)
                )
            ):
                pygame.mixer.music.play(-1)
                musik_dimulai = True
```

`-1` mengulang musik terus-menerus. Muat berkas sekali, lalu mulai setelah klik/tekan tombol; browser dapat membatasi audio sebelum interaksi. Klik lagi di area simulasi jika klik tombol peluncur belum diteruskan ke game. Contoh ini membiarkan musik berjalan saat simulasi dijeda; jika ingin ikut jeda, gunakan `pygame.mixer.music.pause()` dan `unpause()` pada penanganan Space. Saat keluar, `pygame.quit()` mengakhiri subsistem Pygame.

### 7. Pakai font sendiri

Setelah inisialisasi Pygame dan variabel path, **ganti** baris pembentukan font yang ingin diubah. Contoh pengganti `font_biasa`:

```python
font_biasa = pygame.font.Font(
    str(FOLDER_ASET / "fonts" / "teks.ttf"), 28
)
```

Pastikan berkas TTF ikut disalin. Jika tidak memerlukan font khusus, gunakan font bawaan `pygame.font.Font(None, 28)` tanpa aset tambahan.

### 8. Ikutkan aset ketika build dan upload

Jalankan kembali perintah pengujian dan build pada bagian 3–4 setelah perubahan. Pygbag mengemas aset dari folder proyek yang ditargetkan (`game`), bukan berkas di Downloads atau folder lain. File aset bisa berada di arsip internal hasil build; tidak harus terlihat sebagai `assets/` terpisah di ZIP akhir.

| Tujuan | Berkas yang ikut |
| --- | --- |
| GitHub | Kode serta seluruh `game/assets/` yang digunakan. |
| itch.io | `web.zip` hasil build terbaru yang sudah menyertakan aset. |
| Screenshot tutorial README | Tetap mengikuti path/URL gambar README; tidak menjadi aset game secara otomatis. |

Uji gambar tampil, suara tumbukan tidak berulang tanpa tumbukan, dan musik baru dimulai satu kali. Periksa Console browser bila aset gagal dimuat. Gunakan aset berukuran wajar dan sertakan kredit/lisensi aset bila diperlukan. Contoh tambahan ini belum diuji dengan berkas gambar/audio milik pengguna.

## 3. Menjalankan simulasi

### Tes desktop

Jalankan dari folder utama proyek:

```powershell
.\.venv\Scripts\python.exe game/main.py
```

Periksa gerak bola, Space, R, dan pengubahan parameter. Tutup jendela sebelum melanjutkan.

### Tes browser

```powershell
.\.venv\Scripts\python.exe -m pygbag game
```

Buka [http://localhost:8000](http://localhost:8000). Tunggu runtime selesai dimuat, lalu klik area simulasi. Gunakan Space untuk jeda dan R untuk mengulang.

Biarkan terminal tetap berjalan selama pengujian. Tekan **Ctrl+C** di terminal setelah selesai. Jangan membuka `index.html` melalui klik dua kali; gunakan server lokal.

## 4. Membuat ZIP web

Jalankan dari folder utama proyek:

```powershell
.\.venv\Scripts\python.exe -m pygbag --build --archive game
```

Setelah build berhasil, periksa **`game/build/web.zip`**. Arsip ini yang akan diunggah sebagai game browser. Di dalamnya harus ada `index.html` pada tingkat teratas bersama berkas hasil build lainnya.

![Panduan membedakan paket sumber dan ZIP web](docs/images/01-build.png)

*Diagram panduan, bukan screenshot aplikasi. Hasil build baru tersedia setelah perintah berhasil.*

Jika ZIP dibuat manual, kompres semua **isi** folder `game/build/web/`, bukan folder `web` pembungkusnya. Setelah kode diperbarui, lakukan pengujian dan build lagi.

## 5. Upload ke itch.io

Bagian ini memakai **screenshot asli dari tutorial Ajay Karat / devilsgarage di Construct.net**, berlisensi [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). Tutorial sumber diperbarui pada 19 Juni 2025; tata letak itch.io saat ini dapat berbeda. Gambar ditautkan langsung ke sumber dan memerlukan internet.

Screenshot sumber memakai contoh game Construct. Gunakan gambar untuk mengenali menu itch.io; untuk proyek Pygame ini tetap gunakan **`game/build/web.zip`**, judul **Simulasi Jatuh Bebas dan Pantulan Bola**, dan ukuran **1000 × 680**. Langkah ekspor Construct tidak digunakan.

[Buka tutorial sumber beserta semua screenshot](https://www.construct.net/en/tutorials/publish-c2c3-html5-game-itch-2363/page-3). Screenshot ditampilkan tanpa perubahan; penjelasan berbahasa Indonesia disesuaikan untuk program ini.

### A. Buat halaman proyek

Masuk ke [itch.io](https://itch.io/), buka dashboard, lalu buat proyek baru. Gunakan pengisian berikut:

![Screenshot menu Upload new project di itch.io, oleh devilsgarage](https://construct-static.com/images/v1740/uploads/articleuploadobject/0/images/36181/03upload1.jpg)

*Gambar 1 — Menu untuk membuat proyek baru. Sumber: Ajay Karat / devilsgarage, Construct.net, CC BY 4.0; tautan sumber dan lisensi di atas.*

| Bagian | Isi untuk proyek ini |
| --- | --- |
| Judul | Simulasi Jatuh Bebas dan Pantulan Bola |
| Jenis proyek | HTML / HTML Game |
| Deskripsi singkat | Simulasi interaktif gerak jatuh bebas dan pantulan dengan pengaturan gravitasi dan restitusi. |
| Harga | Pilih gratis/tanpa pembayaran untuk tugas yang dibagikan gratis. |

![Screenshot judul dan pilihan jenis proyek HTML di itch.io, oleh devilsgarage](https://construct-static.com/images/v1740/uploads/articleuploadobject/0/images/36182/04title.jpg)

*Gambar 2 — Perhatikan bagian judul dan jenis proyek HTML. Nama game pada screenshot hanya contoh sumber. Kredit: Ajay Karat / devilsgarage, CC BY 4.0.*

### B. Unggah hasil build

Pada bagian unggahan, pilih **`game/build/web.zip`**. Aktifkan opsi agar berkas dimainkan di browser jika tersedia. Jangan memilih ZIP paket sumber yang berisi README.

![Screenshot tombol Upload files di itch.io, oleh devilsgarage](https://construct-static.com/images/v1740/uploads/articleuploadobject/0/images/36184/05upload.png)

*Gambar 3 — Tombol untuk memilih berkas unggahan. Pilih `web.zip` hasil Pygbag. Kredit: Ajay Karat / devilsgarage, CC BY 4.0.*

![Screenshot opsi agar unggahan dimainkan di browser, oleh devilsgarage](https://construct-static.com/images/v1740/uploads/articleuploadobject/0/images/36186/06upload.jpg)

*Gambar 4 — Aktifkan opsi bermain di browser pada berkas hasil build. Kredit: Ajay Karat / devilsgarage, CC BY 4.0.*

Untuk tampilan sematan, gunakan lebar **1000** dan tinggi **680**. Pratinjau halaman: jika template menambahkan area di luar kanvas, sesuaikan tinggi sematan agar kontrol paling bawah tetap terlihat.

![Screenshot Embed options dan Viewport dimensions di itch.io, oleh devilsgarage](https://construct-static.com/images/v1740/uploads/articleuploadobject/0/images/36187/07embed.jpg)

*Gambar 5 — Atur ukuran sematan. Untuk program ini masukkan **1000 × 680**, bukan menyalin ukuran contoh screenshot. Kredit: Ajay Karat / devilsgarage, CC BY 4.0.*

### C. Pratinjau dan publikasikan

Simpan halaman dan pratinjau. Uji semua kontrol, lalu ubah visibilitas ke **Public** ketika sudah siap dibagikan. Simpan dan periksa tautannya melalui jendela privat agar akses orang lain ikut teruji.

![Ilustrasi alur pengecekan dan publikasi](docs/images/04-publikasi.png)

*Gambar di atas merupakan diagram ringkasan buatan untuk panduan ini, bukan screenshot situs.*

Cantumkan nama pembuat/kelompok, mata kuliah, cara menggunakan, batasan model, dan tautan repository GitHub pada deskripsi. Tidak perlu mengunggah data pribadi yang tidak diperlukan untuk tugas.

## 6. Menyimpan di GitHub

Buka repository tujuan, pilih **Add file → Upload files**, lalu unggah berkas proyek beserta folder `game` dan `docs`. Simpan melalui commit. Letakkan `README.md` di tingkat utama repository agar panduan mudah ditemukan.

**Folder `docs/images/` wajib ikut diunggah** untuk diagram lokal. Lima screenshot asli menggunakan URL sumber sehingga tidak perlu ikut diunggah, tetapi memerlukan internet dan ketersediaan situs sumber. Jika gambar sumber gagal dimuat, buka tautan tutorial sumber di awal bagian upload.

File `.gitignore` sudah disertakan. Jika memakai Git lokal, environment `.venv`, cache Python, dan hasil build dikecualikan. Untuk upload lewat website, pilih berkas dengan teliti: `.gitignore` tidak menyaring pilihan unggahan manual.

| Tujuan | Yang diunggah |
| --- | --- |
| GitHub | README, `game/main.py`, `requirements.txt`, `.gitignore`, dan `docs/images/`. |
| itch.io | Hasil build **`game/build/web.zip`**. |

## 7. Solusi masalah

| Masalah | Solusi |
| --- | --- |
| `python` tidak dikenali | Coba `py`; bila keduanya gagal, periksa instalasi Python dan buka ulang terminal. |
| `No module named pygame` atau `pygbag` | Ulangi instalasi requirements dengan Python dari `.venv` yang sama. |
| Instalasi gagal menghubungi server | Periksa koneksi internet/DNS lalu ulangi. Kegagalan koneksi tidak berarti paket tidak tersedia. |
| `main.py` tidak ditemukan | Periksa `game/main.py`, termasuk kemungkinan ekstensi tersembunyi `.txt`. |
| Browser masih loading | Muatan awal mengambil runtime. Periksa koneksi dan error di terminal/Console browser. |
| Tombol tidak merespons | Klik area kanvas; pastikan simulasi belum diakhiri dengan Esc. |
| Setelah Esc layar tidak berjalan | Muat ulang halaman untuk menjalankan program kembali. |
| `index.html` tidak ditemukan di itch.io | Gunakan ZIP hasil build dan periksa tidak ada folder pembungkus tambahan. |
| Tampilan atau kontrol bawah terpotong | Periksa sematan 1000 × 680 dan tinggi tambahan bila template memerlukannya. |
| README tidak menampilkan gambar | Unggah `docs/images/` dengan struktur dan huruf nama yang sama. |
| Aset game `FileNotFoundError` | Periksa `game/assets/`, nama dan ekstensi berkas, serta path berbasis `__file__` pada bagian 2B. |
| PNG kehilangan transparansi | Muat setelah mode layar dibuat dan gunakan `convert_alpha()`. |
| Audio ditolak saat build | Konversi audio ke OGG; jangan hanya mengganti ekstensi. |
| Suara tidak terdengar di browser | Klik area simulasi, periksa volume tab/perangkat, lalu baca pesan mixer/Console. |
| Suara terus terulang atau bertumpuk | Panggil efek pada event tumbukan; jangan memanggil `play()` setiap frame. |

## Checklist sebelum mengumpulkan

- [ ] Simulasi desktop dapat berjalan.
- [ ] Simulasi berjalan di browser lokal.
- [ ] `web.zip` berasal dari build terbaru.
- [ ] Halaman itch.io dapat dibuka tanpa login pemilik.
- [ ] Space, R, dan tombol pengubah parameter berfungsi.
- [ ] Judul, deskripsi, nama kelompok, dan tautan kode sudah diisi.
- [ ] Gambar tutorial tampil pada README GitHub.

## Referensi

- **Sumber screenshot:** Ajay Karat / devilsgarage, [Publish a C2/C3 HTML5 game to itch.io — Create an Edit Game page](https://www.construct.net/en/tutorials/publish-c2c3-html5-game-itch-2363/page-3), diperbarui 19 Juni 2025, [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). Gambar asli tidak diedit. Penggunaan gambar tidak menyiratkan dukungan penulis terhadap proyek ini.
- **Referensi video tambahan:** [Exporting Pygame Games to Web — YouTube](https://www.youtube.com/watch?v=7-cpaJyS-PM). Bagian upload disebut mulai [04:16](https://www.youtube.com/watch?v=7-cpaJyS-PM&t=256s) pada deskripsi hasil pencarian. Video ini menjadi tautan pelengkap; cuplikan video tidak disalin ke paket.
- [Panduan upload itch.io dari dokumentasi Pygbag](https://pygame-web.github.io/wiki/publishing/itch.io/)

- [Panduan Pygbag](https://pygame-web.github.io/wiki/pygbag/)
- [Pygame: memuat gambar](https://www.pygame.org/docs/ref/image.html)
- [Pygame: efek suara dan mixer](https://www.pygame.org/docs/ref/mixer.html)
- [Pygame: musik latar](https://www.pygame.org/docs/ref/music.html)
- [Pygame: font](https://www.pygame.org/docs/ref/font.html)
- [Pygbag: opsi build dan archive](https://github.com/pygame-web/pygbag)
- [Upload HTML5 di itch.io](https://itch.io/docs/creators/html5)
- [Pembuatan halaman itch.io](https://itch.io/docs/creators/getting-started)
- [Python virtual environments](https://docs.python.org/3/library/venv.html)
- [Mengunggah berkas ke GitHub](https://docs.github.com/en/repositories/working-with-files/managing-files/adding-a-file-to-a-repository)

Panduan disusun pada 13 November 2026 berdasarkan program yang diberikan pengguna.
