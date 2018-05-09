"""This file contains all the functions needed to design the sedimentation tank
channels for an AguaClara plant.


"""

from aide_design.play import*
from aide_design.unit_process_design import sed_tank_dict_test as sed_tank

# again we will change this to an import statment from the URL of  aide_template repo
sed_chan_dict = {
            'thickness_wall': 0.15*u.m,
            'plate_settlers': {
                'angle': 60*u.deg, 'S': 2.5*u.cm,
                'thickness': 2*u.mm, 'L_cantilevered': 20*u.cm,
                },
            'tank': {
                'W': 42*u.inch, 'L': 5.8*u.m, 'vel_up': 1*u.mm/u.s
            },
            'manifold': {
                'ratio_Q_man_orifice': 0.8,
                'diffuser': {
                    'thickness_wall': 1.17*u.inch, 'vel_max': 442.9*u.mm/u.s,
                    'A': 0.419*u.inch**2
                },
                'exit_man': {
                    'hl_orifice': 4*u.cm, 'N_orifices': 58
                }
            }
}

x = n_sed_plates_max(sed_tank.sed_dict)
