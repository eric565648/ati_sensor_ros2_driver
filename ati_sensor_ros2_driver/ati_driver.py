# ROS2 package for ati sensor

import rclpy
from rclpy.node import Node
from .rpi_ati_net_ft import NET_FT
import argparse
from geometry_msgs.msg import WrenchStamped
from std_srvs.srv import Trigger

class ATIDriver(Node):
    def __init__(self, host):
        super().__init__('ati_driver')

        self.host = host
        self.ati_obj = NET_FT(host)
        self.ati_obj.set_tare_from_ft()
        print(self.ati_obj.read_ft_http())
        print(self.ati_obj.try_read_ft_http())

        # service server
        self.tare_srv = self.create_service(Trigger,'set_ati_tare',self.set_tare)
        self.clr_tare_srv = self.create_service(Trigger,'clear_ati_tare',self.clear_tare)

        # publisher
        self.ft_pub = self.create_publisher(WrenchStamped,"ati_ft",1)

        self.ati_obj.start_streaming()

        # timer
        self.rate = 1e-3
        self.create_timer(self.rate, self.get_ft)
    
    def get_ft(self):

        res, ft, status = self.ati_obj.try_read_ft_streaming(.1)
        fstamp = self.get_clock().now().to_msg()

        if ft is not None:
            w = WrenchStamped()
            w.header.stamp = fstamp
            w.header.frame_id = 'ati_frame'
            w.wrench.torque.x = ft[0]
            w.wrench.torque.y = ft[1]
            w.wrench.torque.z = ft[2]
            w.wrench.force.x = ft[3]
            w.wrench.force.y = ft[4]
            w.wrench.force.z = ft[5]

            self.ft_pub.publish(w)

    def set_tare(self, req, response):
        
        self.ati_obj.set_tare_from_ft()

        response.success=True
        response.message="ATISensor: The tare is set."

        return response
    
    def clear_tare(self, req, response):

        self.ati_obj.clear_tare()
        
        response.success=True
        response.message="ATISensor: The tare is cleared."

        return response

def main():
    parser = argparse.ArgumentParser(description="ATI force torque sensor driver service for Robot Raconteur")
    parser.add_argument("--sensor-ip", type=str, default="192.168.50.65", help="the ip address of the ati sensor")
    parser.add_argument("--wait-signal",action='store_const',const=True,default=False, help="wait for SIGTERM orSIGINT (Linux only)")

    args,_ = parser.parse_known_args()
    
    rclpy.init()
    ati_driver_obj = ATIDriver(args.sensor_ip)

    rclpy.spin(ati_driver_obj)

if __name__ == '__main__':
    main()
