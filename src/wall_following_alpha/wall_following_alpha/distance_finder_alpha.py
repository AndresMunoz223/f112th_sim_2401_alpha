#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
import sensor_msgs.msg
from math import atan2, cos, sin
from std_msgs.msg import Float32MultiArray


def angle_calculator(data, rayA_index, rayB_index, theta):
        
        rayA = data.ranges[rayA_index]
        rayB = data.ranges[rayB_index]
        alpha = atan2((rayA*cos(theta)-rayB),(rayA*sin(theta))) #Tentative function, look up hera on wiki
        distance = rayB*cos(alpha)

        return alpha, distance

class ScanSub(Node): 
    k = 1 #velocity constant, we're on a ct_speed scenario.

    def scan_callback(self,data):
        msg = Float32MultiArray()
        msg.data= [0.,0.,0.,0.,0.,0.,0.,0.]
        alpha_right, side_distance_right = angle_calculator(data, int(len(data.ranges)/4), int(len(data.ranges)/4)+55, data.angle_increment*60)
        msg.data[0] = round(alpha_right,3) #Offset angle
        msg.data[1] = round(side_distance_right,3) #Side Distance
        msg.data[2] = round(data.ranges[int(len(data.ranges)/2)],3) #Front Distance
        msg.data[3] = round(side_distance_right + self.k*sin(alpha_right),3) #Deviation distance

        alpha_left, side_distance_left = angle_calculator(data, int(len(data.ranges)*(3/4)), int(len(data.ranges)*(3/4)-55), data.angle_increment*60)
        msg.data[4] = round(alpha_left,3) #alpha left
        msg.data[5] = round(side_distance_left,3) #Side Distance left
        msg.data[7] = round(side_distance_left + self.k*sin(alpha_left),3) #Deviation distance left
        
        #Message structure:
        # alpha right_wall [0]
        # Distance right_wall [1]
        # Front distance [2]
        # Deviarion distance Right [3]
        # alpha left_wall [4]
        # Distance left_wall [5]
        # Deviatiom distance Left [6]

        self.get_logger().info(f"distancia : {msg.data}")
        self.cmd_pub.publish(msg)


    def __init__(self):
        super().__init__("distance_finder_alpha") # Redefine node name
        self.pose_subs = self.create_subscription(sensor_msgs.msg.LaserScan,'/scan',self.scan_callback,1)
        self.cmd_pub = self.create_publisher(Float32MultiArray,'/car_params',10)

def main(args=None):
    rclpy.init(args=args)
    node = ScanSub() # Definicion del objeto "node"
    # ejecucion ciclica 
    rclpy.spin(node)
    # finalizacion
    rclpy.shutdown()

if __name__ == "__main__":
    main()