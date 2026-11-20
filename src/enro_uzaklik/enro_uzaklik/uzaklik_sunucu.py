import math
import rclpy
from rclpy.node import Node
from std_msgs.msg import Float64
from enro_interfaces.srv import UzaklikKontrol


class UzaklikSunucu(Node):
    def __init__(self):
        super().__init__('uzaklik_sunucu')
        # Hedef uzakligi kontrol servisini olustur
        self.srv = self.create_service(
            UzaklikKontrol,
            '/enro/uzaklik_kontrol',
            self.uzaklik_kontrol_callback
        )
        # Basarili hesaplamalarda uzakligi yayinlayacak topic yayincisi
        self.publisher_ = self.create_publisher(
            Float64,
            '/enro/hedef_uzakligi',
            10
        )
        self.get_logger().info('ENRO Uzaklik Kontrol Sunucusu baslatildi.')

    def uzaklik_kontrol_callback(self, request, response):
        degerler = [
            request.robot_x,
            request.robot_y,
            request.hedef_x,
            request.hedef_y,
            request.yakinlik_esigi_m
        ]

        # Tum girdilerin sonlu (NaN veya Inf olmayan) sayilar oldugunu dogrula
        if not all(math.isfinite(v) for v in degerler):
            response.basarili = False
            response.uzaklik_m = 0.0
            response.hedefe_yakin = False
            response.aciklama = 'Hata: Tum koordinat ve esik degerleri sonlu sayilar olmalidir.'
            self.get_logger().warn(response.aciklama)
            return response

        # Yakinlik esiginin sifirdan buyuk oldugunu kontrol et
        if request.yakinlik_esigi_m <= 0.0:
            response.basarili = False
            response.uzaklik_m = 0.0
            response.hedefe_yakin = False
            response.aciklama = 'Hata: Yakinlik esigi sifirdan buyuk olmalidir.'
            self.get_logger().warn(response.aciklama)
            return response

        # Koordinat farklari ve Oklid uzakligi hesabi
        dx = request.hedef_x - request.robot_x
        dy = request.hedef_y - request.robot_y
        uzaklik = math.hypot(dx, dy)

        # Uzaklik esikten kucuk veya esitse hedefe yakin kabul edilir
        yakin_mi = uzaklik <= request.yakinlik_esigi_m

        response.basarili = True
        response.uzaklik_m = float(uzaklik)
        response.hedefe_yakin = bool(yakin_mi)
        response.aciklama = (
            f'Uzaklik hesaplandi: {uzaklik:.2f} m. '
            f'Hedefe yakin: {"Evet" if yakin_mi else "Hayir"}.'
        )

        # Yalnizca basarili isteklerde uzakligi topic uzerinden bir kez yayinla
        msg = Float64()
        msg.data = float(uzaklik)
        self.publisher_.publish(msg)

        self.get_logger().info(
            f'Istek islendi -> Uzaklik: {uzaklik:.2f} m | Yakin: {yakin_mi} (Topic yayinlandi)'
        )
        return response


def main(args=None):
    rclpy.init(args=args)
    node = UzaklikSunucu()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()


if __name__ == '__main__':
    main()
