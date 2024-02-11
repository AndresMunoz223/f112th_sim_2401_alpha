#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from turtlesim.msg import Pose
from geometry_msgs.msg import Twist
import sensor_msgs.msg
from math import atan2, cos, sin

def angle_calculator(data, rayA_index, rayB_index, theta):
        rayA = data.ranges[rayA_index]
        rayB = data.ranges[rayB_index]
        alpha = atan2((rayA*cos(theta)-rayB),(rayA*sin(theta))) #Tentative function, look up hera on wiki
        distance = rayB*cos(alpha)

        return alpha, distance

class ScanSub(Node): 

    def scan_callback(self,data):
        msg = Twist()
        alpha, distance = angle_calculator(data, 0, 1, data.angle_increment)
        msg.linear.x = alpha #Offset angle
        msg.linear.y = distance #Side Distance
        msg.angular.z = data.ranges[int(len(data.ranges)/2)] #Front Distance
        self.get_logger().info(f"distancia : {msg.angular.z}")
        self.cmd_pub.publish(msg)


    def __init__(self):
        super().__init__("distance_finder_alpha") # Redefine node name
        self.pose_subs = self.create_subscription(sensor_msgs.msg.LaserScan,'/scan',self.scan_callback,1)
        self.cmd_pub = self.create_publisher(Twist,'/car_params',10)

def main(args=None):
    rclpy.init(args=args)
    node = ScanSub() # Definicion del objeto "node"
    # ejecucion ciclica 
    rclpy.spin(node)
    # finalizacion
    rclpy.shutdown()

if __name__ == "__main__":
    main()