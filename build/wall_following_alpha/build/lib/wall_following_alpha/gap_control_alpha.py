import rclpy
from rclpy.node import Node
from math import atan2, cos, sin, isnan, isinf
from std_msgs.msg import Float32MultiArray
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan

def cut(val,threshold):
   if val < threshold:
      return 0
   elif isinf(val):
    return 200
   else:
      return val 

def data_cleaning(data,self): 

  data_cut = [cut(data.ranges[x], 4) for x in range(int(len(data.ranges)/2) + int(len(data.ranges)*0.25))]
  if len(data_cut) != 0:  
    
    for ii in range(len(data_cut)-1):
      self.get_logger().info(f"i:{ii}")
      if(data_cut[ii] > 0) and (data_cut[ii+1] > 0):
        data_cut[ii] = 1.0
      else:
        data_cut[ii] = 0.0
    data_cut.pop()
  return data_cut
   
   

class Control(Node):
    alpha = 0
    side_distance = 0 

    def controll_callback(self, data):
      msg = Float32MultiArray()
      data_cutted = data_cleaning(data,self)
      self.get_logger().info(f"data:{data_cutted}")
      msg.data = [data_cutted[x] for x in range(len(data_cutted))]
      self.get_logger().info(f"len:{msg.data}")
      self.cmd_pub.publish(msg)


    def __init__(self):
      super().__init__("gap_control_alpha") 
      self.pose_subs = self.create_subscription(LaserScan,'/scan',self.controll_callback,1)
      self.cmd_pub = self.create_publisher(Float32MultiArray,'/scan_filtered',10)


def main(args=None):
    rclpy.init(args=args)
    node = Control() 
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == "__main__":
    main()