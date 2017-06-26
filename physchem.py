"""
Created on Thu Jun 15 14:07:28 2017

@author: Karan Newatia

Last modified: Mon Jun 26 2017 
By: Sage Weber-Shirk


This file contains unit process functions pertaining to the design of 
physical/chemical unit processes for AguaClara water treatment plants.
"""

######################### Imports #########################
import math
import numpy as np
import scipy

from AguaClara_design.units import unit_registry as u

gravity = 9.80665 * (u.m / (u.s**2))
"""Define the gravitational constant."""

#######################Simple geometry#######################
"""A few equations for useful geometry.
Is there a geometry package that we should be using?
"""

def area_circle(diam_Circle):
    """Return the area of a circle."""
    return math.pi/4*diam_Circle**2


def diam_circle(A_Circle):
    """Return the diameter of a circle."""
    A_Circle=A_Circle.to(u.m**2)
    A_Circle=A_Circle.magnitude
    diam_req = np.sqrt(4*A_Circle/math.pi)
    return diam_req*(u.m)

######################### Hydraulics ######################### 

WATER_DENSITY_TABLE = [u.Quantity([0, 5, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100
                                 ],u.degC), 
                     [999.9, 1000, 999.7, 998.2, 995.7, 992.2, 988.1, 983.2, 
                      977.8, 971.8, 965.3, 958.4
                      ]
                     ]


# dynamic viscosity
def viscosity_dynamic(T):
    Ttemp=T.to(u.kelvin).magnitude
    mu=2.414*(10**-5)*u.Pa*u.s*10**((247.8)/(Ttemp-140))
    return mu


def density_water(temp):
    """Return the density of water at a given temperature."""
    rhointerpolated = scipy.interpolate.CubicSpline(WATER_DENSITY_TABLE[0], 
                                                    WATER_DENSITY_TABLE[1])
    rho=rhointerpolated(temp.to(u.degC))
    return rho * u.kg/u.m**3


# kinematic viscosity
def viscosity_kinematic(T):
    nu=viscosity_dynamic(T)/(density_water(T))
    return nu.to(u.mm**2/u.s)


def re_pipe(Q, D, nu):
    """Return the Reynolds number for a pipe."""
    Re=(4*Q)/(math.pi*D*nu)
    return Re.to(u.dimensionless)
    # The .to part forces Re to be dimensionless

Re_TRANSITION_PIPE=2100


def radius_hydraulic(w, b, openchannel):
    """Return the hydraulic radius."""    
    if openchannel == 1:
        h = (w*b) / (w + 2*b)
        # if openchannel==1, the channel is open. Otherwise, the channel is 
        # assumed to have sides    
    else:
        h = (w*b) / (2 * (w+b))
    return h.to(u.m)


def radius_hydraulic_general(A, WP):
    """Return the general hydraulic radius."""
    hGen = A / WP 
    #Area/wetted perimeter
    return hGen.to(u.m)


def re_rect(Q, w, b, nu, openchannel):
    """Return the Reynolds number for a rectangular channel."""
    rect = 4 * Q * radius_hydraulic(w, b, openchannel) / (w*b*nu)
    #Reynolds number for rectangular channel; open = 0 if all sides
    #are wetted; l = D and D = 4*R.h       
    return rect.to(u.dimesnionless)


def re_general(V, A, WP, nu):
    """Return the Reynolds number for a general cross section."""
    gen = 4 * radius_hydraulic_general(A, WP) * V / nu
    return gen.to(u.dimensionless)
        
   
def fric(Q,D,nu,e):
    """Return the friction factor for pipe flow.
    
    This equation applies to both laminar and turbulent flows.
    """
    if re_pipe(Q, D, nu) >= Re_TRANSITION_PIPE:
        #Swamee-Jain friction factor for turbulent flow; best for 
        #Re>3000 and ε/D < 0.02        
        f = 0.25 / (math.log10(e/(3.7*D) + 5.74/re_pipe(Q, D, nu) ** 0.9))**2
    else:
        f = 64 / re_pipe(Q, D, nu)
    return f.to(u.dimensionless)


