import rospy
from std_msgs.msg import Char
from std_msgs.msg import String
import bz2
import binascii

class msg_converter:
    def __init__(self):
        rospy.init_node("frequent_char", anonymous=True)
        self.init()
        self.run()

    def init(self):
        rospy.loginfo("Message Converter Node Started!")

        self.sub = rospy.Subscriber("/bz2_message", String, self.callback)
        self.pub = rospy.Publisher("/frequent_char", Char, queue_size=10)
        self.rate = rospy.Rate(5)

        self.frequent_char = ""

    def callback(self, data):
        input_string = data.data
        
        # convert hex to ascii 
        ascii_string = binascii.unhexlify(input_string)
        
        # decompress bz2
        string_o = bz2.decompress(ascii_string) 
        
        # find the most frequent char
        freq = {}
        for char in string_o:
            if char in freq:
                freq[char] += 1
            else:
                freq[char] = 1

        self.frequent_char = max(freq, key=freq.get)
        rospy.loginfo(self.frequent_char)


    def run(self):
        while not rospy.is_shutdown():
            frequent_char_msg = Char()
            frequent_char_msg.data = self.frequent_char
            self.pub.publish(frequent_char_msg)
            self.rate.sleep()

if __name__ == "__main__":
    try:
        msg_converter()
    except rospy.ROSInterruptException:
        pass

