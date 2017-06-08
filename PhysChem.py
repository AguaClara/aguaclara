# This file contains unit process functions pertaining to the design of physical/chemical unit processes for AguaClara water treatment plants.

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
	
######################### Flocculation #########################

# Function for calculating precipitate concentration
def C_Prec(Dose: 'in mg/L'): 
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

