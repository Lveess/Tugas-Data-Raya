# ==========================================
# Program: Kalkulator BMI (Body Mass Index)
# ==========================================

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

    def tampilkan_hasil(self):
        print(f"\nNama: {self.nama}")
        print(f"Umur: {self.umur} tahun")
        print(f"Berat: {self.berat} kg, Tinggi: {self.tinggi} cm")
        print(f"Hasil BMI: {self.hitung_bmi():.2f}")
        print(f"Kategori: {self.kategori_bmi()}")


def hitung_bmi():
    print("=== Kalkulator BMI (Body Mass Index) ===")
    jumlah = int(input("Berapa banyak pengguna yang ingin dihitung? "))

    for i in range(jumlah):
        print(f"\n--- Data Pengguna ke-{i+1} ---")
        nama = input("Masukkan nama: ")
        berat = float(input("Masukkan berat badan (kg): "))
        tinggi = float(input("Masukkan tinggi badan (cm): "))
        umur = int(input("Masukkan umur: "))

        pengguna = Pengguna(nama, berat, tinggi, umur)
        pengguna.tampilkan_hasil()


if __name__ == "__main__":
    hitung_bmi()
