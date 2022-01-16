#########################################################
#    ros_bert.py
#########################################################

#!/usr/bin/env python
#-- coding:utf8 --
import rospy
import math
import time
import cv2
import csv

from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
from sensor_msgs.msg import Image
from sensor_msgs.msg import LaserScan

from cv_bridge import CvBridge
t1 = time.time()

label_dir = '/home/zhu/Desktop/BERT_temporaryname/bert_output/label_demo.csv'

with open(label_dir) as f:
  reader = csv.reader(f)
  l = [row for row in reader]

move = int(l[0][0])
print(move)

#############Gazebo##################
freeze_speed = 0

linear_speed = 1.0
linear_goal = 2.0
linear_time = linear_goal / linear_speed

angular_speed = 0.5
angular_goal = 2.3
angular_time = angular_goal / angular_speed

m_x = -0.5
m_y = 0
u_x = 6.5
u_y = 0

odom_x, odom_y, ori_x, ori_y, ori_z, ori_w = 0.0, 0.0, 0.0, 0.0, 0.0, 0.0

r, p, y, angleA, angleB, gap, distance_m = 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0

angleC, gap2, distance_u = 0.0, 1.0, 0.0

m_y1 = 2
u_y1 = 2

angleD, angleE, gap3, gap4, distance_m1, distance_u1 = 0.0, 0.0, 1.0, 1.0, 0.0, 0.0

angleF, gap5 = 0.0, 1.0

center_x = 2.5
center_y = 2


#range_min = 0.0

#############action_9/10##############

def odomcbx(msg):
  global odom_x, odom_y, ori_x, ori_y, ori_z, ori_w
  global r, p, y, angleA, angleB, gap, distance_m
  global angleC, gap2, distance_u
  global angleD, angleE, gap3, gap4, distance_m1, distance_u1
  global angleF, gap5
  
  odom_x = msg.pose.pose.position.x
  odom_y = msg.pose.pose.position.y
  ori_x = msg.pose.pose.orientation.x
  ori_y = msg.pose.pose.orientation.y
  ori_z = msg.pose.pose.orientation.z
  ori_w = msg.pose.pose.orientation.w

  r = math.atan2(2*(ori_w*ori_x + ori_y*ori_z), 1-2*(ori_x*ori_x + ori_y*ori_y))
  p = math.asin(2*(ori_w*ori_y - ori_z*ori_x))
  y = math.atan2(2*(ori_w*ori_z + ori_x*ori_y),1-2*(ori_z*ori_z + ori_y*ori_y))
  
  angleA = y
  
  angleB = math.atan2(m_y - odom_y, m_x - odom_x)
  angleC = math.atan2(u_y - odom_y, u_x - odom_x)
  gap = math.degrees(angleA-angleB)
  gap2 = math.degrees(angleA-angleC)

  distance_m = math.sqrt((m_x - odom_x)**2 + (m_y - odom_y)**2)
  distance_u = math.sqrt((u_x - odom_x)**2 + (u_y - odom_y)**2)

  angleD = math.atan2(m_y1 - odom_y, m_x - odom_x)
  angleE = math.atan2(u_y1 - odom_y, u_x - odom_x)
  gap3 = math.degrees(angleA-angleD)
  gap4 = math.degrees(angleA-angleE)

  distance_m1 = math.sqrt((m_x - odom_x)**2 + (m_y1 - odom_y)**2)
  distance_u1 = math.sqrt((u_x - odom_x)**2 + (u_y1 - odom_y)**2)

  angleF = math.atan2(center_y - odom_y, center_x - odom_x)
  gap5 = math.degrees(angleA-angleF)

def move_1():
    cmd_vel = rospy.Publisher('/robot/cmd_vel', Twist, queue_size=1)
    rospy.init_node('move_1', anonymous=True)
    msg = Twist()
    
    n=0
    while not rospy.is_shutdown():
      rospy.sleep(0.2)  
      msg.linear.x = linear_speed
      msg.angular.z = freeze_speed
      cmd_vel.publish(msg)
      n=n+1
      rospy.sleep(linear_time)
      if n >= 1:
        break

    msg.linear.x = freeze_speed
    msg.angular.z = freeze_speed
    cmd_vel.publish(msg)

def move_2():
    cmd_vel = rospy.Publisher('/robot/cmd_vel', Twist, queue_size=1)
    rospy.init_node('move_2', anonymous=True)
    msg = Twist()
    n=0
    
    while not rospy.is_shutdown():
      rospy.sleep(0.2) 
      msg.linear.x = linear_speed * (-1)
      msg.angular.z = freeze_speed
      cmd_vel.publish(msg)
      n=n+1
      rospy.sleep(linear_time)
      if n >= 1:
          break

    msg.linear.x = freeze_speed 
    msg.angular.z = freeze_speed
    cmd_vel.publish(msg)

