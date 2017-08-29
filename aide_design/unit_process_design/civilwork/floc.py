class Flocculator(object):
    def __init__(self, f_module, f_tank, first_f_tank, num_f_tanks, design_specs="design_specs"):
        self.name = "flocculator"
        self.f_module = f_module


class Tank(object):
    def __init__(self):
        self.hi = "hi"


class F_tank(Tank):
    def __init__(self):
        self.hi = "hi"


class First_f_tank(object):
    def __init__(self):
        self.hi = "hi"


class Sheet(object):
    def __init__(self, height, width, d_bottom_hole_to_bottom):
        self.hi = "hi"


class Support_structure(object):
    def __init__(self):
        self.hi = "hi"