# LiDAR 데이터를 구독하여 왼쪽/정면/오른쪽 영역의 거리·속도·충돌위험(TTC)을 계산하고 경고를 출력

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import LaserScan
import math
import time

class LidarThreatMonitor(Node):
    def __init__(self):
        super().__init__('lidar_threat_monitor')
        self.sub = self.create_subscription(LaserScan, '/scan', self.callback, 10)
        self.prev_scan = None
        self.prev_time = None
        self.sector_half_angle = math.radians(60)
        self.walk_speed = 1.2
        self.danger_speed = 2.5
        self.ttc_threshold = 2.0
        self.min_dt = 0.8

    def callback(self, msg: LaserScan):
        now = time.time()
        if self.prev_scan is None:
            self.prev_scan = msg.ranges
            self.prev_time = now
            return

        dt = now - self.prev_time
        if dt < self.min_dt:
            return

        sector_info = {"왼쪽": [], "정면": [], "오른쪽": []}
        dangers = []

        for i, r in enumerate(msg.ranges):
            angle = msg.angle_min + i * msg.angle_increment
            angle_deg = math.degrees(angle)

            if -self.sector_half_angle <= angle <= self.sector_half_angle:
                if 0.0 < r <= 16.0 and self.prev_scan[i] > 0.0:
                    if dt <= 0:
                        continue
                    rel_speed = (self.prev_scan[i] - r) / dt
                    if abs(rel_speed) < 0.05:
                        rel_speed = 0.0
                    if rel_speed > 20:
                        continue
                    if rel_speed > 0:
                        ttc = r / rel_speed
                    else:
                        ttc = float('inf')

                    if -60 <= angle_deg < -20:
                        sector_info["왼쪽"].append((r, rel_speed, ttc))
                        sector = "왼쪽"
                    elif -20 <= angle_deg <= 20:
                        sector_info["정면"].append((r, rel_speed, ttc))
                        sector = "정면"
                    elif 20 < angle_deg <= 60:
                        sector_info["오른쪽"].append((r, rel_speed, ttc))
                        sector = "오른쪽"
                    else:
                        sector = "기타"

                    if r < 5.0 and rel_speed > self.danger_speed and ttc < self.ttc_threshold:
                        dangers.append((sector, angle_deg, r, rel_speed, ttc))

        self.get_logger().info("📊 영역 요약")
        for sector, values in sector_info.items():
            if values:
                min_dist, rel_speed, ttc = min(values, key=lambda x: x[0])
                self.get_logger().info(
                    f" - {sector:<4}: 거리={min_dist:.2f} m | 상대속도={rel_speed:.2f} m/s | TTC={ttc:.2f} s"
                )
            else:
                self.get_logger().info(f" - {sector:<4}: 데이터 없음")

        if dangers:
            self.get_logger().warn("⚠️ 주의! 위험 객체 감지")
            for sector, ang, dist, spd, ttc in dangers:
                self.get_logger().warn(
                    f" -> {sector:<4} | 각도={ang:+.1f}° | 거리={dist:.2f} m | 속도={spd:.2f} m/s | TTC={ttc:.2f} s"
                )

        self.prev_scan = msg.ranges
        self.prev_time = now


def main():
    rclpy.init()
    node = LidarThreatMonitor()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
