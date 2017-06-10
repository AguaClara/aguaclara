# This file contains unit process functions pertaining to the design of physical/chemical unit processes for AguaClara water treatment plants.

######################### Imports #########################
import math

from AguaClara_design.units import unit_registry as u


#######################Simple geometry#######################

#A few equations for useful geometry
# Is there a geometry package that we should be using?

def A_Circle(D_Circle:'Diameter of Circle'):
    return math.pi/4*D_Circle**2

def D_Circle(A_Circle):
    return (4*A_Circle/math.pi)**(1/2)

######################### Hydraulics ######################### 

def Re_pipe(Q,D,nu):
    Re=(4*Q)/(math.pi*D*nu)
    return Re.to(u.dimensionless)
# The .to part forces Re to be dimensionless

Re_TRANSITION_PIPE=2100

# Returns the friction factor for pipe flow for both laminar and turbulent flows
def f(Q,D,nu,e):
    if Re_pipe(Q,D,nu)>=Re_TRANSITION_PIPE:
        f=0.25/(math.log10(e/(3.7*D)+5.74/Re_pipe(Q,D,nu)**0.9))**2
    else:
        f=64/Re_pipe(Q,D,nu)
    return f*u.dimensionless

# Returns the major pipe head loss (due to wall shear) for both laminar and turbulent flows.
def HLf(Q,D,L,nu,e):
    HLf=f(Q,D,nu,e)*8/(u.g_0*math.pi**2)*(L*Q**2)/D**5
    return HLf.to(u.m)

# Returns the minor head loss (due to expansions). This equation applies to both laminar and turbulent flows.
def HLe(Q,D,K):
    HLe=K*8/(u.g_0*math.pi**2)*(Q**2)/(D**4)
    return HLe.to(u.m)

# Returns the total head loss due to major and minor losses. This equation applies to both laminar and turbulent flows.
def HL(Q,D,L,nu,e,K):
    HL=HLf(Q,D,L,nu,e)+HLe(Q,D,K)
    return HL.to(u.m)

def D_Hagen(Q,hf,L,nu):
    D=((128*nu*Q*L)/(u.g_0*hf*math.pi))**(1/4)
    return D.to_base_units()

# The Swamee Jain equation (below) is dimensionally correct and returns the inner diameter of a pipe 
# given the flow rate and the head loss due to shear on the pipe walls.
# The Swamee Jain equation does NOT take minor losses into account.
# This equation ONLY applies to turbulent flow.
# Pint has trouble adding two numbers that are raised to the 25th power. 
# The following code strips the units before adding the two terms and then reattaches the units.
def D_Swamee(Q,hf,L,nu,e):
    a=((e**1.25)*((L*(Q**2))/(u.g_0*hf))**4.75).to_base_units().magnitude
    b=(nu*(Q**9.4)*(L/(u.g_0*hf))**5.2).to_base_units().magnitude
    D=(0.66*(a+b)**0.04)*u.m
    return D.to_base_units()

# Returns the pipe ID that would result in given major losses
# Applies to both laminar and turbulent flow
def D_PipeMajor(Q,hf,L,nu,e):
    D_Laminar= D_Hagen(Q,hf,L,nu)
    if Re_pipe(Q,D_Laminar,nu)<=Re_TRANSITION_PIPE:
        D=D_Laminar
    else:
        D=D_Swamee(Q,hf,L,nu,e)
    return D.to_base_units()

# Returns the pipe ID that would result in the given minor losses
# Applies to both laminar and turbulent flow
def D_PipeMinor(Q,he,K):
    D=(4*Q/math.pi)**(1/2)*(K/(2*u.g_0*he))**(1/4)
    return D.to_base_units()

# Returns the pipe ID that would result in the given total head loss
# Applies to both laminar and turbulent flow and incorporates both minor and major losses
def D_Pipe(Q,hl,L,nu,e,K):
    if K==0:
        D=D_PipeMinor(Q,hl,K)
    else:
        D=D_PipeMajor(Q,hl,L,nu,e)
    err=1.00
    while err > 0.001:
        Dprev=D
        hfnew=hl*HLf(Q,D,L,nu,e)/(HLf(Q,D,L,nu,e) + HLe(Q,D,K))
        D=D_PipeMajor(Q,hfnew,L,nu,e)
        err=abs(D-Dprev)/(D+Dprev)
    return D.to_base_units() 

# Here we define functions that return the flow rate.

# Returns the flow rate for the transition between laminar and turbulent.
# This equation is used in some of the other equations for flow.
def Q_Transition(D,nu):
    return (math.pi*D*Re_TRANSITION_PIPE*nu/4).to(u.L/u.s)

# Flow rate for laminar flow with only major losses
def Q_Hagen(D,hf,L,nu):
    return ((math.pi*D**4)/(128*nu)*u.g_0*hf/L).to(u.L/u.s)

# Flow rate for turbulent flow with only major losses
def Q_Swamee(D,hf,L,nu,e):
    logterm=-math.log10(e/(3.7*D)+2.51*nu*(L/(2*u.g_0*hf*D**3))**(1/2))
    return ((math.pi/2**(1/2))*D**(5/2)*(u.g_0*hf/L)**(1/2)*logterm).to(u.L/u.s)

# Flow rate for turbulent or laminar flow with only major losses
def Q_PipeMajor(D,hf,L,nu,e):
    Q_H=Q_Hagen(D,hf,L,nu)
    if Q_H<Q_Transition(D,nu):
        Q=Q_H
    else:
        Q=Q_Swamee(D,hf,L,nu,e)
    return Q.to(u.L/u.s)

# Flow rate for turbulent or laminar flow with only minor losses
def Q_PipeMinor(D,he,K):
    return (A_Circle(D)*(2*u.g_0*he/K)**(1/2)).to(u.L/u.s)

# Now we put all of the flow equations together and calculate the flow in a 
# straight pipe that has both major and minor losses and might be either
# laminar or turbulent.
def Q_Pipe(D,hl,L,nu,e,K):
    if K==0:
        Q=Q_PipeMajor(D,hl,L,nu,e)
    else:
        Qprev=0*u.L/u.s
        err=1
        Q=min(Q_PipeMajor(D,hl,L,nu,e),Q_PipeMinor(D,hl,K))
        while err>0.01:
            Qprev=Q
            hfnew=hl*HLf(Q,D,L,nu,e)/(HLf(Q,D,L,nu,e)+HLe(Q,D,K))
            Q=Q_PipeMajor(D,hfnew,L,nu,e)
            if Q==0*u.L/u.s:
                err=0
            else:
                err=abs(Q-Qprev)/(Q+Qprev)
    return Q.to(u.L/u.s)  	
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

