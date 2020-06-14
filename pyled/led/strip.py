class LEDStrip():
    def __init__(self, red_pin_number, green_pin_number, blue_pin_number):
        self.red = Channel("red", red_pin_number)
        self.green = Channel("green", green_pin_number)
        self.blue = Channel("blue", blue_pin_number)

        self.palette = []

    def activate(self):
        self.red.start_modulation()
        self.green.start_modulation()
        self.blue.start_modulation()

    def apply_colors(self, r_value, g_value, b_value):
        self.red.apply_color(r_value)
        self.green.apply_color(g_value, bias=1.5)
        self.blue.apply_color(b_value, bias=1.3)

    def add_color(self, r_value, g_value, b_value):
        rgb = (r_value, g_value, b_value)
        if rgb not in self.palette:
            self.palette.append(rgb)

    def apply_random(self):
        rgb = choice(self.palette)
        self.apply_colors(*rgb)


