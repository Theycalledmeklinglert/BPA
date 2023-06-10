import math
import random

import imageio as iio
import numpy as np
import cv2

from data_structs import *

c = 2.0;  # c for Potts model for esmooth
label_counter = 0
image_height = -1
image_width = -1

def e_data_function(pixel, label):  # using the L2-norm
    result = (label.x_mean - pixel.x) ** 2.0 + (label.y_mean - pixel.y) ** 2.0 + (label.r_mean - pixel.r) ** 2.0 + (
            label.g_mean - pixel.g) ** 2.0 + (label.b_mean - pixel.b) ** 2.0
    return result

def e_smooth_function(pixel_label, label_to_compare):  # using the potts model
    if pixel_label.label == label_to_compare.label:  # might have to subtract features of each label here but will see if this works for now
        return 0
    else:
        return c

def calculate_min_energy(pixels_sorted_by_rows_and_cols, pixel, board, label):   #todo: have this function return a tuple of (min_energy, new_msg_sum_for_pixel)
    energy_for_label = -1.0
    if pixel.label == None:
        energy_for_label = e_data_function(pixel, label) #in the first Iteration when Pixel is unlabeled,only Edata function is relevant
        #if(curr_energy < energy_for_label):
        #    energy_for_label[0], energy_for_label[1] = label, curr_energy
    else:
        edata_cost_at_pixel_for_label = e_data_function(pixel, label)    #todo: implement old message in pixel

        adjacent_pixels = get_four_adjacent_pixels(pixels_sorted_by_rows_and_cols, pixel)
        msg_sum = 0.0
        for p in adjacent_pixels:   #todo: s. 5.37


        edata_combined_with_msgs = (edata_cost_at_pixel_for_label + msg_sum) / 2.0
        pixel.message_sum = msg_sum
        #todo: get esmooth costs from adjacent pixels


        #+ e_smooth_function(pixel.label, label)
    return energy_for_label

def choose_elements(pixels, num_of_labels):
    seed_pixels = []
    for i in range(num_of_labels):
        rand = int(random.randrange(180))
        sample = random.sample(pixels[rand], 1)[0]
        print(sample)

        seed_pixels.append( sample )

    return seed_pixels

def get_four_adjacent_pixels(outer_list, pixel):
    adjacent_pixels = [pixel]
    pixel_index = pixel.x
    sublist_index = pixel.y
    # print("subindex: " + str(sublist_index) + " y_val: " + str(pixel.y))
    # print(sublist)
    # print("pixel_index: " + str(pixel_index) + " x_val: " + str(pixel.x))

    if (sublist_index >= 1):                #the two pixels above current seed pixel
        adjacent_pixels.append(outer_list[sublist_index-1][pixel_index])
    if (sublist_index >= 2):                #the two pixels above current seed pixel
        adjacent_pixels.append(outer_list[sublist_index - 2][pixel_index])
    if (sublist_index < len(outer_list)-1): #the two pixels under current seed pixel
        adjacent_pixels.append(outer_list[sublist_index+1][pixel_index])
    if (sublist_index < len(outer_list)-2): #the two pixels under current seed pixel
        adjacent_pixels.append(outer_list[sublist_index+2][pixel_index])

    if (pixel_index >= 1):                  #the two pixels to the left of seed pixel
        adjacent_pixels.append(outer_list[sublist_index][pixel_index-1])
    if (pixel_index >= 2):                  #the two pixels to the left of seed pixel
        adjacent_pixels.append(outer_list[sublist_index][pixel_index-2])
    if (pixel_index < image_width):     #the two pixels to the right of seed pixel
        adjacent_pixels.append(outer_list[sublist_index][pixel_index+1])
    if (pixel_index < image_width):     #the two pixels to the right of seed pixel
        adjacent_pixels.append(outer_list[sublist_index][pixel_index+2])

        print("Seed Pixel: " + str(pixel.x) + "/" + str(
            pixel.y))
        print("Pixel 1 over seed pixel: " + str(outer_list[sublist_index - 1][pixel_index].x) + "/" + str(
            outer_list[sublist_index - 1][pixel_index].y))
        print("Pixel 2 over seed pixel: " + str(outer_list[sublist_index - 2][pixel_index].x) + "/" + str(
            outer_list[sublist_index - 2][pixel_index].y))

    return adjacent_pixels

