import sys
import rclpy
from rclpy.node import Node
from enro_interfaces.srv import UzaklikKontrol


class UzaklikIstemci(Node):
    def __init__(self):
        super().__init__('uzaklik_istemci')
        self.client = self.create_client(UzaklikKontrol, '/enro/uzaklik_kontrol')
        while not self.client.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('/enro/uzaklik_kontrol servisi bekleniyor...')

    def istek_gonder(self, robot_x, robot_y, hedef_x, hedef_y, yakinlik_esigi_m):
        req = UzaklikKontrol.Request()
        req.robot_x = float(robot_x)
        req.robot_y = float(robot_y)
        req.hedef_x = float(hedef_x)
        req.hedef_y = float(hedef_y)
        req.yakinlik_esigi_m = float(yakinlik_esigi_m)

        future = self.client.call_async(req)
        rclpy.spin_until_future_complete(self, future)
        return future.result()


def main(args=None):
    rclpy.init(args=args)
    istemci = UzaklikIstemci()

    # Komut satirindan 5 sayi verilmisse tek istek gonder; verilmemisse 5 kontrol ornegini calistir
    if len(sys.argv) == 6:
        ornekler = [tuple(float(x) for x in sys.argv[1:6])]
    else:
        ornekler = [
            (0.0, 0.0, 3.0, 4.0, 5.0),
            (0.0, 0.0, 3.0, 4.0, 4.0),
            (2.0, 3.0, 2.0, 3.0, 1.0),
            (-1.0, -1.0, 2.0, 3.0, 5.0),
            (0.0, 0.0, 1.0, 1.0, 0.0),
        ]

    try:
        for rx, ry, hx, hy, esik in ornekler:
            yanit = istemci.istek_gonder(rx, ry, hx, hy, esik)
            istemci.get_logger().info(
                f'Girdi: Robot=({rx}, {ry}), Hedef=({hx}, {hy}), Esik={esik} m -> '
                f'basarili={yanit.basarili}, uzaklik_m={yanit.uzaklik_m:.2f}, '
                f'hedefe_yakin={yanit.hedefe_yakin}, aciklama="{yanit.aciklama}"'
            )
    finally:
        istemci.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()


if __name__ == '__main__':
    main()
