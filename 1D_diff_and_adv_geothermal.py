import numpy as np
import matplotlib.pyplot as plt
import pandas as pd


## ------------------------------- IMPORT DATA --------------------------------##
data = pd.read_csv('geothermal_well_data.csv')

## create arrays based on columns in .csv
reinjection_rates = np.array(data.iloc[1:, 4]) ## reinjection rate of geothermal fluid in tonne/hr
temperatures = np.array(data.iloc[1:, 5]) ## reinjection temperature of geothermal fluid in *C
reservoirs = data.iloc[1:, 2].values ## type of reservoir: hot water, 2-phase low enthalpy, 2-phase medium enthalpy, 2-phase high enthalpy

def geothermal_model(reinjection_rate, temperature):
    ## Convert reinjection rate to velocity -- Q = vA or v = Q/A
    ## Q = t/hr or m3/hr -> convert to m3/s
    ## A = average are of reinjection well head (0.5m2)       
    
    velocity = float(reinjection_rate)/60/60/0.5 ## change to float for numeric operations
    
    
    ## ---------------------- INITIAL CONDITIONS ------------------------------##
    dz = 10 ## meter steps between nodes
    z = np.arange(1000, 1500, dz) ## depths 
    nodes = len(z)
    T = np.linspace(150, 250, num=nodes)  ## fills in the array with temps in *C
         
    ## ----------------------- MODEL PARAMETERS -------------------------------## 
    u = velocity  ## m/s 
    p = 1.00 ## density of geothermal fluid (g/cm3)
    cT = 4.186 ## specific heat of geothermal fluid (unit)
    D = 0.6 ## thermal conductivity of geothermal fluid
    dt = 0.1 ## time step
    
    ## -------- DEFINING VARIABLES FOR A MATRIX AND STABILITY CHECK -----------##
    s = (dt*D)/(dz**2*p*cT)
    vn = (dt*D)/(dz**2) ## von neuman coefficient for stability
    c = dt*(u/dz)
    
    """
    --------------------------- STABILITY CHECK  ------------------------------
    
    Both must be true:
    (1) Courant^2 <= 2*vn
    (2) vn + courant/4 <=0.5
    
    if stability check fails, model will not return a result
    """
    
    if c**2 > 2*vn:
        print('unstable #1:', c**2, '>', 2*s)
        return None
    if vn + c/4 > 0.5:
        print('unstable #2:', s+c/4, ">", 0.5)
        return None

    
    ## ----------- BUILDING THE 1D DIFFUSION + ADVECTION A MATRIX -------------##
    A = np.zeros((nodes, nodes))
    for i in range(2, nodes-1):
       A[i, i+1] = s-(3/8*c)
       A[i,i] = 1-(2*s)-(3/8*c)
       A[i, i-1] = s+(7/8*c)
       A[i, i-2] = -1/8*c
    A[0,0] = 1
    A[1,1] = 1
    A[-1,-1] = 1    
     
    
    ## Creates an iterative temperature variable within the function, turned into a float 
    S = float(temperature)    
   
    ## --------------------- MODELING THROUGH TIME ----------------------------##
    time = 0
    totaltime = 10 ## changing total time can result in model instability
    while time <= totaltime:
        new_T = np.dot(A, T)
        T[:] = new_T*1
        T[1:3] = S
        time += dt 
    
    return T, z

##----------------------------- PLOTTING SET UP -------------------------------##

## Initial Conditions
dzi = 10 ## meter steps between nodes
zi = np.arange(1000, 1500, dzi) ## depths 
nodesi = len(zi)
Ti = np.linspace(150, 250, num=nodesi)  ## fills in the array with temps in *C


# Plotting
fig, ax = plt.subplots(2, 2, sharex=True, sharey=True)
axs = ax.flatten()


## --------------------------- PLOT THE FUNCTION ------------------------------##

## using a for loop, which correlates each reinjection rate to its reservoir type 
for reinjection_rate, reservoir, temperature in zip(reinjection_rates, reservoirs, temperatures):
    output = geothermal_model(reinjection_rate, temperature)
    
    if output is not None:    
        T, z = output
        if reservoir == 'Hot Water':
            i = 0
        elif reservoir == "2-Phase, Low E":
            i = 1
        elif reservoir == "2-Phase, Med E": 
            i = 2
        elif reservoir == "2-Phase, High E":
            i = 3
        
        axs[i].plot(T, z, label=f'Injection Temp: {temperature}°C')
        axs[i].plot(Ti, zi, '--k')
        axs[i].set_title(f'Temperature Change - {reservoir} System')
        axs[i].set_xlabel('Temperature (°C)', fontsize = 14)
        axs[i].set_ylabel('Depth (m)', fontsize = 14)
        axs[i].invert_yaxis()
        axs[i].legend()


plt.suptitle('Impact of Reinjection Fluid on Geothermal Reservoir Temperature Change Across Multiple Reservoir Types', fontsize = 20)
plt.show()
