import rclpy
from rclpy.node import Node
from math import isnan, isinf
from std_msgs.msg import Float32MultiArray
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan
from numpy import mean, array

def cut(val,threshold):
   if val < threshold:
      return 0
   elif isinf(val):
    return 200
   else:
      return val 


def get_ranges(data_cutted, self):
  ranges = [[], [], [], [], [], [], [], [], [], []]
  ranges_sizes = [[0], [0], [0], [0], [0], [0], [0], [0], [0], [0]]
  i = 0
  for jj in range(len(data_cutted)-1):
      if data_cutted[jj] == 1 and data_cutted[jj+1] == 1:
         ranges[i].append(jj) 
         ranges_sizes[i] += 1.
      elif data_cutted[jj] == 1 and data_cutted[jj+1] == 0:
         i += 1
  return ranges, ranges_sizes


def calcular_promedio(array):
  dist = -6
  if not array:
    return 0
  suma = sum(array)
  return (suma / len(array)) + dist 

def control_law(data_ranges,data_sizes, self):
     
    array_promedios = list(map(calcular_promedio, data_ranges))
    controller = 90 - array_promedios[0] 
    self.get_logger().info(f"sizesArray:{data_sizes}")
    self.get_logger().info(f"rangesArray:{data_ranges}")
    self.get_logger().info(f"rangos:{controller}")
    if controller > 1.2:
      controller  = 1.2
    elif controller < -1.2:
      controller =  -1.2
    elif (isnan(controller) or isinf(controller)):
      controller = 0.
    control_law = controller + self.prev_control
    self.prev_control = control_law
    return -controller

def data_cleaning(data,self): 
  tresh = 1.5
  data_cut = [cut(data.ranges[x], tresh) for x in range(int(len(data.ranges)*(1/4)), int(len(data.ranges)*(3/4)))]
  if len(data_cut) != 0:  
    for k in range(len(data_cut)-1):
      if(data_cut[k] > 0) and (data_cut[k+1] > 0):
        data_cut[k] = 1.0
      else:
        data_cut[k] = 0.0
    data_cut.pop()

  return data_cut
   
   

class Control(Node):
    prev_control = 0
    alpha = 0
    side_distance = 0 

    def controll_callback(self, data):
      msg = Twist()
      data_cutted = data_cleaning(data,self)
      ranges, sizes = get_ranges(data_cutted, self)
      control = control_law(ranges,sizes, self)
      msg.angular.z = control
      msg.linear.x = 0.25
      self.get_logger().info(f"comando:{msg.angular.z}")
      self.cmd_pub.publish(msg)
      


    def __init__(self):
      super().__init__("gap_control_alpha") 
      self.pose_subs = self.create_subscription(LaserScan,'/scan',self.controll_callback,1)
      self.cmd_pub = self.create_publisher(Twist,'/cmd_vel_ctrl',10)


def main(args=None):
    rclpy.init(args=args)
    node = Control() 
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == "__main__":
    main()