# AppLocker

## Deskripsi Aplikasi
AppLocker adalah aplikasi sederhana yang dibuat untuk membantu menjaga fokus saat ujian atau tugas penting lainnya. Terkadang, kita merasa teralihkan dengan keinginan untuk bermain game, bahkan saat kita sedang membutuhkan konsentrasi untuk ujian. Bukannya hanya meng-uninstall game, yang bisa mempengaruhi umur SSD karena harus mengunduh ulang, AppLocker memungkinkan Anda untuk mengunci aplikasi tertentu untuk jangka waktu tertentu.

Aplikasi ini dapat digunakan untuk mengunci aplikasi agar tidak bisa dijalankan sampai waktu yang telah ditentukan. Jadi, Anda tidak perlu khawatir lagi tentang tergoda untuk bermain game selama ujian atau tugas penting lainnya!

## Fitur
- Menambahkan aplikasi ke daftar kunci dengan waktu tertentu (misalnya 1 hari, 2 jam, 30 menit).
- Menampilkan daftar aplikasi yang sedang dikunci.
- Menghapus aplikasi dari daftar kunci.
- Menampilkan notifikasi Windows ketika aplikasi yang dikunci dijalankan, memberitahukan bahwa aplikasi tersebut sedang dikunci.
- Secara otomatis memantau aplikasi yang sedang berjalan dan menghentikan aplikasi yang ada di daftar kunci.

## Daftar Perintah

```
applocker -p C:\path\to\program.exe -d hari -h jam -m menit
```
```
applocker list
```
```
applocker del list_num
```
```
applocker run
```

## Setup
1. Pastikan Python sudah terinstall di sistem Anda.
2. Jalankan setup.bat
3. Tambahkan ke dalam PATH environment variable untuk kemudahan.

## Catatan
Aplikasi ini sedang dalam pengembangan. Beberapa fitur mungkin mengalami perubahan dan peningkatan di masa mendatang.