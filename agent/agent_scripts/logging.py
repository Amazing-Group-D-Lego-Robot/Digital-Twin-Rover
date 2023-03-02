from spike import PrimeHub, LightMatrix, Button, StatusLight, ForceSensor, MotionSensor, Speaker, ColorSensor, App, DistanceSensor, Motor, MotorPair
from spike.control import wait_for_seconds, wait_until, Timer
from math import *

import hub

primeHub = PrimeHub()

import time

import uos
print(uos.listdir())

timer = Timer()
wait_until = None
time_last_instruction = time.ticks_ms()


front_color = ColorSensor('B')
rear_color = ColorSensor('D')
distance_sensor = DistanceSensor('E')
force_sensor = ForceSensor('F')

steering_motor = Motor('A')
driving_motor = Motor('C')

steering_center_angle = steering_motor.get_degrees_counted()
steering_permitted_offset = 5

driving_center_angle = driving_motor.get_degrees_counted()

steering_motor_target_angle = steering_center_angle
driving_motor_target_angle = driving_center_angle

steering_motor_is_forward = True
driving_motor_is_forward = True

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
        global steering_motor_target_angle
        global driving_motor_target_angle
        global steering_motor_is_forward
        global driving_motor_is_forward
        global steering_center_angle

        change_in_angle = int(change_in_angle)
        speed = int(speed)
        if index == "A":
                speed = 1
                motor = steering_motor

                print("change in angle:", change_in_angle)
                steering_motor_target_angle = clamp(steering_motor.get_degrees_counted()+change_in_angle, steering_center_angle-steering_permitted_offset, steering_center_angle+steering_permitted_offset)
                if change_in_angle > 0:
                        steering_motor_is_forward = True
                else:
                        speed = - speed
                        steering_motor_is_forward = False
                print("Centre", steering_center_angle)
                print("set new steering motor target to", steering_motor_target_angle)
        elif index == "C":
                motor = driving_motor
                print("change in angle:", change_in_angle)
                driving_motor_target_angle = driving_motor.get_degrees_counted()+change_in_angle
                if change_in_angle > 0:
                        driving_motor_is_forward = True
                else:
                        speed = - speed
                        driving_motor_is_forward = False
                print("set new driving motor target to", driving_motor_target_angle)
        else:
                pass
        motor.start(speed)

def handle_wait(time):
        wait_until = timer.now() + int(time)

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

def execute_instruction(instruction_string):
        if "\#n" not in instruction_string:
                interpret_instruction(instruction_string.strip())
        time_last_instruction = time.ticks_ms()

def log_instruction(data_file, instruction_string):
        data_bytes = bytes("I:"+instruction_string.strip(), "utf-8")
        data_file.write(data_bytes)
        data_file.flush()

def log_sensor_data(data_file):
        global time_last_instruction
        front_r, front_g, front_b, front_intensity = front_color.get_rgb_intensity()
        rear_r, rear_g, rear_b, rear_intensity = rear_color.get_rgb_intensity()
        accelerometer_x, accelerometer_y, accelerometer_z = hub.status()['accelerometer']
        yaw, pitch, roll = hub.status()['yaw_pitch_roll']
        gyro_x, gyro_y, gyro_z = hub.status()['gyroscope']
        data = [
                time.ticks_ms()-time_last_instruction,
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
                force_sensor.get_force_newton(),
        ]
        data_strings = [str(x) for x in data]

        data_bytes = bytes("\n".join(data_strings), "utf-8")
        data_file.write(data_bytes)
        data_file.flush()

def within_tolerance(motor, target_angle, target_tolerance):
        motor_value = motor.get_degrees_counted()
        print("checking tolerance, target:", target_angle, "actual:", motor_value)
        print("tolerance", target_tolerance, "difference:", abs(motor_value - target_angle))
        return target_tolerance < abs(motor_value - target_angle)

def is_instruction_completed():
        global wait_until
        global driving_motor_target_angle
        global steering_motor_target_angle
        global driving_motor_is_forward
        global steering_motor_is_forward
        global driving_motor
        global steering_motor

        driving_motor_value = driving_motor.get_degrees_counted()
        steering_motor_value = steering_motor.get_degrees_counted()

        if wait_until != None:
                if timer.now() <= wait_until:
                        return False
                else:
                        wait_until = None
        degree_tolerance = 5
        
        if driving_motor_is_forward:
                if driving_motor_value < driving_motor_target_angle:
                        return False
        else:
                if driving_motor_value > driving_motor_target_angle:
                        return False

        if steering_motor_is_forward:
                if steering_motor_value < steering_motor_target_angle:
                        return False
        else:
                if steering_motor_value > steering_motor_target_angle:
                        return False

        return True
        

print("start")
print(wait_until)
with open("data/sensor_log.txt", "w") as data_file:
        with open("data/instruction_set_2.txt","r") as instruction_file:
                instructions = instruction_file.readlines()
                for instruction_string in instructions:
                        #EXECUTE INSTRUCTION THEN SENSOR
                        print("executing instruction:", instruction_string)
                        log_instruction(data_file, instruction_string)
                        execute_instruction(instruction_string)

                        while not is_instruction_completed():
                                print("measured:", driving_motor.get_degrees_counted(), "/", driving_motor_target_angle)
                                print("measured:", steering_motor.get_degrees_counted(), "/", steering_motor_target_angle)
                                log_sensor_data(data_file)
                        driving_motor.stop()
                        steering_motor.stop()
                        print("instruction is done, measured: ", driving_motor.get_degrees_counted(), "/", driving_motor_target_angle)
                        print("instruction is done, measured: ", steering_motor.get_degrees_counted(), "/", steering_motor_target_angle)
                        
                        




print("done: ",timer.now())
