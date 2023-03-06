import pandas as pd
from .input_data_parser import parse_input_data, structured_input_data_to_pandas

def test_parse_input_data():
    input_data = "['I:MOTOR C 2 -3\n', '1633\n', '0\n', '2\n', '2\n', '2\n', '48\n', '49\n', '51\n', '116\n', '93\n', '0\n', '35\n', '992\n', '-52\n', '1\n', '0\n', '0\n', '0\n', '0\n', '88\n', '84\n', '0\n', '2353\n', '0\n', '2\n', '2\n', '2\n', '46\n', '48\n', '49\n', '111\n', '93\n', '72\n', '11\n', '987\n', '-52\n', '2\n', '-2\n', '0\n', '0\n', '0\n', '88\n', '79\n', '0\n', 'I:MOTOR A 11 -14\n', '4657\n', '1\n', '0\n', '0\n', '2\n', '48\n', '49\n', '51\n', '114\n', '93\n', '42\n', '-29\n', '990\n', '-55\n', '1\n', '0\n', '-1\n', '-1\n', '3\n', '42\n', '62\n', '0\n', 'I:MOTOR C 2 5\n', '6773\n', '1\n', '2\n', '2\n', '2\n', '46\n', '48\n', '49\n', '111\n', '94\n', '-1\n', '21\n', '995\n', '-55\n', '1\n', '0\n', '0\n', '0\n', '0\n', '22\n', '60\n', '0\n', '7441\n', '1\n', '2\n', '2\n', '1\n', '46\n', '48\n', '49\n', '111\n', '94\n', '-32\n', '20\n', '991\n', '-55\n', '1\n', '0\n', '0\n', '0\n', '0\n', '22\n', '62\n', '0\n', 'I:MOTOR C 17 -11\n', '9365\n', '0\n', '2\n', '2\n', '2\n', '50\n', '54\n', '55\n', '121\n', '95\n', '13\n', '21\n', '994\n', '-53\n', '1\n', '0\n', '0\n', '0\n', '-10\n', '22\n', '37\n', '0\n', 'I:MOTOR C 7 -11\n', '11569\n', '0\n', '1\n', '2\n', '2\n', '35\n', '36\n', '37\n', '84\n', '97\n', '0\n', '26\n', '995\n', '-48\n', '1\n', '0\n', '0\n', '0\n', '0\n', '22\n', '358\n', '0\n', '12246\n', '1\n', '0\n', '0\n', '1\n', '48\n', '51\n', '53\n', '117\n', '100\n', '-10\n', '17\n', '1015\n', '-43\n', '1\n', '0\n', '0\n', '0\n', '-11\n', '22\n', '305\n', '0\n', 'I:MOTOR A 17 10\n', '13153\n', '0\n', '1\n', '2\n', '1\n', '55\n', '58\n', '59\n', '132\n', 'None\n', '-1\n', '17\n', '1003\n', '-40\n', '1\n', '0\n', '1\n', '0\n', '-2\n', '37\n', '284\n', '0\n', 'I:MOTOR C 9 -9\n', '13829\n', '0\n', '1\n', '2\n', '1\n', '40\n', '43\n', '43\n', '97\n', '102\n', '-5\n', '31\n', '996\n', '-39\n', '1\n', '0\n', '0\n', '0\n', '0\n', '49\n', '283\n', '0\n', '14117\n', '0\n', '1\n', '2\n', '1\n', '39\n', '41\n', '43\n', '95\n', '102\n', '-4\n', '33\n', '998\n', '-39\n', '2\n', '0\n', '0\n', '0\n', '0\n', '49\n', '283\n', '0\n', '14406\n', '1\n', '1\n', '2\n', '1\n', '33\n', '35\n', '37\n', '81\n', 'None\n', '27\n', '19\n', '1001\n', '-37\n', '1\n', '-1\n', '-2\n', '0\n', '-17\n', '49\n', '265\n', '0\n', 'I:MOTOR C 20 0\n', 'I:MOTOR C 6 11\n', '15505\n', '1\n', '0\n', '0\n', '1\n', '43\n', '44\n', '47\n', '103\n', '105\n', '-3\n', '30\n', '998\n', '-33\n', '1\n', '0\n', '0\n', '0\n', '0\n', '49\n', '238\n', '0\n', '15989\n', '1\n', '0\n', '0\n', '1\n', '37\n', '39\n', '41\n', '89\n', 'None\n', '-24\n', '24\n', '993\n', '-35\n', '1\n', '1\n', '-1\n', '0\n', '7\n', '49\n', '257\n', '0\n', 'I:MOTOR A 12 -4\n', '18193\n', '0\n', '0\n', '0\n', '1\n', '45\n', '47\n', '49\n', '109\n', '103\n', '-11\n', '19\n', '1000\n', '-39\n', '1\n', '0\n', '-1\n', '0\n', '0\n', '18\n', '280\n', '0\n', 'I:MOTOR C 7 13\n', '20401\n', '0\n', '0\n', '0\n', '1\n', '44\n', '47\n', '49\n', '108\n', '103\n', '7\n', '14\n', '996\n', '-39\n', '1\n', '0\n', '-1\n', '0\n', '0\n', '15\n', '285\n', '0\n', '21173\n', '1\n', '0\n', '0\n', '1\n', '57\n', '62\n', '63\n', '139\n', 'None\n', '-17\n', '9\n', '997\n', '-42\n', '0\n', '0\n', '0\n', '0\n', '5\n', '14\n', '323\n', '0\n', 'I:MOTOR C 18 -11\n', '22453\n', '1\n', '0\n', '0\n', '2\n', '59\n', '62\n', '63\n', '142\n', '100\n', '33\n', '25\n', '1017\n', '-45\n', '0\n', '0\n', '2\n', '0\n', '-1\n', '14\n', '342\n', '0\n', 'I:MOTOR C 0 -13\n', '23281\n', '1\n', '0\n', '0\n', '2\n', '52\n', '55\n', '57\n', '125\n', '101\n', '-7\n', '13\n', '998\n', '-44\n', '0\n', '0\n', '0\n', '0\n', '0\n', '15\n', '328\n', '0\n'] "

    expected_result = [{'instruction': 'I:MOTOR C 2 -3', 'measurements': [{'time': '1633', 'front_r': '0', 'front_g': '2', 'front_b': '2', 'front_intensity': '2', 'rear_r': '48', 'rear_g': '49', 'rear_b': '51', 'rear_intensity': '116', 'distance_sensor': '93', 'accelerometer_x': '0', 'accelerometer_y': '35', 'accelerometer_z': '992', 'yaw': '-52', 'pitch': '1', 'roll': '0', 'gyro_x': '0', 'gyro_y': '0', 'gyro_z': '0', 'steering_motor_position': '88', 'driving_motor_position': '84', 'force_sensor_newton': '0'}, {'time': '2353', 'front_r': '0', 'front_g': '2', 'front_b': '2', 'front_intensity': '2', 'rear_r': '46', 'rear_g': '48', 'rear_b': '49', 'rear_intensity': '111', 'distance_sensor': '93', 'accelerometer_x': '72', 'accelerometer_y': '11', 'accelerometer_z': '987', 'yaw': '-52', 'pitch': '2', 'roll': '-2', 'gyro_x': '0', 'gyro_y': '0', 'gyro_z': '0', 'steering_motor_position': '88', 'driving_motor_position': '79', 'force_sensor_newton': '0'}]}, {'instruction': 'I:MOTOR A 11 -14', 'measurements': [{'time': '4657', 'front_r': '1', 'front_g': '0', 'front_b': '0', 'front_intensity': '2', 'rear_r': '48', 'rear_g': '49', 'rear_b': '51', 'rear_intensity': '114', 'distance_sensor': '93', 'accelerometer_x': '42', 'accelerometer_y': '-29', 'accelerometer_z': '990', 'yaw': '-55', 'pitch': '1', 'roll': '0', 'gyro_x': '-1', 'gyro_y': '-1', 'gyro_z': '3', 'steering_motor_position': '42', 'driving_motor_position': '62', 'force_sensor_newton': '0'}]}, {'instruction': 'I:MOTOR C 2 5', 'measurements': [{'time': '6773', 'front_r': '1', 'front_g': '2', 'front_b': '2', 'front_intensity': '2', 'rear_r': '46', 'rear_g': '48', 'rear_b': '49', 'rear_intensity': '111', 'distance_sensor': '94', 'accelerometer_x': '-1', 'accelerometer_y': '21', 'accelerometer_z': '995', 'yaw': '-55', 'pitch': '1', 'roll': '0', 'gyro_x': '0', 'gyro_y': '0', 'gyro_z': '0', 'steering_motor_position': '22', 'driving_motor_position': '60', 'force_sensor_newton': '0'}, {'time': '7441', 'front_r': '1', 'front_g': '2', 'front_b': '2', 'front_intensity': '1', 'rear_r': '46', 'rear_g': '48', 'rear_b': '49', 'rear_intensity': '111', 'distance_sensor': '94', 'accelerometer_x': '-32', 'accelerometer_y': '20', 'accelerometer_z': '991', 'yaw': '-55', 'pitch': '1', 'roll': '0', 'gyro_x': '0', 'gyro_y': '0', 'gyro_z': '0', 'steering_motor_position': '22', 'driving_motor_position': '62', 'force_sensor_newton': '0'}]}, {'instruction': 'I:MOTOR C 17 -11', 'measurements': [{'time': '9365', 'front_r': '0', 'front_g': '2', 'front_b': '2', 'front_intensity': '2', 'rear_r': '50', 'rear_g': '54', 'rear_b': '55', 'rear_intensity': '121', 'distance_sensor': '95', 'accelerometer_x': '13', 'accelerometer_y': '21', 'accelerometer_z': '994', 'yaw': '-53', 'pitch': '1', 'roll': '0', 'gyro_x': '0', 'gyro_y': '0', 'gyro_z': '-10', 'steering_motor_position': '22', 'driving_motor_position': '37', 'force_sensor_newton': '0'}]}, {'instruction': 'I:MOTOR C 7 -11', 'measurements': [{'time': '11569', 'front_r': '0', 'front_g': '1', 'front_b': '2', 'front_intensity': '2', 'rear_r': '35', 'rear_g': '36', 'rear_b': '37', 'rear_intensity': '84', 'distance_sensor': '97', 'accelerometer_x': '0', 'accelerometer_y': '26', 'accelerometer_z': '995', 'yaw': '-48', 'pitch': '1', 'roll': '0', 'gyro_x': '0', 'gyro_y': '0', 'gyro_z': '0', 'steering_motor_position': '22', 'driving_motor_position': '358', 'force_sensor_newton': '0'}, {'time': '12246', 'front_r': '1', 'front_g': '0', 'front_b': '0', 'front_intensity': '1', 'rear_r': '48', 'rear_g': '51', 'rear_b': '53', 'rear_intensity': '117', 'distance_sensor': '100', 'accelerometer_x': '-10', 'accelerometer_y': '17', 'accelerometer_z': '1015', 'yaw': '-43', 'pitch': '1', 'roll': '0', 'gyro_x': '0', 'gyro_y': '0', 'gyro_z': '-11', 'steering_motor_position': '22', 'driving_motor_position': '305', 'force_sensor_newton': '0'}]}, {'instruction': 'I:MOTOR A 17 10', 'measurements': [{'time': '13153', 'front_r': '0', 'front_g': '1', 'front_b': '2', 'front_intensity': '1', 'rear_r': '55', 'rear_g': '58', 'rear_b': '59', 'rear_intensity': '132', 'distance_sensor': 'None', 'accelerometer_x': '-1', 'accelerometer_y': '17', 'accelerometer_z': '1003', 'yaw': '-40', 'pitch': '1', 'roll': '0', 'gyro_x': '1', 'gyro_y': '0', 'gyro_z': '-2', 'steering_motor_position': '37', 'driving_motor_position': '284', 'force_sensor_newton': '0'}]}, {'instruction': 'I:MOTOR C 9 -9', 'measurements': [{'time': '13829', 'front_r': '0', 'front_g': '1', 'front_b': '2', 'front_intensity': '1', 'rear_r': '40', 'rear_g': '43', 'rear_b': '43', 'rear_intensity': '97', 'distance_sensor': '102', 'accelerometer_x': '-5', 'accelerometer_y': '31', 'accelerometer_z': '996', 'yaw': '-39', 'pitch': '1', 'roll': '0', 'gyro_x': '0', 'gyro_y': '0', 'gyro_z': '0', 'steering_motor_position': '49', 'driving_motor_position': '283', 'force_sensor_newton': '0'}, {'time': '14117', 'front_r': '0', 'front_g': '1', 'front_b': '2', 'front_intensity': '1', 'rear_r': '39', 'rear_g': '41', 'rear_b': '43', 'rear_intensity': '95', 'distance_sensor': '102', 'accelerometer_x': '-4', 'accelerometer_y': '33', 'accelerometer_z': '998', 'yaw': '-39', 'pitch': '2', 'roll': '0', 'gyro_x': '0', 'gyro_y': '0', 'gyro_z': '0', 'steering_motor_position': '49', 'driving_motor_position': '283', 'force_sensor_newton': '0'}, {'time': '14406', 'front_r': '1', 'front_g': '1', 'front_b': '2', 'front_intensity': '1', 'rear_r': '33', 'rear_g': '35', 'rear_b': '37', 'rear_intensity': '81', 'distance_sensor': 'None', 'accelerometer_x': '27', 'accelerometer_y': '19', 'accelerometer_z': '1001', 'yaw': '-37', 'pitch': '1', 'roll': '-1', 'gyro_x': '-2', 'gyro_y': '0', 'gyro_z': '-17', 'steering_motor_position': '49', 'driving_motor_position': '265', 'force_sensor_newton': '0'}]}, {'instruction': 'I:MOTOR C 20 0', 'measurements': []}, {'instruction': 'I:MOTOR C 6 11', 'measurements': [{'time': '15505', 'front_r': '1', 'front_g': '0', 'front_b': '0', 'front_intensity': '1', 'rear_r': '43', 'rear_g': '44', 'rear_b': '47', 'rear_intensity': '103', 'distance_sensor': '105', 'accelerometer_x': '-3', 'accelerometer_y': '30', 'accelerometer_z': '998', 'yaw': '-33', 'pitch': '1', 'roll': '0', 'gyro_x': '0', 'gyro_y': '0', 'gyro_z': '0', 'steering_motor_position': '49', 'driving_motor_position': '238', 'force_sensor_newton': '0'}, {'time': '15989', 'front_r': '1', 'front_g': '0', 'front_b': '0', 'front_intensity': '1', 'rear_r': '37', 'rear_g': '39', 'rear_b': '41', 'rear_intensity': '89', 'distance_sensor': 'None', 'accelerometer_x': '-24', 'accelerometer_y': '24', 'accelerometer_z': '993', 'yaw': '-35', 'pitch': '1', 'roll': '1', 'gyro_x': '-1', 'gyro_y': '0', 'gyro_z': '7', 'steering_motor_position': '49', 'driving_motor_position': '257', 'force_sensor_newton': '0'}]}, {'instruction': 'I:MOTOR A 12 -4', 'measurements': [{'time': '18193', 'front_r': '0', 'front_g': '0', 'front_b': '0', 'front_intensity': '1', 'rear_r': '45', 'rear_g': '47', 'rear_b': '49', 'rear_intensity': '109', 'distance_sensor': '103', 'accelerometer_x': '-11', 'accelerometer_y': '19', 'accelerometer_z': '1000', 'yaw': '-39', 'pitch': '1', 'roll': '0', 'gyro_x': '-1', 'gyro_y': '0', 'gyro_z': '0', 'steering_motor_position': '18', 'driving_motor_position': '280', 'force_sensor_newton': '0'}]}, {'instruction': 'I:MOTOR C 7 13', 'measurements': [{'time': '20401', 'front_r': '0', 'front_g': '0', 'front_b': '0', 'front_intensity': '1', 'rear_r': '44', 'rear_g': '47', 'rear_b': '49', 'rear_intensity': '108', 'distance_sensor': '103', 'accelerometer_x': '7', 'accelerometer_y': '14', 'accelerometer_z': '996', 'yaw': '-39', 'pitch': '1', 'roll': '0', 'gyro_x': '-1', 'gyro_y': '0', 'gyro_z': '0', 'steering_motor_position': '15', 'driving_motor_position': '285', 'force_sensor_newton': '0'}, {'time': '21173', 'front_r': '1', 'front_g': '0', 'front_b': '0', 'front_intensity': '1', 'rear_r': '57', 'rear_g': '62', 'rear_b': '63', 'rear_intensity': '139', 'distance_sensor': 'None', 'accelerometer_x': '-17', 'accelerometer_y': '9', 'accelerometer_z': '997', 'yaw': '-42', 'pitch': '0', 'roll': '0', 'gyro_x': '0', 'gyro_y': '0', 'gyro_z': '5', 'steering_motor_position': '14', 'driving_motor_position': '323', 'force_sensor_newton': '0'}]}, {'instruction': 'I:MOTOR C 18 -11', 'measurements': [{'time': '22453', 'front_r': '1', 'front_g': '0', 'front_b': '0', 'front_intensity': '2', 'rear_r': '59', 'rear_g': '62', 'rear_b': '63', 'rear_intensity': '142', 'distance_sensor': '100', 'accelerometer_x': '33', 'accelerometer_y': '25', 'accelerometer_z': '1017', 'yaw': '-45', 'pitch': '0', 'roll': '0', 'gyro_x': '2', 'gyro_y': '0', 'gyro_z': '-1', 'steering_motor_position': '14', 'driving_motor_position': '342', 'force_sensor_newton': '0'}]}]

    actual_result = parse_input_data(input_data)

    assert actual_result == expected_result

