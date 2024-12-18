# Research Question

## This model iterates on my previous Week 2 Project, adding the advection portion of a geothermal system and importing data from the literature. As water is reinjected into a geothermal reservoir, how does the temperature gradient change? I found data from the literature to import into this model to investigate two variables: reinjection rate and reinjection temperature. 

# What Does this Model Do?
## This model utilizes a function that will change the value for reinjection rate, pulled from the .csv, and later on add in injection temperature. Since the review I pulled the data from did not report thermal conductivity, depth of injection, thermal gradient of the reservoir, or density of geothermal fluid, I have opted to keep those constant for all of the model. Future work could focus on discerning these parameters and updating the model with them. 

# The Output
![image](https://github.com/user-attachments/assets/832fc4ac-60a6-48d0-8e99-4e2cd611f1ed)

## Above is an example using the literature data for an output of the model. Shown are the four types of geothermal reservoir (Hot Water, 2-Phase Low Enthalpy, 2-Phase Medium Enthalpy, and 2-Phase High Enthalpy) reviewed by Rivera Diaz et al. (2016). These were modeled using provided reinjection rates and reinjection temperatures, standardized to a mock geothermal system.


## Source
### Data from Rivera Diaz, Alexandre, Eylem Kaya, and Sadiq J. Zarrouk. “Reinjection in Geothermal Fields − A Worldwide Review Update.” Renewable and Sustainable Energy Reviews 53 (January 1, 2016): 105–62. https://doi.org/10.1016/j.rser.2015.07.151


