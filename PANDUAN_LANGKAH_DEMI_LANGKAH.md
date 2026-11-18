# HADIRIN — Panduan instalasi dan penggunaan

Paket aplikasi mandiri untuk pilot lokal dan pengembangan skripsi. Backend FastAPI, database SQLite, frontend HTML/CSS/JavaScript, dan Isolation Forest scikit-learn. Bukan patch untuk kode Laravel lama. Tidak membutuhkan API AI berbayar. Belum dipublikasikan ke internet.

## 1. Persiapan Windows

1. Instal Python 3.11 atau 3.12 dari https://www.python.org/downloads/ . Centang **Add Python to PATH** dan sertakan Python Launcher.
2. Ekstrak seluruh ZIP, misalnya ke `D:\HADIRIN`. Jangan menjalankan langsung dari dalam ZIP.
3. Buka folder sampai terlihat `app.py`, `requirements.txt`, dan `MULAI_WINDOWS.bat`.
4. Klik dua kali `MULAI_WINDOWS.bat`. Pertama kali diperlukan internet untuk mengunduh dependensi.
5. Tunggu tulisan `Uvicorn running on http://127.0.0.1:8000`. Biarkan jendela terminal terbuka.
6. Buka http://localhost:8000 . Jika browser terbuka terlalu awal, muat ulang setelah server siap.

Alternatif manual: buka PowerShell pada folder aplikasi, kemudian jalankan satu per satu:

```powershell
py -3 -m venv .venv
.venv\Scripts\python.exe -m pip install -r requirements.txt
.venv\Scripts\python.exe -m uvicorn app:app --host 127.0.0.1 --port 8000
```

Tidak perlu mengaktifkan virtual environment; perintah langsung di atas menghindari masalah execution policy PowerShell.

## 2. Membuat admin

1. Pada kunjungan pertama, isi nama admin, email dan password minimal 10 karakter.
2. Klik **Buat akun admin**. Sistem membuat akun dan langsung memasukkan Anda.
3. Tidak ada password bawaan untuk database operasional.
4. Setup pertama hanya bisa dilakukan saat database kosong. Jangan membuka server di jaringan sebelum admin dibuat.

## 3. Mengatur jadwal dan lokasi

1. Buka **Jadwal & Lokasi**.
2. Isi nama kantor, latitude, longitude, radius meter, jam masuk WIB, serta toleransi keterlambatan.
3. Untuk memperoleh koordinat Anda, login sebagai karyawan dan gunakan **Periksa GPS**; atau salin koordinat kantor dari peta yang sudah Anda pastikan tepat.
4. Hari kerja berupa angka dipisah koma: `0,1,2,3,4` untuk Senin–Jumat; `0,1,2,3,4,5` untuk Senin–Sabtu.
5. Klik **Simpan pengaturan**. Server memvalidasi nilai.
6. Perubahan berlaku pada catatan berikutnya. Catatan lama menyimpan nama lokasi, hasil jarak, keterlambatan dan snapshot fitur pada saat dicatat.

## 4. Menambah karyawan

1. Buka **Karyawan**, isi nama, email, password awal dan peran Karyawan.
2. Simpan akun. Gunakan email unik.
3. Untuk menguji dua akun bersamaan, buka admin di jendela biasa dan karyawan di jendela samaran.
4. Admin dapat menonaktifkan akun. Sesi akun tersebut ikut dihapus. Akun sendiri tidak bisa dinonaktifkan dari menu ini.
5. Versi awal belum memiliki reset atau perubahan password mandiri. Gunakan akun pilot; pengelolaan password lanjutan perlu ditambahkan sebelum pemakaian organisasi.

## 5. Melakukan presensi

1. Login dengan akun karyawan, buka **Presensi**.
2. Klik **Aktifkan kamera**, izinkan kamera di browser, lalu **Ambil foto**.
3. Klik **Periksa GPS**, izinkan lokasi. Tunggu koordinat dan akurasi muncul.
4. Centang persetujuan pemrosesan foto/lokasi dan klik **Kirim presensi**.
5. Server memeriksa hari kerja, radius, akurasi maksimal 100 meter, foto JPEG, dan duplikasi.
6. Satu karyawan hanya dapat check-in satu kali per tanggal WIB. Waktu server adalah acuan; jam perangkat tidak dipercaya sebagai waktu pencatatan.
7. Lihat catatan di **Riwayat Saya**. Foto hanya bisa diakses pemilik dan admin terautentikasi.
8. Layanan ML tidak dipanggil saat check-in, sehingga kegagalan analitik tidak menghentikan pencatatan.

