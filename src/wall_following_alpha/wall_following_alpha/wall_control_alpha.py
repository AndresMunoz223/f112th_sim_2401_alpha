import rclpy
from rclpy.node import Node
from math import atan2, cos, sin, isnan, isinf
from std_msgs.msg import Float32MultiArray
from geometry_msgs.msg import Twist


def pd_controller(self,set_point_angle, set_point_distance, alpha, side_distance):
  l = 1
  Kp = 1
  error = (2.5*(side_distance-set_point_distance) + (l*sin(-alpha+set_point_angle))) #revisar el angulo
  self.get_logger().info(f"anglegain: {l*sin(-alpha+set_point_angle)}, distancegain: {(side_distance-set_point_distance)}")
  controller = Kp*error
  if controller > 1.2:
    controller  = 1.2
  elif controller < -1.2:
    controller =  -1.2
  elif (isnan(controller) or isinf(controller)):
    controller = 0.
  return controller
  

class Control(Node):
    alpha = 0
    side_distance = 0


    def controll_callback(self, data):
      msg = Twist()
      self.get_logger().info(f"right:{data.data[1]} left:{data.data[5]}") # Info for debugging 

      if (data.data[1] < data.data[5]) or (isnan(data.data[5])): #check right wall
        self.alpha = data.data[0] 
        self.side_distance = data.data[1]
        control_action = pd_controller(self,0,1,self.alpha,self.side_distance)
        msg.angular.z = -control_action 

      elif (data.data[1] > data.data[5]) or (isnan(data.data[1])): #check left wall
        self.alpha = data.data[4] 
        self.side_distance = data.data[5]
        control_action = pd_controller(self,0,1,self.alpha,self.side_distance)
        msg.angular.z = control_action 

      else: # In case of no conclusive action
        msg.angular.z = 0.
      msg.linear.x = 0.25
      self.get_logger().info(f"comando:{msg.angular.z}")
      self.cmd_pub.publish(msg)



    def __init__(self):
      super().__init__("control_alpha") 
      self.pose_subs = self.create_subscription(Float32MultiArray,'/car_params',self.controll_callback,1)
      self.cmd_pub = self.create_publisher(Twist,'/cmd_vel_ctrl',10)


def main(args=None):
    rclpy.init(args=args)
    node = Control() 
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == "__main__":
    main()