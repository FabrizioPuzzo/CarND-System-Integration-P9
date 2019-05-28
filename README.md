# **Udacity self-driving Car Capstone Project : System Integration** 
[![Udacity - Self-Driving Car NanoDegree](https://s3.amazonaws.com/udacity-sdc/github/shield-carnd.svg)](http://www.udacity.com/drive)

---

This repo contains my solution to the Capstone Project: System Integration Project for the Udacity's Self-Driving Car Engineer Nanodegree Program.

---


![](/img/simulator.png)



## Project Overview

   In this project, the task is to write ROS nodes to implement core functionality of the autonomous vehicle system, including detection of traffic lights, control, lane following. The code is tested using a simulator and run on a real car named Carla. The system architecture diagram including ROS topics and ROS nodes is shonw below: 
![](/img/system_architecture.png)

### Subsystems

The three subsystems are:

   1. Perception - Camera and sensors to detect obstacles and traffic lights. In this project, we need to implement a node for traffic light detection. We chose to train a deep learning network model for the traffic light classification. 

   2. Planning - Subsystem (node waypoint updater) to update the waypoints and the associated target velocitie at any givin waypoint.

   3. Control - Subsystem to calculate and set the throttle-, steering-, and brake-outputs to navigate the waypoints with the target velocity.


### ROS Architecture

The ROS Architecture consists of different nodes (written in Python or C++) that communicate with each other via ROS messages (subscribing and publishing to ROS-topics). The ROS-architecture is shown below. (Ovally outlined text boxes inside rectangular boxes = ROS nodes; Simple rectangular boxes = ROS-topics). 
![](/img/rosgraph.jpg)

### Tasks

The three main Task of the project were the following:


   1. Perception - Implementation of a traffic light detection node. (Deep learning network model for the traffic light classification). 

   2. Planning - Implementation of a waypoint updater node to update the target velocity at according to a given situation (traffic light).  

   3. Control - Implementation of a control node (DBW node) to actuate the throttle, steering, and brake in order to navigate the waypoints with the target velocity.


## Starter Code Setup
### Native Installation

* Be sure that your workstation is running Ubuntu 16.04 Xenial Xerus or Ubuntu 14.04 Trusty Tahir. [Ubuntu downloads can be found here](https://www.ubuntu.com/download/desktop).
* If using a Virtual Machine to install Ubuntu, use the following configuration as minimum:
  * 2 CPU
  * 2 GB system memory
  * 25 GB of free hard drive space

  The Udacity provided virtual machine has ROS and Dataspeed DBW already installed, so you can skip the next two steps if you are using this.

* Follow these instructions to install ROS
  * [ROS Kinetic](http://wiki.ros.org/kinetic/Installation/Ubuntu) if you have Ubuntu 16.04.
  * [ROS Indigo](http://wiki.ros.org/indigo/Installation/Ubuntu) if you have Ubuntu 14.04.
* [Dataspeed DBW](https://bitbucket.org/DataspeedInc/dbw_mkz_ros)
  * Use this option to install the SDK on a workstation that already has ROS installed: [One Line SDK Install (binary)](https://bitbucket.org/DataspeedInc/dbw_mkz_ros/src/81e63fcc335d7b64139d7482017d6a97b405e250/ROS_SETUP.md?fileviewer=file-view-default)
* Download the [Udacity Simulator](https://github.com/udacity/CarND-Capstone/releases).

### Docker Installation
[Install Docker](https://docs.docker.com/engine/installation/)

Build the docker container
```bash
docker build . -t capstone
```

Run the docker file
```bash
docker run -p 4567:4567 -v $PWD:/capstone -v /tmp/log:/root/.ros/ --rm -it capstone
```

### Port Forwarding
To set up port forwarding, please refer to the [instructions from term 2](https://classroom.udacity.com/nanodegrees/nd013/parts/40f38239-66b6-46ec-ae68-03afd8a601c8/modules/0949fca6-b379-42af-a919-ee50aa304e6a/lessons/f758c44c-5e40-4e01-93b5-1a82aa4e044f/concepts/16cf4a78-4fc7-49e1-8621-3450ca938b77)

### Usage

1. Clone the project repository
```bash
git clone https://github.com/udacity/CarND-Capstone.git
```

2. Install python dependencies
```bash
cd CarND-Capstone
pip install -r requirements.txt
```
3. Make and run styx
```bash
cd ros
catkin_make
source devel/setup.sh
roslaunch launch/styx.launch
```
4. Run the simulator

### Real world testing
1. Download [training bag](https://s3-us-west-1.amazonaws.com/udacity-selfdrivingcar/traffic_light_bag_file.zip) that was recorded on the Udacity self-driving car.
2. Unzip the file
```bash
unzip traffic_light_bag_file.zip
```
3. Play the bag file
```bash
rosbag play -l traffic_light_bag_file/traffic_light_training.bag
```
4. Launch your project in site mode
```bash
cd CarND-Capstone/ros
roslaunch launch/site.launch
```
5. Confirm that traffic light detection works on real life images

## Implementation 
### Waypoint Updater

The Waypoint Updater node has the following subscribes to the following ROS-topics:

-   `/base_waypoints`
-   `/current_pose`


and publish a list of waypoints to the following ROS-topic:

-   `/final_waypoints`


The main functionality of the Waypoint Updater node is to calculate the correct target velocities (depending on traffic lights and maximum velocity) for a fixed number of waypoints ahead of the vehicle and publish those to the ROS-topic `/final_waypoints`. 


### Twist Controller

The twist controller package contains two main modules: dbw_node.py and twist_controller.py. 

The dbw_node.py, subscribes to the ROS-topics `/current_velocity`, `/twist_cmd`, and `/vehicle/dbw_enabled` and publishes the thottle, steering and brake signals. 

In the twist controller, a yaw controller (steering signal) and a PID controller (throttle signal) are implemented. Those signals are published to the ROS-Topic `/twist_cmd`.


### Traffic Light Detection

The tl_detector.py module subscribes to the ROS-topics `/current_pose`, `/base_waypoints`, `/image_color`(= Image input from camera) and publishes the waypoint index of the nearest RED light to the ROS-topic `/traffic_waypoint` (if detected). This module uses the traffic light classifier defined in the modle tl_classifier.py.

In this project a SSD Inception V2 model is used to classify the traffic light state. Two seperate models are trained: One for simulator and one for the real-world application. Both models are saved under ./ros/src/tl_detector/light_classification/model/.
