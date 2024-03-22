import rospy
from std_msgs.msg import Char
from std_msgs.msg import String
import bz2
import binascii

class StringOperations:
    def __init__(self):
        rospy.init_node("frequent_char", anonymous=True)
        self.init()
        self.run()

    def init(self):
        rospy.loginfo("String Operations Node Started!")

        self.sub = rospy.Subscriber("/bz2_message", String, self.callback)
        self.pub = rospy.Publisher("/frequent_char", Char, queue_size=10)
        self.rate = rospy.Rate(5)

        self.frequent_char = ""

    def callback(self, data):
        input_string = data.data
        
        
        # convert hex to ascii 
        ascii_string = binascii.unhexlify(input_string)
        string_o = bz2.decompress(ascii_string) 
        # Perform operations on the input string
        freq = {}
        for char in string_o:
            if char in freq:
                freq[char] += 1
            else:
                freq[char] = 1

        self.frequent_char = max(freq, key=freq.get)
        rospy.loginfo(self.frequent_char)

        # Publish the most frequent character

    def run(self):
        while not rospy.is_shutdown():

            frequent_char_msg = Char()
            frequent_char_msg.data = self.frequent_char
            self.pub.publish(frequent_char_msg)
            self.rate.sleep()

if __name__ == "__main__":
    try:
        StringOperations()
    except rospy.ROSInterruptException:
        pass

