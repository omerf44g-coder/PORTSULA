# PORTSULA
Automated Nmap scanner with CVE research link generator.

# 🧭 PORTSULA v1.0
"Siber Güvenlik Yolculuğunda Pusulanız"

PORTSULA, ağ tarama sonuçlarını analiz eden ve tespit edilen servisler için otomatik olarak zafiyet (CVE) araştırma linkleri oluşturan Python tabanlı bir güvenlik aracıdır.

 Öne Çıkan Özellikler
 
- Servis Tespiti: Nmap altyapısını kullanarak portlardaki servis ve versiyon bilgilerini yakalar.
- Otomatik CVE Analizi: Bulunan her servis için Google üzerinden saniyeler içinde zafiyet tarama linki hazırlar.
- Raporlama: Tüm bulguları `Portsula_Rapor.txt` dosyasına kaydederek dokümantasyon sağlar.

##  Nasıl Çalıştırılır?
1. Kali Linux terminalinizi açın.
2. `python3 portsula.py` komutunu girin.
3. Hedef IP veya Domain adresini yazıp taramayı başlatın.

## 👨‍💻 Geliştirici
Ömer Faruk Güner / Siber Güvenlik Öğrencisi

---
> "Bu proje, bir siber güvenlik öğrencisinin Python öğrenme sürecindeki ilk profesyonel adımıdır."
