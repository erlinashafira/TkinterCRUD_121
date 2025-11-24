import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

def create_db():
    conn = sqlite3.connect("nilai_siswa.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS nilai_siswa (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nama_siswa TEXT NOT NULL,
            biologi INTEGER NOT NULL,
            fisika INTEGER NOT NULL,
            inggris INTEGER NOT NULL,
            prediksi_fakultas TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

create_db()

def prediksi_fakultas(bio, fis, ing):
    if bio > fis and bio > ing:
        return "Kedokteran"
    elif fis > bio and fis > ing:
        return "Teknik"
    elif ing > bio and ing > fis:
        return "Bahasa"
    return "Tidak Dapat Ditentukan"

def submit_nilai():
    nama = entry_nama.get().strip()
    try:
        bio = int(entry_bio.get())
        fis = int(entry_fis.get())
        ing = int(entry_ing.get())
    except ValueError:
        messagebox.showerror("Error", "Nilai harus angka!")
        return

    if not nama:
        messagebox.showerror("Error", "Nama tidak boleh kosong!")
        return

    for nilai, pelajaran in [(bio, "Biologi"), (fis, "Fisika"), (ing, "Inggris")]:
        if nilai < 0 or nilai > 100:
            messagebox.showerror("Error", f"Nilai {pelajaran} tidak boleh lebih dari 100!")
            return

    hasil = prediksi_fakultas(bio, fis, ing)

    conn = sqlite3.connect("nilai_siswa.db")
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO nilai_siswa (nama_siswa, biologi, fisika, inggris, prediksi_fakultas)
        VALUES (?, ?, ?, ?, ?)
    """, (nama, bio, fis, ing, hasil))
    conn.commit()
    conn.close()

    load_data()
    entry_nama.delete(0, tk.END)
    entry_bio.delete(0, tk.END)
    entry_fis.delete(0, tk.END)
    entry_ing.delete(0, tk.END)

    conn = sqlite3.connect("nilai_siswa.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM nilai_siswa")
    rows = cursor.fetchall()
    print("Isi database saat ini:")
    for row in rows:
        print(row)
    conn.close()

def update_data():
    selected = table.focus()
    if not selected:
        messagebox.showerror("Error, Pilih data dari tabel!")
        return
    
    nama_baru = entry_nama.get().strip()

    try:
        bio = int(entry_bio.get())
        fis = int(entry_fis.get())
        ing = int(entry_ing.get())
    except:
        messagebox.showerror("Error", "Nilai harus angka!")
        return

    hasil = prediksi_fakultas(bio, fis, ing)


    nama_lama = table.item(selected, "values")[0]

    conn = sqlite3.connect("nilai_siswa.db")
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE nilai_siswa
        SET nama_siswa=?, biologi=?, fisika=?, inggris=?, prediksi_fakultas=?
        WHERE nama_siswa=?
    """, (nama_baru, bio, fis, ing, hasil, nama_lama))
    conn.commit()
    conn.close()

    load_data()
    messagebox.showinfo("Success", "Data berhasil diperbarui!")

def delete_data():
    selected = table.focus()
    if not selected:
        messagebox.showerror("Error", "Pilih data dari tabel!")
        return

    nama = table.item(selected, "values")[0]

    if not messagebox.askyesno("Hapus", f"Yakin hapus data '{nama}'?"):
        return

    conn = sqlite3.connect("nilai_siswa.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM nilai_siswa WHERE nama_siswa=?", (nama,))
    conn.commit()
    conn.close()

    load_data()
    messagebox.showinfo("Success", "Data berhasil dihapus!")

def load_data():
    for i in table.get_children():
        table.delete(i)
    conn = sqlite3.connect("nilai_siswa.db")
    cursor = conn.cursor()
    cursor.execute("SELECT nama_siswa, biologi, fisika, inggris, prediksi_fakultas FROM nilai_siswa")
    rows = cursor.fetchall()
    conn.close()
    for row in rows:
        table.insert("", tk.END, values=row)

def pilih_baris(event):
    selected = table.focus()
    if not selected:
        return

    values = table.item(selected, "values")

    entry_nama.delete(0, tk.END)
    entry_bio.delete(0, tk.END)
    entry_fis.delete(0, tk.END)
    entry_ing.delete(0, tk.END)

    entry_nama.insert(0, values[0])
    entry_bio.insert(0, values[1])
    entry_fis.insert(0, values[2])
    entry_ing.insert(0, values[3])

root = tk.Tk()
root.title("Aplikasi Prediksi Fakultas")
root.geometry("880x460")

main_frame = tk.Frame(root)
main_frame.pack(fill="both", expand=True, padx=10, pady=10)

left_frame = tk.LabelFrame(main_frame, text="Input Nilai Siswa", padx=10, pady=10)
left_frame.pack(side="left", fill="y")

tk.Label(left_frame, text="Nama Siswa").pack(anchor="w")
entry_nama = tk.Entry(left_frame, width=25)
entry_nama.pack(pady=3)

tk.Label(left_frame, text="Nilai (0-100)").pack(anchor="w", pady=(10,3))
nilai_frame = tk.Frame(left_frame)
nilai_frame.pack(pady=5)

tk.Label(nilai_frame, text="Biologi").grid(row=0, column=0, padx=5, sticky="e")
entry_bio = tk.Entry(nilai_frame, width=10)
entry_bio.grid(row=0, column=1, padx=5)

tk.Label(nilai_frame, text="Fisika").grid(row=0, column=2, padx=5, sticky="e")
entry_fis = tk.Entry(nilai_frame, width=10)
entry_fis.grid(row=0, column=3, padx=5)

tk.Label(nilai_frame, text="Inggris").grid(row=0, column=4, padx=5, sticky="e")
entry_ing = tk.Entry(nilai_frame, width=10)
entry_ing.grid(row=0, column=5, padx=5)

btn_frame = tk.Frame(left_frame)
btn_frame.pack(pady=15)

btn_submit = tk.Button(btn_frame, text="Submit", command=submit_nilai, width=10)
btn_submit.grid(row=0, column=0, padx=5)

btn_close = tk.Button(btn_frame, text="Close", command=root.destroy, width=10)
btn_close.grid(row=0, column=1, padx=5)

btn_update = tk.Button(btn_frame, text="Update", command=update_data, width=10)
btn_update.grid(row=1, column=0, padx=5, pady=5)

btn_delete = tk.Button(btn_frame, text="Delete", command=delete_data, width=10)
btn_delete.grid(row=1, column=1, padx=5, pady=5)

right_frame = tk.LabelFrame(main_frame, text="Data Nilai Siswa", padx=10, pady=10)
right_frame.pack(side="left", padx=20)

table = ttk.Treeview(right_frame, columns=("nama","bio","fis","ing","hasil"), show="headings", height=15)
table.pack()

table.heading("nama", text="Nama")
table.heading("bio", text="Biologi")
table.heading("fis", text="Fisika")
table.heading("ing", text="Inggris")
table.heading("hasil", text="Prediksi Fakultas")

table.column("nama", width=150)
table.column("bio", width=70)
table.column("fis", width=70)
table.column("ing", width=70)
table.column("hasil", width=150)

load_data()

root.mainloop()
