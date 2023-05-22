from spike import PrimeHub, LightMatrix, Button, StatusLight, ForceSensor, MotionSensor, Speaker, ColorSensor, App, DistanceSensor, Motor, MotorPair
from spike.control import wait_for_seconds, wait_until, Timer
from math import *
import os

import hub

primeHub = PrimeHub()

import time

import uos
print(uos.listdir())

timer = Timer()
wait_until = None
time_last_instruction = time.ticks_ms()

STEERING_PERMITTED_OFFSET = 100000 
INSTRUCTION_FILEPATH = "DEMO.txt"
DATA_FILEPATH = "DATA.txt"
INTERRUPTS_ON = True
MAX_LIM = 31
MAX_EITHER_SIDE = 31
DRIVING_SPEED = 10

front_color = ColorSensor('B')
bottom_color = ColorSensor('D')
distance_sensor = DistanceSensor('E')
force_sensor = ForceSensor('F')

steering_motor = Motor('A')
driving_motor = Motor('C')

steering_center_angle = steering_motor.get_degrees_counted()

driving_center_angle = driving_motor.get_degrees_counted()

steering_motor_target_angle = steering_center_angle
driving_motor_target_angle = driving_center_angle

steering_motor_is_forward = True
driving_motor_is_forward = True

# Define the Imperial March melody
imperial_march = [
        (60, 1), (60, 1), (60, 1), (56, 0.75), (63, 0.25),
        (60, 1), (56, 0.75), (63, 0.25), (60, 1)
    ]

def play_song(melody):
    # Play each note in the melody
    for note, duration in melody:
        primeHub.speaker.beep(note, float(duration))
        time.sleep(duration / 10)# Delay between notes

def interpret_instruction(instruction):
        instruction_code = instruction.split(" ")
        opcode = instruction_code[0]
        operand = instruction_code[1:]
        if opcode == "MOTOR":
                handle_motor(operand[0], operand[1], operand[2])
                # BODGE - if steering - attempt two more times to ensure full lock
                if operand[0] == 'A':
                        handle_motor(operand[0], operand[1], int(operand[2])-1)
                        handle_motor(operand[0], operand[1], int(operand[2])+1)
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

        # Negated here so Backwards/Left = negative as opcode
        change_in_angle = -int(change_in_angle)
        speed = int(speed)
        if index == "A":
                speed = 50
                #if change_in_angle > 0:
                #        change_in_angle = MAX_LIM
                #else:
                #        change_in_angle = -MAX_LIM
                motor = steering_motor

                print("change in angle:", change_in_angle)
                steering_motor_target_angle = clamp(steering_motor.get_degrees_counted()+change_in_angle, steering_center_angle-STEERING_PERMITTED_OFFSET, steering_center_angle+STEERING_PERMITTED_OFFSET)                
                if change_in_angle > 0:
                        steering_motor_is_forward = True
                        # IMPORTANT - WE'RE NOW HARD CODING TO HARD LEFT HARD RIGHT
                        steering_motor_target_angle = steering_center_angle 
                else:
                        speed = - speed
                        steering_motor_is_forward = False
                        # IMPORTANT - WE'RE NOW HARD CODING TO HARD LEFT HARD RIGHT
                        steering_motor_target_angle = steering_center_angle - MAX_EITHER_SIDE
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
                # UNCOMMENT FOR MAX SPEED
                if speed > 0:
                        speed = DRIVING_SPEED
                else:
                        speed = -DRIVING_SPEED
                        driving_motor_is_forward = False
                print("set new driving motor target to", driving_motor_target_angle)
        else:
                pass
        motor.start(speed)

def handle_wait(time):
        global wait_until
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
        global time_last_instruction
        if "\#n" not in instruction_string:
                interpret_instruction(instruction_string.strip())
        time_last_instruction = time.ticks_ms()

def log_instruction(data_file, instruction_string):
        data_bytes = bytes("I:"+instruction_string.strip()+"\n", "utf-8")
        data_file.write(data_bytes)
        data_file.flush()

def log_interrupt(data_file, interrupt_string):
        data_bytes = bytes("E:"+interrupt_string.strip()+"\n", "utf-8")
        data_file.write(data_bytes)
        data_file.flush()

def log_sensor_data(data_file):
        global time_last_instruction
        front_r, front_g, front_b, front_intensity = front_color.get_rgb_intensity()
        bottom_r, bottom_g, bottom_b, bottom_intensity = bottom_color.get_rgb_intensity()
        accelerometer_x, accelerometer_y, accelerometer_z = hub.status()['accelerometer']
        yaw, pitch, roll = hub.status()['yaw_pitch_roll']
        gyro_x, gyro_y, gyro_z = hub.status()['gyroscope']
        data = [
                time.ticks_ms()-time_last_instruction,
                front_r,
                front_g,
                front_b,
                front_intensity,
                bottom_r,
                bottom_g,
                bottom_b,
                bottom_intensity,
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

        data_bytes = bytes("\n".join(data_strings)+"\n", "utf-8")
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


def bottom_color_interrupt(color_sensor):
        return color_sensor.get_color() == 'white' and INTERRUPTS_ON

def front_color_interrupt(color_sensor):
        return color_sensor.get_color() == 'yellow' and INTERRUPTS_ON

def distance_interrupt(distance_sensor):
        distance = distance_sensor.get_distance_cm()
        # distance is sometimes None when past 200cm
        if (distance == None):
                return False
        return distance<5 and INTERRUPTS_ON

def check_interrupt():
        if bottom_color_interrupt(bottom_color):
                #driving_motor.stop()
                handle_beep(58, 1)
                handle_beep(62, 1)
                interrupt_string = 'Bottom Colour'
                interrupt_string = None
        elif front_color_interrupt(front_color):
                driving_motor.stop()
                handle_beep(62, 1)
                handle_beep(58, 1)
                interrupt_string = 'Front Colour'
        elif distance_interrupt(distance_sensor):
                driving_motor.stop()
                #handle_beep(65, 1)
                #handle_beep(55, 1)
                #handle_beep(65, 1)
                play_song(imperial_march)
                interrupt_string = 'Distance'
        else:
                interrupt_string = None
        return interrupt_string


print("start")
print(wait_until)
with open(DATA_FILEPATH, "w") as data_file:
        with open(INSTRUCTION_FILEPATH, "r") as instruction_file:
                instructions = instruction_file.readlines()
                stop_agent = False
                for instruction_string in instructions:
                        #EXECUTE INSTRUCTION THEN SENSOR
                        print("executing instruction:", instruction_string)
                        log_instruction(data_file, instruction_string)
                        execute_instruction(instruction_string)

                        while not is_instruction_completed() and stop_agent == False:
                                #print("measured:", driving_motor.get_degrees_counted(), "/", driving_motor_target_angle)
                                #print("measured:", steering_motor.get_degrees_counted(), "/", steering_motor_target_angle)
                                interrupt_string = check_interrupt()
                                log_sensor_data(data_file)
                                if interrupt_string != None:
                                        log_interrupt(data_file, interrupt_string)
                                        print(interrupt_string)
                                        stop_agent = True
                        driving_motor.stop()
                        steering_motor.stop()
                        #print("instruction is done, measured: ", driving_motor.get_degrees_counted(), "/", driving_motor_target_angle)
                        #print("instruction is done, measured: ", steering_motor.get_degrees_counted(), "/", steering_motor_target_angle)
                        print(os.stat(DATA_FILEPATH))
                        if stop_agent:
                                print("STOPPING!!!")
                                break





print("done: ",timer.now())
