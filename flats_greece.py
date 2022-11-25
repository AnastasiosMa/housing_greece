#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 26 00:20:22 2022

@author: anmavrol
"""
import pandas as pd
import numpy as np
import os
from sklearn.preprocessing import OneHotEncoder, StandardScaler, MinMaxScaler
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import seaborn as sns
import ptitprince as pt
import sys

os.chdir('/Users/anmavrol/Documents/projects/Flats_Greece')
 
data = pd.read_excel('Greece_flats_data.xlsx')

#data = data.drop(labels=[0,2,3,5], axis=0) #delete high outliers

xNum = data[['Size','Floor','Construction Year','Bathrooms','Bedrooms']]
#scaler = StandardScaler()
#scaler.fit(xNum)
#xNum = scaler.transform(xNum)

cat_vars = "subArea","Katastasi","Energy class", "Heating", "Dapedo", "Koufomata"
enc = OneHotEncoder(handle_unknown='ignore')
xCat=enc.fit_transform(data[["Katastasi"]]).toarray()

x = np.hstack([xCat, xNum])
#scaler = MinMaxScaler()
#scaler.fit(x)
#x = scaler.transform(x)
y = data[['Price']]
#scaler.fit(y)
#y = scaler.transform(y)

reg = LinearRegression().fit(x,y)
reg.score(x,y)

reg.coef_

#get residuals
x_pred = reg.predict(x)
residual = (y-x_pred)

#mean residual value
residual.abs().mean()

houses = [[1,0,0,0,43,2,1979,1,1],[0,0,1,0,45,0,1972,1,1],[1,0,0,0,45,0,1972,1,1]]
houses_pred = reg.predict(houses)
#%%Plots
# make a folder for plots
if not os.path.exists('Plots'):
 os.makedirs('Plots')
 
plt.rcParams["figure.figsize"] = [7, 5]
plt.rcParams["figure.autolayout"] = True

#pt.RainCloud(y='Price',data=data,palette='Set2', bw=.2, width_viol=.6, move=.2,\
 #             ax=ax,orient='h', point_size=.35,box_showfliers = False)
fig1,ax = plt.subplots(figsize=(7, 5))
pt.RainCloud(y='Price',data=data,palette='Set2', orient = 'h',bw=.2, width_viol=.6, move=.2,\
             ax = ax,point_size=3,box_showfliers = False)
plt.title('Τιμή (σε χιλιάδες) όλων των ακινήτων στην βάση δεδομένων')
plt.xlabel('Τιμή (σε χιλιάδες)')

fig2,ax = plt.subplots(figsize=(7, 5))
pt.RainCloud(y='Size',data=data,palette='Set2', orient = 'h',bw=.2, width_viol=.6, move=.2,\
             ax = ax,point_size=3,box_showfliers = False)
plt.title('Τετραγωνικά όλων των ακινήτων στην βάση δεδομένων')
plt.xlabel('Τετραγωνικά')

fig3,ax = plt.subplots(figsize=(7, 5))
pt.RainCloud(y='Construction Year',data=data,palette='Set2', orient = 'h',bw=.2, width_viol=.6, move=.2,\
             ax = ax,point_size=3,box_showfliers = False)
plt.title('Έτος κατασκευής όλων των ακινήτων στην βάση δεδομένων')
plt.xlabel('Έτος κατασκευής')

fig4,ax = plt.subplots(figsize=(7, 5), dpi=300)
pt.RainCloud(x='Katastasi',y='Price',data=data,palette='Set2', orient = 'h',bw=.2, width_viol=2, move=.2,\
             ax = ax,point_size=3,box_showfliers = False)
plt.title('Τιμή (σε χιλιάδες) σε σχέση με την κατάσταση')
plt.xlabel('Τιμή (σε χιλιάδες)')

fig5 = plt.subplots()
sns.scatterplot(data=data,x='Size',y='Price',hue='Katastasi')
plt.title('Σχέση τιμής και τετραγωνικών')
plt.ylabel('Τιμή (σε χιλιάδες)')
plt.xlabel('Τετραγωνικά')

fig6 = plt.subplots()
sns.scatterplot(data=data,x='Construction Year',y='Price',hue='Katastasi')
plt.title('Σχέση τιμής και Έτους κατασκευής')
plt.ylabel('Τιμή (σε χιλιάδες)')
plt.xlabel('Έτος κατασκευής')

def save_multi_image(filename):
    pp = PdfPages(filename)
    fig_nums = plt.get_fignums()
    figs = [plt.figure(n) for n in fig_nums]
    for fig in figs:
        fig.savefig(pp, format='pdf')
    pp.close()

filename = "Γραφήματα.pdf"
save_multi_image(filename)

#https://oleheggli.medium.com/easily-analyse-audio-features-from-spotify-playlists-part-3-ec00a55e87e4

#%%Printing messages
original_stdout = sys.stdout
with open('Αποτελέσματα.txt','w') as f:
    sys.stdout=f
    print('Αριθμός σπιτιών στην βάση δεδομένων: {}'.format(len(xNum)))
    
    print('Επιτυχία πρόβλεψης μοντέλου: {}%'.format(round(reg.score(x,y)*100,2)))
    print('Προβλεπώμενη τιμή πώλησης')
    print('Πρωτοπαπαδάκη: {}€ \nΧρ. Σμύρνης: {}€'.format(float(houses_pred[0].round(3)),float(houses_pred[1].round(3))))
    print('Σχέση μεταξύ σπιτιών: {}%'.format(float((houses_pred[1]/houses_pred[0]*100).round(1))))
    sys.stdout=original_stdout
#%%Renting
#ENFIA
#ΕΝΦΙΑ = (τ.μ. συνολικής επιφάνειας κύριων χώρων) x (Βασικος φορος:τιμη ζωνης) x (Συντελεστης Παλαιτητας) x 
#[(Συντελεστης Οροφου) ή (Μονοκατοικιας)] x (Συντελεστης προσοψης) x (ΣΒΧ αν υπάρχουν) x (ΣΗΚ αν υπάρχουν)
timiZonisMoschato = 1950
timiZonisRenti = 1250
vfRenti = 2
vfMoschato = 2.8
tetragwnikaSpitiwn = [42.6+13.7,45,86]
enfiaProtopap = vfRenti*56.3
enfiaSmirnis = vfRenti*45*0.98
enfiaMoschato = vfMoschato*86

rent = [350,250]
TAPP = 5* (42.6+13)
TAPS = 5* (45)
#Τέλη ακίνητης περιουσίας(5€ * τετραγωνικά)
KatharaP = round((rent[0]*11-enfiaProtopap) - ((rent[0]*12)-rent[0]*12/20)*0.15,2)
KatharaS = round((rent[1]*11-enfiaSmirnis) - ((rent[1]*12)-rent[1]*12/20)*0.15,2)
aposvesiP = round(int(houses_pred[0]*1000)/(KatharaP),2)
aposvesiS = round(int(houses_pred[1]*1000)/(KatharaS),2)
rent[0] * 11 *0.15 
FEAS = rent[1] * 11 *0.15 
with open('Αποτελέσματα.txt','a') as f:
    sys.stdout=f
    print('')
    print('ΝΟΙΚΙ και απόσβεση σε σχέση με τιμή πώλησης')
    print('Νοίκι Πρωτοπαπαδάκη: {}€\nΝοίκι Χρ. Σμύρνης: {}€'.format(rent[0],rent[1]))
    print('Φόροι = Φόρος εκμίσθωσης ακινήτου(15%) + ΕΝΦΙΑ')
    print('Η φοροαπαλλαγή για εξοδα σπιτιού π.χ. ανακαίνισης είναι 5% χωρίς δικαιολογητικά')
    print('ΕΝΦΙΑ Πρωτοπαπαδάκη: {}€\nΕΝΦΙΑ Χρ. Σμύρνης: {}€'.format(enfiaProtopap,enfiaSmirnis))
    print('Υποθέτοντας ότι ένα νοίκι τον μήνα πάει για έξοδα συντήρησης σπιτιού: \n'\
      'Καθαρά Ετήσια έσοδα Νοικιού = Μηνιαίο νοίκι * 11 - Φόροι + Φοροαπαλλαγή')
    print('Καθαρά Ετήσια Έσοδα:')
    print('Πρωτοπαπαδάκη: {}€\nΧρ. Σμύρνης: {}€'.format(KatharaP,\
                                                                KatharaS))
    print('')    
    print('Χρόνια απόσβεσης της τιμής πώλησης')
    print('Πρωτοπαπαδάκη: {} Χρόνια {}%\nΧρ. Σμύρνης: {} Χρόνια {}%'.format(aposvesiP,houses_pred[0]/aposvesiP, \
                                                                           aposvesiS, houses_pred[1]/aposvesiS))
    sys.stdout=original_stdout
