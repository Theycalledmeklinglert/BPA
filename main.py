import math
import random

import imageio as iio
import numpy as np
import cv2

from data_structs import *

c = 2.0;  # c for Potts model for esmooth
label_counter = 0

def e_data_function(pixel, label):  # using the L2-norm
    result = (label.x_mean - pixel.x) ** 2 + (label.y_mean - pixel.y) ** 2 + (label.r_mean - pixel.r) ** 2 + (
            label.g_mean - pixel.g) ** 2 + (label.b_mean - pixel.b) ** 2
    return result

def e_smooth_function(label_1, label_2):  # using the potts model
    if label_1.label == label_2.label:  # might have to subtract features of each label here but will see if this works for now
        return 0
    else:
        return c

def choose_elements(pixels, num_of_labels):
    chosen_elements = []
    for i in range(num_of_labels):
        rand = int(random.randrange(180))
        sublist = pixels[rand]

        print(sublist)
        sample = random.sample(sublist, 1)[0]
        print(sample)

        chosen_elements.append( [sublist, sample] )

    return chosen_elements

def calculate_5x5_label(outer_list, sublist, label, seed_pixel):
    relevant_pixels = [seed_pixel]
    sublist_index = outer_list.index(sublist)
    #print(sublist)
    pixel_index = sublist.index(seed_pixel)
    if (sublist_index >= 1):                #the two pixels above current seed pixel
        relevant_pixels.append(outer_list[sublist_index-1][pixel_index])
    if (sublist_index >= 2):                #the two pixels above current seed pixel
            relevant_pixels.append(outer_list[sublist_index - 2][pixel_index])
    if (sublist_index < len(outer_list)-1): #the two pixels under current seed pixel
        relevant_pixels.append(outer_list[sublist_index+1][pixel_index])
    if (sublist_index < len(outer_list)-2): #the two pixels under current seed pixel
        relevant_pixels.append(outer_list[sublist_index+2][pixel_index])

    if (pixel_index >= 1):                  #the two pixels to the left of seed pixel
        relevant_pixels.append(outer_list[sublist_index][pixel_index-1])
    if (pixel_index >= 2):                  #the two pixels to the left of seed pixel
        relevant_pixels.append(outer_list[sublist_index][pixel_index-2])
    if (pixel_index < len(sublist)-1):     #the two pixels to the right of seed pixel
        relevant_pixels.append(outer_list[sublist_index][pixel_index+1])
    if (pixel_index < len(sublist)-2):     #the two pixels to the right of seed pixel
        relevant_pixels.append(outer_list[sublist_index][pixel_index+2])

    for pixel in relevant_pixels:
        print(vars(pixel))
        label = label.add_label_and_BPAPixel_vals(pixel)
        print(vars(label))
        print("\n")
    label = label.calculate_means_and_std_dev(float(len(relevant_pixels)), relevant_pixels)    #calculate mean attributes of label
    print("After calculate_means_and_std_dev: " + str(vars(label)))
    return label

def find_seed_pixels_with_max_variance(pixels_sorted_by_rows_and_cols):
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
        labels[i] = calculate_5x5_label(pixels_sorted_by_rows_and_cols, chosen_elements[i][0], labels[i], chosen_elements[i][1])

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
    # img = iio.imread("mqdefault.jpg")
    # write it in a new format
    # iio.imwrite("g4g.jpg", img)
    # print(img)
    # print(img.shape)
    # arr = np.random.rand(3, 2, 4)
    # print(arr)
    iterations = 100
    img = cv2.imread("mqdefault.jpg")
    rows, cols, _ = img.shape
    pixels_sorted_by_rows_and_cols = []
    print("Rows: " + str(rows) + " Cols: " + str(cols))
    for i in range(rows):
        curr_row = []
        for j in range(cols):
            k = img[i, j]
            curr_pixel = BPA_pixel(i, j, int(k[0]), int(k[1]), int(k[2]), None)
            curr_row.append(curr_pixel)
        pixels_sorted_by_rows_and_cols.append(curr_row)

    # print(len(pixels))
    # print(len(pixels_sorted_by_rows_and_cols))

    #elems_with_max_variance = find_seed_pixels_with_max_variance(pixels_sorted_by_rows_and_cols)    #todo: This whole function is very likely very stupid and very wrong but i dont know how else you would calculate it so the "maximum variance" can be achieved
    labels = find_seed_pixels_with_max_variance(pixels_sorted_by_rows_and_cols)
    print(len(labels))
    for label in labels:
        print(vars(label))
        # for l in range(iterations):


if __name__ == "__main__":
    main()
