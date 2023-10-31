#%% Load appropriate libraries and (visually) inspect data
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

url = "https://docs.google.com/spreadsheets/d/1I1s3XwAGz_jYa7JMFvpfeENETm40rhRi/edit?usp=sharing&ouid=115663395387832444860&rtpof=true&sd=true"
output = "assignment2_data_2023.xlsx"

#print("Previous working directoruy was: ", os.getcwd())
#os.chdir(r'C:\Users\nikol\OneDrive - Danmarks Tekniske Universitet\Desktop\python')
#print("This was changed to: ", os.getcwd())

df = pd.read_excel('assignment2_data_2023.xlsx')

t = df['Time (h)']
C = df['Consumption']
P = df['Production']

sns.set_theme(style='whitegrid')
sns.set_color_codes('deep')
plt.figure(figsize=(10, 4), dpi=80)
sns.lineplot(x='Time (h)', y='Consumption', data=df,
                estimator=None, sort=False, linestyle='-', color='red', label='Consumption')
sns.lineplot(x='Time (h)', y='Production', data=df, linestyle='-',
             color='black', label='Production')
#plt.scatter(x=0, y=0, c='r', marker='o', linewidth=5, label='Leading edge')
#plt.scatter(x=100, y=0, c='r', marker='^', linewidth=5, label='Trailing edge')
plt.xlabel('Time of day [h]', fontsize=10)
plt.ylabel('Power [MW]', fontsize=10)
plt.title('Daily electricity generation and consumption', fontsize=15)
plt.legend(loc='best', fontsize=8.5)

'''plt.fill_between(t, C, P, color='green', where = (P >= C),
                 alpha=0.25)
plt.fill_between(t, C, P, color='red', where = (P < C),
                 alpha=0.25)
'''
'''
plt.fill_between(t[0:2], C[0:2], P[0:2], alpha=0.25, color='green')
plt.fill_between(t[1:10], C[1:10], P[1:10], alpha=0.25, color='red')
plt.fill_between(t[9:18], C[9:18], P[9:18], alpha=0.25, color='green')
plt.fill_between(t[17:20], C[17:20], P[17:20], alpha=0.25, color='red')
plt.fill_between(t[19:24], C[19:24], P[19:24], alpha=0.25, color='green')
'''

plt.show()

#%%Task 1a
P_tot = sum(P)
C_tot = sum(C)
print("Task 1a:")
print("Total daily energy surplus is: %.0f MWh" % (P_tot-C_tot))
print("This corresponds to %.1f%%  of the daily consumption" % ( (P_tot-C_tot)/C_tot*100 ) )

#1/2*(124-53)*(18-9) compare this to sum(P[9:18]-C[9:18]). It's the same, right?
#%% Task 1b
#The total energy that should be stored in the sum of the hourly deficits of energy throughout
#the day, without counting the hours with surplus.
ES_nonRenew = sum(C[i]-P[i] for i in t if C[i]>P[i])
print("\nTask 1b:")
print("The total amount of energy that is currently not being supplied by renewable sources is %.0f MWh" % (ES_nonRenew))

#%%Task 1c
#The maximum energy storage (ignoring efficiencies) that the ES solutoins should provide
#is given by the largest deficit computed by summing the P,C difference througout the day:
def ES_reqf(P, C):
    deficit = [0 for i in range(len(P))]
    deficit[0] = C[0] - P[0] #calculating whether we have a deficit at hour 0
    if  deficit[0] < 0:
        deficit[0] = 0 #if we do not have a deficit, then we should not count C[0]-P[0] as this energy surplus is NOT stored
    for i in range(1,len(P)):
        deficit[i] =  deficit[i-1] + C[i] - P[i] #the energy not provided by renewables in the first i hours
        if  deficit[i] < 0:
             deficit[i] = 0
    return max(deficit), deficit

ES_req, ES_req_t = ES_reqf(P=P,C=C) #Energy storage required
print("\nTask 1c:")
print("The maximum ENERGY that the energy storage solutions should provide is: %.0f MWh" % ES_req)
print("The maximum POWER that the energy storage solutions should provide is: %.1f MW" % max(C-P))

