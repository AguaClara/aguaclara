from core.units import unit_registry as u

WALL_THICKNESS = 5*u.mm

# each element in the following array is tank volume

VOL_SUPPLIER = [208.198, 450, 600, 750, 1100, 2500]*u.L

# the following array is a 2D array in which
# in each element, the first element is tank diameter
# and the second element is tank height

DIMENSIONS_SUPPLIER = [[0.571, 0.851], [0.85, 0.99], [0.96, 1.10], [1.10, 1.02], [1.10, 1.39], [1.55, 1.65]]*u.m

FACTOR = [1.05, 1.05, 1.05, 1.05, 1.05, 1.05]