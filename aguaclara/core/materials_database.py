
"""

"""

try:
    from aguaclara.core.units import unit_registry as u
    from aguaclara.core import constants as con, utility as ut
except ModuleNotFoundError:
    from aguaclara.core.units import unit_registry as u
    from aguaclara import utility as ut
    from aguaclara import constants as con


########### Materials Constants - general ############

PIPE_ROUGH_PVC = 0.12*u.mm

PIPE_ROUGH_CONCRETE = 2*u.mm

RHO_CONCRETE = 2400*(u.kg/(u.m**3)) #used in the sed tank drawing

THICKNESS_CONCRETE_MIN = 5*u.cm  #used throughout the code

#0 is English, 1 is metric, drill series is needed for the
#drill series at the bottom of this sheet and tube series
#is needed for the Cdc code
EN_DRILL_SERIES = 0

EN_TUBE_SERIES = 0

DIAM_REBAR = (1/2)*u.inch

########### Material constants - entrance tank ############

SDR_LFOM = 26

THICKNESS_LFOM_SHEET = THICKNESS_CONCRETE_MIN

NOM_DIAM_ENT_TANK_FLOAT =  8*u.inch

#Minimum pipe size to handle grit and to ensure that the pipe can be easily unclogged
NOM_DIAM_ENT_TANK_DRAIN_MIN =  3*u.inch

NOM_DIAM_ENT_TANK_DRAIN =  3*u.inch #This is constant for now

THICKNESS_ENT_TANK_REMOVABLE_WALL = 5*u.cm

#Parameters are arbitrary - need to be calculated
HEIGHT_ENT_TANK_REMOVABLE_WALL_SUPPORT = 4*u.cm

THICKNESS_ENT_TANK_REMOVABLE_WALL_SUPPORT = 5*u.cm

THICKNESS_ENT_TANK_HOPPER_LEDGE = 15*u.cm

THICKNESS_RAPID_MIX_ORIFICE_PLATE = 2*u.cm

NOM_DIAM_RAPID_MIX_AIR_RELEASE = 1*u.inch

 ############ Material constants - chem storage tanks  ############

THICKNESS_CHEM_TANK_WALL = 5*u.mm

 #Supplier Information:
#http://www.rotoplas.com/assets/files/industria/catalogo.pdf

#each element in the following array is tank volume

VOL_SUPPLIER_CHEM_TANK = [208.198, 450, 600, 750, 1100, 2500]*u.L

#the following array is a 2D array in which
#in each element, the first element is tank diameter
#and the second element is tank height

DIMENSIONS_SUPPLIER_CHEM_TANK = [[0.571, 0.851], [0.85, 0.99], [0.96, 1.10], [1.10, 1.02], [1.10, 1.39], [1.55, 1.65]]*u.m

FACTOR = [1.05, 1.05, 1.05, 1.05, 1.05, 1.05]

############ Material constants - chemical dose controller ###########

DIAM_TUBE_ENGLISH = [1, 2, 3 ,4 ,5 ,6, 7]*u.inch/16

DIAM_TUBE_METRIC = [2, 3, 4, 6, 8, 10]*u.mm

DIAM_FLT_VLV_ORIFICES_AVAIL = [0.093, 0.187, 0.25, 0.312]*u.inch

############# Material constants - flocculator #####################

THICKNESS_FLOC_BAFFLE_RIGID_HEIGHT = 15*u.cm

#The piping size for the main part of the floc modules
NOM_DIAM_FLOC_MODULES_MAIN = (1/2)*u.inch

#The diameter of the oversized cap used to assemble the floc modules
NOM_DIAM_FLOC_MODULES_LARGE = 1.5*u.inch

############ Material constants - sedimentation  #############
#Maximum length of sed plate sticking out past module pipes without any
#additional support. The goal is to prevent floppy modules that don't maintain
# constant distances between the plates

LENGTH_SED_PLATE_CANTILEVERED = 20*u.cm

NOM_DIAM_SED_HOPPER_DRAIN = 1*u.inch

NOM_DIAM_SED_HOPPER_VIEWER = 2*u.inch

NOM_DIAM_SED_HOPPER_SKIMMER = 2*u.inch

##Diffusers/Jet Reverser

NOM_DIAM_SED_DIFFUSER = 1*u.inch

NOM_DIAM_SED_JET_REVERSER = 3*u.inch

############ Material constants - stacked rapid sand filter ############

#We are going to take this pipe size for the slotted pipes as a given.
# Larger pipes may block too much flow and they are harder to install.
NOM_DIAM_FILTER_MANIFOLD_BRANCH = 1*u.inch

NOM_DIAM_FILTER_BACKWASH_MANIFOLD_BRANCH = 1.5*u.inch

#A slot thickness of 0.008 in or 0.2 mm is selected so that sand
# will not enter the slotted pipes.
WIDTH_FILTER_MANIFOLD_SLOTS = 0.008*u.inch

NOM_DIAM_FILTER_BRANCH_HOLDER = 2*u.inch

NOM_DIAM_FILTER_BACKWASH_BRANCH_HOLDER = 2*u.inch

#Minimum vertical spacing between trunk line pipes going through
#the filter wall for concrete construction
SPACE_FILTER_TRUNK_MIN = 3*u.cm

#Space between the ends of the branch receiver pipes and the walls so that
#the manifold assemblies are easy to lower into the filter boxes
# (if the branch receivers extended the entire length of the box they would
#just barely fit and it would be hard to get into place)
SPACE_FILTER_MANIFOLD_ASSEMBLY = 1*u.cm

LENGTH_FILTER_MANIFOLD_FEMCO_COUPLING = 4*u.cm

##Sand Properties

DIAM_FILTER_SAND_EFFECTIVE_SIZE = 0.5*u.mm

RATIO_UNIFORMITY_COEFF_FILTER_SAND = 1.65

DIAM_FILTER_SAND_60 = DIAM_FILTER_SAND_EFFECTIVE_SIZE * RATIO_UNIFORMITY_COEFF_FILTER_SAND

#Porosity in a sand bed
POROSITY_FILTER_SAND = 0.4

RHO_FILTER_SAND = 2650*u.kg/(u.m**3)

RATIO_FILTER_FLUIDIZED = 1.3 #Bed expands 30% when fluidized

#Carman-Kozeny coefficient
K_KOZENY = 5

############## Drill Series ##############

DIAM_DRILL_ENG = [0.03125, 0.0625, 0.09375, 0.125, 0.15625, 0.1875, 0.21875, 0.25, 0.375, 0.5, 0.625, 0.75, 0.875, 1, 1.25, 1.5, 1.75, 2]*u.inch

DIAM_DRILL_MET = [0.5*u.mm]

counter = 0
# these drill series should have been created using arange.

while DIAM_DRILL_MET[counter] <= 4.98*u.mm:
    counter+=1
    DIAM_DRILL_MET.append(DIAM_DRILL_MET[counter-1] + 0.1*u.mm)

while DIAM_DRILL_MET[counter] < 20*u.mm:
    counter+=1
    DIAM_DRILL_MET.append(DIAM_DRILL_MET[counter-1] + 1*u.mm)

while DIAM_DRILL_MET[counter] < 50*u.mm:
    counter+=1
    DIAM_DRILL_MET.append(DIAM_DRILL_MET[counter-1] + 2*u.mm)

def diam_drill(EN_DRILL_SERIES):
    if EN_DRILL_SERIES == 0:
        DIAM_DRILL = DIAM_DRILL_ENG
    else:
        DIAM_DRILL = DIAM_DRILL_MET
    return DIAM_DRILL
