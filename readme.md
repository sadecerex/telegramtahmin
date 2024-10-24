////

PYTHON KURULUMU : 

1- https://www.python.org/downloads/ Sayfasından Uygun Setup'ı indirin ve kurun

2- Kurulum Tamamlandıktan sonra Botun Klasörünü Açın

3- Botun Klasöründe Bir Komut Dosyası Başlatın

4- pip install -r requirements.txt (olmazsa) python install -r requirements.txt komutunu kullanın .

5- Gerekli Tüm Modüller Yüklenecek ve Ardından Diğer İşlemlere Geçin

/// 

TELEGRAM TOKENİ ALMAK İÇİN : 

1 - @BotFather isimli Kullanıcıya Telegramdan Mesaj Atıyorsunuz
2 - Sonra Sırasıyla Bu Komutları Kullanıyorsunuz

(/newbot)
(BOTUN ON ISMI) NORMAL MESAJ OLARAK GÖNDERİCEKSİNİZ BU İKİ ARGÜMANI
(BOTUN KULLANICI ADI)

3 - DONE! ile başlayan bir metin gönderecek size orda HTTP API : ile belirtilen kısımdan sonra karmaşık şekilde Bir Token Gönderecek Onu Kullanacaksınız.
4 - Config.py Dosyasında TELEGRAM_TOKEN = '' Kısmında Çizgilerin Arasına Tokeni Yerleştireceksiniz.


/////

API_KEY ALMAK İÇİN : 

1- https://rapidapi.com/ adresine girip hesap oluşturuyorsunuz. 

2- https://rapidapi.com/api-sports/api/api-football/ bu adrese girip ordan subscribe seçeneği ile aboneliğinizi alıyorsunuz (Basic Plan Ücretsizdir Ondan Alabilirsiniz)

3- ABONELİK İŞLEMİ TAMAMLANDIKTAN SONRA ARAMA KISMINA FOOTBALL yazarak Tekrardan Api nin sayfasına gelin

4- Orada Size Listelediği X-RapidAPI-Key = kısmındaki Anahtarı Kopyalayın

5- config.py dosyasında API_KEY= '' kısmında çizgilerin arasına anahtarı yapıştırın


////

GROUP CHAT ID İÇİN 

1 - https://api.telegram.org/bot<YourBOTToken>/getUpdates adresindeki "/bot<YourBOTToken>/" şu kısmı Telegram Tokenini Yazacaksınız

2 - Karşınızdaki Sayfadan Group Chat ID yi Bulabilirsiniz.


////////

Botu İlham Almak İçin Kullanabilirsiniz.

baslat.bat dosyasından botu başlatabilirsiniz , İyi Kullanımlar (Not: Gerçeklik Payı Düşüktür.) 