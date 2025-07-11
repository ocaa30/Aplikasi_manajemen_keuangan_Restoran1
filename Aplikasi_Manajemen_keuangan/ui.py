import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from tkcalendar import DateEntry
from logic import tambah, baca_semua, hapus, update, CSV_FILE

def setup_ui(root):
    global entry_nama, combo_jenis, entry_jumlah, entry_tanggal, tree

    frame_input = tk.Frame(root)
    frame_input.pack(pady=10, padx=10, fill=tk.X)

    tk.Label(frame_input, text="Keterangan Transaksi").grid(row=0, column=0, sticky=tk.W)
    entry_nama = tk.Entry(frame_input)
    entry_nama.grid(row=0, column=1)

    tk.Label(frame_input, text="Jenis").grid(row=1, column=0, sticky=tk.W)
    combo_jenis = ttk.Combobox(frame_input, values=["Pemasukan", "Pengeluaran"])
    combo_jenis.grid(row=1, column=1)

    tk.Label(frame_input, text="Jumlah").grid(row=2, column=0, sticky=tk.W)
    entry_jumlah = tk.Entry(frame_input)
    entry_jumlah.grid(row=2, column=1)

    tk.Label(frame_input, text="Tanggal").grid(row=3, column=0, sticky=tk.W)
    entry_tanggal = DateEntry(frame_input, date_pattern='dd-mm-yyyy')
    entry_tanggal.set_date(datetime.today())
    entry_tanggal.grid(row=3, column=1)

    def reset():
        entry_nama.delete(0, tk.END)
        combo_jenis.set("")
        entry_jumlah.delete(0, tk.END)
        entry_tanggal.set_date(datetime.today())

    def tambah_data():
        tanggal_str = entry_tanggal.get_date().strftime('%d-%m-%Y')
        tambah(entry_nama.get(), combo_jenis.get(), entry_jumlah.get(), tanggal_str)
        tampilkan()
        reset()

    def update_data():
        selected = tree.selection()
        if selected:
            index = tree.index(selected)
            tanggal_str = entry_tanggal.get_date().strftime('%d-%m-%Y')
            update(index, entry_nama.get(), combo_jenis.get(), entry_jumlah.get(), tanggal_str)
            tampilkan()
            reset()

    def hapus_data():
        selected = tree.selection()
        if selected:
            index = tree.index(selected)
            hapus(index)
            tampilkan()
            reset()

    def pilih_item(event):
        selected = tree.selection()
        if selected:
            item = tree.item(selected)
            values = item['values']
            entry_nama.delete(0, tk.END)
            entry_nama.insert(0, values[0])
            combo_jenis.set(values[1])
            entry_jumlah.delete(0, tk.END)
            entry_jumlah.insert(0, values[2])
            entry_tanggal.set_date(datetime.strptime(values[3], '%d-%m-%Y'))

    def hitung_ringkasan():
        data = baca_semua()
        total_pemasukan = sum(float(row[2]) for row in data if row[1] == "Pemasukan")
        total_pengeluaran = sum(float(row[2]) for row in data if row[1] == "Pengeluaran")
        sisa_saldo = total_pemasukan - total_pengeluaran
        messagebox.showinfo("Ringkasan Total Keuangan",
                            f"Total Pemasukan: Rp{total_pemasukan:,.2f}\n"
                            f"Total Pengeluaran: Rp{total_pengeluaran:,.2f}\n"
                            f"Sisa Saldo: Rp{sisa_saldo:,.2f}")

    tk.Button(frame_input, text="Tambah", command=tambah_data).grid(row=4, column=0, pady=10)
    tk.Button(frame_input, text="Update", command=update_data).grid(row=4, column=1)
    tk.Button(frame_input, text="Hapus", command=hapus_data).grid(row=4, column=2)
    tk.Button(frame_input, text="Lihat Total", command=hitung_ringkasan).grid(row=4, column=3)

    frame_table = tk.Frame(root)
    frame_table.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

    tree = ttk.Treeview(frame_table, columns=("Keterangan", "Jenis", "Jumlah", "Tanggal"), show="headings")
    for col in ("Keterangan", "Jenis", "Jumlah", "Tanggal"):
        tree.heading(col, text=col)
        tree.column(col, anchor=tk.CENTER)
    tree.pack(fill=tk.BOTH, expand=True)
    tree.bind("<<TreeviewSelect>>", pilih_item)

    tampilkan()

def tampilkan():
    for row in tree.get_children():
        tree.delete(row)
    for data in baca_semua():
        tree.insert('', tk.END, values=data)
