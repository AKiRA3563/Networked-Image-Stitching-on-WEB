import cv2
import streamlit as st
import numpy as np
# import imutils


def stitcher(images, clean_pano=False):

    # Create a stitcher object
    stitcher = cv2.Stitcher_create()

    error, panorama = stitcher.stitch(images)

    # Check if the stitching was successful, identified based on the returned ref
    if not error:
        panorama = cv2.cvtColor(panorama, cv2.COLOR_BGR2RGB)
        if clean_pano:
            # Perform boundary crop for a clean border result
            st.sidebar.text('Cleaning...')
            return crop_edges(panorama)
        else:
            return panorama
    else:
        return None


def crop_edges(panorama):

    grayscale_panorama = cv2.cvtColor(panorama, cv2.COLOR_BGR2GRAY)

    # Threshold + Blur + Threshold = Remove all the random black pixel in the white part of the first threshold
    _, threshold_image = cv2.threshold(grayscale_panorama, 0, 255, cv2.THRESH_BINARY)
    blur_image = cv2.GaussianBlur(threshold_image, (5, 5), 0)
    _, threshold_image = cv2.threshold(blur_image, 0, 255 , cv2.THRESH_BINARY)

    is_cropped = False
    for crop_factor in range(100, -1, -1):
        crop_factor = 0.01 * crop_factor
        trial_mask = crop_image(threshold_image, crop_factor)[1]
        if not is_black_pixel_outline(trial_mask):
            is_cropped = True
            break

    if is_cropped:
        crop_location = crop_image(threshold_image, crop_factor)[0]

        height, width = threshold_image.shape[:2]
        h_lower, h_upper, w_left, w_right = crop_location
        # Left side (h, 0)
        for w in range(w_left, -1, -1):
            if is_black_ver_line(threshold_image, h_lower, h_upper, w):
                w_left = w + 5
                break
        # Right side (h, w)
        for w in range(w_right, width):
            if is_black_ver_line(threshold_image, h_lower, h_upper, w):
                w_right = w - 5
                break
        # Lower side (0, w)
        for h in range(h_lower, -1, -1):
            if is_black_hor_line(threshold_image, w_left, w_right, h):
                h_lower = h + 5
                break
        # Upper side (w, 0)
        for h in range(h_upper, height):
            if is_black_hor_line(threshold_image, w_left, w_right, h):
                h_upper = h - 5
                break

        if crop_location is not (h_lower, h_upper, w_left, w_right):
            return panorama[h_lower:h_upper, w_left:w_right]
        else:
            return None
    else:
        return None

def crop_image(image, factor):
    """
    Crops an image inward proportionally based on the specified factor.

    Args:
        image (numpy.ndarray): Image array to be cropped.
        factor (float): Proportion of the image to be cropped (0.0 to 1.0).

    Returns:
        Tuple containing the crop location (lower height, upper height, left width, right width)
        and the cropped image (numpy.ndarray).
    """
    (h, w) = image.shape[:2]
    # Crop horizontally (width)
    amount_crop = w * (1 - factor)
    w_right = int(w - amount_crop // 2)
    w_left = int(amount_crop // 2)
    # Crop vertically (height)
    amount_crop = h * (1 - factor)
    h_upper = int(h - amount_crop // 2)
    h_lower = int(amount_crop // 2)
    return (h_lower, h_upper, w_left, w_right), image[h_lower:h_upper, w_left:w_right]

def is_black_pixel_outline(threshold_image):
    """
    Checks if there are black pixels on the four sides of the thresholded image.

    Args:
        threshold_image (numpy.ndarray): Thresholded image array.

    Returns:
        True if black pixels are found on the outline, False otherwise.
    """
    (height, width) = threshold_image.shape[:2]
    # Lower side (0, w)
    if is_black_hor_line(threshold_image, 0, width, 0):
        return True
    # Upper side (h, w)
    if is_black_hor_line(threshold_image, 0, width, height - 1):
        return True
    # Left side (h, 0)
    if is_black_ver_line(threshold_image, 0, height, 0):
        return True
    # Right side (h, w)
    if is_black_ver_line(threshold_image, 0, height, width - 1):
        return True
    return False

def is_black_ver_line(image, start_h, end_h, w):
    """
    Checks if there is a black pixel in a straight vertical line within the specified image region.

    Args:
        image (numpy.ndarray): Image array.
        start_h (int): Starting height of the region.
        end_h (int): Ending height of the region.
        w (int): Width of the vertical line.

    Returns:
        True if a black pixel is found, False otherwise.
    """
    for value in range(start_h, end_h):
        if all(image[value, w] == [0, 0, 0]):
            return True
    return False

def is_black_hor_line(image, start_w, end_w, h):
    """
    Checks if there is a black pixel in a straight horizontal line within the specified image region.

    Args:
        image (numpy.ndarray): Image array.
        start_w (int): Starting width of the region.
        end_w (int): Ending width of the region.
        h (int): Height of the horizontal line.

    Returns:
        True if a black pixel is found, False otherwise.
    """
    for value in range(start_w, end_w):
        if all(image[h, value] == [0, 0, 0]):
            return True
    return False


##################################################################################################

    # Pad the borders of the original panorama
    # bordersize=10, mean=0
    # panorama = cv2.copyMakeBorder(panorama, top=bordersize, bottom=bordersize, left=bordersize, right=bordersize,
    #                               borderType=cv2.BORDER_CONSTANT, value=[mean, mean, mean])
    # contours = cv2.findContours(threshold_image.copy(), cv2.RETR_EXTERNAL, 
    #                             cv2.CHAIN_APPROX_SIMPLE)
    # contours = imutils.grab_contours(contours)
    # areaOI = max(contours, key=cv2.contourArea)

    # mask = np.zeros(threshold_image.shape, dtype="uint8")
    # x, y, w, h = cv2.boundingRect(areaOI)
    # cv2.rectangle(mask, (x,y), (x + w, y + h), 255, -1)

    # minRectangle = mask.copy()
    # sub = mask.copy()   

    # while cv2.countNonZero(sub) > 0:
    #     minRectangle = cv2.erode(minRectangle, None)
    #     sub = cv2.subtract(minRectangle, threshold_image)

    # contours = cv2.findContours(minRectangle.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # contours = imutils.grab_contours(contours)
    # areaOI = max(contours, key=cv2.contourArea)

    # x, y, w, h = cv2.boundingRect(areaOI)

    # return panorama[y:y + h, x:x + w]



    # '''
    # Finds the minimum bounding rectangle and returns a cropped, cleaned panorama image.
    # 1. Convert the original panorama to a single channel image.
    # 2. Threshold the gray panorama to seperate the edge pixels.
    # 3. Find the edges in the image that have more than 90% valid pixels.
    # 3. Slice the orginal image.
    # '''

    # # Find the edges which contain more than 90% non-black (i.e. valid) pixels
    # horizontal_edge = (np.count_nonzero(threshold_image, axis=1) > 0.9*threshold_image.shape[1]).nonzero()
    # vertical_edge = (np.count_nonzero(threshold_image, axis=0) > 0.9*threshold_image.shape[0]).nonzero()
    
    # # Select the first and last encountered edge respectively
    # y1, y2 = horizontal_edge[0][0], horizontal_edge[0][-1]
    # x1, x2 = vertical_edge[0][0], vertical_edge[0][-1]

    # return panorama[y1:y2, x1:x2]