def fric_rect(Q, w, b, nu, e, openchannel):
    """Return the friction factor for a rectangular channel."""
    if re_rect(Q, w, b, nu, openchannel) >= Re_TRANSITION_PIPE:
        #Swamee-Jain friction factor adapted for rectangular channel.
        #D = 4*R*h in this case.         
        f = 0.25 / (math.log10(e/(3.7 * 4 * radius_hydraulic(w,b,openchannel))
                               + 5.74 / re_rect(Q,w,b,nu,openchannel)**0.9
                               )
                    ) ** 2
    else:
        f = 64 / re_rect(Q, w, b, nu, openchannel)
    return f.to(u.dimensionless)   
 
    
def fric_general(A, WP, V, nu, e):
    """Return the friction factor for a general channel."""
    if re_general(V, A, WP, nu) >= Re_TRANSITION_PIPE:
        #Swamee-Jain friction factor adapted for any cross-section.
        #D = 4*R*h 
        f=0.25 / (math.log10(e/(3.7 * 4 * radius_hydraulic_general(A, WP)) 
                             + 5.74/re_general(V, A, WP, nu)**0.9
                             )
                  ) ** 2
    else:
        f = 64 / re_general(V, A, WP, nu)
    return f.to(u.dimensionless)      
         
        
def headloss_fric(Q, D, L, nu, e):
    """Return the major head loss (due to wall shear) in a pipe.
    
    This equation applies to both laminar and turbulent flows.
    """
    HLf = fric(Q, D, nu, e) * 8 / (gravity*math.pi**2) * (L * Q**2) / D**5
    return HLf.to(u.m)  


def headloss_exp(Q, D, K):
    """Return the minor head loss (due to expansions) in a pipe. 
    
    This equation applies to both laminar and turbulent flows.
    """
    HLe = K * 8 / (gravity * math.pi**2) * Q**2 / D**4
    return HLe.to(u.m)


def headloss(Q, D, L, nu, e, K):
    """Return the total head loss from major and minor losses in a pipe.
    
    This equation applies to both laminar and turbulent flows.
    """
    HL = headloss_fric(Q, D, L, nu, e) + headloss_exp(Q, D, K)
    return HL.to(u.m)


def headloss_fric_rect(Q, w, b, L, nu, e, openchannel):
    """Return the major head loss due to wall shear in a rectangular channel.
    
    This equation applies to both laminar and turbulent flows.
    """
    Hfrect = (fric_rect(Q, w, b, nu, e, openchannel) * L 
              / (4 * radius_hydraulic(w, b, openchannel)) * Q**2 
              / (2 * gravity * (w*b)**2)
              )
    return Hfrect.to(u.m)


def headloss_exp_rect(Q, w, b, K):
     """Return the minor head loss due to expansion in a rectangular channel.
     
     This equation applies to both laminar and turbulent flows.
     """
     Herect = K * Q**2 / (2 * gravity * (w*b)**2)
     return Herect.to(u.m)
 
    
def headloss_rect(Q, w, b, L, K, nu, e, openchannel):
      """Return the total head loss in a rectangular channel. 
      
      Total head loss is a combination of the major and minor losses.
      This equation applies to both laminar and turbulent flows.
      """
      Hlrect = (headloss_exp_rect(Q, w, b, K) 
                + headloss_fric_rect(Q, w, b, L, nu, e, openchannel))
      return Hlrect.to(u.m)
    
    
def headloss_fric_general(A, WP, V, L, nu, e):
     """Return the major head loss due to wall shear in the general case.
     
     This equation applies to both laminar and turbulent flows.
     """
     Hfgen = (fric_general(A, WP, V, nu, e) * L 
              / (4*radius_hydraulic_general(A,WP)) * V**2 / (2*gravity)
              )
     return Hfgen.to(u.m)
 
    
def headloss_exp_general(V, K):
    """Return the minor head loss due to expansion in the general case.
    
    This equation applies to both laminar and turbulent flows.
    """
    Hegen=K * V**2 / (2*gravity)
    return Hegen.to(u.m)


def headloss_gen(A, V, WP, L, K, nu, e):
     """Return the total head lossin the general case.
     
     Total head loss is a combination of major and minor losses.
     This equation applies to both laminar and turbulent flows.
     """
     Hlgen = headloss_exp_general(V,K) + headloss_fric_general(A,WP,V,L,nu,e)
     return Hlgen.to(u.m)
 
    
def headloss_manifold(Q, D, L, K, nu, e, n):
    """Return the total head loss through the manifold."""
    hlmani = headloss(Q,D,L,nu,e,K) * (1/3 + 1/(2*n) + 1/((6*n)**2))
    return hlmani.to(u.m)


