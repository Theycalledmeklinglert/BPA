import math
import random

import imageio as iio
import numpy as np
import cv2

from data_structs import *

c = 1000.0  # c for Potts model for esmooth
label_counter = 0
image_height = -1
image_width = -1

def e_data_function(pixel, label):  # using the L2-norm
    #result = math.sqrt( ( label.r_mean - pixel.r) ** 2.0 + (      # L2 norm
            #label.g_mean - pixel.g) ** 2.0 + (label.b_mean - pixel.b) ** 2.0) **2.0

    result = abs(label.r_mean - pixel.r)  + abs(  # L1 norm
        label.g_mean - pixel.g) + abs(label.b_mean - pixel.b)
    return result

def e_smooth_function(iterator_label, label_to_compare):  # using the potts model
    if iterator_label.label == label_to_compare.label:
        return 0
    else:
        return c

def get_board_for_label(label, msg_boards):
    for board in msg_boards:
        if(label.label == board.label.label):
            return board

def calculate_min_energy_and_assign_msgsums_to_all_boards_for_pixel(pixels_sorted_by_rows_and_cols, pixel, all_labels, msg_boards):
    adjacent_pixels = get_5x5_window(pixels_sorted_by_rows_and_cols, pixel, False)
    temp = []
    for p in adjacent_pixels:
        if p.label is not None:
            temp.append(p)
    adjacent_pixels = temp

    for board in msg_boards:
        msg_sum_for_curr_label = 0.0
        edata_cost = e_data_function(pixel, board.label)

        if pixel.label is None: #initialization step
            for p in adjacent_pixels:
                msg_vals_of_curr_pixel_for_each_label = []
                for h in all_labels:
                    val = e_data_function(p, h) + e_smooth_function(h, board.label)
                    msg_vals_of_curr_pixel_for_each_label.append(val)
                msg_sum_for_curr_label += min(msg_vals_of_curr_pixel_for_each_label)#see 5.39
            board.pixel_energy_vals[str(pixel.x) + "/" + str(pixel.y)] = edata_cost + msg_sum_for_curr_label    #update of msg value of current central pixel in msg board for each label
            board.past_msg_sum[str(pixel.x) + "/" + str(pixel.y)] = msg_sum_for_curr_label

        else:
            for p in adjacent_pixels:
                msg_vals_of_curr_pixel_for_each_label = []
                for h in all_labels:
                    h_board = get_board_for_label(h, msg_boards)
                    val = e_data_function(p, h) + e_smooth_function(h, board.label) + h_board.past_msg_sum[str(p.x) + "/" + str(p.y)]  #message_sum of messages that the adjacent pixels received in of previous iterations
                    msg_vals_of_curr_pixel_for_each_label.append(val)
                msg_sum_for_curr_label += min(msg_vals_of_curr_pixel_for_each_label)#see 5.39

            msg_sum_for_curr_label /= len(adjacent_pixels)+1 #todo:experimental change
            board.pixel_energy_vals[str(pixel.x) + "/" + str(pixel.y)] = (edata_cost + msg_sum_for_curr_label) #update of msg value of current central pixel in msg board for each label
            board.past_msg_sum[str(pixel.x) + "/" + str(pixel.y)] = msg_sum_for_curr_label

def choose_seed_pixels(pixels, num_of_labels):
    seed_pixels = []
    for i in range(num_of_labels):
        rand = int(random.randrange(image_height))
        sample = random.sample(pixels[rand], 1)[0]
        print(sample)

        seed_pixels.append( sample )

    return seed_pixels

def get_5x5_window(outer_list, pixel, flag):
    adjacent_pixels = []
    if flag:
        adjacent_pixels.append(pixel)
    pixel_index = pixel.x
    sublist_index = pixel.y

    if (sublist_index >= 1):                #the two pixels above current seed pixel
        adjacent_pixels.append(outer_list[sublist_index-1][pixel_index])
    if (sublist_index >= 2 and flag):                #the two pixels above current seed pixel
        adjacent_pixels.append(outer_list[sublist_index - 2][pixel_index])
    if (sublist_index < image_height-1): #the two pixels under current seed pixel
        adjacent_pixels.append(outer_list[sublist_index+1][pixel_index])
    if (sublist_index < image_height-2 and flag): #the two pixels under current seed pixel
        adjacent_pixels.append(outer_list[sublist_index+2][pixel_index])

    if (pixel_index >= 1):                  #the two pixels to the left of seed pixel
        adjacent_pixels.append(outer_list[sublist_index][pixel_index-1])
    if (pixel_index >= 2 and flag):                  #the two pixels to the left of seed pixel
        adjacent_pixels.append(outer_list[sublist_index][pixel_index-2])
    if (pixel_index < image_width-1):     #the two pixels to the right of seed pixel
        adjacent_pixels.append(outer_list[sublist_index][pixel_index+1])
    if (pixel_index < image_width-2 and flag):     #the two pixels to the right of seed pixel
        adjacent_pixels.append(outer_list[sublist_index][pixel_index+2])


    if (pixel_index < image_width - 1 and sublist_index < image_height - 1 and flag):
        adjacent_pixels.append(outer_list[sublist_index + 1][pixel_index + 1])
    if (pixel_index < image_width - 2 and sublist_index < image_height - 2 and flag):
        adjacent_pixels.append(outer_list[sublist_index + 2][pixel_index + 2])
    if (pixel_index >= 1 and sublist_index < image_height - 1 and flag):
        adjacent_pixels.append(outer_list[sublist_index + 1][pixel_index - 1])
    if (pixel_index >= 2 and sublist_index < image_height - 2 and flag):
        adjacent_pixels.append(outer_list[sublist_index + 2][pixel_index - 2])

    if (pixel_index < image_width - 1 and sublist_index >= 1 and flag):
        adjacent_pixels.append(outer_list[sublist_index - 1][pixel_index + 1])
    if (pixel_index < image_width - 2 and sublist_index >= 2 and flag):
        adjacent_pixels.append(outer_list[sublist_index - 2][pixel_index + 2])
    if (pixel_index >= 1 and sublist_index >= 1 and flag):
        adjacent_pixels.append(outer_list[sublist_index - 1][pixel_index - 1])
    if (pixel_index >= 2 and sublist_index >= 2 and flag):
        adjacent_pixels.append(outer_list[sublist_index - 2][pixel_index - 2])

        print("Seed Pixel: " + str(pixel.x) + "/" + str(
            pixel.y))
    return adjacent_pixels

