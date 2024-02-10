#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from std_msgs.msg import Bool

class BreakNode(Node): # reemplazar YY por el numero de grupo
    
    def scan_callback(self,data):
        msg = Bool()
        distance = data.linear.y
        if distance < 0.5:
            msg.data = True
        else:
            msg.data = True
        self.cmd_pub.publish(msg)


    def __init__(self):
        super().__init__("break") # Redefine node name
        self.pose_subs = self.create_subscription(Twist,'/autoparams',self.scan_callback,1)
        self.cmd_pub = self.create_publisher(Bool,'/break',10)


def main(args=None):
    rclpy.init(args=args)
    node = BreakNode() # Definicion del objeto "node"
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == "__main__":
    main()