'''
for i in range(len(P)):
    if C[i] > P[i]:
        print("Hour: ", i)
sum(C[i]-P[i] for i in range(1,len(P)) if C[i] > P[i]) - sum(C[17:19] - P[17:19]) #so the above function corresponds to this calculation
'''

#%%Task 2a
#Energy capacity of the gravity ES (GES) ignoring its height.
z = 1000 #m
m = 12*10**6 #kg
g = 9.81 #N/kg
PE_J = m*g*z
#1 J = 1/3600 Wh, so 1 J = 1/(3.6*10^3*10^6)=1/(3.6*10^9) MWh
PE = PE_J / (3.6*10**9)
print("\n##############################################################################")
print("\nTask 2a:")
#1 J = 1/3600 Wh, so 1 J = 1/(3.6*10^3*10^6)=1/(3.6*10^9) MWh
print("The energy that can technically be stored in the GES is the PE of it: %.1f MWh" % (PE))
eta_dch = 0.95
print("The useful amount of energy needs to take into account the discharging efficiency of the GES: %.1f MWh\nThis is not nearly enough by itself." % (PE*eta_dch))
print("The maximum power output of %.0f MW is also too little." % 20)

#%%Task 2b
#Energy required to charge the GES
eta_ch = 0.95 #charging (and discharging efficiency of the GES)
print("\nTask 2b")
print("Energy required to charge the GES is %.1f MWh, whilst only getting %.1f MWh" % ( (PE/eta_ch), (PE*eta_dch) ))

#%% Task 2c
#Roundtrip efficiency of the thermal energy storage (TES)
print("\nTask 2c")
eta_th_TES = 0.96 #ch/dch of Carnot battery, so the electricity used to produce 0.96 MWh of heat is 1.0 MWh. And you get 0.92 MWh out again.

#Carnot efficiency is given by: eta_Carnot = 1-Tc/Th, slide 11 brush-up ThDyn2
#2nd law efficiency is given by: eta_2nd = eta_cycle/eta_Carnot, slide 12 brush-up ThDyn2
T_c = 288 #K 15 C
T_h = 873 #K 600 C
eta_2nd = 0.70 #70% 2nd law efficiency
eta_Carnot = 1 - T_c/T_h

eta_cycle = eta_2nd * eta_Carnot
print("The cycle efficiency of the heat engine is %.1f%%" % (100*eta_cycle))
roundtrip = eta_th_TES**2 * eta_cycle
print("Given the charging/discharging efficiency of %.0f%%, the roundtrip effiency of the entire TES is: %.1f%%" % ( (100*eta_th_TES),(100*roundtrip) ))
print("\nWe have assumed no other losses than the charging and discharging efficiency of the TES and the cycle efficiency of the heat engine.")

#%% Task 3a
#Consumption, production and SOCs for the two storage options.
print("\n##############################################################################")
print("\nTask 3a: See plot.\n")

#%%GES, TES test

#init GES
P_cap_GES=20
eta_in_GES=eta_ch
eta_out_GES=eta_dch
SOC_GES = [0 for i in range(len(P))] 
SOC_GES[0] = PE

#init TES
eta_in_TES=eta_th_TES
eta_out_TES=eta_th_TES*eta_cycle
TES_req=(ES_req - PE*eta_out_GES)/eta_out_TES
P_cap_TES = max(max(C-P)/eta_out_TES,max(P-C)*eta_in_TES) #1st is max P_cap for TES if this is for discharging, the 2nd is for if the limit is required during charging
eta_in=eta_th_TES
eta_out=eta_th_TES*eta_cycle
SOC_TES = [0 for i in range(len(P))] 
SOC_TES[0] = TES_req

