# BTC Wallet Checker [Termux UI]

BTC Wallet Checker, rastgele Bitcoin özel anahtarları üreterek bunlara karşılık gelen Bitcoin adreslerini kontrol eden basit bir Python scriptidir. Termux üzerinde çalışmak üzere tasarlanmıştır ve kullanıcı dostu renkli bir arayüze sahiptir.

---

## Özellikler

- Rastgele 256-bit Bitcoin özel anahtarı oluşturma
- Özel anahtardan açık anahtar ve Bitcoin adresi türetme
- Gerçek zamanlı olarak blockchain.info API'sinden bakiye kontrolü
- Bakiyesi olan adresleri `found.txt` dosyasına kaydetme
- Termux için kurulumu ve çalıştırması kolay bash script

---

## Gereksinimler

- Termux (Android terminal emülatörü)
- Python 3
- Aşağıdaki Python paketleri:
  - `requests`
  - `ecdsa`
  - `base58`
  - `colorama`

---

## Kurulum

Termux'ta aşağıdaki adımları izleyin:

1. Depoları güncelleyin ve yükseltin:
   ```bash
   pkg update -y && pkg upgrade -y

2. Gerekli paketleri yükleyin:

pkg install python git -y


3. Python bağımlılıklarını yükleyin:

pip install requests ecdsa base58 colorama


4. Proje dosyalarını indirin veya kopyalayın.


5. start.sh scriptine çalıştırma izni verin:

chmod +x start.sh


6. Scripti başlatın:

./start.sh




---

Kullanım

Script başlatıldığında:

Her yarattığı Bitcoin adresini ve bakiyesini terminalde gösterir.

Bakiyesi sıfır olmayan adresleri found.txt dosyasına kaydeder.

Çalışmayı durdurmak için CTRL+C kombinasyonunu kullanabilirsiniz.



---

Dikkat Edilmesi Gerekenler

Bu script gerçek Bitcoin özel anahtarları üzerinde işlem yapar; büyük bir ihtimalle bakiyesi sıfırdır.

Bu yöntemle anlamlı Bitcoin bulunma şansı son derece düşüktür ve pratik bir yatırım veya madencilik yöntemi değildir.

Script yalnızca eğitim ve deneme amaçlıdır.



---

Lisans

Bu proje MIT Lisansı ile lisanslanmıştır.


---

İletişim

Herhangi bir soru veya öneriniz için iletişime geçebilirsiniz.
