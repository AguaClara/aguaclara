"""
Created on Thu Jun 15 14:07:28 2017

@author: kn348
"""

# This file contains unit process functions pertaining to the design of physical/chemical unit processes for AguaClara water treatment plants.

######################### Imports #########################
import math
import numpy as np
import scipy

from units import unit_registry as u


#######################Simple geometry#######################

#A few equations for useful geometry
# Is there a geometry package that we should be using?

def area_circle(diam_Circle):
    return math.pi/4*diam_Circle**2

def diam_circle(A_Circle):
    return (4*A_Circle/math.pi)**(1/2)

######################### Hydraulics ######################### 

def re_pipe(Q,D,nu):
    Re=(4*Q)/(math.pi*D*nu)
    return Re.to(u.dimensionless)
# The .to part forces Re to be dimensionless

Re_TRANSITION_PIPE=2100


def radius_hydraulic(w,b,openchannel):
    """ returns the hydraulic radius"""    
    if openchannel==1:
        h=(w*b)/(w + 2*b)
#if openchnnael==1, the channel is open. Otherwise, the channel is assumed to have sides    
    else:
        h=(w*b)/(2*(w+b))
    return h.to(u.m)


def radius_hydraulic_general(A,WP):
    """returns the general hydraulic radius"""
    hGen= A/WP 
#Area/wetted perimeter
    return hGen.to(u.m)


def re_rect(Q,w,b,nu,openchannel):
    """returns the Reynolds number for rectangular channel"""
    rect=4*Q*radius_hydraulic(w,b,openchannel)/(w*b*nu)
#Reynolds number for rectangular channel; open = 0 if all sides are wetted; l = D and D = 4*R.h       
    return rect.to(u.dimesnionless)


def re_general(V,A,WP,nu):
    """returns the Reynolds number for general cross section"""
    gen=4*radius_hydraulic_general(A,WP)*V/nu
    return gen.to(u.dimensionless)
           
def fric(Q,D,nu,e):
    """Returns the friction factor for pipe flow for both laminar and turbulent flows"""
    if re_pipe(Q,D,nu)>=Re_TRANSITION_PIPE:
#Swamee-Jain friction factor for turbulent flow; best for Re>3000 and ε/D < 0.02        
        f=0.25/(math.log10(e/(3.7*D)+5.74/re_pipe(Q,D,nu)**0.9))**2
    else:
        f=64/re_pipe(Q,D,nu)
    return f.to(u.dimensionless)

def fric_rect(Q,w,b,nu,e,openchannel):
    """returns the friction factor for a rectangular channel"""
    if re_rect(Q,w,b,nu,openchannel)>=Re_TRANSITION_PIPE:
#Swamee-Jain friction factor adapted for rectangular channel.
#D = 4*R*h in this case.         
          f=0.25/(math.log10(e/(3.7*4*radius_hydraulic(w,b,openchannel))+5.74/re_rect(Q,w,b,nu,openchannel)**0.9))**2
    else:
         f=64/re_rect(Q,w,b,nu,openchannel)
    return f.to(u.dimensionless)   
 
def fric_general(A,WP,V,nu,e):
    """returns the friction factor for a general channel"""
    if re_general(V,A,WP,nu)>=Re_TRANSITION_PIPE:
#Swamee-Jain friction factor adapted for any cross-section.
#D = 4*R*h 
        f=0.25/(math.log10(e/(3.7*4*radius_hydraulic_general(A,WP))+5.74/re_general(V,A,WP,nu)**0.9))**2
    else:
        f=64/re_general(V,A,WP,nu)
    return f.to(u.dimensionless)      
                 
def headloss_fric(Q,D,L,nu,e):
    """Returns the major head loss (due to wall shear) in a pipe for both laminar and turbulent flows"""
    HLf=fric(Q,D,nu,e)*8/(u.g_0*math.pi**2)*(L*Q**2)/D**5
    return HLf.to(u.m)  

def headloss_exp(Q,D,K):
    """Returns the minor head loss (due to expansions) in a pipe. This equation applies to both laminar and turbulent flows"""
    HLe=K*8/(u.g_0*math.pi**2)*(Q**2)/(D**4)
    return HLe.to(u.m)

