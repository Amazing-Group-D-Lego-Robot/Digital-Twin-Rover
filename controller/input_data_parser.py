import pandas as pd


def parse_input_data(input_data: str):
    entries = input_data.split('\n')

    # stripping_regex = re.compile(r"(?<=')[^'\n]*(?=\n')")

    # stripped_entries = [stripping_regex.search(entry).group(0) for entry in entries]

    instructions = []
    instruction = []
    for entry in entries:
        if entry[:2] == "I:":
            instructions.append(instruction)
            instruction = []
        instruction.append(entry)
    instructions.append(instruction)
    instructions = instructions[1:]

    structured_data = []
    headers = ["time", "front_r", "front_g", "front_b", "front_intensity", "rear_r", "rear_g", "rear_b",
               "rear_intensity", "distance_sensor", "accelerometer_x", "accelerometer_y", "accelerometer_z", "yaw",
               "pitch", "roll", "gyro_x", "gyro_y", "gyro_z", "steering_motor_position", "driving_motor_position",
               "force_sensor_newton"]
    for instruction in instructions:
        instruction_string = instruction[0]

        instruction_measurements = instruction[1:]
        number_of_measurements = len(instruction_measurements) // 22
        structured_measurements = pd.DataFrame(columns=headers)
        for i in range(number_of_measurements):
            measurements = instruction_measurements[i * 22:(i + 1) * 22]
            measurements = [[None if m == 'None' else int(m) for m in measurements]]
            row = pd.DataFrame(measurements, columns=headers)
            structured_measurements = pd.concat([structured_measurements, row])

        structured_datum = {
            "instruction": instruction_string,
            "measurements": structured_measurements,
        }
        structured_data.append(structured_datum)

    return structured_data
