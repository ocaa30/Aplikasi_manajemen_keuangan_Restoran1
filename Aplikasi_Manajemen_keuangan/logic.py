import csv
from tkinter import messagebox
import os

CSV_FILE = "data_keuangan.csv"

def tambah(nama, jenis, jumlah, tanggal):
    if not (nama and jenis and jumlah and tanggal):
        messagebox.showwarning("Peringatan", "Semua kolom harus diisi.")
        return
    try:
        jumlah = float(jumlah)
    except ValueError:
        messagebox.showerror("Error", "Jumlah harus angka.")
        return
    with open(CSV_FILE, 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([nama, jenis, jumlah, tanggal])
    messagebox.showinfo("Sukses", "Data ditambahkan.")

def baca_semua():
    if not os.path.exists(CSV_FILE):
        return []
    with open(CSV_FILE, 'r') as f:
        return list(csv.reader(f))

def hapus(index):
    data = baca_semua()
    if 0 <= index < len(data):
        data.pop(index)
        with open(CSV_FILE, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerows(data)
        messagebox.showinfo("Sukses", "Data dihapus.")

def update(index, nama, jenis, jumlah, tanggal):
    data = baca_semua()
    if not (nama and jenis and jumlah and tanggal):
        messagebox.showwarning("Peringatan", "Semua kolom harus diisi.")
        return
    try:
        jumlah = float(jumlah)
    except ValueError:
        messagebox.showerror("Error", "Jumlah harus angka.")
        return
    if 0 <= index < len(data):
        data[index] = [nama, jenis, jumlah, tanggal]
        with open(CSV_FILE, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerows(data)
        messagebox.showinfo("Sukses", "Data diperbarui.")
