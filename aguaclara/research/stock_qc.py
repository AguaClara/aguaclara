from aguaclara.core.units import u
import aguaclara.core.utility as ut


class Stock(object):
    """A stock of material in solution, with functions for calculations
    involving flow rate and concentration. A parent class to be used in
    Variable_C_Stock and Variable_Q_Stock.
    """

    def rpm(self, vol_per_rev, Q):
        return (Q / vol_per_rev)

    def T_stock(self, V_stock, Q_stock):
        return (V_stock / Q_stock)

    def M_stock(self, V_stock, C_stock):
        return C_stock * V_stock

    def V_super_stock(self, V_stock, C_stock, C_super_stock):
        return V_stock * (C_stock / C_super_stock).to(u.dimensionless)

    def dilution_factor(self, C_stock, C_super_stock):
        return (C_stock / C_super_stock).to(u.dimensionless)


class Variable_C_Stock(Stock):
    """A flow reactor with input from a stock of material of unknown
    concentration.

    :Examples:

    >>> from aguaclara.research.stock_qc import Variable_C_Stock
    >>> from aguaclara.core.units import u
    >>> reactor = Variable_C_Stock(Q_sys = 1*u.mL/u.s, C_sys = 1.4*u.mg/u.L, Q_stock = .01*u.mL/u.s)
    >>> reactor.C_stock()
    <Quantity(140.0, 'milligram / liter')>
    """

    def __init__(self, Q_sys, C_sys, Q_stock):
        """Initialize a reactor of unknown material stock concentration.

        :param Q_sys: Flow rate of the system
        :type Q_sys: float
        :param C_sys: Concentration of the material in the system
        :type C_sys: float
        :param Q_stock: Flow rate from the stock of material
        :type Q_stock: float
        """
        self._Q_sys = Q_sys
        self._C_sys = C_sys
        self._Q_stock = Q_stock

    def Q_sys(self):
        """Return the flow rate of the system.

        :return: Flow rate of the system
        :rtype: float
        """
        return self._Q_sys

    def C_sys(self):
        """Return the concentration of the material in the system.

        :return: Concentration of the material in the system
        :rtype: float
        """
        return self._C_sys

    def Q_stock(self):
        """Return the flow rate from the stock of material.

        :return: Flow rate from the stock of material
        :rtype: float
        """
        return self._Q_stock

    def C_stock(self):
        """Return the required concentration of material in the stock given a
        reactor's desired system flow rate, system concentration, and stock
        flow rate.

        :return: Concentration of material in the stock
        :rtype: float
        """
        return self._C_sys * (self._Q_sys / self._Q_stock).to(u.dimensionless)

    @ut.list_handler()
    def rpm(self, vol_per_rev):
        """Return the pump speed required for the reactor's stock of material
        given the volume of fluid output per revolution by the stock's pump.

        :param vol_per_rev: Volume of fluid pumped per revolution (dependent on pump and tubing)
        :type vol_per_rev: float

        :return: Pump speed for the material stock, in revolutions per minute
        :rtype: float
        """
        return Stock.rpm(self, vol_per_rev, self._Q_stock).to(u.rev/u.min)

    @ut.list_handler()
    def T_stock(self, V_stock):
        """Return the amount of time at which the stock of materal will be
        depleted.

        :param V_stock: Volume of the stock of material
        :type V_stock: float

        :return: Time at which the stock will be depleted
        :rtype: float
        """
        return Stock.T_stock(self, V_stock, self._Q_stock).to(u.hr)

    @ut.list_handler()
    def M_stock(self, V_stock):
        """Return the mass of undiluted material required for the stock
        concentration.

        :param V_stock: Volume of the stock of material
        :type V_stock: float

        :return: Mass of undiluted stock material
        :rtype: float
        """
        return Stock.M_stock(self, V_stock, self.C_stock())

    @ut.list_handler()
    def V_super_stock(self, V_stock, C_super_stock):
        """Return the volume of super (more concentrated) stock that must be
        diluted for the desired stock volume and required stock concentration.

        :param V_stock: Volume of the stock of material
        :type V_stock: float
        :param C_super_stock: Concentration of the super stock
        :type C_super_stock: float

        :return: Volume of super stock to dilute
        :rtype: float
        """
        return Stock.V_super_stock(self, V_stock, self.C_stock(), C_super_stock)

    @ut.list_handler()
    def dilution_factor(self, C_super_stock):
        """Return the dilution factor of the concentration of material in the
        stock relative to the super stock.

        :param C_super_stock: Concentration of the super stock
        :type C_super_stock: float

        :return: dilution factor of stock concentration over super stock concentration (< 1)
        :rtype: float
        """
        return Stock.dilution_factor(self, self.C_stock(), C_super_stock)


