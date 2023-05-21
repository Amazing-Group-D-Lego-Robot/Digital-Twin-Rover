import math
import numpy as np
import cv2
import json
from time import sleep
from copy import deepcopy

HEADLESS = False
SF = 1
SAFE_ZONE = 0.5

class EnvironmentConverter:
    """
    Input an image from draw.io, the measurements are in millimeters
    Then converted to cm for Ursina
    """
    def __init__(self, filename, output_path):
        self.contours = None
        self.input_filename = filename
        self.output_path = output_path
        self.opencv_image = cv2.imread(self.input_filename)
        self.origin_index = 0

        self.environment_data = []

        # Extract the contours from the input image
        self.contour_extraction()

    def contour_extraction(self):
        grey_img = cv2.cvtColor(self.opencv_image, cv2.COLOR_BGR2GRAY)

        ret, thrash = cv2.threshold(grey_img, 240, 255, cv2.CHAIN_APPROX_NONE)
        self.contours, hierarchy = cv2.findContours(thrash, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

        if not HEADLESS:
            contour_img = grey_img.copy()

            cv2.drawContours(contour_img, self.contours, -1, (0, 0, 255), 2)

            # Show the resulting image
            cv2.imshow("Contours", contour_img)
            cv2.waitKey(0)
            cv2.destroyAllWindows()

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
            img = deepcopy(self.opencv_image)

            img_height, img_width, _ = img.shape

            epsilon = 0.01 * cv2.arcLength(contour, True)
            approx = cv2.approxPolyDP(contour, epsilon, True)

            x = approx.ravel()[0]
            y = approx.ravel()[1] - 5

            # Centre calculation
            moment = cv2.moments(contour)
            centre_x = int(moment["m10"] / moment["m00"])
            centre_y = int(moment["m01"] / moment["m00"])

            # Colour extraction, BGR -> RGB
            # print(centre_x, centre_y)
            colour = img[centre_y, centre_x].tolist()
            colour.reverse()

            # Shape detection
            if len(approx) == 4:
                print(f"Found quadrilateral at {centre_x}, {centre_y}, with contours {len(approx)}")
                shape = 'quad'
                points = [(point[0].tolist()[0]*SF, img_height-point[0].tolist()[1]*SF) for point in approx]
                _, _, w, h = cv2.boundingRect(contour)
                dimensions = [w*SF, h*SF]

            elif len(approx) != 12:
                print(f"Found border at {centre_x}, {centre_y}, with contours {len(approx)}")
                shape = 'border'
                points = [(point[0].tolist()[0]*SF, img_height-point[0].tolist()[1]*SF) for point in approx]
                if not HEADLESS:
                    for point in points:
                        cv2.circle(img, (int(point[0]/SF), int(point[1]/SF)), 7, (0, 255, 255), -1)

                dimensions = None

            else:
                print(f"Found circle at {centre_x}, {centre_y}, with contours {len(approx)}")
                shape = 'origin'
                points = None
                dimensions = None
                self.origin_index = i

            if not HEADLESS:
                cv2.drawContours(img, [approx], 0, (0, 0, 0), 5)
                cv2.circle(img, (centre_x, centre_y), 7, (255, 255, 255), -1)
                cv2.putText(img, shape, (x, y), cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 0, 0))

            current_structure = {
                'shape': shape,
                'points': points,
                'dimensions': dimensions,
                'centre': [centre_x*SF, centre_y*SF],
                'colour': colour
            }

            self.environment_data.append(current_structure)
            print()

        if not HEADLESS:
            cv2.imshow('shapes', img)
            cv2.waitKey(0)
            cv2.destroyAllWindows()

    def dimension_calculation(self):
        for i, structure in enumerate(self.environment_data):
            if structure['shape'] != 'quad': continue

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
            structure['height'] = 5

            self.environment_data[i] = structure

    def sort_corners(self):
        for i, structure in enumerate(self.environment_data):
            if structure['shape'] != 'quad': continue

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
                [bl_x, bl_y],
                [ul_x, ul_y],
                [ur_x, ur_y],
                [lr_x, lr_y]
            ]

            self.environment_data[i]['safe-points'] = [
                [bl_x - SAFE_ZONE, bl_y - SAFE_ZONE],
                [ul_x - SAFE_ZONE, ul_y + SAFE_ZONE],
                [ur_x + SAFE_ZONE, ur_y + SAFE_ZONE],
                [lr_x + SAFE_ZONE, lr_y - SAFE_ZONE]
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

    def convert_for_rrt(self):
        # Define as BGR
        boundary_color = (204, 153, 255)
        outer_color = (181, 135, 77)
        goal_color = (0, 0, 255)
        output_path = f"{self.output_path}/map-<QUAD_NUM>.png"

        # Load the image
        img = deepcopy(self.opencv_image)
        grey_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        tolerance = 30
        lower = np.array([c - tolerance for c in boundary_color])
        upper = np.array([c + tolerance for c in boundary_color])
        mask = cv2.inRange(img, lower, upper)

        # Find the contours in the image
        contours, hierarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # Filter contours by size and shape
        min_area = 100
        min_ratio = 0.5
        selected_contours = []
        for cnt in contours:
            area = cv2.contourArea(cnt)
            x, y, w, h = cv2.boundingRect(cnt)
            aspect_ratio = w / float(h)
            if area > min_area and aspect_ratio > min_ratio:
                selected_contours.append(cnt)

        # Draw the selected contours on a blank image
        result = np.zeros_like(img)
        cv2.drawContours(result, selected_contours, -1, (255, 255, 255), -1)
        result[np.where((result == [0, 0, 0]).all(axis=2))] = outer_color

        # Reset for the next step
        ret, thrash = cv2.threshold(grey_img, 240, 255, cv2.CHAIN_APPROX_NONE)
        contours, hierarchy = cv2.findContours(thrash, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

        num_quads = sum(
            [1 if len(cv2.approxPolyDP(cnt, 0.01 * cv2.arcLength(cnt, True), True)) == 4 else 0 for cnt in contours])

        print(f"Number of quads: {num_quads}")

        # Loop over the quads
        for i in range(num_quads):
            quad_num = 0

            # Loop over the contours
            for cnt in contours:
                # Approximate the contour to a polygon
                epsilon = 0.01 * cv2.arcLength(cnt, True)
                approx = cv2.approxPolyDP(cnt, epsilon, True)

                # Determine the shape type based on the number of vertices
                if len(approx) == 4:
                    if quad_num == i:
                        # Draw the quad as a dummy colour
                        cv2.fillPoly(result, pts=[cnt], color=boundary_color)
                        # Find the centre of the quad
                        moment = cv2.moments(cnt)
                        centre_x = int(moment["m10"] / moment["m00"])
                        centre_y = int(moment["m01"] / moment["m00"])
                        # Draw a circle at the centre of the quad
                        # cv2.circle(result, (centre_x, centre_y), 20, goal_color, -1)
                    else:
                        cv2.fillPoly(result, pts=[cnt], color=outer_color)

                    quad_num += 1

            # Draw a circle for start point
            # cv2.circle(result, (100, 100), 20, (0, 255, 0), -1)

            # Display the image with the shapes and their corners
            cv2.imwrite(output_path.replace("<QUAD_NUM>", f'{i}'), result)
            print(f"Saved image {i} to {output_path.replace('<QUAD_NUM>', f'{i}')}")

        if not HEADLESS:
            cv2.imshow("Shapes", result)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