for i in range(1,len(P)):
    
    if P[i] < C[i]:#DIScharge    
        if SOC_GES[i-1] > (C[i] - P[i]) / eta_out_GES: #GES can supply sufficient energy
            if P_cap_GES >= (C[i] - P[i]) / eta_out_GES: #ignore for now is 20 MW is before or after discharging efficiency!!
                SOC_GES[i] = SOC_GES[i-1] + (P[i] - C[i]) / eta_out_GES
                SOC_TES[i] = SOC_TES[i-1] #GES is sufficient and SOC_TES remains at the same SOC
            else:
                SOC_GES[i] = SOC_GES[i-1] - P_cap_GES
        
        else: #GES cannot supply sufficient energy
            SOC_GES[i] = 0
        #now we make use of the TES. Note that this should only be activated if GES did not satisfy demand!
        TES_req_temp = SOC_GES[i-1] - SOC_GES[i]
        if TES_req_temp != (C[i] - P[i]) / eta_out_GES:
            if SOC_TES[i-1] > (C[i] - (P[i] + TES_req_temp*eta_out_GES) ) / eta_out_TES: #GES can supply sufficient energy
                if P_cap_TES >= (C[i] - (P[i] + TES_req_temp*eta_out_GES) ) / eta_out_TES:
                    SOC_TES[i] = SOC_TES[i-1] + (P[i] + TES_req_temp*eta_out_GES - C[i]) / eta_out_TES
                    
                else:
                    SOC_TES[i] = SOC_TES[i-1] - P_cap_TES
            
            else: #GES cannot supply sufficient energy
                SOC_TES[i] = 0
            
            
    elif P[i] > C[i]: #charge
        if SOC_GES[i-1] < PE: #If GES is not fully charged, then it can be charged
            if P_cap_GES >= (P[i] - C[i])*eta_in_GES:
                SOC_GES[i] = SOC_GES[i-1] + (P[i] - C[i]) * eta_in_GES
            else:
                SOC_GES[i] = SOC_GES[i-1] + P_cap_GES
            if SOC_GES[i] > PE: #if the battery is supposedly charged more than to it max capacity. Remove any excess stored energy.
                SOC_GES[i] = PE
        else:    #if the battery is fully charged but more power is available due to overproduction.
            SOC_GES[i] = SOC_GES[i-1]
        #we charge the TES if any energy is left after charging the GES
        TES_surplus_temp = SOC_GES[i-1] - SOC_GES[i]
        if TES_surplus_temp != (P[i] - C[i]) * eta_in_GES:
            if SOC_TES[i-1] < TES_req: #If GES is not fully charged, then it can be charged
                if P_cap_TES >= (P[i] + TES_surplus_temp/eta_in_GES - C[i])*eta_in_TES:
                    SOC_TES[i] = SOC_TES[i-1] + (P[i] + TES_surplus_temp/eta_in_GES - C[i]) * eta_in_TES
                else:
                    SOC_TES[i] = SOC_TES[i-1] + P_cap_TES
                if SOC_TES[i] > TES_req: #if the battery is supposedly charged more than to it max capacity. Remove any excess stored energy.
                    SOC_TES[i] = TES_req
            else:    #if the battery is fully charged but more power is available due to overproduction.
                SOC_TES[i] = SOC_TES[i-1]
    else: #if consumption and production is completely balanced    
        SOC_GES[i] = SOC_GES[i-1]
        SOC_TES[i] = SOC_TES[i-1]

#%%plots for Task 3a

df['SOC_GES'] = SOC_GES
df['SOC_TES'] = SOC_TES

#df['TES+Prod']=df['SOC_TES']
#df['TES+Prod'][0]=df['SOC_TES'][len(P)-1] + df['Production'][0]
#df['TES+Prod'][1:len(P)]=[ df['SOC_TES'][i-1] + df['Production'][i] for i in range(1,len(P)) ]

plt.figure(0, dpi=400)
font_tnr = {'fontname' : 'Neo Sans Pro'}


sns.lineplot(x='Time (h)', y='Consumption', data=df,
                estimator=None, sort=False, linestyle='-', color='red', label='Consumption')
sns.lineplot(x='Time (h)', y='Production', data=df, linestyle='-',
             color='black', label='Production')
