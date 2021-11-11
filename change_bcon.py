#!/bin/python

# The *BCON.yyyymmdd.nc* files are formed by *mozart2camx.26feb19.tgz* from : 
# https://www.camx.com/download/support-software/
#  
# This python script is used to change the trpospheric ozone value over the sea. 
# The computational domain can be found in *namelist.wps* .
# 

import xarray as xr
import pandas as pd

datedate=pd.date_range(start = '20190326',end='20190406',freq='d')
all_date=datedate.strftime('%Y%m%d')

sea_ice=3/1000
sea=10/1000
coastal=15/1000

for dateinput in all_date:
	print('>> For: ',dateinput)
	bc_file='./BCON.'+dateinput+'.nc'
	dataset=xr.open_dataset(bc_file)
	# reduce when its Free Air from 30 Mar 
	if ((dateinput != '20190328')and(dateinput != '20190329')):
		dataset.O3.values[:,3:7,:]=dataset.O3.values[:,3:7,:]*0.5
	if (dateinput=='20190328'):
		dataset.O3.values[:,3:7,433:634]=dataset.O3.values[:,3:7,433:634]*0.2  # Arctic Sea
		dataset.O3.values[:,:4,723:781]=sea_ice  # Chukotka Peninsula
		dataset.O3.values[:,3:7,700:740]=sea    # South bank of Chukotka Peninsula
		dataset.O3.values[:,3:7,770:]=sea    # North bank of Chukotka Peninsula and East Siberian Sea
		dataset.O3.values[:,:4,658:690]=dataset.O3.values[:,:4,658:690]*0.4
	if (dateinput=='20190329'):
		dataset.O3.values[:,:7,710:]=dataset.O3.values[:,:7,710:]*0.35
	# reduce when its sea ice (bcon) in the BL
	dataset.O3.values[:,:4,38:42]=sea_ice
	dataset.O3.values[:,:4,54:56]=sea_ice
	dataset.O3.values[:,:4,205:213]=sea_ice
	dataset.O3.values[:,:4,355:374]=sea_ice
	dataset.O3.values[:,:4,408:422]=sea_ice
	dataset.O3.values[:,:4,433:634]=sea_ice
	dataset.O3.values[:,:4,691:723]=sea_ice
	dataset.O3.values[:,:4,781:]=sea_ice
	# reduce when its sea (bcon) in the BL
	dataset.O3.values[:,:4,0:58]=sea
	dataset.O3.values[:,:4,658:690]=sea
	dataset.O3.values[:,:4,375:407]=sea  # Banks Island
	dataset.O3.values[:,:4,423:433]=sea  # Prince Patirck Island & Melville Island
	dataset.O3.values[:,:4,634:659]=sea  # Prince Patirck Island & Melville Island
	# reduce when its coastal (bcon) in the BL
	dataset.O3.values[:,:4,723:726]=coastal
	dataset.O3.values[:,:4,778:781]=coastal
	dataset.to_netcdf('./BCON_new_'+dateinput+'.nc')

print('>> Done.')
