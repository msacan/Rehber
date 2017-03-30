import sqlite3

baglanti = sqlite3.connect('veriler.db')
baglanti.row_factory = sqlite3.Row

veritabani_sec = baglanti.cursor()

veritabani_sec.execute("""
CREATE TABLE IF NOT EXISTS kisiler(
kayit_no VARCHAR(50),
firma VARCHAR(50),
ad VARCHAR(50),
soyad VARCHAR(50),
adres VARCHAR(100),
tel1 VARCHAR(50),
tel2 VARCHAR(50),
fax VARCHAR(50),
eposta VARCHAR(50),
web VARCHAR(50)
)
""")

bos = " "*50

def kisiler():
    baglanti = sqlite3.connect('veriler.db')
    baglanti.row_factory = sqlite3.Row
    veritabani_sec = baglanti.cursor()
    oku = veritabani_sec.execute('SELECT * FROM kisiler')

    print("="*72)
    print("Kart No\t\t\t Firma\t\t\t\t Ad Soyad")
    print("="*72)

    kartlar = []
    for veri_cek in oku.fetchall():
        print( veri_cek['kayit_no'], "\t\t\t", veri_cek['firma'], "\t\t\t", veri_cek['ad'], veri_cek['soyad'])
        kartlar.append(veri_cek['kayit_no'])
    print("="*72)

    while True:
        baslik = input("Detay [Kart No] / Çıkış [x] : ")
        print("-"*72)
        oku = veritabani_sec.execute('SELECT * FROM kisiler Where kayit_no LIKE "{}%"'.format(baslik))

        if not baslik:
            print("\nKart No girin: ")
            
        elif baslik == "x" or baslik == "X":
            break         
                
        else:
            for veri_cek in oku.fetchall():
                print(" Kart No:", veri_cek['kayit_no'],"\n",
                      "Firma\t:", veri_cek['firma'], "\n",
                      "Ad\t:", veri_cek['ad'], "\n",
                      "Soyad\t:", veri_cek['soyad'], "\n",
                      "Adres\t:", veri_cek['adres'], "\n",
                      "Telefon:", veri_cek['tel1'], "\n",
                      "Telefon:", veri_cek['tel2'], "\n",
                      "Fax\t:", veri_cek['fax'], "\n",
                      "Eposta\t:", veri_cek['eposta'], "\n",
                      "Web\t:", veri_cek['web'] )
                print("-"*72)

        
    baglanti.commit()
    baglanti.close()



def kisi_ekle():
    baglanti = sqlite3.connect('veriler.db')

    if(baglanti):
        print("Veri bankasınabağlanıldı.\n")
    else:
        print("Bağlantı başarısız!")

    veritabani_sec = baglanti.cursor()

    while True:
        liste_oku = []
        kartlar = []
        firmalar = []
        adlar = []
        soyadlar = []
        oku = veritabani_sec.execute('SELECT * FROM kisiler')
        for i in oku:
            liste_oku.append(i)
            kartlar.append(i[0])
            firmalar.append(i[1])
            adlar.append(i[2])
            soyadlar.append(i[3])

        while True:
            k_kayit_no = input("Kart No: ")
            if not k_kayit_no or k_kayit_no in bos:
                print("Kart No boş bırakılamaz")
            elif k_kayit_no in kartlar:
                print("'{}' numaralı kart kullanılıyor. Lütfen yeni bir Kart No belirleyin.\n".format(k_kayit_no))            
            else:
                break
        while True:
            k_firma = input("Firma Adı: ")
            k_ad = input("Ad: ")
            k_soyad = input("Soyad: ")  
            if k_firma in firmalar and k_ad in adlar and k_soyad in soyadlar:
                cevap = input("'{}' firmasından '{} {}' adlı kişi farklı bir Kart No ile kayıtlıdır\nKayda devam etmek istiyor musunuz? E / H : ".format(k_firma, k_ad, k_soyad))
                if cevap == "h" or cevap == "H":
                    continue
                elif cevap == "e" or cevap == "E":
                    break
                else:
                    continue
                        
            else:
                break      
        k_adres = input("Adres: ")
        k_tel1 = input("Telefon: ")
        k_tel2 = input("Telefon: ")
        k_fax = input("Fax: ")
        k_eposta = input("Eposta: ")
        k_web = input("Web: ")
       
        kayit = k_kayit_no, k_firma, k_ad, k_soyad, k_adres, k_tel1, k_tel2, k_fax, k_eposta, k_web
        
        veritabani_sec.execute("INSERT INTO kisiler(kayit_no, firma, ad, soyad, adres, tel1, tel2, fax, eposta, web) VALUES('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}')".format(k_kayit_no, k_firma, k_ad, k_soyad, k_adres, k_tel1, k_tel2, k_fax, k_eposta, k_web))
        print("'{}' Numaralı '{}' firma adlı '{} {}' rehbere eklendi\n".format(k_kayit_no, k_firma, k_ad, k_soyad))

        baglanti.commit()

        yeni_kayit = input("YENİ KAYIT [Enter] / ÇIKIŞ [x] : ")
        if yeni_kayit == "x" or yeni_kayit == "X":
            break
        else:
            print("\n")
            continue

    baglanti.close()

