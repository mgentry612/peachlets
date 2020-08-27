import numpy as np
import cv2
import math

# apple image depth data
# TODO: is depth from camera or a perpendicular line from camera?
depth_np = np.load(r".\sampleDepthImage1_NPY.npy")
print(depth_np.shape)
print(depth_np)
image_width = depth_np.shape[1]
image_height = depth_np.shape[0]


# apple image pixel colors
image_np = cv2.imread(r".\sampleColorImage1.jpg")
print(image_np.shape)
print(image_np)

# TF apple locations [y1, x1, y2, x2]
# extracted from colab int testing phase
# https://colab.research.google.com/drive/1HFRDm0V7WyTI8QjUvB57A9hxneQ7HD6y#scrollTo=WcE6OwrHQJya
apples_np = np.array([[0.4460203 , 0.54542696, 0.48503673, 0.5766896 ],
        [0.70534945, 0.5356468 , 0.75217474, 0.57101226],
        [0.5234536 , 0.47795552, 0.56277406, 0.5158596 ]])
print(apples_np.shape)
print(apples_np)

# https://www.intelrealsense.com/depth-camera-d435/
aovRow = 86
aovCol = 57

depth_apples_np = np.zeros((3,5))
row = 0
for apple in apples_np:
    y1_pixels = apple[0] * image_height
    x1_pixels = apple[1] * image_width
    y2_pixels = apple[2] * image_height
    x2_pixels = apple[3] * image_width

    # center x, y
    depth_apples_np[row, 1] = int((x2_pixels + x1_pixels) / 2)
    depth_apples_np[row, 2] = int((y2_pixels + y1_pixels) / 2)

    # Depth at center
    # TODO: get average
    depth_apples_np[row, 0] = depth_np[int(depth_apples_np[row, 2]), int(depth_apples_np[row, 1])]

    # Depth at left edge (this is more accurate to the radius of the apple), it is also a risk that it misses the apple so we use above ^
    # depth_apples_np[row, 0] = depth_np[int((y2_pixels + y1_pixels) / 2), int(x1_pixels)]

    # apple width px
    apple_width_px = x2_pixels - x1_pixels
    # apple height px
    apple_height_px = y2_pixels - y1_pixels

    # Calculate row and col resolutions
    # https://www.researchgate.net/publication/282954352_Calculating_real_world_object_dimensions_from_Kinect_RGB-D_image_using_dynamic_resolution
    # mm / px in width
    res_row = (2 * depth_apples_np[row, 0] * math.tan(math.radians(aovRow / 2))) / image_width
    # mm / px in height
    res_col = (2 * depth_apples_np[row, 0] * math.tan(math.radians(aovCol / 2))) / image_height

    # apple width mm
    depth_apples_np[row, 3] = res_row * apple_width_px
    # apple height mm
    depth_apples_np[row, 4] = res_col * apple_height_px

    # center x, y in mm
    depth_apples_np[row, 1] = int(depth_apples_np[row, 1] * res_row)
    depth_apples_np[row, 2] = int(depth_apples_np[row, 2] * res_col)


    # Accuracy calc +- 3 degrees
    # https://www.intelrealsense.com/depth-camera-d435/
    # mm / px in width
    res_row_max = (2 * depth_apples_np[row, 0] * math.tan(math.radians((aovRow + 3) / 2))) / image_width
    # mm / px in height
    res_col_max = (2 * depth_apples_np[row, 0] * math.tan(math.radians((aovCol + 3) / 2))) / image_height

    width_max = res_row_max * apple_width_px
    height_max = res_col_max * apple_height_px
    error_x = width_max - depth_apples_np[row, 3]
    error_y = height_max - depth_apples_np[row, 4]

    print(error_x)
    print(error_y)


    row += 1

print(depth_apples_np)
    

