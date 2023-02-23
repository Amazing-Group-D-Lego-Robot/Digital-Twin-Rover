from spike import PrimeHub, LightMatrix, Button, StatusLight, ForceSensor, MotionSensor, Speaker, ColorSensor, App, DistanceSensor, Motor, MotorPair
from spike.control import wait_for_seconds, wait_until, Timer
from math import *

import hub

primeHub = PrimeHub()

import time

import uos
print(uos.listdir())

timer = Timer()

front_color = ColorSensor('D')
rear_color = ColorSensor('F')
distance_sensor = DistanceSensor('B')

steering_motor = Motor('A')
driving_motor = Motor('C')

def interpret_instruction(instruction):
        instruction_code = instruction.split(" ")
        opcode = instruction_code[0]
        operand = instruction_code[1:]
        if opcode == "MOTOR":
                handle_motor(operand[0], operand[1], operand[2])
        elif opcode == "WAIT":
                handle_wait(operand[0])
        elif opcode == "LIGHT_DISTANCE":
                handle_light_distance(operand[0], operand[1])
        elif opcode == "LIGHT_MATRIX":
                handle_light_matrix(operand[0], operand[1], operand[2])
        elif opcode == "LIGHT_STATUS":
                handle_light_status(operand[0], operand[1])
        elif opcode == "BEEP":
                handle_beep(operand[0], operand[1])

def clamp(n, smallest, largest):
        return max(smallest, min(n, largest))


def handle_motor(index, speed, change_in_angle):
        change_in_angle = int(change_in_angle)
        speed = int(speed)
        if index == "A":
                motor = steering_motor
                max_motor_degrees = 15
                if abs(change_in_angle) > max_motor_degrees:
                        print("Steering max angle exceeded, " + str(max_motor_degrees) + " degrees is the max +- angle")
                        change_in_angle = clamp(change_in_angle, -max_motor_degrees, max_motor_degrees)
        elif index == "C":
                motor = driving_motor
        else: 
                pass
        motor.run_for_degrees(change_in_angle, speed)

def handle_wait(time):
        wait_for_seconds(float(time))

def handle_light_distance(index, intensity):
        distance_sensor.light_up_all(int(intensity))

def handle_light_matrix(x_index, y_index, intensity):
        primeHub.light_matrix.set_pixel(int(x_index), int(y_index), int(intensity))
        

def handle_light_status(color, intensity):
        if intensity == "1":
                primeHub.status_light.on(color)
        else: 
                primeHub.status_light.off()

def handle_beep(note, time):
        primeHub.speaker.beep(int(note), float(time))


with open("data/sensor_log.txt", "w") as data_file:
        with open("data/instruction_set.txt","r") as instruction_file:
                instructions = instruction_file.readlines()
                for instruction_string in instructions:
                        #EXECUTE INSTRUCTION THEN SENSOR
                        print(instruction_string)
                        if "\#n" not in instruction_string:
                                interpret_instruction(instruction_string.strip())
                        front_r, front_g, front_b, front_intensity = front_color.get_rgb_intensity()
                        rear_r, rear_g, rear_b, rear_intensity = rear_color.get_rgb_intensity()
                        accelerometer_x, accelerometer_y, accelerometer_z = hub.status()['accelerometer']
                        yaw, pitch, roll = hub.status()['yaw_pitch_roll']
                        gyro_x, gyro_y, gyro_z = hub.status()['gyroscope']
                        data = [
                                "I:"+instruction_string.strip(),
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
                        data_file.write(data_bytes)
                        data_file.flush()



print("done: ",timer.now())