def kisi_guncelle():
    baglanti = sqlite3.connect('veriler.db')
    baglanti.row_factory = sqlite3.Row
    veritabani_sec = baglanti.cursor()
    while True:
        kartlar = []
        kriter = []
        while True:    
            sorgu_guncelle = input("Arama Kriteri  ==> (1) Kart No / (2) Firma / (3) Ad / (4) Soyad: ")
            if sorgu_guncelle == "1":
                konu = "kayit_no"
                break
            elif sorgu_guncelle == "2":
                konu = "firma"
                break
            elif sorgu_guncelle == "3":
                konu = "ad"
                break
            elif sorgu_guncelle == "4":
                konu = "soyad"
                break
            else:
                print("Lütfen arama kriteriniz için belirlenmiş sayı değerlerinden girin!\n")

        while True:
            ara = input("Aranacak Veri: ")
            print("-"*72)
            oku = veritabani_sec.execute('SELECT * FROM kisiler Where {} LIKE "{}%"'.format(konu, ara))
            for veri_cek in oku.fetchall():
                kisi = (" Kart No:", veri_cek['kayit_no'],"\n",
                        "Firma\t:", veri_cek['firma'], "\n",
                        "Ad\t:", veri_cek['ad'], "\n",
                        "Soyad\t:", veri_cek['soyad'], "\n",
                        "Adres\t:", veri_cek['adres'], "\n",
                        "Telefon:", veri_cek['tel1'], "\n",
                        "Telefon:", veri_cek['tel2'], "\n",
                        "Fax\t:", veri_cek['fax'], "\n",
                        "Eposta\t:", veri_cek['eposta'], "\n",
                        "Web\t:", veri_cek['web'])
                kartlar.append(veri_cek['kayit_no'])
                kriter.append(veri_cek[konu])
               
                print(*kisi)
                print("-"*72)
            
            if len(kriter) < 1:
                print("'{}' başlığında '{}' bilgisi bulunamadı".format(konu, ara))
            else:
                break

        if len(kriter) > 1:
            while True:
                no = input("Değiştirilecek Kartın Numarasını girin: ")
                if no in kartlar:
                    break
                else:
                    print("Geçersiz Kart No")
            

            oku_1 = veritabani_sec.execute('SELECT * FROM kisiler Where kayit_no LIKE "{}"'.format(no))
            for veri_cek in oku_1.fetchall():
                kisi_1 = (" Kart No:", veri_cek['kayit_no'],"\n",
                        "Firma\t:", veri_cek['firma'], "\n",
                        "Ad\t:", veri_cek['ad'], "\n",
                        "Soyad\t:", veri_cek['soyad'], "\n",
                        "Adres\t:", veri_cek['adres'], "\n",
                        "Telefon:", veri_cek['tel1'], "\n",
                        "Telefon:", veri_cek['tel2'], "\n",
                        "Fax\t:", veri_cek['fax'], "\n",
                        "Eposta\t:", veri_cek['eposta'], "\n",
                        "Web\t:", veri_cek['web'])
            print("-"*72)
            print(*kisi_1)
            print("-"*72)
            
                
        else:
            no = veri_cek['kayit_no']
        while True:
            sorgu_baslik = input("""\nDeğiştirilecek başlığı seçin   ==>
1) Kart No\t 2) Firma\t 3) Ad\t 4) Soyad\t 5) Adres
6) Telefon 1\t 7) Telefon 2\t 8) Fax\t 9) E-posta\t 10) Web
: """)          
            if sorgu_baslik == "1":
                degis_baslik = 'kayit_no'
                break
            elif sorgu_baslik == "2":
                degis_baslik = 'firma'
                break
            elif sorgu_baslik == "3":
                degis_baslik = 'ad'
                break
            elif sorgu_baslik == "4":
                degis_baslik = 'soyad'
                break
            elif sorgu_baslik == "5":
                degis_baslik = 'adres'
                break
            elif sorgu_baslik == "6":
                degis_baslik = 'tel1'
                break
            elif sorgu_baslik == "7":
                degis_baslik = 'tel2'
                break
            elif sorgu_baslik == "8":
                degis_baslik = 'fax'
                break
            elif sorgu_baslik == "9":
                degis_baslik = 'eposta'
                break
            elif sorgu_baslik == "10":
                degis_baslik = 'web'
                break
            else:
                print("Lütfen arama kriteriniz için belirlenmiş sayı değerlerinden girin!\n")
            
        eski = veri_cek[degis_baslik]
        print(eski)
        yeni = input("Yeni bilgi: ")

        veritabani_sec.execute("update kisiler set {}='{}' where {}='{}' and kayit_no='{}'".format(degis_baslik, yeni, degis_baslik, eski, no))
        baglanti.commit()
        print("{} Kart No'lu üyenin '{}' olan '{}' bilgisi '{}' olarak güncellendi.".format(no, eski, degis_baslik, yeni))

        yeni_islem = input("\nYENİ İŞLEM [Enter] / ÇIKIŞ [x] : ")
        if yeni_islem == "x" or yeni_islem == "X":
            break
        else:
            continue   
    baglanti.close()

    
    
