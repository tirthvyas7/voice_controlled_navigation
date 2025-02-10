# Voice-Controlled Robot:
Controlling Robot just got simpler using voice commands



## System Requirements
- **Operating System:** Ubuntu 22.04
- **ROS 2 Distribution:** Humble
- Working Microphone

## Dependencies
Ensure the following dependencies are installed before running the project:

```bash
sudo apt update
sudo apt install ros-humble-gazebo-ros-pkgs
sudo apt install portaudio19-dev
pip install pyaudio
```

## Cloning the Repository
Clone this repository to your workspace:

```bash
mkdir ros2_ws
cd ros2_ws
mkdir src
cd src
git clone https://github.com/tirthvyas7/voice_controlled_navigation.git
```

## Building the Package:
Build and Source Packages with these commands
```bash
cd ../.. #Ensure you are in ros2_ws
colcon build
source install/setup.bash
```

## Running the Launch File
To start the voice-controlled robot, run the following command:

```bash
ros2 launch bot_world robot.launch.xml
```
The above command will open gazebo classic and spawn the differential drive robot in a custom world ready to be controlled by voice commands.

## Acceptable Voice Commands:
The system recognizes the following voice commands:
- "move forward"
- "turn left"
- "turn right"
- "stop"
- "move backward"

You can also give multiple commands in a sentence and robot will follow those in the given sequence.
Eg:
- "Turn right and then move forward"

Make sure to speak clearly for better recognition performance.

