# ROS 2 Temel Kavramlar Araştırması

## 1. ROS 2 Nedir ve Neden Kullanılır?
ROS 2, robot yazılımı geliştirmek için kullanılan açık kaynaklı bir kütüphane ve araç topluluğudur. Robot yazılımını sensör okuma, motor sürme, karar verme gibi küçük parçalara böler ve bu parçalar birbiriyle mesajlaşarak çalışır. Haberleşme DDS gibi bir altyapıyla yapıldığı için merkezi bir sunucuya gerek yoktur. Böylece kodlar yeniden kullanılabilir ve ayrı ayrı test edilebilir.

## 2. Workspace, Package ve Node
* **Workspace:** Paketlerin bir arada tutulup `colcon build` ile derlendiği ana klasördür (`~/ros2_ws`).
* **Package:** Kodun, bağımlılıkların ve ayar dosyalarının (`package.xml`, `setup.py`) toplandığı birimdir.
* **Node:** ROS ağına katılan ve tek bir işe odaklanan programdır. Örneğin yalnızca mesafe hesaplayan bir düğüm.

## 3. Topic, Message, Publisher ve Subscriber
* **Topic:** Düğümlerin veri alışverişi yaptığı isimli kanaldır (`/enro/hedef_uzakligi`).
* **Message:** Kanaldan geçen verinin tipidir (`std_msgs/msg/Float64`).
* **Publisher:** Topic'e mesaj gönderen düğümdür.
* **Subscriber:** Topic'i dinleyip gelen mesajı işleyen düğümdür. Veri tek yönlü akar, publisher cevap beklemez.

## 4. Service, Client, Request ve Response
* **Service:** Sadece ihtiyaç olduğunda çağrılan istek-yanıt yapısıdır.
* **Client:** Servise istek gönderip yanıtı alan düğümdür.
* **Request / Response:** `.srv` dosyasında `---` çizgisinin üstü istek (girdiler), altı yanıttır (çıktılar).

## 5. Action, Goal, Feedback ve Result
* **Action:** Uzun süren, ilerlemesi takip edilmek istenen ve iptal edilebilen işler için kullanılır.
* **Goal:** İstemcinin istediği görevdir.
* **Feedback:** Görev sürerken gelen ilerleme bilgisidir.
* **Result:** Görev bitince (veya iptal edilince) gelen son sonuçtur.

## 6. Parameter, Launch ve ros2 Komutları
* **Parameter:** Kodu değiştirmeden düğümün ayarlarını (eşik, frekans gibi) değiştirmeyi sağlar.
* **Launch:** Birden fazla düğümü tek komutla başlatır.
* **ros2 komutları:** Sistemi çalıştırmak ve izlemek için kullanılır (`ros2 run`, `ros2 topic echo`, `ros2 service call`, `ros2 node list`).

## 7. Topic, Service ve Action Karşılaştırması

| | Topic | Service | Action |
| :--- | :--- | :--- | :--- |
| **Ne zaman?** | Sürekli veri akışı | Kısa, tek seferlik soru-cevap | Uzun süren görev |
| **Geri bildirim** | Yok | Sadece son yanıt | Süreç boyunca feedback |
| **İptal** | Yok | Yok | Var |
| **Örnek** | IMU sensörünün saniyede 50 kez ivme verisi yayınlaması | "Robot hedefe eşik içinde mi?" sorgusu | "10 metre ilerideki odaya git" komutu ve giderken kalan mesafenin izlenmesi |
