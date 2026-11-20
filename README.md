# ENRO Yazılım Ekibi Aday Ödevi — Hedef Uzaklığı Kontrol Servisi

Bu proje, ENRO robot köpeğinin mevcut konumu ile hedef konumu arasındaki Öklid uzaklığını hesaplayan ve belirlenen yakınlık eşiğine ulaşılıp ulaşılmadığını kontrol eden bir ROS 2 Jazzy uygulamasıdır.

## Programın İşleyişi

* **Özel Servis Arayüzü (`enro_interfaces`):** `/enro/uzaklik_kontrol` servisi için `UzaklikKontrol.srv` arayüzünü tanımlar. İstemciden `robot_x`, `robot_y`, `hedef_x`, `hedef_y` ve `yakinlik_esigi_m` (metre) bilgilerini alır; yanıt olarak `basarili`, `uzaklik_m`, `hedefe_yakin` ve `aciklama` alanlarını döndürür.
* **Servis Sunucusu (`uzaklik_sunucu`):** Gelen girdilerin sonlu sayı (`math.isfinite`) ve `yakinlik_esigi_m > 0` olup olmadığını denetler. Geçerli isteklerde `sqrt((hedef_x - robot_x)^2 + (hedef_y - robot_y)^2)` formülüyle mesafeyi hesaplar, `uzaklik_m <= yakinlik_esigi_m` ise `hedefe_yakin = true` sonucunu döndürür ve hesaplanan mesafeyi `/enro/hedef_uzakligi` (`std_msgs/msg/Float64`) topic'ine **bir kez** yayınlar. Geçersiz girdilerde `basarili = false`, `uzaklik_m = 0.0`, `hedefe_yakin = false` döndürür ve topic'e yayın yapmaz.
* **İstemci (`uzaklik_istemci`):** Komut satırından verilen 5 sayıyı (veya argüman verilmezse ödevdeki 5 kontrol örneğini) `/enro/uzaklik_kontrol` servisine gönderip yanıtları ekrana yazdırır.

## Derleme ve Çalıştırma Komutları

Çalışma alanını derlemek için:
```bash
cd ~/ros2_ws
colcon build
source install/setup.bash
```

Terminal 1 — servis sunucusu:
```bash
source /opt/ros/jazzy/setup.bash
source ~/ros2_ws/install/setup.bash
ros2 run enro_uzaklik uzaklik_sunucu
```

Terminal 2 — topic izleme:
```bash
source /opt/ros/jazzy/setup.bash
source ~/ros2_ws/install/setup.bash
ros2 topic echo /enro/hedef_uzakligi
```

Terminal 3 — istemci (5 örneğin hepsi):
```bash
source /opt/ros/jazzy/setup.bash
source ~/ros2_ws/install/setup.bash
ros2 run enro_uzaklik uzaklik_istemci
```

Tek bir istek göndermek için: `ros2 run enro_uzaklik uzaklik_istemci 0 0 3 4 5`

## Örnek Çıktılar

### Servis yanıtları (istemci çıktısı)
```
$ ros2 run enro_uzaklik uzaklik_istemci
[INFO] [1795141415.382592411] [uzaklik_istemci]: Girdi: Robot=(0.0, 0.0), Hedef=(3.0, 4.0), Esik=5.0 m -> basarili=True, uzaklik_m=5.00, hedefe_yakin=True, aciklama="Uzaklik hesaplandi: 5.00 m. Hedefe yakin: Evet."
[INFO] [1795141415.383764059] [uzaklik_istemci]: Girdi: Robot=(0.0, 0.0), Hedef=(3.0, 4.0), Esik=4.0 m -> basarili=True, uzaklik_m=5.00, hedefe_yakin=False, aciklama="Uzaklik hesaplandi: 5.00 m. Hedefe yakin: Hayir."
[INFO] [1795141415.384881387] [uzaklik_istemci]: Girdi: Robot=(2.0, 3.0), Hedef=(2.0, 3.0), Esik=1.0 m -> basarili=True, uzaklik_m=0.00, hedefe_yakin=True, aciklama="Uzaklik hesaplandi: 0.00 m. Hedefe yakin: Evet."
[INFO] [1795141415.385716702] [uzaklik_istemci]: Girdi: Robot=(-1.0, -1.0), Hedef=(2.0, 3.0), Esik=5.0 m -> basarili=True, uzaklik_m=5.00, hedefe_yakin=True, aciklama="Uzaklik hesaplandi: 5.00 m. Hedefe yakin: Evet."
[INFO] [1795141415.386501885] [uzaklik_istemci]: Girdi: Robot=(0.0, 0.0), Hedef=(1.0, 1.0), Esik=0.0 m -> basarili=False, uzaklik_m=0.00, hedefe_yakin=False, aciklama="Hata: Yakinlik esigi sifirdan buyuk olmalidir."
```

### Sunucu logu
```
$ ros2 run enro_uzaklik uzaklik_sunucu
[INFO] [1795141398.652840559] [uzaklik_sunucu]: ENRO Uzaklik Kontrol Sunucusu baslatildi.
[INFO] [1795141415.369674659] [uzaklik_sunucu]: Istek islendi -> Uzaklik: 5.00 m | Yakin: True (Topic yayinlandi)
[INFO] [1795141415.383279072] [uzaklik_sunucu]: Istek islendi -> Uzaklik: 5.00 m | Yakin: False (Topic yayinlandi)
[INFO] [1795141415.384434760] [uzaklik_sunucu]: Istek islendi -> Uzaklik: 0.00 m | Yakin: True (Topic yayinlandi)
[INFO] [1795141415.385325699] [uzaklik_sunucu]: Istek islendi -> Uzaklik: 5.00 m | Yakin: True (Topic yayinlandi)
[WARN] [1795141415.386114428] [uzaklik_sunucu]: Hata: Yakinlik esigi sifirdan buyuk olmalidir.
```

### Topic çıktısı
```
$ ros2 topic echo /enro/hedef_uzakligi
data: 5.0
---
data: 5.0
---
data: 0.0
---
data: 5.0
---
```

Topic'te yalnızca 4 başarılı örneğin uzaklığı görünür. Beşinci örnekte (eşik = 0) `basarili = false` döndüğü için topic'e yayın yapılmaz; sunucu logundaki `WARN` satırında da "Topic yayinlandi" ifadesi yoktur.
