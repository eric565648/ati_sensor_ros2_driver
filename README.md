# ATIForceSensorROS2Driver
The ROS2 package for ATI force torque sensor.

## System Requirement

1. ROS2 Foxy
2. Python3.8

## Run
Remeber to set up the workspace every time opening a new terminal.

Open a terminal
```
ros2 run ati_sensor_ros_driver ati_driver
```

If you want to visualize the wrench measure, 
1. open rviz. `ros2 run rviz2 rviz2`
2. Change the frame to `ati_frame`
3. Add -> By topic -> ati_ft

You should be seeing an pink arrow point to the total force direcion and a yellow arrow and circle illustrating the total torque.

## ROS Service

### Set tare
In one terminal
```
ros2 service call /set_ati_tare std_srvs/srv/Trigger
```

### Clear tare
In one terminal
```
ros2 service call /clear_ati_tare std_srvs/srv/Trigger
```

Generally you will not clear the tare.
