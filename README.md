# AppLocker

## Deskripsi Aplikasi
Mau nugas tapi kegoda buat login? Kunci aja pakai **AppLocker**.

> Q: Lah kenapa nggak uninstall aja?  
> A: Ntar TBW SSD kalian nambah pas install lagi njir awokawok.

![alt text](image.png)

<!-- AppLocker bantu kamu tetap fokus dengan cara memblokir aplikasi tertentu selama waktu yang kamu tentukan. Cocok buat mahasiswa yang butuh mode "NO DISTRACTION" tapi nggak mau uninstall game kesayangan 😎. -->

## Setup
1. Pastikan Python sudah terinstall.
2. Jalankan `requirements.bat` & `install.bat`.
3. Tambahkan path `/applocker/dist/` ke dalam **Environment Variable > PATH** _(opsional)_.

## Huh?

| File               | Fungsi                                                                 |
|--------------------|------------------------------------------------------------------------|
| `applocker.exe`       | command dispatcher utama untuk AppLocker CLI.  |
| `addapp.exe`       | Menambahkan aplikasi ke daftar aplikasi yang akan dikunci.             |
| `runapp.exe`       | Menjalankan background monitoring + system tray untuk AppLocker.       |
| `listapp.exe`      | Melihat dan menghapus aplikasi yang dikunci.       |

### Contoh Penggunaan `applocker.exe`
```bash
applocker -p "C:\Games\valorant.exe" -d 1 -h 2 -m 30
```
> Mengunci *Valorant* selama 1 hari, 2 jam, dan 30 menit.

### Command tambahan:
- `applocker list` — Menampilkan semua aplikasi yang sedang dikunci.
- `applocker del <id>` — Menghapus aplikasi dari daftar berdasarkan ID.
---
**Catatan:** Masih dalam pengembangan.
