'''
This model iterates on my previous Week 2 Project, adding the advection portion of
a geothermal system and importing data from the literature. As water is reinjected
into a geothermal reservoir, how does the temperature gradient change? I found data
from the literature to import into this model to investigate two variables:
reinjection rate and reinjection temperature. 

Data from Rivera Diaz, Alexandre, Eylem Kaya, and Sadiq J. Zarrouk. “Reinjection in 
Geothermal Fields − A Worldwide Review Update.” Renewable and Sustainable Energy Reviews 
53 (January 1, 2016): 105–62. https://doi.org/10.1016/j.rser.2015.07.151

'''


import numpy as np
import matplotlib.pyplot as plt
import pandas as pd


## ------------------------------- IMPORT DATA --------------------------------##
data = pd.read_csv('geothermal_well_data.csv')

## create arrays based on columns in .csv
reinjection_rates = np.array(data.iloc[1:, 4]) ## reinjection rate of geothermal fluid in tonne/hr
temperatures = np.array(data.iloc[1:, 5]) ## reinjection temperature of geothermal fluid in *C
reservoirs = data.iloc[1:, 2].values ## type of reservoir: hot water, 2-phase low enthalpy, 2-phase medium enthalpy, 2-phase high enthalpy


'''
This model utilizes a function that will change the value for reinjection rate,
pulled from the above .csv, and later on add in injection temperature. Since the 
review I pulled the data from did not report thermal conductivity, depth of injection,
thermal gradient of the reservoir, or density of geothermal fluid, I have opted to keep
those constant for all of the model. Future work could focus on discerning these parameters
and updating the model with them.
That being said, small tweaks in this model could result in instability - for example,
changing the dt or dz steps. If this occurs, then reset the model to the preset options.
'''

def geothermal_model(reinjection_rate):
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
     
    
    ## Supply variable pulls a reinjection temperature from its position relative to reinjection rate
    S = temperatures[reinjection_rates==reinjection_rate]     
   
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

## Reintroduce Initial Conditions to Plot
dzi = 10
zi = np.arange(1000, 1500, dzi)
nodesi = len(zi)
Ti = np.linspace(150, 250, num=nodesi)

fig, ax = plt.subplots(1,1, figsize=(10,8))
ax.plot(Ti, zi, "--", c='b', label = 'Geothermal Gradient', lw=2)

## Changing colors 
labels = np.unique(reservoirs)
colors = dict(zip(labels, plt.cm.magma(np.linspace(0, 1, len(labels)))))

## --------------------------- PLOT THE FUNCTION ------------------------------##

## using a for loop, which correlates each reinjection rate to its reservoir type 
for reinjection_rate, reservoirs in zip(reinjection_rates, reservoirs):
    output = geothermal_model(reinjection_rate)
    
    if output is not None: ## references stability check
        T, z = output
        reservoir_color = colors[reservoirs]
        ax.plot(T, z, label =f'{reservoirs}', color=reservoir_color)
        
        
ax.set_title('Temperature Change with Different Velocities',fontsize=20)
ax.set_xlabel('Temperature (°C)', fontsize=14)
ax.set_ylabel('Depth (m)', fontsize=14)
ax.set_ylim(ax.get_ylim()[::-1])
ax.legend()
plt.show()