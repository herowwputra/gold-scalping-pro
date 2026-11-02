# GOLD SCALPING PRO v3 — kerangka koneksi MT4 + MT5 (akun DEMO)

## Status yang jujur
- Dashboard PWA: siap dipublikasikan sebagai website statis.
- Backend API: contoh server siap dijalankan/deploy.
- EA MT4 dan EA MT5: source awal untuk mengirim tick ke backend melalui HTTPS.
- **Belum live/terhubung** sampai backend dideploy, URL + API key diatur, EA dikompilasi dan dijalankan pada terminal desktop MT4/MT5.
- Tidak ada order yang dikirim oleh EA ini. Hanya mengirim data harga.

## File
- `index.html`, `app.js`, `manifest.webmanifest`, `sw.js`, `icon.svg`: dashboard PWA.
- `backend/server.py`: API penerima tick dan endpoint data dashboard.
- `backend/requirements.txt`: dependensi Python.
- `bridge/MT4/GSP_Bridge_MT4.mq4`: EA pengirim tick MT4.
- `bridge/MT5/GSP_Bridge_MT5.mq5`: EA pengirim tick MT5.

## Cara kerja
1. Website statis (misalnya GitHub Pages) menampilkan dashboard.
2. Backend HTTPS menerima tick dari EA MT4/MT5.
3. EA berjalan pada terminal desktop MetaTrader di Windows PC/VPS yang terus menyala.
4. Dashboard memilih feed MT4 atau MT5. Kedua EA boleh mengirim ke backend yang sama.

## Menjalankan backend secara lokal (untuk pengembang)
```bash
cd backend
pip install -r requirements.txt
# Buat API key acak panjang dan set environment variable GSP_API_KEY
python -c "import secrets; print(secrets.token_urlsafe(32))"
# Linux/macOS: export GSP_API_KEY='KEY_RAHASIA'
# Windows PowerShell: $env:GSP_API_KEY='KEY_RAHASIA'
python server.py
```
Backend berjalan pada port 8080. Untuk deployment publik gunakan hosting backend HTTPS yang mendukung Python. GitHub Pages hanya untuk file website; tidak menjalankan backend Python. Paket gratis backend bisa tidur/terbatas sehingga bukan jaminan koneksi tanpa putus.

## Pengaturan EA MT4/MT5
1. Buka terminal desktop MT4/MT5 pada Windows PC/VPS.
2. Buka MetaEditor, buat/masukkan file EA sesuai folder platform, lalu compile.
3. Pada terminal, buka Tools → Options → Expert Advisors → centang izin WebRequest dan tambahkan URL dasar backend, misalnya `https://domain-backend-anda`.
4. Pasang EA pada chart XAUUSD. Isi `ApiBaseUrl` dan `ApiKey` pada Inputs.
5. Pastikan tombol Algo Trading/AutoTrading aktif. EA ini hanya mengirim harga, bukan membuka/menutup posisi.

## Keamanan
- Jangan pernah memasukkan nomor akun, password trading, investor password, atau kredensial HFM ke website, GitHub, atau chat.
- `GSP_API_KEY` di backend harus sama dengan `ApiKey` pada EA. Jangan commit API key asli ke repository. Ganti key jika bocor.
- Gunakan akun DEMO untuk pengujian.

## Keterbatasan penting untuk pengguna HP saja
Aplikasi MT4/MT5 versi iPhone/Android tidak menjalankan EA/bridge MQL. Agar feed akun HFM MT4 dan MT5 terkirim terus-menerus, diperlukan Windows PC/VPS yang menjalankan terminal desktop dan EA. VPS Windows gratis yang stabil untuk kebutuhan ini tidak dapat dijanjikan; program VPS gratis broker biasanya memiliki syarat kelayakan akun.

## Format API
- `GET /health` — status server.
- `POST /api/bridge/tick` — menerima `{platform,symbol,bid,ask,time_utc}` dengan header `X-API-Key`.
- `GET /api/market?platform=mt4` atau `mt5` — membaca tick terbaru.

Belum ada indikator/sinyal BUY/SELL aktif di versi ini. Sinyal baru boleh dihitung setelah data candle historis dan tick tervalidasi tersedia. Jangan menganggap WAIT/indikator kosong sebagai sinyal trading.
