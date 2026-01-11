import tkinter as tk
from tkinter import messagebox, scrolledtext
import subprocess
import threading

# [Ana Pencere Kurulumu]
root = tk.Tk()
root.title("PORTSULA v2.4 - Real-Time Dashboard")
root.geometry("800x850")
root.configure(bg="#1a1a1a")

# [Değişkenler]
sv_var = tk.BooleanVar()
sc_var = tk.BooleanVar()
pn_var = tk.BooleanVar()
a_var = tk.BooleanVar()
ss_var = tk.BooleanVar()
f_var = tk.BooleanVar()
decoy_var = tk.BooleanVar()
stats_var = tk.BooleanVar()


def arayuzu_yenile():
    hedef_entry.delete(0, tk.END)
    port_entry.delete(0, tk.END)
    log_ekrani.delete(1.0, tk.END)
    for v in [sv_var, sc_var, pn_var, a_var, ss_var, f_var, decoy_var, stats_var]:
        v.set(False)
    hiz_slider.set(3)


def tarama_yap():
    hedef = hedef_entry.get()
    if not hedef:
        messagebox.showwarning("Hata", "Lütfen hedef girin!")
        return

    # [Komut Oluşturma]
    komut = ["nmap"]
    if sv_var.get(): komut.append("-sV")
    if sc_var.get(): komut.append("-sC")
    if pn_var.get(): komut.append("-Pn")
    if a_var.get(): komut.append("-A")
    if ss_var.get(): komut.append("-sS")
    if f_var.get(): komut.append("-f")
    if decoy_var.get(): komut.extend(["-D", "RND:10"])

    # İsteğin üzerine 2 saniyede bir durum raporu:
    if stats_var.get():
        komut.append("--stats-every=2s")

    komut.append(f"-T{hiz_slider.get()}")

    if port_entry.get():
        komut.extend(["-p", port_entry.get()])

    komut.append(hedef)

    log_ekrani.delete(1.0, tk.END)
    log_ekrani.insert(tk.END, f"[*] Tarama Başladı: {hedef}\n[*] Komut: {' '.join(komut)}\n" + "-" * 40 + "\n")

    def nmap_islem():
        try:
            # Canlı akış için Popen
            process = subprocess.Popen(komut, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)

            for line in iter(process.stdout.readline, ""):
                log_ekrani.insert(tk.END, line)
                log_ekrani.see(tk.END)  # Otomatik aşağı kaydır

            process.stdout.close()
            process.wait()
            log_ekrani.insert(tk.END, "\n[✔] Tarama Bitti.")
        except Exception as e:
            log_ekrani.insert(tk.END, f"\n[!] Hata oluştu: {e}")

    threading.Thread(target=nmap_islem, daemon=True).start()


# [Arayüz Tasarımı]
tk.Label(root, text="🧭 PORTSULA v2.4", fg="#00ff00", bg="#1a1a1a", font=("Courier", 20, "bold")).pack(pady=10)

tk.Label(root, text="HEDEF IP / DOMAIN:", fg="white", bg="#1a1a1a").pack()
hedef_entry = tk.Entry(root, width=45, bg="#333", fg="white", insertbackground="white")
hedef_entry.pack(pady=5)

tk.Label(root, text="PORTLAR (Opsiyonel):", fg="white", bg="#1a1a1a").pack()
port_entry = tk.Entry(root, width=45, bg="#333", fg="white", insertbackground="white")
port_entry.pack(pady=5)

frame = tk.LabelFrame(root, text=" Nmap Parametreleri ", fg="#00ff00", bg="#1a1a1a", pady=10)
frame.pack(pady=10, padx=20, fill="x")

# Checkbutton Yerleşimi
tk.Checkbutton(frame, text="-sV (Versiyon)", variable=sv_var, bg="#1a1a1a", fg="white", selectcolor="#444").grid(row=0,
                                                                                                                 column=0,
                                                                                                                 sticky="w",
                                                                                                                 padx=20)
tk.Checkbutton(frame, text="-sC (Script)", variable=sc_var, bg="#1a1a1a", fg="white", selectcolor="#444").grid(row=0,
                                                                                                               column=1,
                                                                                                               sticky="w",
                                                                                                               padx=20)
tk.Checkbutton(frame, text="-Pn (Ping Yok)", variable=pn_var, bg="#1a1a1a", fg="white", selectcolor="#444").grid(row=1,
                                                                                                                 column=0,
                                                                                                                 sticky="w",
                                                                                                                 padx=20)
tk.Checkbutton(frame, text="-A (Agresif)", variable=a_var, bg="#1a1a1a", fg="white", selectcolor="#444").grid(row=1,
                                                                                                              column=1,
                                                                                                              sticky="w",
                                                                                                              padx=20)
tk.Checkbutton(frame, text="-sS (Syn Scan)", variable=ss_var, bg="#1a1a1a", fg="white", selectcolor="#444").grid(row=2,
                                                                                                                 column=0,
                                                                                                                 sticky="w",
                                                                                                                 padx=20)
tk.Checkbutton(frame, text="-f (Fragment)", variable=f_var, bg="#1a1a1a", fg="white", selectcolor="#444").grid(row=2,
                                                                                                               column=1,
                                                                                                               sticky="w",
                                                                                                               padx=20)
tk.Checkbutton(frame, text="Decoy (Gizlilik)", variable=decoy_var, bg="#1a1a1a", fg="white", selectcolor="#444").grid(
    row=3, column=0, sticky="w", padx=20)
tk.Checkbutton(frame, text="Durum Raporu (2s)", variable=stats_var, bg="#1a1a1a", fg="white", selectcolor="#444").grid(
    row=3, column=1, sticky="w", padx=20)

hiz_slider = tk.Scale(root, from_=0, to=5, orient=tk.HORIZONTAL, label="Tarama Hızı (T)", bg="#1a1a1a", fg="white",
                      highlightthickness=0)
hiz_slider.set(3)
hiz_slider.pack(pady=10)

btn_frame = tk.Frame(root, bg="#1a1a1a")
btn_frame.pack(pady=10)
tk.Button(btn_frame, text="BAŞLAT", command=tarama_yap, bg="#27ae60", fg="white", width=15,
          font=("Arial", 10, "bold")).grid(row=0, column=0, padx=10)
tk.Button(btn_frame, text="YENİLE", command=arayuzu_yenile, bg="#2980b9", fg="white", width=15,
          font=("Arial", 10, "bold")).grid(row=0, column=1, padx=10)

log_ekrani = scrolledtext.ScrolledText(root, width=90, height=22, bg="black", fg="#00ff00", font=("Courier", 10))
log_ekrani.pack(pady=10, padx=10)

# [Final]
root.mainloop()