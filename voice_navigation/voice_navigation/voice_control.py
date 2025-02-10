import rclpy
from rclpy.node import Node
from std_msgs.msg import String
import speech_recognition as sr
from geometry_msgs.msg import Twist
import time

class SpeechToTextNode(Node):
    def __init__(self):
        super().__init__('voice_control')

        # Publisher to publish transcribed text
        self.vel_publisher = self.create_publisher(Twist, 'cmd_vel', 10)

        # Recognizer instance
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()

        # Start listening
        self.get_logger().info("Listening for speech...")
        self.listen_for_speech()

    def listen_for_speech(self):
        with self.microphone as source:
            self.recognizer.adjust_for_ambient_noise(source)
            self.get_logger().info("Listening...")

            while rclpy.ok():
                try:
                    audio = self.recognizer.listen(source)

                    # Send to Google Speech API
                    text = self.recognizer.recognize_google(audio)
                    self.get_logger().info(f"Recognized: {text}")

                    self.process_command(text)
                    
                    
                    

                except sr.UnknownValueError:
                    self.get_logger().warn("Could not understand the audio.")
                except sr.RequestError as e:
                    self.get_logger().error(f"API request failed: {e}")
    
    def process_command(self,text):

        
        text=str(text).lower()
        
        commands = ["move forward", "turn left", "turn right", "stop", "move backward"]

        # Store (index, phrase) pairs
        found_commands = []

        for command in commands:
            start = 0
            while (pos := text.find(command, start)) != -1:  # Find all occurrences
                found_commands.append((pos, command))
                start = pos + 1  # Move start position forward to find the next occurrence

        # Sort by index to maintain the order in text
        found_commands.sort()

        # Extract only the phrases in order
        ordered_commands = [phrase for _, phrase in found_commands]

        for command in ordered_commands:
            if command == "stop":
                self.stop()
                self.get_logger().info("Stopped")
            elif command == "move forward":
                self.move_forward()
            elif command == "move backward":
                self.move_backward()
            elif command == "turn left":
                self.turn_left()
            elif command == "turn right":
                self.turn_right()


        

    def stop(self):
        msg = Twist()
        self.vel_publisher.publish(msg)


    def move_forward(self):
        self.is_moving=True
        msg = Twist()
        msg.linear.x=0.3
        self.vel_publisher.publish(msg)
        self.get_logger().info("Moving Forward")
    
    def move_backward(self):
        msg = Twist()
        msg.linear.x=-0.3
        self.vel_publisher.publish(msg)
        self.get_logger().info("Moving Backward")

    def turn_left(self):
        msg = Twist()
        msg.angular.z=0.3
        self.vel_publisher.publish(msg)
        time.sleep(5.0)
        self.stop()
        self.get_logger().info("Turned Left")
    def turn_right(self):
        msg = Twist()
        msg.angular.z=-0.35
        self.vel_publisher.publish(msg)
        time.sleep(5.0)
        self.stop()
        self.get_logger().info("Turned Right")



def main(args=None):
    rclpy.init(args=args)
    node = SpeechToTextNode()
    
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.get_logger().info("Shutting down speech-to-text node.")
    
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()