def flow_orifice(D, h, ratio_VC_orifice):
    """Return the flow rate of the orifice."""
    if h > 0 * u.cm:
        Q = ratio_VC_orifice * area_circle(D) * np.sqrt(2*gravity*h)
        return Q.to(u.L/u.s)
    else:
         return 0 * (u.L/u.s)


def flow_orifice_vert(D,h,ratio_VC_orifice):
    """Return the vertical flow rate of the orifice."""
    if h>-D/2:
        h = h.to(u.m)
        D = D.to(u.m)
        h = h.magnitude
        D = D.magnitude
        Q = scipy.integrate.quad(lambda z: D * math.sin(math.acos(z/(D/2))) 
                                 * np.sqrt(h-z),-D/2,min(D/2,h)
                                 )
        Qnew = Q[0]
        Q = ratio_VC_orifice * np.sqrt(2*gravity.magnitude) * Qnew * 1000
        return Q * (u.L/u.s)
    else:
       return 0 * (u.L/u.s)


def head_orifice(D, ratio_VC_orifice, Q):
     """Return the head of the orifice."""
     h = (Q / (ratio_VC_orifice*area_circle(D)))**2 / (2*gravity)
     return h.to(u.m)
 
    
def area_orifice(h, ratio_VC_orifice, Q):
    """Return the area of the orifice."""
    area = Q / (ratio_VC_orifice * np.sqrt(2*gravity*h))
    return area.to(u.mm**2)
    

def number_orifices(Q_plant,ratio_VC_orifice,headloss_orifice,D_orifice):
     """Return the number of orifices."""
     n = math.ceil(area_orifice(headloss_orifice, ratio_VC_orifice, Q_plant)
                   / area_circle(D_orifice)
                   )
     return n.to(u.dimensionless)
 
    
def diam_orifice_manifold(Q_manifold_ratio, Q_tank, d_pipe, L_s, L_l, K_total, 
                          n_orifice, nu, e, ratio_VC_orifice):
     """Return the diameter of the orifice in the manifold."""
     d = (((1 - Q_manifold_ratio)*d_pipe) ** 4 
          / ((((K_total + (fric(Q_tank, d_pipe, nu, e) * L_l/d_pipe)) 
               * (Q_manifold_ratio)) - K_total 
               - (fric(Q_tank,d_pipe,nu,e) * L_l / d_pipe) 
               * (ratio_VC_orifice)**2 * (n_orifice) **2)
             )
          ) ** (1/4)
     return d.to(u.m)
 
    
# Here we define functions that return the flow rate.
def flow_transition(D, nu):
    """Return the flow rate for the laminar/turbulent transition.
    
    This equation is used in some of the other equations for flow.
    """
    return (math.pi * D * Re_TRANSITION_PIPE * nu / 4).to(u.L/u.s)


def flow_hagen(D, hf, L, nu):
    """Return the flow rate for laminar flow with only major losses."""
    return ((math.pi * D**4) / (128*nu) * gravity * hf / L).to(u.L/u.s)


def flow_swamee(D, hf, L, nu, e):
    """Return the flow rate for turbulent flow with only major losses."""
    logterm = -math.log10(e/(3.7*D) + 2.51*nu*np.sqrt(L/(2 * gravity * hf * 
                                                         D**3)))
    return ((math.pi / np.sqrt(2)) * D**(5/2) 
            * np.sqrt(gravity * hf / L) * logterm
            ).to(u.L/u.s)


def flow_pipemajor(D,hf,L,nu,e):
    """Return the flow rate with only major losses.
    
    This function applies to both laminar and turbulent flows.
    """
    Q_H = flow_hagen(D, hf, L, nu)
    if Q_H < flow_transition(D, nu):
        Q = Q_H
    else:
        Q = flow_swamee(D, hf, L, nu, e)
    return Q.to(u.L/u.s)


def flow_pipeminor(D,he,K):
    """Return the flow rate with only minor losses.
    
    This function applies to both laminar and turbulent flows.
    """ 
    return (area_circle(D) * np.sqrt(2 * gravity * he / K)).to(u.L/u.s)

