from aguaclara.core.units import unit_registry as u
import aguaclara.core.physchem as pc
import aguaclara.core.constants as con
import aguaclara.core.materials as mat
import aguaclara.core.pipes as pipe
import aguaclara.core.head_loss as hl

class EntTankFloc:
    def __init__(self, q,
                max_L=6 * u.m,
                Gt=37000,
                HL = 40 * u.cm,
                downstream_H = 2 * u.m,
                ent_L=1.5 * u.m,
                max_W=42 * u.inch,
                drain_t=30 * u.min,
                floc_chan_w=42. * u.inch,
                temp=20. * u.degC,
                floc_end_depth=2. * u.m, 
                sdr=41.,
                lfom_hl=20 * u.cm,
                safety_factor=1.5,
                lfom_sdr=26,
                drill_bits=drills.DRILL_BITS_D_IMPERIAL,
                s_orifice=0.5*u.cm ):
        self.floc = Flocculator(q, floc_temp, max_L, Gt, HL, downstream_H, 
                                ent_L, max_W, drain_t)
        self.ent_tank = ent_tank(q, floc_chan_w, floc_end_depth, ent_temp, sdr)
        self.lfom = lfom(q, lfom_hl, safety_factor, lfom_sdr, drill_bits, s_orifice)
	