def headloss(Q,D,L,nu,e,K):
    """ Returns the total head loss due to major and minor losses in a pipe. This equation applies to both laminar and turbulent flows"""
    HL= headloss_fric(Q,D,L,nu,e)+headloss_exp(Q,D,K)
    return HL.to(u.m)

def headloss_fric_rect(Q,w,b,L,nu,e,openchannel):
    """Returns the major head loss (due to wall shear) in a rectangular channel for both laminar and turbulent flows"""
    Hfrect=fric_rect(Q,w,b,nu,e,openchannel)*L/(4*radius_hydraulic(w,b,openchannel))*Q**2/(2*u.g_0*(w*b)**2)
    return Hfrect.to(u.m)

def headloss_exp_rect(Q,w,b,K):
     """Returns the minor head loss (due to expansions) in a rectangular channel. This equation applies to both laminar and turbulent flows"""
     Herect=K*Q**2/(2*u.g_0*(w*b)**2)
     return Herect.to(u.m)
 
def headloss_rect(Q,w,b,L,K,nu,e,openchannel):
      """ Returns the total head loss due to major and minor losses in a rectangular channel. This equation applies to both laminar and turbulent flows"""
      Hlrect=headloss_exp_rect(Q,w,b,K)+ headloss_fric_rect(Q,w,b,L,nu,e,openchannel)
      return Hlrect.to(u.m)
    
def headloss_fric_general(A,WP,V,L,nu,e):
     """Returns the major head loss (due to wall shear) in the general case for both laminar and turbulent flows"""
     Hfgen=fric_general(A,WP,V,nu,e)*L/(4*radius_hydraulic_general(A,WP))*V**2/(2*u.g_0)
     return Hfgen.to(u.m)
 
def headloss_exp_general(V,K):
    """Returns the minor head loss (due to expansions) in the general case. This equation applies to both laminar and turbulent flows"""
    Hegen=K*V**2/(2*u.g_0)
    return Hegen.to(u.m)

def headloss_gen(A,V,WP,L,K,nu,e):
     """ Returns the total head loss due to major and minor losses in the general case. This equation applies to both laminar and turbulent flows"""
     Hlgen=headloss_exp_general(V,K) + headloss_fric_general(A,WP,V,L,nu,e)
     return Hlgen.to(u.m)
 
def headloss_manifold(Q,D,L,K,nu,e,n):
    """Returns the total head loss through the manifold"""
    hlmani=headloss(Q,D,L,nu,e,K)*(1/3+1/(2*n)+1/((6*n)**2))
    return hlmani.to(u.m)

def flow_orifice(D,h,ratio_VC_orifice):
    """Returns the flow rate of orifice"""
    if h>0*u.cm:
        Q=ratio_VC_orifice*area_circle(D)*(2*u.g_0*h)**(1/2)
        return Q.to(u.L/u.s)
    else:
         return 0*(u.L/u.s)

def flow_orifice_vert(D,h,ratio_VC_orifice):
    """Returns the vertical flow rate of orifice"""
    if h>-D/2:
        h = h.to(u.m)
        D = D.to(u.m)
        h=h.magnitude
        D=D.magnitude

        Q=scipy.integrate.quad(lambda z: D*math.sin(math.acos(z/(D/2)))*((h-z)**(1/2)),-D/2,min(D/2,h))
        Qnew=Q[0]
        Q=ratio_VC_orifice*((2*9.80665)**(1/2))*Qnew*1000
       
        return Q*(u.L/u.s)
    else:
       return 0*(u.L/u.s)

def head_orifice(D,ratio_VC_orifice,Q):
     """Returns the head of orifice"""
     h=(Q/(ratio_VC_orifice*area_circle(D)))**2/(2*u.g_0)
     return h.to(u.m)
 
def area_orifice(h,ratio_VC_orifice,Q):
    """Returns the area of orifice"""
    area=Q/(ratio_VC_orifice*(2*u.g_0*h)**(1/2))
    return area.to(u.mm**2)
    