def move_3():
    cmd_vel = rospy.Publisher('/robot/cmd_vel', Twist, queue_size=1)
    rospy.init_node('move_3', anonymous=True)
    msg = Twist()
    n=0

    while not rospy.is_shutdown():
      rospy.sleep(0.2) 
      msg.linear.x = freeze_speed
      msg.angular.z = angular_speed
      cmd_vel.publish(msg)
      n=n+1
      rospy.sleep(angular_time)
      if n >= 1:
          break

    msg.linear.x = freeze_speed
    msg.angular.z = freeze_speed
    cmd_vel.publish(msg)

def move_4():
    cmd_vel = rospy.Publisher('/robot/cmd_vel', Twist, queue_size=1)
    rospy.init_node('move_4', anonymous=True)
    msg = Twist()
    n=0

    while not rospy.is_shutdown():
      rospy.sleep(0.2)
      msg.linear.x = freeze_speed
      msg.angular.z = angular_speed * (-1)
      cmd_vel.publish(msg)
      n=n+1
      rospy.sleep(angular_time)
      if n >= 1:
          break

    msg.linear.x = freeze_speed
    msg.angular.z = freeze_speed
    cmd_vel.publish(msg)

class image:
  
  def __init__(self):
    self.image_pub = rospy.Publisher('image_topic', Image, queue_size=1)
    self.bridge = CvBridge()
    self.image_sub = rospy.Subscriber('robot/camera_side/image_raw', Image, self.callback)
   
  def callback(self, data):    
    cv_image = self.bridge.imgmsg_to_cv2(data, "bgr8")
    img = cv_image
    cv2.imwrite('/home/zhu/Desktop/picture_take.png', cv_image)

def move_5():
  ic = image()
  rospy.init_node('image', anonymous=True)

def move_5_1():
  rospy.sleep(0.5)

##  img = cv2.imread("/home/zhu/Desktop/picture_take.png")
##  cv2.imshow('image', img)
##  cv2.waitKey(0)
##  cv2.destroyAllWindows()
  
  import matplotlib.pyplot as plt
  import matplotlib.image  as mpimg
  img = mpimg.imread('/home/zhu/Desktop/picture_take.png')
  plt.figure(figsize=(10.0, 8.0))
  plt.imshow(img)
  plt.axis("off")
  plt.show()

ranges_min = 0.0

class range_min:
  
  def __init__(self):
    self.range_min_sub = rospy.Subscriber('/robot/hokuyo2', LaserScan, self.callback_ranges)

  def callback_ranges(eslf, msg):
    global ranges_min
    ranges_min = min(msg.ranges)

path = '/home/zhu/Desktop/BERT_temporaryname/bert_fine_tuning/range.txt'
 
def move_6():
  rm = range_min()
  rospy.init_node('move_6', anonymous=True)
  
  with open(path, mode='w') as f:
    f.write('距離 ＝ ')
  with open(path, mode='a') as f:
    f.write(str(ranges_min))

  with open(path, mode='r') as f:
    print(f.readline())

def move_7():
  rospy.init_node('move_7', anonymous=True)
  cmd_vel = rospy.Publisher('/robot/cmd_vel', Twist, queue_size=1)
  rospy.Subscriber('/robot/odom', Odometry, odomcbx)
  msg = Twist()
  n=0
  
  while True:
    print(gap5)
    msg.linear.x = freeze_speed
    msg.angular.z = angular_speed
    cmd_vel.publish(msg)
    if gap5 > -0.5 and gap5 < 0.5:
      break

  msg.linear.x = freeze_speed
  msg.angular.z = freeze_speed
  cmd_vel.publish(msg)
  rospy.sleep(0.1)

  while not rospy.is_shutdown():
    rospy.sleep(0.2) 
    msg.linear.x = linear_speed * (-0.5)
    msg.angular.z = freeze_speed
    cmd_vel.publish(msg)
    n=n+1
    rospy.sleep(linear_time)
    if n >= 1:
      break

  msg.linear.x = freeze_speed 
  msg.angular.z = freeze_speed
  cmd_vel.publish(msg)