sns.lineplot(x='Time (h)', y='SOC_GES', data=df, linestyle='-',
             color='blue', label='SOC$_{\mathbf{G}ES}$')
sns.lineplot(x='Time (h)', y='SOC_TES', data=df, linestyle='-',
             color='orange', label='SOC$_{\mathbf{T}ES}$')
#sns.lineplot(x='Time (h)', y='TES+Prod', data=df, linestyle='-',
#             color='green', label='TES+Prod')
#plt.scatter(x=0, y=0, c='r', marker='o', linewidth=5, label='Leading edge')
#plt.scatter(x=100, y=0, c='r', marker='^', linewidth=5, label='Trailing edge')
plt.xlabel('Time of day [h]', **font_tnr, fontsize=10)
plt.ylabel('Power [MWh, MW]', **font_tnr, fontsize=10)
plt.title('Daily electricity generation & consumption and SOCs in MWh', **font_tnr, fontsize=12)
plt.legend(loc='best', fontsize=8.5)

plt.show()

#checking the power capacity needed for the SOCs above. This is simply the largest difference in SOC between any two hours.
def P_SOC(SOC_T):
    P_SOC = [0 for i in range(len(SOC_T))]
    for i in range(1,len(P_SOC)):
        P_SOC[i] = SOC_T[i] - SOC_T[i-1]
    return max(P_SOC), P_SOC
    
P_SOC_GES, P_SOC_GES_t = P_SOC(SOC_GES)
P_SOC_TES, P_SOC_TES_t = P_SOC(SOC_TES)
print("\nPower capaties of the two systems are:\nGES: %.1f MW\nTES: %.1f MW" % (P_SOC_GES,P_SOC_TES))

#%% SOC in %'s
df['SOC_GES_perc'] = df['SOC_GES'] / PE * 100
df['SOC_TES_perc'] = df['SOC_TES'] / TES_req * 100
plt.figure(2, dpi=400)
ax=sns.lineplot(x='Time (h)', y='Consumption', data=df,
                estimator=None, sort=False, linestyle='-', color='red', label='Consumption',
                legend=False)
sns.lineplot(x='Time (h)', y='Production', data=df, ax=ax, linestyle='-',
             color='black', label='Production', legend=False)
plt.grid(None)

ax2=ax.twinx()
#plt.grid(None)

sns.lineplot(x='Time (h)', y='SOC_GES_perc', data=df, ax=ax2, linestyle='-',
             color='blue', label='SOC$_{\mathbf{G}ES}$', legend=False)
sns.lineplot(x='Time (h)', y='SOC_TES_perc', data=df, ax=ax2, linestyle='-',
             color='orange', label='SOC$_{\mathbf{T}ES}$', legend=False)
#sns.lineplot(x='Time (h)', y='TES+Prod', data=df, linestyle='-',
#             color='green', label='TES+Prod')
#plt.scatter(x=0, y=0, c='r', marker='o', linewidth=5, label='Leading edge')
#plt.scatter(x=100, y=0, c='r', marker='^', linewidth=5, label='Trailing edge')
ax.set_xlabel('Time of day [h]', **font_tnr, fontsize=10)
ax.set_ylabel('Power [MWh, MW]', **font_tnr, fontsize=10)
ax2.set_ylabel('SOC [%]', **font_tnr, fontsize=10)
plt.title('Daily electricity generation & consumption and SOCs', **font_tnr, fontsize=12)
ax.figure.legend(loc='lower right', fontsize=8.5)
plt.show()

#%% Task 3b
#What should the capacity of the TES be to store enough energy to provide electricity to the grid during this period?
print("\nThe TES should have a capacity of %.1f MWh. Taking into account its discharging and heat engine efficiency of %.1f%%" % (ES_req-PE*eta_dch, eta_cycle*eta_th_TES*100))
print("This yields a total required capacity of: %.1f MWh for the TES." % TES_req )
print("\nA total of %.1f MWh is required to fully charge it." % (TES_req/eta_in_TES)) #equivalent to: (ES_req-PE*eta_out_GES)/roundtrip









