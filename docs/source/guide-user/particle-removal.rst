===================
Particle Removal
===================

Calculating flow rates and determining the pump speed for a given concentration
-----------------------------------------------------------------------------------
.. code:: python

    import aguaclara as ac
    from aguaclara.core.units import u
    import matplotlib.pyplot as plt
    import numpy as np

Calculating Flow Rates
~~~~~~~~~~~~~~~~~~~~~~
.. code:: python

    # Recirculator:
    # velocity = 1 mm/s
    # total flow rate = velocity * cross sectional area
    r = 12.7 * u.mm
    vt = 1 * u.mm / u.s
    a = np.pi*(r**2)
    qt = vt * a 

    # Humic acid:
    # stock flow rate HA = total flow rate HA * desired concentration HA / stock concentration HA
    cHAs = 0.25 * u.g / u.L
    cHAd = 0.05 * u.g / u.L
    qHAs = qt * cHAd / cHAs

    # Coagulant:
    # stock flow rate coag = total flow rate coag * desired concentration coag / stock concentration coag
    cCGs = 0.5 * u.g / u.L
    cCGd = 0.0016 * u.g / u.L
    qCGs = qt * cCGd / cCGs

    # Water:
    # total flow rate = stock flow rate HA + stock flow rate Coag + water flow rate
    qW = qt - qCGs - qHAs

    vHA = ac.vol_per_rev_3_stop('yellow-blue')
    sHA = qHAs.to(u.ml/u.s) / vHA

    vCG = ac.vol_per_rev_3_stop('yellow-blue')
    sCG = qCGs.to(u.ml/u.s) / vHA

    vW = ac.vol_per_rev_LS(17)
    sW = qW.to(u.ml/u.s) / vW

    print("Humic acid: " + str(sHA.to(u.rpm)))
    print("Coagulant: " + str(sCG.to(u.rpm)))
    print("Water: " + str(sW.to(u.rpm)))
    #Numbers to put in ProCoDA
    #Note: 2 is the coefficient
    print("The HA pump speed in ProCoDA should be", sHA.to(u.rev/u.sec)*2) 
    print("The PACl pump speed in ProCoDA should be", sCG.to(u.rev/u.sec)*2)
    print("The water pump speed in ProCoDA should be", sW.to(u.rev/u.sec)*2)


    """
    Output:
        Humic acid: 40.85 revolutions_per_minute
        Coagulant: 0.6536 revolutions_per_minute
        Water: 8.652 revolutions_per_minute
        The HA pump speed in ProCoDA should be 1.362 rev / second
        The PACl pump speed in ProCoDA should be 0.02179 rev / second
        The water pump speed in ProCoDA should be 0.2884 rev / second
    """



Determining the Pump Speed for a Given Concentration
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. code:: python

    # Recirculator:
    # velocity = 1 mm/s
    # total flow rate = velocity * cross sectional area
    r = 12.7 * u.mm
    vt = 1 * u.mm / u.s
    a = np.pi*(r**2)
    qt = vt * a 

    # Humic acid:
    # stock flow rate HA = total flow rate HA * desired concentration HA / stock concentration HA
    cHAs = 1 * u.g / u.L
    cHAd = 0.015 * u.g / u.L
    qHAs = qt * cHAd / cHAs

    # Coagulant:
    # stock flow rate coag = total flow rate coag * desired concentration coag / stock concentration coag
    cCGs = 0.5 * u.g / u.L
    cCGd = 0.0015 * u.g / u.L
    qCGs = qt * cCGd / cCGs

    # Water:
    # total flow rate = stock flow rate HA + stock flow rate Coag + water flow rate
    qW = qt - qCGs - qHAs

    vHA = ac.vol_per_rev_3_stop('yellow-blue')
    sHA = qHAs.to(u.ml/u.s) / vHA

    vCG = ac.vol_per_rev_3_stop('yellow-blue')
    sCG = qCGs.to(u.ml/u.s) / vHA

    vW = ac.vol_per_rev_LS(17)
    sW = qW.to(u.ml/u.s) / vW

    print("Humic acid: " + str(sHA.to(u.rpm)))
    print("Coagulant: " + str(sCG.to(u.rpm)))
    print("Water: " + str(sW.to(u.rpm)))


    """
    Output:
        Humic acid: 3.064 revolutions_per_minute
        Coagulant: 0.6128 revolutions_per_minute
        Water: 10.66 revolutions_per_minute
    """


Want to try some of this out? **Interact and play with the code** `here <https://colab.research.google.com/github/AguaClara/humic_acid/blob/master/HA_Report_1_Spring2020.ipynb>`_. Taken from Humic Acid Removal Spring 2020 Report.