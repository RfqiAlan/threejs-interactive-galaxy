import os
import glob
try:
    from PIL import Image
    from pillow_heif import register_heif_opener
except ImportError:
    print("Error: Library belum terinstall.")
    print("Silakan jalankan perintah ini di terminal VSCode-mu:")
    print("pip install Pillow pillow-heif")
    exit(1)

# Daftarkan HEIF opener agar Pillow bisa membaca file HEIC Apple
register_heif_opener()

def convert_and_compress():
    # Folder tempat kamu menaruh foto HEIC asli 
    SOURCE_DIR = "./raw_photos" 
    
    # Folder tujuan (otomatis akan diletakkan di assets website)
    TARGET_DIR = "./assets/images"
    
    # Maksimal ukuran pixel (agar ukurannya kecil tapi tetap tajam)
    MAX_SIZE = (1000, 1000)
    
    # Buat folder sumber jika belum ada
    if not os.path.exists(SOURCE_DIR):
        os.makedirs(SOURCE_DIR)
        print(f"Folder '{SOURCE_DIR}' telah dibuat.")
        print(f"Silakan pindahkan semua foto HEIC dari HP-mu ke dalam folder '{SOURCE_DIR}', lalu jalankan ulang script ini!")
        return
        
    if not os.path.exists(TARGET_DIR):
        os.makedirs(TARGET_DIR)

    # Cari semua file gambar di folder sumber
    valid_extensions = ['*.heic', '*.HEIC', '*.jpg', '*.JPG', '*.jpeg', '*.JPEG', '*.png', '*.PNG']
    heic_files = []
    for ext in valid_extensions:
        heic_files.extend(glob.glob(os.path.join(SOURCE_DIR, ext)))
    
    if not heic_files:
        print(f"Tidak ada file gambar ditemukan di dalam folder '{SOURCE_DIR}'.")
        return

    print(f"Ditemukan {len(heic_files)} foto. Mulai mengonversi...")

    for i, file_path in enumerate(heic_files, start=1):
        try:
            print(f"Memproses {i}/{len(heic_files)}: {os.path.basename(file_path)}")
            
            # Buka foto HEIC
            img = Image.open(file_path)
            
            # Ubah orientasi secara otomatis jika perlu (karena foto HP sering miring kalau dibaca python)
            from PIL import ImageOps
            img = ImageOps.exif_transpose(img)
            
            # Kecilkan ukuran maksimal ke 1000x1000px (tetap proporsional)
            img.thumbnail(MAX_SIZE, Image.Resampling.LANCZOS)
            
            # Karena format JPEG tidak mendukung transparansi, pastikan modenya RGB
            if img.mode != 'RGB':
                img = img.convert('RGB')
                
            # Tentukan nama file tujuan: b1.jpg, b2.jpg, dst
            target_name = f"b{i}.jpg"
            target_path = os.path.join(TARGET_DIR, target_name)
            
            # Simpan dan kompres sebagai JPEG (Quality 75 terbukti bagus dan ukurannya sangat kecil)
            img.save(target_path, format="JPEG", quality=75, optimize=True)
            
        except Exception as e:
            print(f"Gagal memproses {file_path}: {e}")
            
    print("\n✅ SELESAI!")
    print(f"Semua foto berhasil di-convert, dikompres, dan disimpan dengan nama b1.jpg, b2.jpg, dst di folder '{TARGET_DIR}'.")
    print("\n👉 JANGAN LUPA: Karena ekstensinya sekarang '.jpg', kamu harus mengubah tulisan '.png' menjadi '.jpg' di file js/imageRing.js dan index.html!")

if __name__ == "__main__":
    convert_and_compress()