def calculate_5x5_label(outer_list, label, seed_pixel):
    adjacent_pixels = get_5x5_window(outer_list, seed_pixel, True)
    for pixel in adjacent_pixels:
        print(vars(pixel))
        label = label.add_label_and_BPAPixel_vals(pixel)
        print(vars(label))
        print("\n")
    label = label.calculate_means_and_std_dev(float(len(adjacent_pixels)), adjacent_pixels)    #calculate mean attributes of label
    print("After calculate_means_and_std_dev: " + str(vars(label)))
    return label

def get_seed_pixel_labels(pixels_sorted_by_rows_and_cols, num_of_labels):
    labels = []
    global label_counter
    for i in range(num_of_labels):
        labels.append(Label(label_counter, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0))
        label_counter += 1
    seed_pixels = choose_seed_pixels(pixels_sorted_by_rows_and_cols, num_of_labels)       # get 5x5 neighbourhood of all chosen pixels using index

    for i in range(len(seed_pixels)):
        labels[i] = calculate_5x5_label(pixels_sorted_by_rows_and_cols, labels[i], seed_pixels[i])
    return labels

def main():
    iterations = 1
    num_of_labels = 15
    #img = cv2.imread("mqdefault.jpg")
    #img = cv2.imread("spring.png")
    img = cv2.imread("mean_shift_spring.png")
    rows, cols, _ = img.shape
    global image_height
    global image_width
    image_height = rows
    image_width = cols

    pixels_sorted_by_rows_and_cols = []
    print("Rows: " + str(rows) + " Cols: " + str(cols))
    for i in range(rows):
        curr_row = []
        for j in range(cols):
            k = img[i, j]
            curr_pixel = BPA_pixel(None, j, i, int(k[0]), int(k[1]), int(k[2]))
            curr_row.append(curr_pixel)
        pixels_sorted_by_rows_and_cols.append(curr_row)

    all_labels = get_seed_pixel_labels(pixels_sorted_by_rows_and_cols, num_of_labels) #10#
    print(len(all_labels))
    msg_boards = []
    for label in all_labels:
        print(vars(label))
        msg_boards.append(Message_board(label, pixels_sorted_by_rows_and_cols))

    for i in range(iterations):
        for sublist in pixels_sorted_by_rows_and_cols:
            for pixel in sublist:
                calculate_min_energy_and_assign_msgsums_to_all_boards_for_pixel(pixels_sorted_by_rows_and_cols, pixel, all_labels, msg_boards)
                smallest_energy = 1.7976931348623157e+308
                best_label = None
                for board in msg_boards:
                    if board.pixel_energy_vals[str(pixel.x) + "/" + str(pixel.y)] < smallest_energy:
                        smallest_energy = board.pixel_energy_vals[str(pixel.x) + "/" + str(pixel.y)]
                        best_label = board.label.label
                pixel.label = best_label
        print(i)

    red = [255, 0, 0]
    green = [0, 255, 0]
    blue = [0,0,255]
    purple = [255, 0, 230]
    white = [255, 255, 255]
    black = [0,0,0]
    l_blue = [0, 255, 255]
    yellow = [255, 255, 0]
    gray = [192, 192, 192]
    d_green = [0, 25, 51]
    c1 = [180, 255, 0]
    c2 = [180, 180, 180]
    c3= [70, 70, 70]
    c4= [150, 150, 150]
    c5= [220, 220, 220]

    segmented_image_data = []
    for sublist in pixels_sorted_by_rows_and_cols:
        pixel_row = []
        for pixel in sublist:
            color = []
            if(pixel.label == 0):
                color = red
            elif(pixel.label == 1):
                color = green
            elif(pixel.label == 2):
                color = blue
            elif(pixel.label == 3):
                color = purple
            elif(pixel.label == 4):
                color = white
            elif(pixel.label == 5):
                color = d_green
            elif(pixel.label == 6):
                color = l_blue
            elif(pixel.label == 7):
                color = yellow
            elif(pixel.label == 8):
                color = gray
            elif(pixel.label == 9):
                color = black
            elif(pixel.label == 10):
                color = c1
            elif (pixel.label == 11):
                color = c2
            elif (pixel.label == 12):
                color = c3
            elif (pixel.label == 13):
                color = c4
            elif (pixel.label == 14):
                color = c5
            elif(pixel.label is None):
                print("Pixel: " + str(pixel.x) + "/" + str(pixel.y))
                raise Exception("Some Pixel had no label")
            pixel_row.append(color)
        segmented_image_data.append(pixel_row)

    print(segmented_image_data)
    print(len(img))
    print(len(segmented_image_data))
    nmpy_array = np.array(segmented_image_data, dtype=np.uint8)
    iio.imwrite('result.jpg', nmpy_array)

if __name__ == "__main__":
    main()
