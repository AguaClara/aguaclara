===================
Experimental Design
===================

Designing an experiment with a contaminant and a coagulant of unknown concentration
-----------------------------------------------------------------------------------
.. code:: python

    import aguaclara as ac
    from aguaclara.core.units import u

    # volume per revolution flowing from the pump for PACl (coagulant) stock
    vol_per_rev_PACl = ac.vol_per_rev_3_stop("yellow-blue")
    # revolutions per minute of PACl stock pump
    rpm_PACl = 3 * u.rev/u.min
    # flow rate from the PACl stock pump
    Q_PACl = ac.flow_rate(vol_per_rev_PACl, rpm_PACl)

    # desired system flow rate
    Q_sys = 2 * u.mL/u.s
    # desired system concentration of PACl
    C_sys = 1.4 * u.mg/u.L
    # a variable representing the reactor and its parameters
    reactor = ac.Variable_C_Stock(Q_sys, C_sys, Q_PACl)

    # required concentration of PACl stock
    C_stock_PACl = reactor.C_stock()
    # concentration of purchased PACl super stock in lab
    C_super_PACl = 70.28 * u.g/u.L
    # dilution factor of PACl super stock necessary to achieve PACl stock
    # concentration (in L of super stock per L water)
    dilution = reactor.dilution_factor(C_super_PACl)
    mL_per_L = dilution * 1000

    print("A reactor with a system flow rate of", Q_sys, ",")
    print("a system PACl concentration of", C_sys, ",")
    print("and a PACl stock flow rate of", Q_PACl)
    print("will require a dilution factor of", round(mL_per_L.magnitude, 3),
    "milliliters of PACl super")
    print("stock per liter of water for the PACl stock.")