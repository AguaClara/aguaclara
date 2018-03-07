"""This file contains all the functions needed to design a sedimentation tank
for an AguaClara plant.

"""
from aide_design.play import*

@u.wraps(None, [u.cm], False)
def n_sed_plates_max(dist_center_sed_plate):
    """Return the maximum number of plate settlers possible given the center
    to center distance.

    Parameters
    ----------
    var1 : float
        Center to center distance between plate settlers

    Returns
    -------
    int
        Maximum number of plates

    Examples
    --------
    >>> from aide_design.play import*
    >>>

    """
    return math.floor((mat.LENGTH_SED_PLATE_CANTILEVERED/dist_center_sed_plate
                      * np.tan(con.ANGLE_SED_PLATE.to(u.rad).magnitude)) + 1)
