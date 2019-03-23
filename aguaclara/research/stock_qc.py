class Reactor(object):
    def rpm(self, vol_per_rev, Q):
        return Q / vol_per_rev

    def Q_stock(self, vol_per_rev, rpm):
        return vol_per_rev * rpm

    def T_stock(self, V_stock, Q_stock):
        return V_stock / Q_stock

    def M_stock(self, V_stock, C_stock):
        return C_stock * V_stock

    def V_super_stock(self, V_stock, C_stock, C_super_stock):
        return V_stock * C_stock / C_super_stock

    def dilution_factor(self, C_stock, C_super_stock):
        return C_stock / C_super_stock


class Variable_C_Stock(Reactor):

    def __init__(self, Q_sys, C_sys, Q_stock):
        self.Q_sys = Q_sys
        self.C_sys = C_sys
        self.Q_stock = Q_stock

    def C_stock(self):
        return self.Q_sys * self.C_sys / self.Q_stock

    def rpm(self, vol_per_rev):
        return Reactor.rpm(vol_per_rev, self.Q_stock)

    def Q_stock(self):
        return self.Q_stock

    def T_stock(self, V_stock):
        return Reactor.T_stock(V_stock, self.Q_stock)

    def M_stock(self, V_stock):
        return Reactor.M_stock(V_stock, self.C_stock())

    def V_super_stock(self, V_stock, C_super_stock):
        return Reactor.V_super_stock(V_stock, self.C_stock(),
        C_super_stock)

    def dilution_factor(self, C_super_stock):
        return Reactor.dilution_factor(self.C_stock(), C_super_stock)


class Variable_Q_Stock(Reactor):

    def __init__(self, Q_sys, C_sys, C_stock, vol_per_rev):
        self.Q_sys = Q_sys
        self.C_sys = C_sys
        self.C_stock = C_stock
        self.vol_per_rev = vol_per_rev

    def Q_stock(self):
        return self.Q_sys * self.C_sys / self.C_stock

    def rpm(self):
        return Reactor.rpm(self.Q_stock(), self.vol_per_rev)

    def T_stock(self, V_stock):
        return V_stock / self.Q_stock()

    def M_stock(self, V_stock):
        return self.C_stock * V_stock

    def V_super_stock(self, V_stock, C_super_stock):
        return V_stock * self.C_stock / C_super_stock

    def dilution_factor(self, C_super_stock):
        return self.C_stock / C_super_stock