def kisi_sil():
    baglanti = sqlite3.connect('veriler.db')
    baglanti.row_factory = sqlite3.Row
    veritabani_sec = baglanti.cursor()
    kartlar = []
        
    while True:
        oku = veritabani_sec.execute('SELECT * FROM kisiler')
        for veri_cek in oku.fetchall():
            if veri_cek['kayit_no'] not in kartlar:
                    kartlar.append(veri_cek['kayit_no'])
        
        sil_menu = input("\n(1) Kartları Görüntüle / (Enter) Devam : ")
        if sil_menu == "1":
            print("Kart No\t\t\t Firma\t\t\t\t Ad Soyad")
            print("-"*72)
            
            oku = veritabani_sec.execute('SELECT * FROM kisiler')
            for veri_cek in oku.fetchall():
                print(veri_cek['kayit_no'], "\t\t\t", veri_cek['firma'], "\t\t\t", veri_cek['ad'], veri_cek['soyad'])
            print("-"*72)
            pass
        else:
            pass
        
        while True:
            sil = input("Silinecek Kart No Girin: ")
            if sil not in kartlar:
                print("Geçersiz Kart No!\n")
                continue
            else:
                break
            
        while True:  
            print("'{}' kart numaralı veri silinecek!".format(sil))
            sil_ok = input("(1) Sil / (2) İptal: ")
            if sil_ok == "2":
                print("\nSilme İşlemi İptal Edildi")
                break
            elif sil_ok == "1":
                veritabani_sec.execute("Delete from kisiler where kayit_no='{}'".format(sil))
                kartlar.remove(sil)
                print("\nSilme İşlemi Tamamlandı")
                baglanti.commit()
                break
            else:
                print("Tekrar deneyin!")
                continue
            
        yeni_sil = input("YENİ İŞLEM [Enter] / ÇIKIŞ [x] : ")
        if yeni_sil == "x" or yeni_sil == "X":
            break
        else:
            continue
            
    baglanti.close()

def menu():
    while True:
        print("\n"*3)
        print("[1] KİŞİLER    [2] YENİ KİŞİ    [3] BİLGİ GÜNCELLE    [4] KİŞİ SİL    [x] ÇIKIŞ")
     
        giris = input("İsleminizi Secin: ")
        if giris == "1":
            print("\nKİŞİLER ", "="*63, "\n")
            kisiler()
            
        elif giris == "2":
            print("\nREHBERE KİŞİ EKLEME ", "="*51)
            kisi_ekle()
            
        elif giris == "3":
            print("\nBİLGİ GÜNCELLE ", "="*57)
            kisi_guncelle()
            
        elif giris == "4":
            print("\nREHBERDEN KİŞİ SİL ", "="*53)
            kisi_sil()

        elif giris == "x" or giris == "X":
            quit()
            
        else:
            print("Tekrar Deneyin")

menu()
    

baglanti.commit()
baglanti.close()
