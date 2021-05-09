# -*- coding: utf-8 -*-
"""Constant quantities of widely-accepted physical properties."""

from aguaclara.core.units import u

# NOTE: "#: <optional_description>"  required for Sphinx autodocumentation

#: The ratio of maximum energy dissipation rate in a round jet to the kinetic
#: energy per time required for the jet to travel a distance equal to its
#: diameter. See `round jet
#: <https://aguaclara.github.io/Textbook/Rapid_Mix/RM_Derivations.html?#round-jet>`_
#: in the AguaClara textbook for more details.
JET_ROUND_RATIO = 0.08

#: The ratio of maximum energy dissipation rate in a plane jet to the kinetic
#: energy per time required for the jet to travel a distance equal to its
#: diameter. This ratio applies to jets in the flocculator and sedimentation
#: tank. See `plane jet
#: <https://aguaclara.github.io/Textbook/Rapid_Mix/RM_Derivations.html?#plane-jet>`_
#: in the AguaClara textbook for more details.
JET_PLANE_RATIO = 0.0124

#: Vena contracta coefficient through an orifice with 90˚ bends. This is the
#: ratio of the flow area at the point of maximal contraction to the flow area
#: before the contraction.
VC_ORIFICE_RATIO = 0.63

#: Kozeny constant
K_KOZENY = 5