class Variable_Q_Stock(Stock):
    """A flow reactor with input from a stock of material at an unknown flow
    rate.

    :Examples:

    >>> from aguaclara.research.stock_qc import Variable_Q_Stock
    >>> from aguaclara.core.units import u
    >>> reactor = Variable_Q_Stock(Q_sys = 1*u.mL/u.s, C_sys = 1.4*u.mg/u.L, C_stock = 7.6*u.mg/u.L)
    >>> reactor.Q_stock()
    <Quantity(0.18421052631578946, 'milliliter / second')>
    >>> reactor.rpm(vol_per_rev = .5*u.mL/u.rev).to(u.rev/u.min)
    <Quantity(22.105263157894736, 'rev / minute')>
    """

    def __init__(self, Q_sys, C_sys, C_stock):
        """Initialize a reactor of unknown material stock flow rate.

        :param Q_sys: Flow rate of the system
        :type Q_sys: float
        :param C_sys: Concentration of the material in the system
        :type C_sys: float
        :param C_stock: Concentration of the material in the stock
        :type C_stock: float
        """
        self._Q_sys = Q_sys
        self._C_sys = C_sys
        self._C_stock = C_stock

    def Q_sys(self):
        """Return the flow rate of the system.

        :return: Flow rate of the system
        :rtype: float
        """
        return self._Q_sys

    def C_sys(self):
        """Return the concentration of the material in the system.

        :return: Concentration of the material in the system
        :rtype: float
        """
        return self._C_sys

    def C_stock(self):
        """Return the concentration of the material in the stock.

        :return: Concentration of the material in the stock
        :rtype: float
        """
        return self._C_stock

    def Q_stock(self):
        """Return the required flow rate from the stock of material given
        a reactor's desired system flow rate, system concentration, and stock
        concentration.

        :return: Flow rate from the stock of material
        :rtype: float
        """
        return self._Q_sys * (self._C_sys / self._C_stock).to(u.dimensionless)

    @ut.list_handler()
    def rpm(self, vol_per_rev):
        """Return the pump speed required for the reactor's stock of material
        given the volume of fluid output per revolution by the stock's pump.

        :param vol_per_rev: Volume of fluid pumped per revolution (dependent on pump and tubing)
        :type vol_per_rev: float

        :return: Pump speed for the material stock, in revolutions per minute
        :rtype: float
        """
        return Stock.rpm(self, vol_per_rev, self.Q_stock()).to(u.rev/u.min)

    @ut.list_handler()
    def T_stock(self, V_stock):
        """Return the amount of time at which the stock of materal will be
        depleted.

        :param V_stock: Volume of the stock of material
        :type V_stock: float

        :return: Time at which the stock will be depleted
        :rtype: float
        """
        return Stock.T_stock(self, V_stock, self.Q_stock()).to(u.hr)

    @ut.list_handler()
    def M_stock(self, V_stock):
        """Return the mass of undiluted material required for the stock
        concentration.

        :param V_stock: Volume of the stock of material
        :type V_stock: float

        :return: Mass of undiluted stock material
        :rtype: float
        """
        return Stock.M_stock(self, V_stock, self._C_stock)

    @ut.list_handler()
    def V_super_stock(self, V_stock, C_super_stock):
        """Return the volume of super (more concentrated) stock that must be
        diluted for the desired stock volume and stock concentration.

        :param V_stock: Volume of the stock of material
        :type V_stock: float
        :param C_super_stock: Concentration of the super stock
        :type C_super_stock: float

        :return: Volume of super stock to dilute
        :rtype: float
        """
        return Stock.V_super_stock(self, V_stock, self._C_stock, C_super_stock)

    @ut.list_handler()
    def dilution_factor(self, C_super_stock):
        """Return the dilution factor of the concentration of material in the
        stock relative to the super stock.

        :param C_super_stock: Concentration of the super stock
        :type C_super_stock: float

        :return: dilution factor of stock concentration over super stock concentration (< 1)
        :rtype: float
        """
        return Stock.dilution_factor(self, self._C_stock, C_super_stock)
