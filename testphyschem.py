# -*- coding: utf-8 -*-
"""
Created on Thu Jun 15 14:07:28 2017

@author: kn348
"""

# This file contains unit process functions pertaining to the design of physical/chemical unit processes for AguaClara water treatment plants.

######################### Imports #########################
import math
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
        Q=ratio_VC_orifice*area_circle(D)*(2*u.g_0*h)**1/2
    else:
         Q=0
    return Q.to(u.L/u.s)

def flow_orifice_vert(D,h,ratio_VC_orifice):
    """Returns the vertical flow rate of orifice"""
    if h>-D/2:
        Q=ratio_VC_orifice*((2*u.g_0)**1/2)*scipy.integrate.quad(lambda z: D*math.sin(math.acos(z/(D/2)))*((h-z)**1/2),-D/2,min(D/2,h))
    else:
        Q=0
    return Q.to(u.m)