def number_orifices(Q_plant,ratio_VC_orifice,headloss_orifice,D_orifice):
     """Returns the number of orifice"""
     n=math.ceil(area_orifice(headloss_orifice,ratio_VC_orifice,Q_plant)/area_circle(D_orifice))
     return n.to(u.dimensionless)
 
def diam_orifice_manifold(Q_manifold_ratio,Q_tank,d_pipe,L_s,L_l,K_total,n_orifice,nu,e,ratio_VC_orifice):
     """Returns the diameter of orifice in the manifold"""
     d=(((1-Q_manifold_ratio)*d_pipe)**4/((((K_total + (fric(Q_tank,d_pipe,nu,e)*L_l/d_pipe))*(Q_manifold_ratio)) - K_total - (fric(Q_tank,d_pipe,nu,e)*L_l/d_pipe)*(ratio_VC_orifice)**2*(n_orifice) **2)))**(1/4)
     return d.to(u.m)
 
# Here we define functions that return the flow rate.

# This equation is used in some of the other equations for flow.
def flow_transition(D,nu):
    """Returns the flow rate for the transition between laminar and turbulent."""
    return (math.pi*D*Re_TRANSITION_PIPE*nu/4).to(u.L/u.s)

def flow_hagen(D,hf,L,nu):
    """Returns the Flow rate for laminar flow with only major losses"""
    return ((math.pi*D**4)/(128*nu)*u.g_0*hf/L).to(u.L/u.s)

def flow_swamee(D,hf,L,nu,e):
    """Returns the  Flow rate for turbulent flow with only major losses"""
    logterm=-math.log10(e/(3.7*D)+2.51*nu*(L/(2*u.g_0*hf*D**3))**(1/2))
    return ((math.pi/2**(1/2))*D**(5/2)*(u.g_0*hf/L)**(1/2)*logterm).to(u.L/u.s)

def flow_pipemajor(D,hf,L,nu,e):
    """Returns the Flow rate for turbulent or laminar flow with only major losses"""
    Q_H=flow_hagen(D,hf,L,nu)
    if Q_H<flow_transition(D,nu):
        Q=Q_H
    else:
        Q=flow_swamee(D,hf,L,nu,e)
    return Q.to(u.L/u.s)

def flow_pipeminor(D,he,K):
    """Returns the  Flow rate for turbulent or laminar flow with only minor losses""" 
    return (area_circle(D)*(2*u.g_0*he/K)**(1/2)).to(u.L/u.s)

# Now we put all of the flow equations together and calculate the flow in a 
# straight pipe that has both major and minor losses and might be either
# laminar or turbulent.
def flow_pipe(D,hl,L,nu,e,K):
    """Returns the the flow in a straight pipe that has both major and minor losses and might be either laminar or turbulent."""
    if K==0:
        Q=flow_pipemajor(D,hl,L,nu,e)
    else:
        Qprev=0*u.L/u.s
        err=1
        Q=min(flow_pipemajor(D,hl,L,nu,e),flow_pipeminor(D,hl,K))
        while err>0.01:
            Qprev=Q
            hfnew=hl*headloss_fric(Q,D,L,nu,e)/(headloss_fric(Q,D,L,nu,e)+headloss_exp(Q,D,K))
            Q=flow_pipemajor(D,hfnew,L,nu,e)
            if Q==0*u.L/u.s:
                err=0
            else:
                err=abs(Q-Qprev)/(Q+Qprev)
    return Q.to(u.L/u.s)  	
 

def diam_hagen(Q,hf,L,nu):
    D=((128*nu*Q*L)/(u.g_0*hf*math.pi))**(1/4)
    return D.to_base_units()

# The Swamee Jain equation (below) is dimensionally correct and returns the inner diameter of a pipe 
# given the flow rate and the head loss due to shear on the pipe walls.
# The Swamee Jain equation does NOT take minor losses into account.
# This equation ONLY applies to turbulent flow.
# Pint has trouble adding two numbers that are raised to the 25th power. 
# The following code strips the units before adding the two terms and then reattaches the units.

def diam_swamee(Q,hf,L,nu,e):
    """Returns the inner diameter of a pipe"""
    a=((e**1.25)*((L*(Q**2))/(u.g_0*hf))**4.75).to_base_units().magnitude
    b=(nu*(Q**9.4)*(L/(u.g_0*hf))**5.2).to_base_units().magnitude
    D=(0.66*(a+b)**0.04)*u.m
    return D.to_base_units()

