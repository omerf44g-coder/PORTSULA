import customtkinter as ctk
import subprocess
import threading
from datetime import datetime

# Görünüm Ayarları
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")

class Portsula(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("PORTSULA v6.0 - Ultimate Recon Engine")
        self.geometry("1300x950")

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # --- SOL KONTROL PANELİ ---
        self.sidebar = ctk.CTkFrame(self, width=350, corner_radius=0)
        self.sidebar.grid(row=0, column=0, sticky="nsew")

        ctk.CTkLabel(self.sidebar, text="PORTSULA v6.0", font=("Orbitron", 28, "bold"), text_color="#2ecc71").pack(pady=20)

        # Hedef ve Port Girişi
        self.hedef_entry = ctk.CTkEntry(self.sidebar, placeholder_text="Hedef IP/Domain/Aralık", width=280, height=35)
        self.hedef_entry.pack(pady=5)
        
        self.port_entry = ctk.CTkEntry(self.sidebar, placeholder_text="Özel Portlar (örn: 80,443)", width=280, height=35)
        self.port_entry.pack(pady=5)

        # --- TÜM PARAMETRELER (KAYDIRILABİLİR LİSTE) ---
        self.scroll_frame = ctk.CTkScrollableFrame(self.sidebar, label_text="Nmap Silah Deposu", width=310, height=500, fg_color="transparent")
        self.scroll_frame.pack(pady=10, padx=10, fill="both")

        # 1. TARAMA TİPLERİ (SCAN TYPES)
        ctk.CTkLabel(self.scroll_frame, text="--- Tarama Tipleri ---", text_color="orange").pack(anchor="w", pady=(10,0))
        self.ss_var = ctk.BooleanVar(value=True); ctk.CTkCheckBox(self.scroll_frame, text="Stealth Scan (-sS)", variable=self.ss_var).pack(pady=2, anchor="w")
        self.st_var = ctk.BooleanVar(); ctk.CTkCheckBox(self.scroll_frame, text="TCP Connect (-sT)", variable=self.st_var).pack(pady=2, anchor="w")
        self.su_var = ctk.BooleanVar(); ctk.CTkCheckBox(self.scroll_frame, text="UDP Scan (-sU)", variable=self.su_var).pack(pady=2, anchor="w")
        self.sf_var = ctk.BooleanVar(); ctk.CTkCheckBox(self.scroll_frame, text="FIN Scan (-sF)", variable=self.sf_var).pack(pady=2, anchor="w")
        self.sx_var = ctk.BooleanVar(); ctk.CTkCheckBox(self.scroll_frame, text="Xmas Scan (-sX)", variable=self.sx_var).pack(pady=2, anchor="w")
        self.sn_var = ctk.BooleanVar(); ctk.CTkCheckBox(self.scroll_frame, text="Null Scan (-sN)", variable=self.sn_var).pack(pady=2, anchor="w")

        # 2. SERVİS VE OS TESPİTİ
        ctk.CTkLabel(self.scroll_frame, text="--- Analiz & Tespit ---", text_color="orange").pack(anchor="w", pady=(10,0))
        self.sv_var = ctk.BooleanVar(value=True); ctk.CTkCheckBox(self.scroll_frame, text="Versiyon Tespiti (-sV)", variable=self.sv_var).pack(pady=2, anchor="w")
        self.sc_var = ctk.BooleanVar(); ctk.CTkCheckBox(self.scroll_frame, text="Default Scripts (-sC)", variable=self.sc_var).pack(pady=2, anchor="w")
        self.os_var = ctk.BooleanVar(); ctk.CTkCheckBox(self.scroll_frame, text="OS Tespiti (-O)", variable=self.os_var).pack(pady=2, anchor="w")
        self.a_var = ctk.BooleanVar(); ctk.CTkCheckBox(self.scroll_frame, text="Agresif Mod (-A)", variable=self.a_var).pack(pady=2, anchor="w")

        # 3. HEDEF VE PORT AYARLARI
        ctk.CTkLabel(self.scroll_frame, text="--- Port & Hedef ---", text_color="orange").pack(anchor="w", pady=(10,0))
        self.p_all_var = ctk.BooleanVar(); ctk.CTkCheckBox(self.scroll_frame, text="Tüm Portlar (-p-)", variable=self.p_all_var).pack(pady=2, anchor="w")
        self.fast_var = ctk.BooleanVar(); ctk.CTkCheckBox(self.scroll_frame, text="Hızlı Tarama (-F)", variable=self.fast_var).pack(pady=2, anchor="w")
        self.random_var = ctk.BooleanVar(); ctk.CTkCheckBox(self.scroll_frame, text="Random IP (-iR 1)", variable=self.random_var, command=self.toggle_random).pack(pady=2, anchor="w")

        # 4. FIREWALL & IDS ATLATMA (EVASION)
        ctk.CTkLabel(self.scroll_frame, text="--- Firewall Atlatma ---", text_color="orange").pack(anchor="w", pady=(10,0))
        self.pn_var = ctk.BooleanVar(); ctk.CTkCheckBox(self.scroll_frame, text="No Ping (-Pn)", variable=self.pn_var).pack(pady=2, anchor="w")
        self.f_frag_var = ctk.BooleanVar(); ctk.CTkCheckBox(self.scroll_frame, text="Paket Parçala (-f)", variable=self.f_frag_var).pack(pady=2, anchor="w")
        self.badsum_var = ctk.BooleanVar(); ctk.CTkCheckBox(self.scroll_frame, text="Bozuk Checksum (--badsum)", variable=self.badsum_var).pack(pady=2, anchor="w")
        self.mtu_var = ctk.BooleanVar(); ctk.CTkCheckBox(self.scroll_frame, text="MTU Ayarı (8)", variable=self.mtu_var).pack(pady=2, anchor="w")

        # 5. GÖZLEM VE LOGLAMA
        ctk.CTkLabel(self.scroll_frame, text="--- İzleme ---", text_color="orange").pack(anchor="w", pady=(10,0))
        self.stats_var = ctk.BooleanVar(value=True); ctk.CTkCheckBox(self.scroll_frame, text="İlerleme Göster (Stats)", variable=self.stats_var).pack(pady=2, anchor="w")
        self.reason_var = ctk.BooleanVar(); ctk.CTkCheckBox(self.scroll_frame, text="Nedenini Yaz (--reason)", variable=self.reason_var).pack(pady=2, anchor="w")
        self.vv_var = ctk.BooleanVar(); ctk.CTkCheckBox(self.scroll_frame, text="Detaylı Log (-vv)", variable=self.vv_var).pack(pady=2, anchor="w")

        # --- HIZ AYARI VE GÖSTERGE ---
        hiz_frame = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        hiz_frame.pack(pady=5)
        ctk.CTkLabel(hiz_frame, text="Tarama Hızı: ").pack(side="left")
        self.hiz_label = ctk.CTkLabel(hiz_frame, text="T4", text_color="#2ecc71", font=("Bold", 14))
        self.hiz_label.pack(side="left")
        self.hiz_slider = ctk.CTkSlider(self.sidebar, from_=0, to=5, number_of_steps=5, command=self.update_hiz_label)
        self.hiz_slider.set(4); self.hiz_slider.pack(pady=5, padx=20)

        # --- BUTONLAR ---
        self.start_btn = ctk.CTkButton(self.sidebar, text="OPERASYONU BAŞLAT", command=self.start_scan_thread, fg_color="#27ae60", hover_color="#1e8449", font=("Segoe UI", 14, "bold"))
        self.start_btn.pack(pady=10, padx=20, fill="x")
        self.stop_btn = ctk.CTkButton(self.sidebar, text="DURDUR", command=self.stop_scan, fg_color="#c0392b", hover_color="#922b21")
        self.stop_btn.pack(pady=5, padx=20, fill="x")

        # --- SAĞ ÇIKTI EKRANI ---
        self.output_box = ctk.CTkTextbox(self, font=("Courier New", 15), text_color="#00FF00", border_width=2, border_color="#2ecc71")
        self.output_box.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")
        self.output_box.insert("0.0", ">>> PORTSULA v6.0 Hazır. Operasyon Bekleniyor...\n")

        self.process = None

    def update_hiz_label(self, value):
        self.hiz_label.configure(text=f"T{int(value)}")

    def toggle_random(self):
        if self.random_var.get():
            self.hedef_entry.delete(0, 'end'); self.hedef_entry.insert(0, "RASTGELE HEDEF"); self.hedef_entry.configure(state="disabled")
        else:
            self.hedef_entry.configure(state="normal"); self.hedef_entry.delete(0, 'end')

    def start_scan_thread(self):
        self.start_btn.configure(state="disabled", text="OPERASYON SÜRÜYOR")
        threading.Thread(target=self.run_nmap, daemon=True).start()

    def run_nmap(self):
        command = ["nmap"]
        if self.random_var.get(): command.extend(["-iR", "1"])
        else:
            target = self.hedef_entry.get().strip()
            if not target or target == "RASTGELE HEDEF":
                self.output_box.insert("end", "\n[!] HATA: Hedef belirtilmedi!\n"); self.start_btn.configure(state="normal", text="OPERASYONU BAŞLAT"); return
            command.append(target)

        # Parametrelerin Hepsini Ekle
        if self.ss_var.get(): command.append("-sS")
        if self.st_var.get(): command.append("-sT")
        if self.su_var.get(): command.append("-sU")
        if self.sf_var.get(): command.append("-sF")
        if self.sx_var.get(): command.append("-sX")
        if self.sn_var.get(): command.append("-sN")
        if self.sv_var.get(): command.append("-sV")
        if self.sc_var.get(): command.append("-sC")
        if self.os_var.get(): command.append("-O")
        if self.a_var.get(): command.append("-A")
        if self.p_all_var.get(): command.append("-p-")
        if self.fast_var.get(): command.append("-F")
        if self.pn_var.get(): command.append("-Pn")
        if self.f_frag_var.get(): command.append("-f")
        if self.badsum_var.get(): command.append("--badsum")
        if self.mtu_var.get(): command.extend(["--mtu", "8"])
        if self.stats_var.get(): command.append("--stats-every=5s")
        if self.reason_var.get(): command.append("--reason")
        if self.vv_var.get(): command.append("-vv")

        ports = self.port_entry.get().strip()
        if ports and not self.p_all_var.get(): command.extend(["-p", ports])
        command.append(f"-T{int(self.hiz_slider.get())}")

        self.output_box.delete("1.0", "end")
        self.output_box.insert("end", f"🚀 Operasyon Komutu: {' '.join(command)}\n" + "="*60 + "\n")

        try:
            self.process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
            for line in iter(self.process.stdout.readline, ""):
                self.output_box.insert("end", line); self.output_box.see("end")
            self.process.wait()
        except Exception as e:
            self.output_box.insert("end", f"\n[!] Kritik Hata: {str(e)}")
        
        self.output_box.insert("end", "\n" + "="*60 + "\n[✔] Operasyon Tamamlandı."); self.start_btn.configure(state="normal", text="OPERASYONU BAŞLAT")

    def stop_scan(self):
        if self.process:
            self.process.terminate(); self.output_box.insert("end", "\n[🛑] OPERASYON DURDURULDU."); self.start_btn.configure(state="normal", text="OPERASYONU BAŞLAT")

if __name__ == "__main__":
    app = Portsula()
    app.mainloop()
