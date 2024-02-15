#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from std_msgs.msg import Bool
from std_msgs.msg import Float32MultiArray

class BreakNode(Node):

    front_distance = 0 #Distancia frontal

    def break_callback(self,data):
        msg = Bool()
        time = self.front_distance/(data.linear.x+(1e-10)) # tiempo de frenado
        if 0  < time < 1:
            msg.data = True
        else:
            msg.data = False    
        self.get_logger().info(f"condicional :{self.front_distance/(data.linear.x+(1e-10))}") #Log por remas de debug
        self.cmd_pub.publish(msg)

    def pose_callback(self,data):
        self.front_distance = data.data[2] #Distancia frontal
        


    def __init__(self):
        super().__init__("break") 
        self.vel_subs = self.create_subscription(Twist,'/cmd_vel_joy',self.break_callback,1)
        self.vel_subs = self.create_subscription(Twist,'/cmd_vel',self.break_callback,1)
        self.vel_subs = self.create_subscription(Twist,'/cmd_vel_ctrl',self.break_callback,1)
        self.pose_subs = self.create_subscription(Float32MultiArray,'/car_params',self.pose_callback,1)
        self.cmd_pub = self.create_publisher(Bool,'/error',10)


def main(args=None):
    rclpy.init(args=args)
    node = BreakNode() # Definicion del objeto "node"
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == "__main__":
    main()