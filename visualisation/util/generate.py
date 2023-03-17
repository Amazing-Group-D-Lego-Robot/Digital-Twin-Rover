import math
import numpy as np
import cv2
import json

HEADLESS = True
SF = 0.01

class EnvironmentConverter:
    """
    Input an image from draw.io, the measurements are in millimeters
    Then converted to cm for Ursina
    """
    def __init__(self, filename):
        self.contours = None
        self.input_filename = filename
        self.opencv_image = cv2.imread(self.input_filename)
        self.origin_index = 0

        self.environment_data = []

        # Extract the contours from the input image
        self.contour_extraction()

    def contour_extraction(self):
        grey_img = cv2.cvtColor(self.opencv_image, cv2.COLOR_BGR2GRAY)

        ret, thrash = cv2.threshold(grey_img, 240, 255, cv2.CHAIN_APPROX_NONE)
        self.contours, hierarchy = cv2.findContours(thrash, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

    def convert(self):
        print(f"Starting to convert {self.input_filename} for Ursina")
        self.extraction()
        self.sort_corners()
        self.dimension_calculation()
        self.dump()
        print(f"Finished converting {self.input_filename} for Ursina")

    def extraction(self):
        for i, contour in enumerate(self.contours):
            print(f"Extracting coordinates for contour {i}/{len(self.contours)}")

            approx = cv2.approxPolyDP(contour, 0.01 * cv2.arcLength(contour, True), True)

            x = approx.ravel()[0]
            y = approx.ravel()[1] - 5

            # Centre calculation
            moment = cv2.moments(contour)
            centre_x = int(moment["m10"] / moment["m00"])
            centre_y = int(moment["m01"] / moment["m00"])

            # Colour extraction, BGR -> RGB
            colour = self.opencv_image[centre_y, centre_x].tolist()
            colour.reverse()

            if not HEADLESS:
                cv2.drawContours(self.opencv_image, [approx], 0, (0, 0, 0), 5)
                cv2.circle(self.opencv_image, (centre_x, centre_y), 7, (255, 255, 255), -1)

            # Shape detection
            if len(approx) == 4:
                shape = 'quad'
                points = [point[0].tolist() for point in approx]

                # Dimensions
                _, _, w, h = cv2.boundingRect(contour)
                dimensions = [w*SF, h*SF]

                if not HEADLESS:
                    cv2.putText(self.opencv_image, "quadrilateral", (x, y), cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 0, 0))

            else:
                shape = 'origin'
                points = None
                dimensions = None
                self.origin_index = i
                if not HEADLESS:
                    cv2.putText(self.opencv_image, "circle", (x, y), cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 0, 0))

            current_structure = {
                'shape': shape,
                'points': points,
                'dimensions': dimensions,
                'centre': [centre_x*SF, -centre_y*SF],
                'colour': colour
            }

            self.environment_data.append(current_structure)

        if not HEADLESS:
            cv2.imshow('shapes', self.opencv_image)
            cv2.waitkey(0)
            cv2.destroyAllWindows()

    def dimension_calculation(self):
        for i, structure in enumerate(self.environment_data):
            if structure['shape'] == 'origin': continue

            points = structure['points']
            side_lengths = []
            for a, b in zip(points, points[1:] + [points[0]]):
                # Side length
                side_lengths.append(math.dist(a, b)/10)

                # Rotation
                rot_rads = math.atan2(b[1] - a[1], b[0] - a[0])
                rot_degrees = math.degrees(rot_rads) % 90

            structure['sides'] = side_lengths
            structure['rotation'] = rot_degrees
            structure['height'] = 50 * SF

            self.environment_data[i] = structure

    def sort_corners(self):
        # invert the y because ursina has the _wrong_ coordinate system
        for i, structure in enumerate(self.environment_data):
            if structure['shape'] == 'origin': continue

            for j, point in enumerate(structure['points']):
                self.environment_data[i]['points'][j][1] *= -1

        for i, structure in enumerate(self.environment_data):
            if structure['shape'] == 'origin': continue

            # Bottom left corner
            bl_x = min([point[0] for point in structure['points']])
            bl_y = min([point[1] for point in structure['points'] if point[0] == bl_x])

            # Upper left corner
            ul_y = max([point[1] for point in structure['points']])
            ul_x = min([point[0] for point in structure['points'] if point[1] == ul_y])

            # Upper right corner
            ur_x = max([point[0] for point in structure['points']])
            ur_y = max([point[1] for point in structure['points'] if point[0] == ur_x])

            # Lower right corner
            lr_y = min([point[1] for point in structure['points']])
            lr_x = max([point[0] for point in structure['points'] if point[1] == lr_y])

            self.environment_data[i]['points'] = [
                [bl_x*SF, bl_y*SF],
                [ul_x*SF, ul_y*SF],
                [ur_x*SF, ur_y*SF],
                [lr_x*SF, lr_y*SF]
            ]

    def dump(self):
        # Move origin to start of list
        self.environment_data.insert(0, self.environment_data.pop(self.origin_index))

        # two files because two threads ig?

        # for the visualisation
        with open("./visualisation/assets/environment.json", 'w', encoding='utf-8') as environment_file:
            json.dump(self.environment_data, environment_file, ensure_ascii=False, indent=4, sort_keys=True)

        # for the twin
        with open("./res/environment.json", 'w', encoding='utf-8') as environment_file:
            json.dump(self.environment_data, environment_file, ensure_ascii=False, indent=4, sort_keys=True)
