import pandas as pd
import re

def parse_input_data(input_data: str):

    entries = input_data.split(',')

    stripping_regex = re.compile(r"(?<=')[^'\n]*(?=\n')")
    
    stripped_entries = [stripping_regex.search(entry).group(0) for entry in entries]
    
    instructions = []
    instruction = []
    for entry in stripped_entries:
        if entry[:2] == "I:":
            instructions.append(instruction)
            instruction = []
        instruction.append(entry)
    instructions = instructions[1:]

    structured_data = []
    for instruction in instructions:
        instruction_string = instruction[0]


        instruction_measurements = instruction[1:]
        number_of_measurements = len(instruction_measurements)//22
        print(len(instruction_measurements))
        pass
        
        structured_measurements = []
        for i in range(number_of_measurements):
            measurements = instruction_measurements[i*22:(i+1)*22]
            structured_measurement = {
                "time": measurements[0],
                "front_r": measurements[1],
                "front_g": measurements[2],
                "front_b": measurements[3],
                "front_intensity": measurements[4],
                "rear_r": measurements[5],
                "rear_g": measurements[6],
                "rear_b": measurements[7],
                "rear_intensity": measurements[8],
                "distance_sensor": measurements[9],
                "accelerometer_x": measurements[10],
                "accelerometer_y": measurements[11],
                "accelerometer_z": measurements[12],
                "yaw": measurements[13],
                "pitch": measurements[14],
                "roll": measurements[15],
                "gyro_x": measurements[16],
                "gyro_y": measurements[17],
                "gyro_z": measurements[18],
                "steering_motor_position": measurements[19],
                "driving_motor_position": measurements[20],
                "force_sensor_newton": measurements[21],
            }
            structured_measurements.append(structured_measurement)

        structured_datum = {
            "instruction": instruction_string,
            "measurements": structured_measurements,
        }
        structured_data.append(structured_datum)








    return True
