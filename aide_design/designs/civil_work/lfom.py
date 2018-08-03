import aide_design.shared.materials_database as mat
import aide_design.shared.pipedatabase as pipe
import numpy as np
from aide_design.shared.units import unit_registry as u
from aide_render.builder_classes import DP, HP


class LFOM:
    r""" This is an example class for an LFOM. It already has a lot of features built in,
    such as constants that go in the class attribute section (defaults), and methods.
    As well as an instantiation process that can be used to set custom values.

    Attributes
    ----------
    These are the default values for an LFOM. To overwrite, pass these into the bod
    (Basis Of Design) variable into the constructor.

    ratio_safety : float
        Percent above the top hole safety height.
    sdr : float
        Standard dimensional ratio of the LFOM pipe.
    S_orifice : length
        Minimum distance between orifices.
    hl : length
        Headloss of the LFOM



    Methods
    -------
    All these methods are just imported from the aide_design lfom. This would
    replace that.

    n_lfom_rows(q, hl_lfom)
        number of rows of orifices in an lfom. This could be defined directly
        within the LFOM class here instead of in lfom_prefab... just copy & paste!
    nom_diam_lfom_pipe(q, hl_lfom)
        nominal diameter of the lfom pipe.
    orifice_diameter(q, hl_lfom, mat.DIAM_DRILL_ENG)
        orifice diameter
    n_lfom_orifices_fusion
        List of numbers of rows

    Examples
    --------

    >>> my_lfom = LFOM(HP(20, u.L/u.s))
    >>> from aide_render.builder import extract_types
    >>> lfom_design_dict = extract_types(my_lfom, [DP], [])
    >>> #print(lfom_design_dict)
    >>> from aide_render.yaml import load, dump
    >>> dump(lfom_design_dict)
    "{b_orifice_rows: !DP '2.5 centimeter ', centerline_0: !DP '1 ', centerline_1: !DP '0 ',\n  centerline_2: !DP '1 ', centerline_3: !DP '0 ', centerline_4: !DP '1 ', centerline_5: !DP '0 ',\n  centerline_6: !DP '1 ', centerline_7: !DP '0 ', d_orifice: !DP '2 meter ', n_rows: !DP '8 ',\n  num_orifices_final_0: !DP '1 ', num_orifices_final_1: !DP '0 ', num_orifices_final_2: !DP '0 ',\n  num_orifices_final_3: !DP '0 ', num_orifices_final_4: !DP '0 ', num_orifices_final_5: !DP '0 ',\n  num_orifices_final_6: !DP '0 ', num_orifices_final_7: !DP '0 ', od: !DP '10.75 inch ',\n  q: !DP '20 liter / second ', sdr: !DP '26 '}\n"


    """

    ############## ATTRIBUTES ################
    ratio_safety = HP(1.5)
    sdr = DP(26)
    S_orifice = HP(1, u.cm)
    hl = HP(20, u.cm)

    ############### METHODS #################
    # Methods I import that are already defined in the functional layer.
    from aide_design.functions.lfom import (
        n_lfom_rows,
        nom_diam_lfom_pipe,
        orifice_diameter,
        n_lfom_orifices,
    )
    # We have to turn these into static methods so that the instance isn't passed in!
    n_lfom_rows = staticmethod(n_lfom_rows)
    nom_diam_lfom_pipe = staticmethod(nom_diam_lfom_pipe)
    orifice_diameter = staticmethod(orifice_diameter)
    n_lfom_orifices = staticmethod(n_lfom_orifices)


    # This function takes the output of n_lfom_orifices and converts it to a list with 8
    # entries that corresponds to the 8 possible rows. This is necessary to make the lfom
    # easier to construct in Fusion using patterns
    @staticmethod
    @u.wraps(None, [u.m ** 3 / u.s, u.m, u.inch, None], False)
    def n_lfom_orifices_fusion(FLOW, HL_LFOM, drill_bits, num_rows):
        num_orifices_per_row = LFOM.n_lfom_orifices(FLOW, HL_LFOM, drill_bits)
        num_orifices_final = np.zeros(8)
        centerline = np.zeros(8)
        center = True
        for i in range(8):
            if i % 2 == 1 and num_rows == 4:
                centerline[i] = int(center)
            elif num_rows == 4:
                num_orifices_final[i] = num_orifices_per_row[i / 2]
                centerline[i] = int(center)
                center = not center
            else:
                num_orifices_final[i] = num_orifices_per_row[i]
                centerline[i] = int(center)
                center = not center

        return num_orifices_final, centerline


    def __init__(self, q, bod=None):
        """
        This is where the "instantiation" occurs. Think of this as "rendering the
        template" or "using the cookie-cutter to make the cookie". Here is where we
        call all the methods that determine design parameters of the specific LFOM
        we are building.

        Parameters
        ----------
        bod (Basis of Design) : dict: optional
            A dict of values that will override or add any attributes of the LFOM
            component.
        q : flow rate
            The max flow rate the LFOM can handle
        """

        # add bod as instance fields:
        if bod:
            for k, v in bod.items():
                setattr(self, k, v)

        self.q = DP(q)
        self.n_rows = DP(self.n_lfom_rows(q, self.hl))
        self.b_orifice_rows = DP(self.hl/self.n_rows)
        self.od = DP(pipe.OD(self.nom_diam_lfom_pipe(q, self.hl)))
        self.d_orifice = DP(self.orifice_diameter(q, self.hl, mat.DIAM_DRILL_ENG))
        num_orifices_final_list, centerline_list = self.n_lfom_orifices_fusion(q, self.hl, mat.DIAM_DRILL_ENG, self.n_rows)
        i = 0
        for num_orifices_final, centerline in zip(num_orifices_final_list, centerline_list):
            setattr(self, 'num_orifices_final_' + str(i), DP(num_orifices_final))
            setattr(self, 'centerline_' + str(i), DP(centerline))
            i += 1
