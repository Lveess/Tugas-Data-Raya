# ==========================================
# Program: Kalkulator BMI (Body Mass Index)
# Versi: SQLite3 Database + Ekspor CSV/JSON (No External Libs)
# ==========================================

import sqlite3
import json
import csv
import os

DB_FILE = "bmi_data.db"


# ==========================================
# Setup Database
# ==========================================
def init_db():
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS pengguna_bmi (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nama TEXT,
            umur INTEGER,
            berat REAL,
            tinggi REAL,
            bmi REAL,
            kategori TEXT
        )
    """)
    conn.commit()
    conn.close()


# ==========================================
# Kelas Pengguna
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
        bmi = self.hitung_bmi()
        print(f"\nNama: {self.nama}")
        print(f"Umur: {self.umur} tahun")
        print(f"Berat: {self.berat} kg, Tinggi: {self.tinggi} cm")
        print(f"Hasil BMI: {bmi:.2f}")
        print(f"Kategori: {self.kategori_bmi()}")

    def simpan_ke_db(self):
        conn = sqlite3.connect(DB_FILE)
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO pengguna_bmi (nama, umur, berat, tinggi, bmi, kategori)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (self.nama, self.umur, self.berat, self.tinggi, self.hitung_bmi(), self.kategori_bmi()))
        conn.commit()
        conn.close()


# ==========================================
# Fungsi Database
# ==========================================
def tampilkan_semua_data():
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    cur.execute("SELECT * FROM pengguna_bmi")
    data = cur.fetchall()
    conn.close()

    if not data:
        print("\n⚠️ Tidak ada data tersimpan.")
    else:
        print("\n=== Riwayat BMI dari Database ===")
        for d in data:
            print(f"{d[0]}. {d[1]} | Umur: {d[2]} | Berat: {d[3]} kg | Tinggi: {d[4]} cm | BMI: {d[5]:.2f} | {d[6]}")


def hapus_semua_data():
    konfirmasi = input("⚠️ Yakin ingin menghapus semua data? (y/n): ").lower().strip()
    if konfirmasi == "y":
        conn = sqlite3.connect(DB_FILE)
        cur = conn.cursor()
        cur.execute("DELETE FROM pengguna_bmi")
        conn.commit()
        conn.close()
        print("🗑️ Semua data telah dihapus dari database.")
    else:
        print("❎ Penghapusan dibatalkan.")


# ==========================================
# Fungsi Ekspor
# ==========================================
def ekspor_csv():
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    cur.execute("SELECT nama, umur, berat, tinggi, bmi, kategori FROM pengguna_bmi")
    data = cur.fetchall()
    conn.close()

    if not data:
        print("\n⚠️ Tidak ada data untuk diekspor.")
        return

    with open("riwayat_bmi.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Nama", "Umur", "Berat (kg)", "Tinggi (cm)", "BMI", "Kategori"])
        writer.writerows(data)
    print("✅ Data berhasil diekspor ke 'riwayat_bmi.csv'")


def ekspor_json():
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    cur.execute("SELECT nama, umur, berat, tinggi, bmi, kategori FROM pengguna_bmi")
    data = cur.fetchall()
    conn.close()

    if not data:
        print("\n⚠️ Tidak ada data untuk diekspor.")
        return

    json_data = []
    for row in data:
        json_data.append({
            "Nama": row[0],
            "Umur": row[1],
            "Berat (kg)": row[2],
            "Tinggi (cm)": row[3],
            "BMI": round(row[4], 2),
            "Kategori": row[5]
        })

    with open("riwayat_bmi.json", "w", encoding="utf-8") as f:
        json.dump(json_data, f, indent=4, ensure_ascii=False)
    print("✅ Data berhasil diekspor ke 'riwayat_bmi.json'")


# ==========================================
# Menu Utama
# ==========================================
def menu():
    init_db()

    while True:
        print("\n================================")
        print("     🧮 KALKULATOR BMI (SQLite3)  ")
        print("================================")
        print("1. Hitung & Simpan BMI baru")
        print("2. Lihat semua data dari database")
        print("3. Ekspor data (CSV / JSON)")
        print("4. Hapus semua data di database")
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
                pengguna.simpan_ke_db()
                print("✅ Data telah disimpan ke database.")

            except ValueError:
                print("⚠️ Input tidak valid! Pastikan angka dimasukkan dengan benar.")

        elif pilihan == "2":
            tampilkan_semua_data()

        elif pilihan == "3":
            print("\n1. CSV\n2. JSON")
            sub = input("Pilih format ekspor (1/2): ").strip()
            if sub == "1":
                ekspor_csv()
            elif sub == "2":
                ekspor_json()
            else:
                print("⚠️ Pilihan tidak valid.")

        elif pilihan == "4":
            hapus_semua_data()

        elif pilihan == "5":
            print("\nTerima kasih telah menggunakan Kalkulator BMI. 👋")
            break

        else:
            print("⚠️ Pilihan tidak valid. Silakan pilih antara 1-5.")


if __name__ == "__main__":
    menu()
