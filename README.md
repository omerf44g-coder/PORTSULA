# PORTSULA
Automated Nmap scanner with CVE research link generator.

# 🧭 PORTSULA v2.4 Artık Arayüzlü
"Siber Güvenlik Yolculuğunda Pusulanız"

###  Yeni Özellikler:
- Canlı Takip: `--stats-every` entegrasyonu sayesinde taramanın yüzde kaçta olduğunu saniye saniye izleyin.
- Gelişmiş Parametreler: Syn Scan (-sS), Fragment (-f) ve Decoy IP gibi siber güvenlik taktiklerini tek tıkla seçin.
- Hız Kontrolü: T0'dan T5'e kadar ayarlanabilir tarama hızı.
- Yenileme Modu: Tek butonla tüm ayarları sıfırlayıp yeni taramaya geçme imkanı.




PORTSULA, ağ tarama sonuçlarını analiz eden ve tespit edilen servisler için otomatik olarak zafiyet (CVE) araştırma linkleri oluşturan Python tabanlı bir IP Port Tarama-Güvenlik aracıdır.

 Öne Çıkan Özellikler
 
- Servis Tespiti: Nmap altyapısını kullanarak portlardaki servis ve versiyon bilgilerini yakalar.
- Otomatik CVE Analizi: Bulunan her servis için Google üzerinden saniyeler içinde zafiyet tarama linki hazırlar.
- Raporlama: Tüm bulguları `Portsula_Rapor.txt` dosyasına kaydederek dokümantasyon sağlar.

  

- ### 🛠️ Kurulum ve Çalıştırma

# Gerekli kütüphaneyi kurun (Kali)
sudo apt install python3-tk

# Uygulamayı başlatın
python3 portsula_gui.py

## 👨‍💻 Geliştirici
Ömer Faruk Güner / Siber Güvenlik Öğrencisi

---
> "Bu proje, bir siber güvenlik öğrencisinin Python öğrenme sürecindeki ilk profesyonel adımıdır."