Kamera dan lokasi memerlukan localhost atau HTTPS. Membuka `http://IP-laptop:8000` dari HP biasanya tidak memenuhi secure context. Untuk HP, siapkan hosting HTTPS; jangan menganggap penggantian host menjadi `0.0.0.0` saja sudah cukup.

## 6. Mencoba model dengan data simulasi

Data demo adalah data SINTETIS, bukan hasil responden atau bukti hasil penelitian. Database demo terpisah dari database operasional. Tidak ada foto orang di dalam data demo.

1. Hentikan server dengan Ctrl+C.
2. Jalankan:

```powershell
.venv\Scripts\python.exe seed_demo.py
$env:HADIRIN_DATA="demo_data"
.venv\Scripts\python.exe -m uvicorn app:app --host 127.0.0.1 --port 8000
```

3. Buka http://localhost:8000 . Jika ada sesi lama, keluar lalu login lagi.
4. Admin demo: `admin@demo.local`, password `DemoHadirin2026!`.
5. Karyawan demo: `user1@demo.local` sampai `user5@demo.local`, password sama.
6. Buka **Model ML**, klik **Jalankan analisis**.
7. Generator menyiapkan 175 catatan. Model pertama memakai 122 catatan awal, dan 53 catatan berikutnya dapat dinilai. Data baseline tetap bertuliskan Belum dinilai / baseline.
8. Buka **Pusat Anomali**, periksa catatan yang ditandai; jumlah indikasi bukan metrik akurasi.
9. Generator menolak menimpa database demo yang sudah ada. Untuk mengulang, hentikan server dan pindahkan folder `demo_data` terlebih dahulu.
10. Kembali ke data operasional dengan menghentikan server lalu:

```powershell
Remove-Item Env:HADIRIN_DATA
.venv\Scripts\python.exe -m uvicorn app:app --host 127.0.0.1 --port 8000
```

## 7. Analisis data operasional

1. Kumpulkan minimal 40 catatan valid. Angka ini adalah batas pilot perangkat lunak, bukan jaminan kecukupan sampel penelitian.
2. Klik **Jalankan analisis** di menu **Model ML**.
3. Model pertama menggunakan sekitar 70% catatan paling awal (minimal 30) untuk baseline kronologis.
4. Baseline dibekukan. Catatan setelah cutoff yang belum memiliki skor dinilai pada eksekusi berikutnya.
5. Snapshot fitur presensi dihitung dari waktu kini dan maksimum 30 catatan sebelumnya; tidak menggunakan data masa depan. Jarak delta memakai median riwayat lokasi bernama sama. Perubahan lokasi/jadwal perlu diperiksa admin.
6. Fitur: keterlambatan setelah toleransi; sin/cos jam; sin/cos hari; jarak; delta jarak; jumlah koordinat berulang; jarak hari dari presensi sebelumnya. Baseline pertama/gap pertama bernilai 0 dan perlu dipertimbangkan dalam interpretasi.
7. Model: 100 estimator, contamination auto, random_state 42. `decision_function` lebih rendah berarti lebih abnormal. Label -1 adalah indikasi; bukan vonis pelanggaran. Persentil dihitung relatif terhadap skor baseline dan bukan probabilitas.
8. Versi model, cutoff, parameter, fitur dan artefak joblib disimpan pada folder data. Jangan memuat berkas joblib dari sumber luar.
9. Versi awal belum menyediakan pelatihan ulang, uji sensitivitas parameter, evaluasi berlabel, scheduler atau queue. Eksekusi dilakukan manual dari admin. Riwayat audit mencatat eksekusi.

## 8. Review dan klarifikasi

1. Admin membuka **Pusat Anomali**. Tabel diurutkan dari skor paling rendah.
2. Gunakan pencarian, tanggal dan status untuk memfilter.
3. Buka detail, lihat foto bila tersedia, periksa konteks dan riwayat.
4. Klik **Catat review**; ketik salah satu status persis: `Wajar`, `Perlu klarifikasi`, atau `Ditindaklanjuti`.
5. Isi alasan. Sistem menyimpan status terakhir dan riwayat perubahan di audit.
6. Jika Perlu klarifikasi, karyawan membuka Riwayat Saya → detail → Kirim klarifikasi.
7. Admin membaca klarifikasi dan memperbarui keputusan. Klarifikasi tidak otomatis menjadi label training.
8. CSV dari menu Presensi berisi catatan, skor, versi model dan hasil review. Ekspor hanya untuk admin.

