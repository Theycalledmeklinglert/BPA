import math


class BPA_pixel:
    def __init__(self, label, x, y, r, g, b):
        self.label = label
        self.x = x
        self.y = y
        self.r = r
        self.g = g
        self.b = b
        #self.mean = mean  # TODO: is the mean of all features meant here (so including colors and xy coords?) --> i will do so here but as Prof. Deinzer SOON
        #self.standard_deviation = standard_deviation  # TODO: same as with mean?

    def __sub__(self, other):
        new_x = self.x - other.x
        new_y = self.y - other.y
        new_r = self.r - other.r
        new_g = self.g - other.g
        new_b = self.b - other.b

        return BPA_pixel(self.label, new_x, new_y, new_r, new_g, new_b)

    def __add__(self, other):
        new_x = self.x + other.x
        new_y = self.y + other.y
        new_r = self.r + other.r
        new_g = self.g + other.g
        new_b = self.b + other.b

        return BPA_pixel(self.label, new_x, new_y, new_r, new_g, new_b)

    def __pow__(self, exponent):
        new_x = self.x ** exponent
        new_y = self.y ** exponent
        new_r = self.r ** exponent
        new_g = self.g ** exponent
        new_b = self.b ** exponent

        return BPA_pixel(self.label, new_x, new_y, new_r, new_g, new_b)

class Label:
    def __init__(self, label, r_mean, g_mean, b_mean, x_mean, y_mean, r_standard_deviation, g_standard_deviation, b_standard_deviation, x_standard_deviation, y_standard_deviation):
        self.label = label
        self.r_mean = r_mean
        self.g_mean = g_mean
        self.b_mean = b_mean
        self.x_mean = x_mean
        self.y_mean = y_mean
        self.r_standard_deviation = r_standard_deviation
        self.g_standard_deviation = g_standard_deviation
        self.b_standard_deviation = b_standard_deviation
        self.x_standard_deviation = x_standard_deviation
        self.y_standard_deviation = y_standard_deviation

    # def __add__(self, other):
    #     new_r_mean = self.r_mean + other.r
    #     new_g_mean = self.g_mean + other.g
    #     new_b_mean = self.b_mean + other.b
    #     new_x_mean = self.x_mean + other.x
    #     new_y_mean = self.y_mean + other.y
    #
    #     return Label(self.label, new_r_mean, new_g_mean, new_b_mean, new_x_mean, new_y_mean,
    #                  self.r_standard_deviation, self.g_standard_deviation, self.b_standard_deviation, self.x_standard_deviation, self.y_standard_deviation)

    def add_label_and_BPAPixel_vals(self, other):
        new_r_mean = self.r_mean + other.r
        new_g_mean = self.g_mean + other.g
        new_b_mean = self.b_mean + other.b
        new_x_mean = self.x_mean + other.x
        new_y_mean = self.y_mean + other.y

        return Label(self.label, new_r_mean, new_g_mean, new_b_mean, new_x_mean, new_y_mean,
                     self.r_standard_deviation, self.g_standard_deviation, self.b_standard_deviation, self.x_standard_deviation, self.y_standard_deviation)


    def __sub__(self, other):
        new_r_mean = self.r_mean - other.r
        new_g_mean = self.g_mean - other.g
        new_b_mean = self.b_mean - other.b
        new_x_mean = self.x_mean - other.x
        new_y_mean = self.y_mean - other.y

        return Label(self.label, new_r_mean, new_g_mean, new_b_mean, new_x_mean, new_y_mean,
                     self.r_standard_deviation, self.g_standard_deviation, self.b_standard_deviation,
                     self.x_standard_deviation, self.y_standard_deviation)

    def __pow__(self, power):
        new_r_mean = self.r_mean ** power
        new_g_mean = self.g_mean ** power
        new_b_mean = self.b_mean ** power
        new_x_mean = self.x_mean ** power
        new_y_mean = self.y_mean ** power
        new_r_std_dev = self.r_standard_deviation ** power
        new_g_std_dev = self.g_standard_deviation ** power
        new_b_std_dev = self.b_standard_deviation ** power
        new_x_std_dev = self.x_standard_deviation ** power
        new_y_std_dev = self.y_standard_deviation ** power

        return Label(self.label, new_r_mean, new_g_mean, new_b_mean, new_x_mean, new_y_mean, new_r_std_dev, new_g_std_dev, new_b_std_dev, new_x_std_dev, new_y_std_dev)

    def calculate_means_and_std_dev(self, divisor, pixels_in_label):
        new_r_mean = self.r_mean / divisor
        new_g_mean = self.g_mean / divisor
        new_b_mean = self.b_mean / divisor
        new_x_mean = self.x_mean / divisor
        new_y_mean = self.y_mean / divisor
        new_r_std_dev = self.r_standard_deviation
        new_g_std_dev = self.g_standard_deviation
        new_b_std_dev = self.b_standard_deviation
        new_x_std_dev = self.x_standard_deviation
        new_y_std_dev = self.y_standard_deviation

        for pixel in pixels_in_label:
            new_r_std_dev += (pixel.r - new_r_mean) **2
            new_g_std_dev += (pixel.g - new_g_mean) **2
            new_b_std_dev += (pixel.b - new_b_mean) **2
            new_x_std_dev += (pixel.x - new_x_mean) **2
            new_y_std_dev += (pixel.y - new_y_mean) **2

        n = float(len(pixels_in_label))
        new_r_std_dev = math.sqrt(new_r_std_dev / n)
        new_g_std_dev = math.sqrt(new_g_std_dev / n)
        new_b_std_dev = math.sqrt(new_b_std_dev / n)
        new_x_std_dev = math.sqrt(new_x_std_dev / n)
        new_y_std_dev = math.sqrt(new_y_std_dev / n)

        return Label(self.label, new_r_mean, new_g_mean, new_b_mean, new_x_mean, new_y_mean,
                     new_r_std_dev, new_g_std_dev, new_b_std_dev, new_x_std_dev, new_y_std_dev)

class Message_board:
    def __init__(self, label, pixels_sorted_by_rows_and_cols):
        self.label = label
        self.pixel_energy_vals = {}
        for sublist in pixels_sorted_by_rows_and_cols:
            for pixel in sublist:
                self.pixel_energy_vals[str(pixel.x) + "/" + str(pixel.y)] = 0.0
        self.past_msg_sum = {}
        for sublist in pixels_sorted_by_rows_and_cols:
            for pixel in sublist:
                self.past_msg_sum[str(pixel.x) + "/" + str(pixel.y)] = 0.0
