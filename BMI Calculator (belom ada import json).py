# ==========================================
# Program: Kalkulator BMI (Body Mass Index)
# Versi: Interaktif + Simpan File + Grafik
# ==========================================

import matplotlib.pyplot as plt

class Pengguna:
    def __init__(self, nama, berat, tinggi, umur):
        self.nama = nama
        self.berat = berat
        self.tinggi = tinggi
        self.umur = umur

    def hitung_bmi(self):
        return self.berat / (self.tinggi / 100) ** 2

    def kategori_bmi(self):
        bmi = self.hitung_bmi()
        if bmi < 18.5:
            return "Kurus"
        elif 18.5 <= bmi < 25:
            return "Ideal"
        elif 25 <= bmi < 30:
            return "Gemuk"
        else:
            return "Obesitas"

    def saran_kesehatan(self):
        kategori = self.kategori_bmi()
        if kategori == "Kurus":
            return "💡 Disarankan untuk meningkatkan asupan kalori dan olahraga untuk membentuk massa otot."
        elif kategori == "Ideal":
            return "✅ Pertahankan pola makan sehat dan rutin berolahraga untuk menjaga berat badan ideal."
        elif kategori == "Gemuk":
            return "⚠️ Cobalah mengurangi asupan kalori dan tingkatkan aktivitas fisik secara teratur."
        else:
            return "🚨 Disarankan untuk berkonsultasi dengan dokter untuk program penurunan berat badan yang sehat."

    def tampilkan_hasil(self):
        bmi = self.hitung_bmi()
        print(f"\nNama: {self.nama}")
        print(f"Umur: {self.umur} tahun")
        print(f"Berat: {self.berat} kg, Tinggi: {self.tinggi} cm")
        print(f"Hasil BMI: {bmi:.2f}")
        print(f"Kategori: {self.kategori_bmi()}")
        print(f"Saran: {self.saran_kesehatan()}\n")

    def to_string(self):
        return (f"Nama: {self.nama}, Umur: {self.umur} tahun, "
                f"Berat: {self.berat} kg, Tinggi: {self.tinggi} cm, "
                f"BMI: {self.hitung_bmi():.2f}, "
                f"Kategori: {self.kategori_bmi()}")


def simpan_riwayat(pengguna_list):
    if not pengguna_list:
        print("\nBelum ada data untuk disimpan.")
        return

    with open("riwayat_bmi.txt", "a", encoding="utf-8") as file:
        file.write("\n=== Riwayat Perhitungan BMI ===\n")
        for pengguna in pengguna_list:
            file.write(pengguna.to_string() + "\n")

    print("\n✅ Riwayat telah disimpan ke file 'riwayat_bmi.txt'.\n")


def tampilkan_grafik(pengguna_list):
    if not pengguna_list:
        print("\n⚠️ Tidak ada data untuk ditampilkan di grafik.")
        return

    nama_list = [p.nama for p in pengguna_list]
    bmi_list = [p.hitung_bmi() for p in pengguna_list]
    kategori_colors = {
        "Kurus": "skyblue",
        "Ideal": "limegreen",
        "Gemuk": "orange",
        "Obesitas": "red"
    }
    colors = [kategori_colors[p.kategori_bmi()] for p in pengguna_list]

    plt.figure(figsize=(8, 5))
    plt.bar(nama_list, bmi_list, color=colors)
    plt.axhline(18.5, color='blue', linestyle='--', label="Kurus/Ideal")
    plt.axhline(25, color='green', linestyle='--', label="Ideal/Gemuk")
    plt.axhline(30, color='red', linestyle='--', label="Gemuk/Obesitas")
    plt.title("Grafik BMI Pengguna")
    plt.xlabel("Nama Pengguna")
    plt.ylabel("Nilai BMI")
    plt.legend()
    plt.tight_layout()
    plt.show()


def menu():
    pengguna_list = []

    while True:
        print("\n================================")
        print("     🧮 KALKULATOR BMI INTERAKTIF  ")
        print("================================")
        print("1. Hitung BMI baru")
        print("2. Tampilkan semua riwayat BMI")
        print("3. Simpan riwayat ke file")
        print("4. Tampilkan grafik BMI")
        print("5. Keluar program")
        print("================================")

        pilihan = input("Pilih menu (1-5): ").strip()

        if pilihan == "1":
            try:
                nama = input("\nMasukkan nama: ")
                berat = float(input("Masukkan berat badan (kg): "))
                tinggi = float(input("Masukkan tinggi badan (cm): "))
                umur = int(input("Masukkan umur: "))

                pengguna = Pengguna(nama, berat, tinggi, umur)
                pengguna.tampilkan_hasil()
                pengguna_list.append(pengguna)

            except ValueError:
                print("⚠️ Input tidak valid! Pastikan angka dimasukkan dengan benar.")

        elif pilihan == "2":
            if not pengguna_list:
                print("\nBelum ada data yang dihitung.")
            else:
                print("\n=== Riwayat BMI ===")
                for i, pengguna in enumerate(pengguna_list, 1):
                    print(f"{i}. {pengguna.to_string()}")

        elif pilihan == "3":
            simpan_riwayat(pengguna_list)

        elif pilihan == "4":
            tampilkan_grafik(pengguna_list)

        elif pilihan == "5":
            print("\nTerima kasih telah menggunakan Kalkulator BMI. 👋")
            break

        else:
            print("⚠️ Pilihan tidak valid. Silakan pilih antara 1-5.")


if __name__ == "__main__":
    menu()