def test_structured_input_data_to_pandas():
    input_data = [
        {
            'instruction': 'I:MOTOR C 7 13',
            'measurements': [
                {
                    'time': '20401',
                    'front_r': '0',
                    'front_g': '0',
                    'front_b': '0',
                    'front_intensity': '1',
                    'rear_r': '44',
                    'rear_g': '47',
                    'rear_b': '49',
                    'rear_intensity': '108',
                    'distance_sensor': '103',
                    'accelerometer_x': '7',
                    'accelerometer_y': '14',
                    'accelerometer_z': '996',
                    'yaw': '-39',
                    'pitch': '1',
                    'roll': '0',
                    'gyro_x': '-1',
                    'gyro_y': '0',
                    'gyro_z': '0',
                    'steering_motor_position': '15',
                    'driving_motor_position': '285',
                    'force_sensor_newton': '0'
                },
                {
                    'time': '21173',
                    'front_r': '1',
                    'front_g': '0',
                    'front_b': '0',
                    'front_intensity': '1',
                    'rear_r': '57',
                    'rear_g': '62',
                    'rear_b': '63',
                    'rear_intensity': '139',
                    'distance_sensor': 'None',
                    'accelerometer_x': '-17',
                    'accelerometer_y': '9',
                    'accelerometer_z': '997',
                    'yaw': '-42',
                    'pitch': '0',
                    'roll': '0',
                    'gyro_x': '0',
                    'gyro_y': '0',
                    'gyro_z': '5',
                    'steering_motor_position': '14',
                    'driving_motor_position': '323',
                    'force_sensor_newton': '0'
                }]
            },
            {
                'instruction': 'I:MOTOR C 18 -11',
                'measurements': [
                {'time': '22453',
                'front_r': '1',
                'front_g': '0',
                'front_b': '0',
                'front_intensity': '2',
                'rear_r': '59',
                'rear_g': '62',
                'rear_b': '63',
                'rear_intensity': '142',
                'distance_sensor': '100',
                'accelerometer_x': '33',
                'accelerometer_y': '25',
                'accelerometer_z': '1017',
                'yaw': '-45',
                'pitch': '0',
                'roll': '0',
                'gyro_x': '2',
                'gyro_y': '0',
                'gyro_z': '-1',
                'steering_motor_position': '14',
                'driving_motor_position': '342',
                'force_sensor_newton': '0'}
            ]
        }
    ]

    # expected_output = 

    actual_output = structured_input_data_to_pandas(input_data)