def calculate_5x5_label(outer_list, label, seed_pixel):
    adjacent_pixels = get_four_adjacent_pixels(outer_list, seed_pixel)
    for pixel in adjacent_pixels:
        print(vars(pixel))
        label = label.add_label_and_BPAPixel_vals(pixel)
        print(vars(label))
        print("\n")
    label = label.calculate_means_and_std_dev(float(len(adjacent_pixels)), adjacent_pixels)    #calculate mean attributes of label
    print("After calculate_means_and_std_dev: " + str(vars(label)))
    return label

def get_seed_pixel_labels(pixels_sorted_by_rows_and_cols):
    elems_with_max_variance = []
    curr_best_variance = 0.0
    labels = []
    global label_counter
    for i in range(10):
        labels.append(Label(label_counter, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0))
        label_counter += 1
    #for i in range(100):
    chosen_elements = choose_elements(pixels_sorted_by_rows_and_cols, 10)       # get 5x5 neighbourhood of all chosen pixels using index


    for i in range(len(chosen_elements)):
        labels[i] = calculate_5x5_label(pixels_sorted_by_rows_and_cols, labels[i], chosen_elements[i])    #maximisation of variance not yet implemented here

        # curr_variance = result_pixel.x + result_pixel.y + result_pixel.r + result_pixel.g + result_pixel.b + result_pixel.mean + result_pixel.standard_deviation
        # if curr_variance > curr_best_variance:
        #     print("CHANGED!")
        #     print("Old: " + str(curr_best_variance) + " new: " + str(curr_variance))
        #     curr_best_variance = curr_variance
        #     elems_with_max_variance = chosen_elements
        #     print("CHANGED!")

    #return elems_with_max_variance
    return labels

def main():
    # write it in a new format
    # iio.imwrite("g4g.jpg", img)
    iterations = 100
    img = cv2.imread("mqdefault.jpg")
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
            #print("row: " + str(i) + " col: " + str(j))
            curr_pixel = BPA_pixel(None, j, i, int(k[0]), int(k[1]), int(k[2]), None)
            curr_row.append(curr_pixel)
        pixels_sorted_by_rows_and_cols.append(curr_row)

    # print(len(pixels))
    # print(len(pixels_sorted_by_rows_and_cols))
    labels = get_seed_pixel_labels(pixels_sorted_by_rows_and_cols) #todo: This whole function is very likely very stupid and very wrong but i dont know how else you would calculate it so the "maximum variance" can be achieved
    print(len(labels))
    msg_boards = []
    for label in labels:
        print(vars(label))
        msg_boards.append(Message_board(label.label, pixels_sorted_by_rows_and_cols))   #todo: not sure if correct but i initialize all cost with just the lowest edata value since no labels have been set before initialization and therefore no esmooth value can be calculated right?

    for pixel in pixels_sorted_by_rows_and_cols: # initializiation; iteration 0


        #todo: dont forget to save results of energy computation in msg board and assign label with smallest energy to pixel


        for board in msg_boards:
            min_energy_and_new_msg_sum = calculate_min_energy(pixels_sorted_by_rows_and_cols, pixel, board, board.label)
            board.pixel_energy_vals[str(pixel.x)+ "/" + str(pixel.y)] = min_energy_and_new_msg_sum[0]
            #todo: if i change pixel.message_sum in this method, will the pixel from in pixels_sorted_by_rows_and_cols be changed too? or do i have to do this by reference?
            pixel.message_sum = min_energy_and_new_msg_sum[1]
        smallest_energy = 99999999999999.0
        best_label = -1
        for board in msg_boards:
            if board.pixel_energy_vals[str(pixel.x)+ "/" + str(pixel.y)] < smallest_energy:
                smallest_energy = board.pixel_energy_vals[str(pixel.x)+ "/" + str(pixel.y)]
                best_label = board.label
        pixel.label = best_label


    #for i in iterations:




if __name__ == "__main__":
    main()