def move_8():
  rospy.init_node('move_8', anonymous=True)
  cmd_vel = rospy.Publisher('/robot/cmd_vel', Twist, queue_size=1)
  rospy.Subscriber('/robot/odom', Odometry, odomcbx)
  msg = Twist()
  n=0
  
  while True:
    print(gap5)
    msg.linear.x = freeze_speed
    msg.angular.z = angular_speed
    cmd_vel.publish(msg)
    if gap5 > -0.5 and gap5 < 0.5:
      break

  msg.linear.x = freeze_speed
  msg.angular.z = freeze_speed
  cmd_vel.publish(msg)
  rospy.sleep(0.1)

  while not rospy.is_shutdown():
    rospy.sleep(0.2) 
    msg.linear.x = linear_speed * (0.5)
    msg.angular.z = freeze_speed
    cmd_vel.publish(msg)
    n=n+1
    rospy.sleep(linear_time)
    if n >= 1:
      break

  msg.linear.x = freeze_speed 
  msg.angular.z = freeze_speed
  cmd_vel.publish(msg)
  
def move_9():
  rospy.init_node('move_9', anonymous=True)
  cmd_vel = rospy.Publisher('/robot/cmd_vel', Twist, queue_size=1)
  rospy.Subscriber('/robot/odom', Odometry, odomcbx)
  msg = Twist()
  n = 0

  while True:
    print(gap2)
    msg.linear.x = freeze_speed
    msg.angular.z = angular_speed
    cmd_vel.publish(msg)
    if gap2 > -0.5 and gap2 < 0.5:
      break

  msg.linear.x = freeze_speed
  msg.angular.z = freeze_speed
  cmd_vel.publish(msg)
  rospy.sleep(0.1)

  while True:
    print(distance_u)
    msg.linear.x = linear_speed
    msg.angular.z = freeze_speed
    cmd_vel.publish(msg)
    if distance_u < 0.1:
      break
    
  msg.linear.x = freeze_speed
  msg.angular.z = freeze_speed
  cmd_vel.publish(msg)
  rospy.sleep(0.1)

#目標座標に移動
  while True:
    print(gap4)
    msg.linear.x = freeze_speed
    msg.angular.z = angular_speed
    cmd_vel.publish(msg)
    if gap4 > -0.5 and gap4 < 0.5:
      break

  msg.linear.x = freeze_speed
  msg.angular.z = freeze_speed
  cmd_vel.publish(msg)
  rospy.sleep(0.1)

  while True:
    print(distance_u1)
    msg.linear.x = linear_speed
    msg.angular.z = freeze_speed
    cmd_vel.publish(msg)
    if distance_u1 < 0.1:
      break
    
  msg.linear.x = freeze_speed
  msg.angular.z = freeze_speed
  cmd_vel.publish(msg)
  rospy.sleep(0.1)

def move_10():
  rospy.init_node('move_10', anonymous=True)
  cmd_vel = rospy.Publisher('/robot/cmd_vel', Twist, queue_size=1)
  rospy.Subscriber('/robot/odom', Odometry, odomcbx)
  msg = Twist()
  n = 0
  
  while True:
    print(gap)
    msg.linear.x = freeze_speed
    msg.angular.z = angular_speed
    cmd_vel.publish(msg)
    if gap > -0.5 and gap < 0.5:
      break

  msg.linear.x = freeze_speed
  msg.angular.z = freeze_speed
  cmd_vel.publish(msg)
  rospy.sleep(0.1)

  while True:
    print(distance_m)
    msg.linear.x = linear_speed
    msg.angular.z = freeze_speed
    cmd_vel.publish(msg)
    if distance_m < 0.1:
      break
    
  msg.linear.x = freeze_speed
  msg.angular.z = freeze_speed
  cmd_vel.publish(msg)

#目標座標に移動
  while True:
    print(gap3)
    msg.linear.x = freeze_speed
    msg.angular.z = angular_speed
    cmd_vel.publish(msg)
    if gap3 > -0.5 and gap3 < 0.5:
      break

  msg.linear.x = freeze_speed
  msg.angular.z = freeze_speed
  cmd_vel.publish(msg)
  rospy.sleep(0.1)

  while True:
    print(distance_m1)
    msg.linear.x = linear_speed
    msg.angular.z = freeze_speed
    cmd_vel.publish(msg)
    if distance_m1 < 0.1:
      break
    
  msg.linear.x = freeze_speed
  msg.angular.z = freeze_speed
  cmd_vel.publish(msg)
  rospy.sleep(0.1)

def action(label):
  if label == 1:
    move_1()
  if label == 2:
    move_2()
  if label == 3:
    move_3()
  if label == 4:
    move_4()
  if label == 5:
    move_5()
    move_5_1()
  if label == 6:
    move_6()
  if label == 7:
    move_7()
  if label == 8:
    move_8()
  if label == 9:
    move_9()
  if label == 10:
    move_10()
       
if __name__ == '__main__':
    action(move)