## 9. Pengujian

Jalankan pada terminal terpisah:

```powershell
.venv\Scripts\python.exe test_system.py
```

Uji otomatis memakai database sementara: setup sekali, login, role admin/karyawan, penolakan lokasi di luar radius, presensi sukses, penolakan duplikasi, akses foto, pembatasan ekspor, batas minimum ML dan penolakan Origin lintas domain. Paket juga sudah diperiksa untuk analisis kronologis 175 catatan sintetis, scoring 53 catatan dan penyimpanan review. Kamera/GPS perangkat nyata dan tampilan browser belum diuji otomatis; lakukan uji lapangan berikut:

- Kamera ditolak/diizinkan, GPS ditolak/diizinkan, akurasi buruk, presensi di dalam/luar radius.
- Karyawan mencoba URL foto catatan orang lain: harus ditolak.
- Karyawan menerima permintaan klarifikasi dan mengirim penjelasan.
- Tutup/buka ulang server: data harus tetap ada.
- Uji desktop dan layar HP melalui HTTPS.

## 10. Cadangan dan hosting

Hentikan server lalu salin seluruh folder `data` ke lokasi cadangan yang dibatasi akses. Folder itu berisi SQLite, foto privat, dan model; ketiganya perlu dicadangkan bersama. Data demo tersimpan dalam `demo_data`.

Untuk penggunaan online diperlukan server Python dengan disk persisten, domain HTTPS dan reverse proxy. Ini bukan aplikasi statis sehingga tidak dapat langsung dijalankan di GitHub Pages. Gunakan satu proses Uvicorn untuk pilot ini. Contoh perintah server:

```bash
COOKIE_SECURE=1 HADIRIN_DATA=/var/lib/hadirin .venv/bin/python -m uvicorn app:app --host 127.0.0.1 --port 8000
```

Buat folder data dan hak akses lebih dulu. Letakkan reverse proxy HTTPS di depannya, arahkan Host asli, batasi body 3 MB, tambahkan rate limit login serta monitoring. Pilih batas dan kebijakan retensi bersama organisasi. Jangan mengekspos dokumentasi API, port internal, folder data, akun demo, atau menyalin bukti foto ke direktori static.

Sebelum dipakai produksi, tambahkan rate limit aplikasi, reset password, retensi/penghapusan data, pengujian beban, kontrol persetujuan organisasi dan pengujian keamanan. Ini merupakan pilot fungsional, belum implementasi penuh seluruh rancangan dokumen.

## 11. Cakupan terhadap dokumen

Tersedia: login/session, hash password, role, pengelolaan akun dasar, satu jadwal/lokasi, check-in foto/GPS, validasi server, riwayat terfilter, snapshot fitur, Isolation Forest nyata, versi baseline, review, klarifikasi, CSV dan audit.

Belum tersedia: Laravel/PostgreSQL/Supabase Storage, multi-penugasan dengan riwayat masa berlaku, check-out, layanan ML terpisah, queue/retry/scheduler, notifikasi, manajemen model lengkap dan dashboard analitik khusus. Foto disimpan lokal privat dengan route terotorisasi. Tidak ada migrasi atau perubahan terhadap database HADIRIN lama.

Rujukan teknis:
- https://fastapi.tiangolo.com/deployment/manually/
- https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.IsolationForest.html

## 12. Menu Assistant — Generative Agent melalui Groq

Pembaruan ini menambahkan agent pelaporan dengan alur: permintaan pengguna → query agregasi terotorisasi di server → narasi Groq → laporan tersimpan. Agent tidak melakukan tindakan mandiri atau mengubah database presensi/review. Isolation Forest tetap menjadi model deteksi; LLM bertugas menyusun laporan, bukan mengganti hasil deteksi.

### Mengaktifkan Groq pada Windows

1. Ekstrak paket terbaru ke folder aplikasi. Jika memperbarui instalasi lama, pertahankan folder `data` dan `.env` milik Anda; jangan menimpa/menghapus data tersebut. Aplikasi membuat tabel laporan baru tanpa menghapus tabel lama.
2. Hentikan server (Ctrl+C), lalu jalankan instalasi dependensi kembali: `.venv\Scripts\python.exe -m pip install -r requirements.txt`.
3. Buat API key di https://console.groq.com/keys . Jangan mengirim API key melalui chat atau memasukkannya ke JavaScript.
4. Salin `.env.example` menjadi `.env` di folder yang sama dengan `app.py`. Di PowerShell: `Copy-Item .env.example .env` (hanya jika .env belum ada).
5. Buka `.env` memakai editor teks; isi secara lokal:

```dotenv
GROQ_API_KEY=isi_api_key_anda_di_sini
GROQ_MODEL=openai/gpt-oss-20b
COOKIE_SECURE=0
```

6. Simpan sebagai `.env`, bukan `.env.txt`. Di Windows aktifkan tampilan ekstensi nama file bila perlu.
7. Jalankan kembali `MULAI_WINDOWS.bat`, lalu login dan buka **Assistant**. Badge konfigurasi hanya berarti API key sudah diisi, bukan verifikasi koneksi atau kuota.
8. Pilih tanggal awal dan akhir (maksimal 366 hari), lalu isi permintaan. Contoh: "Buat laporan bulanan mengenai presensi, keterlambatan dan indikasi anomali. Pisahkan temuan dan rekomendasi."
9. Centang **Gunakan Groq**, lalu klik **Buat laporan**. Agregat presensi dan pertanyaan akan dikirim ke Groq. Foto, nama, email, koordinat mentah, alasan review, dan klarifikasi tidak disertakan oleh server. Jangan mengetik informasi pribadi dalam pertanyaan.
10. Periksa hasil dan panel angka sumber. Gunakan **Unduh TXT** untuk menyimpan laporan. Riwayat menampilkan maksimal 20 laporan terakhir yang dibuat oleh akun tersebut.
11. Jika ingin ringkasan tanpa layanan eksternal, hilangkan centang Groq. Ringkasan lokal berisi angka dan rekomendasi baku, bukan jawaban generatif atas pertanyaan bebas.

### Jenis laporan

- Ringkasan presensi per periode dan tren jumlah catatan per hari.
- Keterlambatan: jumlah, persentase dari catatan presensi, serta rata-rata menit pada catatan terlambat.
- Anomali: catatan yang sudah/belum dinilai, jumlah indikasi, jumlah indikasi menunggu review, versi model dan status review agregat.
- Rekomendasi peninjauan; tidak menyimpulkan sebab individual dari data agregat.

Admin memperoleh agregat seluruh organisasi. Karyawan hanya memperoleh agregat catatannya sendiri, terlepas dari isi pertanyaan. Pertanyaan yang meminta data di luar konteks tidak menambah akses. Prompt injection tidak membuka SQL atau tools karena model tidak diberikan kemampuan tersebut. Jawaban generatif tetap dapat keliru; panel angka sumber merupakan rujukan untuk pemeriksaan.

Data yang tersedia belum cukup untuk menghitung karyawan absen atau persentase kehadiran terhadap kewajiban kerja historis. Agent diarahkan menyatakan keterbatasan tersebut. Riwayat pertanyaan dan jawaban disimpan privat di database lokal; jangan menggunakan pertanyaan sebagai tempat menyimpan rahasia.

### Kendala dan pengujian

- Belum dikonfigurasi: periksa nama `.env` dan variabel `GROQ_API_KEY`, lalu restart server.
- Ringkasan lokal setelah memilih Groq: kemungkinan key/model tidak berlaku, kuota/rate limit, jaringan, timeout (35 detik), atau respons kosong. Periksa key dan model pada console Groq. Jangan membagikan log yang mengandung key.
- Model default `openai/gpt-oss-20b` dapat diganti melalui `GROQ_MODEL` sesuai model yang tersedia bagi akun Anda. Daftar model dan batas layanan dapat berubah; periksa https://console.groq.com/docs/models . Biaya/kuota mengikuti akun Groq.
- Tidak ada data: Groq tidak dipanggil. Pilih periode yang memuat catatan atau gunakan database demo.
- Permintaan dibatasi satu per akun per 10 detik, termasuk upaya yang gagal.
- Laporan tidak memakai histori chat sebagai konteks percakapan; setiap permintaan memakai agregat periode yang dipilih. Riwayat berfungsi sebagai arsip laporan.
- Uji: `.venv\Scripts\python.exe test_assistant.py` . Mencakup pembatasan data per role, isolasi riwayat, validasi periode, throttle, payload tanpa identitas, jalur Groq dengan mock, dan fallback saat timeout.
- Integrasi panggilan Groq telah diuji dengan mock; koneksi langsung menggunakan API key pengguna belum diuji. Tampilan menu baru juga perlu diperiksa di browser perangkat Anda.

Referensi integrasi: https://console.groq.com/docs/api-reference dan https://console.groq.com/docs/models . API key hanya dibaca oleh backend. Jangan ikut mengunggah `.env` ke repositori atau membagikannya dalam ZIP.
