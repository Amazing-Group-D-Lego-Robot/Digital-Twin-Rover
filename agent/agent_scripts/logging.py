from spike import PrimeHub, LightMatrix, Button, StatusLight, ForceSensor, MotionSensor, Speaker, ColorSensor, App, DistanceSensor, Motor, MotorPair
from spike.control import wait_for_seconds, wait_until, Timer
from math import *

import hub

import time

timer = Timer()

front_color = ColorSensor('D')
rear_color = ColorSensor('F')
distance_sensor = DistanceSensor('B')

steering_motor = Motor('A')
driving_motor = Motor('C')

with open("data/sensor_log.txt", "w") as file:
        for i in range(10):
                wait_for_seconds(0.25)
                front_r, front_g, front_b, front_intensity = front_color.get_rgb_intensity()
                rear_r, rear_g, rear_b, rear_intensity = rear_color.get_rgb_intensity()
                accelerometer_x, accelerometer_y, accelerometer_z = hub.status()['accelerometer']
                yaw, pitch, roll = hub.status()['yaw_pitch_roll']
                gyro_x, gyro_y, gyro_z = hub.status()['gyroscope']
                data = [
                        time.ticks_ms(),
                        front_r, 
                        front_g, 
                        front_b, 
                        front_intensity,
                        rear_r, 
                        rear_g, 
                        rear_b, 
                        rear_intensity,
                        distance_sensor.get_distance_cm(),
                        accelerometer_x, 
                        accelerometer_y, 
                        accelerometer_z,
                        yaw,
                        pitch,
                        roll,
                        gyro_x,
                        gyro_y,
                        gyro_z,
                        steering_motor.get_position(),
                        driving_motor.get_position(),
                ]
                data_strings = [str(x) for x in data]

                data_bytes = bytes("\n".join(data_strings), "utf-8")
                file.write(data_bytes)
                file.flush()



print(timer.now())