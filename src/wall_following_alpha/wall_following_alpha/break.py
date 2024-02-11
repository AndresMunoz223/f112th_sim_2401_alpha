#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from std_msgs.msg import Bool

class BreakNode(Node): # reemplazar YY por el numero de grupo
    distance = 0
    def break_callback(self,data):
        self.get_logger().info(f"ejecutado")
        msg = Bool()
        msg.data = False
        time = self.distance/(data.linear.x+(1e-10))
        if 0  < time < 2.5:
            msg.data = True
        else:
            msg.data = False
        self.get_logger().info(f"condicional :{self.distance/(data.linear.x+(1e-10))}")
        self.cmd_pub.publish(msg)
        

    def pose_callback(self,data):
        self.distance = data.angular.z
        # self.get_logger().info(f"distancia : {self.distance}")


    def __init__(self):
        super().__init__("break") # Redefine node name
        self.vel_subs = self.create_subscription(Twist,'/cmd_vel_joy',self.break_callback,1)
        self.pose_subs = self.create_subscription(Twist,'/car_params',self.pose_callback,1)
        self.cmd_pub = self.create_publisher(Bool,'/error',10)


def main(args=None):
    rclpy.init(args=args)
    node = BreakNode() # Definicion del objeto "node"
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == "__main__":
    main()