# Now we put all of the flow equations together and calculate the flow in a 
# straight pipe that has both major and minor losses and might be either
# laminar or turbulent.
def flow_pipe(D, hl, L, nu, e, K):
    """Return the the flow in a straight pipe.
    
    This function works for both major and minor losses and 
    works whether the flow is laminar or turbulent.
    """
    if K == 0:
        Q = flow_pipemajor(D, hl, L, nu, e)
    else:
        Qprev = 0 * u.L/u.s
        err = 1
        Q = min(flow_pipemajor(D, hl, L, nu, e) , flow_pipeminor(D, hl, K))
        while err > 0.01:
            Qprev = Q
            hfnew = (hl * headloss_fric(Q, D, L, nu, e) 
                     / (headloss_fric(Q, D, L, nu, e) 
                        + headloss_exp(Q,D,K)
                        )
                     )
            Q = flow_pipemajor(D, hfnew, L, nu, e)
            if Q == 0 * u.L/u.s:
                err = 0
            else:
                err = abs(Q-Qprev) / (Q+Qprev)
    return Q.to(u.L/u.s)  	
 

def diam_hagen(Q, hf, L, nu):
    D = ((128 * nu * Q * L) / (gravity * hf * math.pi)) ** (1/4)
    return D.to_base_units()


def diam_swamee(Q, hf, L, nu, e):
    """Return the inner diameter of a pipe.
    
    The Swamee Jain equation is dimensionally correct and returns the 
    inner diameter of a pipe given the flow rate and the head loss due
    to shear on the pipe walls. The Swamee Jain equation does NOT take 
    minor losses into account. This equation ONLY applies to turbulent 
    flow.
    Pint has trouble adding two numbers that are raised to the 25th 
    power. This function strips the units before adding the two 
    terms and then reattaches the units.
    """
    a = ((e**1.25) * ((L * Q**2) / (gravity*hf))**4.75).to_base_units().magnitude
    b = (nu * (Q**9.4) * (L / (gravity*hf))**5.2).to_base_units().magnitude
    D = (0.66 * (a+b)**0.04) * u.m
    return D.to_base_units()


def diam_pipemajor(Q, hf, L, nu, e):
    """Return the pipe ID that would result in given major losses.
    
    This function applies to both laminar and turbulent flow.
    """
    D_Laminar = diam_hagen(Q, hf, L, nu)
    if re_pipe(Q, D_Laminar, nu) <= Re_TRANSITION_PIPE:
        D = D_Laminar
    else:
        D = diam_swamee(Q, hf, L, nu, e)
    return D.to_base_units()


def diam_pipeminor(Q, he, K):
    """Return the pipe ID that would result in the given minor losses.
    
    This function applies to both laminar and turbulent flow.
    """
    D = (np.sqrt(4 * Q / math.pi)) * (K / (2 * gravity * he))**(1/4)
    return D.to(u.m)


def diam_pipe(Q, hl, L, nu, e, K):
    """Return the pipe ID that would result in the given total head loss.
    
    This function applies to both laminar and turbulent flow and
    incorporates both minor and major losses.
    """
    if K == 0:
        D = diam_pipeminor(Q, hl, K)
    else:
        D = diam_pipemajor(Q, hl, L, nu, e)
    err = 1.00
    while err > 0.001:
        Dprev = D
        hfnew = (hl * headloss_fric(Q, D, L, nu, e) 
                 / (headloss_fric(Q, D, L, nu, e) + headloss_exp(Q, D, K))
                 )
        D = diam_pipemajor(Q, hfnew, L, nu, e)
        err = abs(D-Dprev) / (D+Dprev)
    return D.to_base_units() 

# Weir head loss equations
RATIO_VC_ORIFICE = 0.62

def width_rect_weir(Q, H):
    """Return the width of a rectangular weir."""
    w = (3 / 2) * Q / (RATIO_VC_ORIFICE * (np.sqrt(2*gravity) * H**(3/2)))
    return w.to(u.m)

# For a pipe, W is the circumference of the pipe.
# Head loss for a weir is the difference in height between the water
# upstream of the weir and the top of the weir.
def headloss_weir(Q,W):
    """Return the headloss of a weir."""
    hl = ((3/2) * Q / (RATIO_VC_ORIFICE * (np.sqrt(2*gravity)*W))) ** 3
    return hl.to(u.m)


def flow_rect_weir(H, W):
    """Return the flow of a rectangular weir."""
    q = (2/3) * RATIO_VC_ORIFICE * (np.sqrt(2*gravity) * H**(3/2)) * W
    return q.to(u.m)


