import copy
def deger_al(oyun_harita):
    #kurala uygun input alınmasını sağlar
    while True:
        inputs = input("Satır (1-{}), sütun (1-{}) ve işlem (N/D/B)  giriniz: ".format(len(oyun_harita),len(oyun_harita))).split()
        if len(inputs)!=3 or \
                (not (0 <= int(inputs[0]) <= len(oyun_harita) and 0 <= int(inputs[1]) <= len(oyun_harita))) or \
                (inputs[2] != "B" and inputs[2] != "D" and inputs[2] != "N"):
            print("Hatalı giriş...")
            continue
        return [int(inputs[0]),int(inputs[1]),inputs[2]]
def harita_goster(harita,durum):
    # harita listesi sayıları , durum listesi N-B-D karakterlerini tutar.
    #bu listelere göre matris oluşturulur.
    sutun_sayisi=len(harita)
    print(" \t ",end="")
    for i in range(sutun_sayisi):
        print(str((i+1))+"  ",end="")
    print("\n")
    for satir in range(sutun_sayisi):
        print(str(satir+1)+"\t",end="")
        for sutun in range(sutun_sayisi):
            durum_bilgisi=durum[satir][sutun]
            if durum_bilgisi=="N":
                print("-{}-".format(harita[satir][sutun]), end="")
            elif durum_bilgisi == "D":
                print("({})".format(harita[satir][sutun]), end="")
            else:
                print("-X-", end="")
        print("")
def harita_degistir(data,durum_bilgileri):
    durum_bilgileri[data[0] - 1][data[1] - 1] = data[2]
def kural_kontrol(bilgi_liste):
    #listedeki bütün B (X) karakterlerinin komşularını kontrol eder
    length=len(bilgi_liste)
    for i in range(length):
        for j in range(length):
            if bilgi_liste[i][j] == 'B':
                if i < 1:
                    pass
                elif bilgi_liste[i - 1][j] == 'B':
                    return False
                if i > length - 2:
                    pass
                elif bilgi_liste[i + 1][j] == 'B':
                    return False
                if  j < 1:
                    pass
                elif bilgi_liste[i][j - 1] == 'B':
                    return False
                if j > length - 2:
                    pass
                elif bilgi_liste[i][j + 1] == 'B':
                    return False
    return True
def kazandi_mi(harita,durum):
    #her sayının sağından ve aşağısından matris sonuna kadar ilerleyip, çakışma olup olmadığını kontrol eder.
    length=len(harita)
    for i in range(length):
        for j in range(length):
            for k in range(length):
                if durum[i][j]=='B':
                    break
                if j + k > length - 2 or durum[i][j + k + 1] == 'B':
                    pass
                elif harita[i][j] == harita[i][j + k + 1]:
                    return False
                if i + k > length - 2 or durum[i + k + 1][j] == 'B':
                    pass
                elif harita[i][j] == harita[i + k + 1][j]:
                    return False
    # çakışma yoksa oyunun kurallara uygun şekilde bitirilip bitirilmediğini kontrol eder.
    if not kural_kontrol(durum):
        return False
    if ada_var_mi(copy.deepcopy(durum)):
        return False
    return True
def ada_var_mi(liste):
    #sayıların 2 gruba veya daha fazlasına bölünüp bölünmediğini kontrol eder
    def virus():
        #listedeki bir adet N veya D karakterini V'ye çevirir.
        for i in range(len(liste)):
            for j in range(len(liste)):
                if liste[i][j]!='B' :
                    liste[i][j]='V'
                    return liste
    def mitoz(liste):
        #her V karakteri,B olmayan (N-D) dört komşusunu da V ye çevirir.
        #dönüştürme yapılamadığında döngü sonlanır
        bolunme=1
        while bolunme>0:
            bolunme=0
            for i in range(len(liste)):
                for j in range(len(liste)):
                    if liste[i][j]=='V':
                        if i+1<=len(liste)-1:
                            if liste[i+1][j]=='D' or liste[i+1][j]=='N':
                                bolunme += 1
                                liste[i+1][j] = 'V'
                        if i-1>=0:
                            if liste[i-1][j] == 'D' or liste[i-1][j] == 'N':
                                bolunme += 1
                                liste[i-1][j] = 'V'
                        if j+1<=len(liste)-1:
                            if liste[i][j+1] == 'D' or liste[i][j+1] == 'N':
                                bolunme += 1
                                liste[i][j+1] = 'V'
                        if j-1>=0:
                            if liste[i][j-1] == 'D' or liste[i][j-1] == 'N':
                                bolunme+=1
                                liste[i][j-1] = 'V'
    mitoz(virus())
    # listede B veya D karakteri kalmışsa, sayılar arasında bağlantı yoktur.
    for i in range(len(liste)):
        for j in range(len(liste)):
            if liste[i][j]=='D' or liste[i][j]=='N':
                return True
    return False
def set_up():
    # oyunun çalıştığı ana fonksiyondur.
    try:
        # txt dosyasından okunan veriler ile sayıları 2 boyutlu listede kayıt eder.
        with open("hitori_bulmaca.txt","r") as dosya:
            oyun_harita=[]
            for satir in dosya:
                oyun_harita.append(satir.split())
            kare_kenar=len(oyun_harita)
            # N-D-B durumlarının tutulması için bir liste daha oluşturup, varsayılan olarak bütün elemanları N yapar.
            durum_bilgileri = []
            for i in range(kare_kenar):
                durum_bilgileri.append([])
                for j in range(kare_kenar):
                    durum_bilgileri[i].append([])
                    durum_bilgileri[i][j] = "N"
    except IOError:
        print("Oyunu oynayabilmek için txt dosyası gereklidir.")
        exit()
    harita_goster(oyun_harita,durum_bilgileri)
    while True:
        # kullanıcıdan kurallara uygun input alır , listeyi değiştirir.
        # bu göngü oyun bitene kadar devam eder.
        harita_degistir(deger_al(oyun_harita),durum_bilgileri)
        if kazandi_mi(oyun_harita,durum_bilgileri):
            break
        harita_goster(oyun_harita,durum_bilgileri)
    print("\n-x-x-x-x-x-x-x-x-x-\nTebrikler...\nOyunun son hâli:")
    harita_goster(oyun_harita,durum_bilgileri)
set_up()