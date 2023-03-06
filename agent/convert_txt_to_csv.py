import csv

data_file = "PuttyExample.txt"

headers = [
    'instruction',
    'timestamp',
    'front_r', 
    'front_g', 
    'front_b', 
    'front_intensity',
    'rear_r', 
    'rear_g', 
    'rear_b', 
    'rear_intensity',
    'distance',
    'accelerometer_x', 
    'accelerometer_y', 
    'accelerometer_z',
    'yaw',
    'pitch',
    'roll',
    'gyro_x',
    'gyro_y',
    'gyro_z',
    'steering_motor_angle',
    'driving_motor_angle',
]

text_file = open(data_file, 'r')

with open('csv_test_data.csv', 'w') as csv_file:
    writer = csv.writer(csv_file)

    text = text_file.readlines()

    print(len(text))
    
    writer.writerow(headers)
    
    # Change logging.py to make each output on a new line
    for line in text:
        # sanitise line
        writer.writerow(line)