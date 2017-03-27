#!/usr/bin/python
import rospy
from geometry_msgs.msg import Twist
from sensor_msgs.msg import Joy
import std_srvs.srv

class TeleopTurtle:
    def __init__(self):
        rospy.init_node('turtle_teleop_joy')
        self.linear_axis = rospy.get_param("axis_linear")
        self.angular_axis = rospy.get_param("axis_angular")
        self.linear_scale = rospy.get_param("scale_linear")
        self.angular_scale = rospy.get_param("scale_angular")
        self.robot_topic_name = rospy.get_param("robot_topic_name") 

        rospy.wait_for_service('reset')

        self.twist = None
        self.twist_pub = rospy.Publisher(self.robot_topic_name, Twist,queue_size=1)
        rospy.Subscriber("joy", Joy, self.callback)
        rate = rospy.Rate(rospy.get_param('~hz', 20))

        while not rospy.is_shutdown():
            rate.sleep()
            if self.twist:
                self.twist_pub.publish(self.twist)

    def callback(self,msg):
        twist = Twist()
        twist.linear.x = 10*abs(msg.axes[3]) * msg.axes[self.linear_axis]
        twist.angular.z = self.angular_scale * msg.axes[self.angular_axis]
        self.twist=twist
	if (msg.buttons[3]==1 and msg.buttons[2]==1):
          serv = rospy.ServiceProxy('reset', std_srvs.srv.Empty)
          serv()

if __name__ == "__main__": 
    TeleopTurtle()