# Applies to both laminar and turbulent flow
def diam_pipemajor(Q,hf,L,nu,e):
    """Returns the pipe ID that would result in given major losses"""
    D_Laminar= diam_hagen(Q,hf,L,nu)
    if re_pipe(Q,D_Laminar,nu)<=Re_TRANSITION_PIPE:
        D=D_Laminar
    else:
        D=diam_swamee(Q,hf,L,nu,e)
    return D.to_base_units()

# Applies to both laminar and turbulent flow
def diam_pipeminor(Q,he,K):
    """Returns the pipe ID that would result in the given minor losses"""
    D=(4*Q/math.pi)**(1/2)*(K/(2*u.g_0*he))**(1/4)
    return D.to_base_units()

# Applies to both laminar and turbulent flow and incorporates both minor and major losses
def diam_pipe(Q,hl,L,nu,e,K):
    """Returns the pipe ID that would result in the given total head loss"""
    if K==0:
        D=diam_pipeminor(Q,hl,K)
    else:
        D=diam_pipemajor(Q,hl,L,nu,e)
    err=1.00
    while err > 0.001:
        Dprev=D
        hfnew=hl*headloss_fric(Q,D,L,nu,e)/(headloss_fric(Q,D,L,nu,e) + headloss_exp(Q,D,K))
        D=diam_pipemajor(Q,hfnew,L,nu,e)
        err=abs(D-Dprev)/(D+Dprev)
    return D.to_base_units() 


  	
######################### Flocculation #########################

# Calculates precipitate concentration given Aluminum concentration.
def C_Prec(D: 'Dose in mg/L as Al'): 
	return Dose.to(u.mg/u.L)*1.3/0.027/13 # Changed 1.039384 to 1.3

# Function for calculation phi_0
def phi_0(Dose: 'in mg/L',Inf: 'in NTU'): 
	x = C_Prec(Dose)/r_Co + Inf.to(u.mg/u.L)/r_Cl
	return x.to(u.dimensionless) 

# Function for SA to volume ratio for clay normalized to that of a sphere
def P_ClSphere(P_HD): 
	return (0.5 + P_HD)*(2/(3*P_HD))**(2/3)

#Function to normalize surface area of clay by total surface area (clay + walls)
def P_AClATot(Inf: 'in NTU',D_Cl: 'in um',D_T: 'in inches',P_HD): 
	x = 1/(1+(2*D_Cl.to(u.m)/(3*D_T.to(u.m)*P_ClSphere(P_HD)*Inf/r_Cl)))
	return x.to(u.dimensionless)

# Function for calculating Gamma
def Gamma(Inf,D,D_T,D_Cl,P_HD,D_Co): 
	return 1 - np.exp((-phi_0(D,0*u.mg/u.L)*D_Cl)/(phi_0(0*u.mg/u.L,Inf)*D_Co)*1/np.pi*(P_AClATot(Inf,D_Cl,D_T,P_HD))/(P_ClSphere(P_HD)))

# Function to give the particle separation distance.
def D_Sep(phi,D_Cl): 
	x = (np.pi/6/phi)**(1/3)*D_Cl
	return x.to(u.micrometer)

def P_V(Gam,t,EDR,nu,phi):
	x = Gam*t*np.sqrt(EDR.to(u.m**2/u.s**3)/nu.to(u.m**2/u.s))*phi**(2/3)
	return x.to(u.dimensionless)

def P_I(Gam,t,EDR,D_Cl,phi):
	x = Gam*t*(EDR.to(u.m**2/u.s**3)/D_Cl.to(u.m)**2)**(1/3)*phi**(8/9)
	return x.to(u.dimensionless)

def pC_I(N, k):
	return 9.0/8.0*np.log10(8.0/9.0*np.pi*k*N*(6.0/np.pi)**(8.0/9.0) + 1)

def pC_V(N, k): 
	return 1.5*np.log10(2.0/3.0*np.pi*k*N*(6.0/np.pi)**(2.0/3.0) + 1)