def height_water_critical(Q, W):
    """Return the critical local water depth."""
    hw = (Q / (W * gravity)) ** (2/3)
    return hw.to(u.m)


def vel_horizontal(height_water_critical):
    """Return the horizontal velocity."""
    v = np.sqrt(gravity * height_water_critical)
    return v.to(u.m/u.s)

K_KOZENY=5

def headloss_kozeny(L,D,V,e,nu):
    """Return the Carmen Kozeny Sand Bed head loss."""
    hl = K_KOZENY * L * nu / gravity * (1-e) ** 2 / e**3 * 36 * V / D**2
    return hl.to(u.m)
    


  	
######################### Flocculation #########################
PHI_FLOC = 45 / 24


def C_Prec(Dose: 'Dose in mg/L as Al'): 
    """Calculate precipitate concentration given Aluminum concentration."""
    return Dose.to(u.mg/u.L) * 1.3 / 0.027 / 13 # Changed 1.039384 to 1.3


def phi_0(Dose: 'in mg/L', Inf: 'in NTU'): 
    """Calculate phi_0. 
    
    Currently broken."""
    x = C_Prec(Dose) / r_Co + Inf.to(u.mg/u.L) / r_Cl
    return x.to(u.dimensionless) 


def P_ClSphere(P_HD): 
    """Calculate surface area to volume ratio for clay.
    
    Normalized to that of a sphere.
    """
    return (0.5 + P_HD) * (2/(3*P_HD))**(2/3)


def P_AClATot(Inf: 'in NTU', D_Cl: 'in um', D_T: 'in inches', P_HD): 
    """Normalize surface area of clay by total surface area.
    
    Currently broken.
    Surface area is calculated as the sum of clay + walls.
    """
    x = (1 / (1+(2 * D_Cl.to(u.m) / (3 * D_T.to(u.m) * P_ClSphere(P_HD) 
                                    * Inf / r_Cl
                                    )))
         )
    return x.to(u.dimensionless)


def Gamma(Inf, D, D_T, D_Cl, P_HD, D_Co): 
    """Calculate Gamma."""
    return (1 - np.exp((-phi_0(D, 0*u.mg/u.L) * D_Cl)
                       / (phi_0(0*u.mg/u.L, Inf) * D_Co) * 1 / np.pi
                       * (P_AClATot(Inf, D_Cl, D_T, P_HD))
                       / (P_ClSphere(P_HD))
                       )
            )


def D_Sep(phi, D_Cl): 
    """Return the particle separation distance."""
    x = (np.pi / 6 / phi)**(1/3) * D_Cl
    return x.to(u.micrometer)


def P_V(Gam, t, EDR, nu, phi):
    x = (Gam * t * np.sqrt(EDR.to(u.m**2/u.s**3) / nu.to(u.m**2/u.s)) 
         * phi**(2/3)
         )
    return x.to(u.dimensionless)


def P_I(Gam, t, EDR, D_Cl, phi):
    x = (Gam * t * (EDR.to(u.m**2/u.s**3) / D_Cl.to(u.m)**2)**(1/3)
         * phi**(8/9)
         )
    return x.to(u.dimensionless)


def pC_I(N, k):
    return 9/8 * np.log10(8/9 * np.pi * k * N * (6.0 / np.pi)**(8/9) + 1)


def pC_V(N, k): 
    return 1.5 * np.log10(2/3 * np.pi * k * N * (6.0 / np.pi)**(2/3) + 1)


def diam_floc_max(epsMax):
    """Return floc size as a function of energy dissipation rate.
    
    Based on Ian Tse's work with floc size as a function of energy 
    dissipation rate. This is for the average energy dissipation rate 
    in a tube flocculator. It isn't clear how to convert this to the 
    turbulent flow case. Maybe the flocs are mostly experiencing viscous
    shear. But that isn't clear. Some authors have made the case that 
    floc breakup is due to viscous effects. If that is the case, then 
    the results from the tube flocculator should be applicable to the 
    turbulent case. We will have to account for the temporal and spatial
    variability in the turbulent energy dissipation rate. The factor of 
    95 μm is based on the assumption that the ratio of the max to 
    average energy dissipation rate for laminar flow is approximately 2.
    """
    return 95 * u.um * (1 / (epsMax.to(u.W/u.kg).magnitude)**(1/3))