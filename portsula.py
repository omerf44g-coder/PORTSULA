# [TAG: Kütüphane] - Kali'nin terminal komutlarını yönetmemizi sağlar.
import subprocess


# [TAG: Branding] - Aracın açılış manşeti.
def program_basligi():
    print("=" * 60)
    print("        PORTSULA - Zaafiyet Tarama ve Analiz Aracı                  ")
    print("        Hazırlayan: Ömer Faruk Güner / Siber Güvenlik Öğrencisi    ")
    print("=" * 60)


# [TAG: Analiz_Motoru] - Nmap çıktısını okur ve Google linkleri oluşturur.
# Bu fonksiyon bağımsız bir oda olarak yukarıda durmalı.
def zafiyet_analizi(nmap_ciktisi):
    print("\n" + "=" * 20 + " ZAFAYET ARAŞTIRMA LİNKLERİ " + "=" * 20)
    satirlar = nmap_ciktisi.split("\n")
    bulunan_servis = False

    for satir in satirlar:
        if "open" in satir:
            bulunan_servis = True
            parcalar = satir.split()
            # Nmap çıktısında servis bilgisi genellikle 3. sütundan sonra başlar.
            servis_bilgisi = " ".join(parcalar[2:])

            if servis_bilgisi:
                arama_sorgusu = f"{servis_bilgisi} CVE vulnerabilities".replace(" ", "+")
                link = f"https://www.google.com/search?q={arama_sorgusu}"
                print(f"[!] Tespit Edilen Servis: {servis_bilgisi}")
                print(f"    [>] Zafiyetleri Araştır: {link}\n")

    if not bulunan_servis:
        print("[i] Analiz edilecek açık bir port bulunamadı.")


# [TAG: Nmap_Motoru] - Nmap'i başlatan fonksiyon.
def tarama_baslat(hedef_ip):
    print(f"\n[*] {hedef_ip} hedefi mercek altına alınıyor...")
    try:
        komut = ["nmap", "-sV", "-p-", "--open", hedef_ip]
        cikti = subprocess.run(komut, capture_output=True, text=True)
        return cikti.stdout
    except Exception as e:
        return f"Hata oluştu: {e}"


# [TAG: Main] - Programın ana kumanda merkezi.
def main():
    program_basligi()
    hedef = input("[?] Taramak istediğiniz IP veya Domain girin (Örn: google.com): ")

    # 1. Taramayı yap ve sonucu 'sonuc' değişkenine al.
    sonuc = tarama_baslat(hedef)

    # 2. Ham tarama sonucunu ekrana bas.
    print("\n[+] Tarama Sonuçları:")
    print(sonuc)

    # 3. ŞİMDİ analiz motorunu çalıştır.
    zafiyet_analizi(sonuc)

    # 4. Raporu dosyaya yaz.
    with open("Portsula_Rapor.txt", "w") as rapor:
        rapor.write(sonuc)
        print("\n[✔] Rapor 'Portsula_Rapor.txt' olarak kaydedildi.")


# [TAG: Trigger] - Programı başlatan tetikleyici.
if __name__ == "__main__":
    main()