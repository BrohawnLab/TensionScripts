#load stuff
import circle_fit
from circle_fit import taubinSVD
import os                                                                                            
import csv                                                                                           
import os.path                                                                                       
import matplotlib.pyplot as plt
import pandas as pd                                                                      
import numpy as np                                                                                   
from scipy import linalg
from imageio import imread
from scipy.optimize import curve_fit
from itertools import zip_longest
import statistics
import traceback
import sys
from pathlib import Path




##SETUP##

message = '*** You will be prompted to input file paths with this script, please read the prompts for each file location to ensure the script runs correctly. ***'
print("\n\n", message, "\n\n") 

#Where are the txt files?
def get_directory_path():
    while True:
        path = input("Where are your txt files? include the final /: ")
        if os.path.isdir(path):
            return path
        else:
            print("Invalid directory path. Please try again.")

#Where should the script save the results?
def get_save_path():
    while True:
        path = input("Where would you like this script to save its output file? include the final /: ")
        if os.path.isdir(path):
            return path
        else:
            print("Invalid directory path. Please try again.")

#Printing the pathways & setting pathways
dir_path = get_directory_path()
print("\n", "Your txt files have been found here:", dir_path, "\n")
save_path = get_save_path()
print("\n", "Your results can be found header:", save_path, "\n")


#Setting your % multiplier, reference X coordinate, and checking if the script should save your plots. 
window_range = int(input("\n\nHow many pixels wide is your membrane?: "))
KeepPlots = input("\nWould you like to save the plots of your selected dataplots? Type True if yes and False if no: ")
VisualizeNumber = input("\nWhich trial would you like to visualize (number in 0000 format)? \nIf you do not wish to visualize the data you may enter a comically large number or any text value: ")
VisualizeFile = VisualizeNumber + ".txt"

#Creating your two result files
header = ('Frame', 'Radius', 'Xc', 'Yc', 'Sigma', 'Highest Point', 'Highest Average')
#ResultsFile1
resultsfile1 = save_path+'Results_Original.csv'
f = open(resultsfile1, 'w')
# create the csv writer
writer = csv.writer(f)
# Writing header
writer.writerow(header)
f.close()

#ResultsFile2
resultsfile2 = save_path+'Results_Filtered.csv'
f2 = open(resultsfile2, 'w')
# create the csv writer
writer = csv.writer(f2)
# Writing header
writer.writerow(header)
f2.close()

#CreatePlotSaveDirectories
if KeepPlots == "True":
	FigurePath_Raw = save_path + "Results_Raw"
	Path(FigurePath_Raw).mkdir(parents=True, exist_ok=True)
	FigurePath_Filtered = save_path + "Results_Filtered"
	Path(FigurePath_Filtered).mkdir(parents=True, exist_ok=True)
else:
	print("\n\nNot saving dataplots\n\n")


count = 0
# Iterate directory
for path in os.listdir(dir_path):
    # check if current path is a file
    if os.path.isfile(os.path.join(dir_path, path)):
        count += 1
print('Frame count:', count)

radiuslist = []

os.chdir(dir_path)
#begin scipt - it will iterate based on 
for i in range(count): 
	#import txt file as dataframe
	file_name = f"{i:04d}.txt"
	print("\nOpening file ", file_name, "\n")
	data = pd.read_csv(file_name, delimiter = '\t', header=None)
	shape = data.shape
	xlim = shape[1]
	ylim = shape[0]
	print(shape)
	#plt.imshow(data, cmap='viridis', interpolation='nearest')
	#plt.show()



	count_row = data.shape[0]
	row_indices = count_row  # Gives number of rows
	#specifices window size and step size
	window_size = window_range
	step_size = 1
	

	BoxFit_coordinates = []
	BoxFit_coordinates_1 = []
	BoxFit_coordinates_2 = []
	CircleFit_Coordinates = []
	GraphyA = []
	GraphyV = []
	df1 = []
	values_plot = []
	values_pixel = []

	for row_index in range(row_indices):
		row = data.iloc[row_index]

		highest_average = float('-inf')
		highest_average_iteration = None
		highest_value = float('-inf')
		highest_value_position = None
		firstvalue = None
		higha_mean = []
		highv_mean = []
		higha = []
		highv = []
		colorRangeX = []
		ColorRangeY1 = []
		ColorRangeY2 = []
		

		num_iterations = len(row) - window_size + 1

		for i in range(num_iterations):
			values = row.iloc[i:i+window_size]

			average = values.mean()

			if average > highest_average:
				highest_average = average
				highest_average_iteration = i+1
				
				pass

				highest_value = values.max()
				firstitem = highest_average_iteration - 1
				firstvalue = firstitem
				highest_value_position = values.idxmax()
				values_plot = values



		GraphyA.append(highest_average)
		dfA = pd.DataFrame(GraphyA)

		GraphyV.append(highest_value)
		dfV = pd.DataFrame(GraphyV)
		

		coordinateList =[]
		boxlocation_1 = []
		boxlocation_2 = []
		coordinate_x = highest_value_position
		coordinate_y = row_index
		value_x = firstvalue
		value_x_window = firstvalue + window_size
		boxlocation_1.append(value_x)
		boxlocation_1.append(coordinate_y)
		ColorRangeY1.append(boxlocation_1)
		ColorRangeY2.append(boxlocation_2)
		colorRangeX.append(coordinate_y)
		values_pixel.append(values_plot)
		vp = pd.DataFrame(values_pixel)
		BoxFit_coordinates.append(boxlocation_1)
		BoxFit_coordinates_1.append(boxlocation_1)
		boxlocation_2.append(value_x_window)
		boxlocation_2.append(coordinate_y)
		BoxFit_coordinates.append(boxlocation_2)
		BoxFit_coordinates_2.append(boxlocation_2)
		coordinateList.append(coordinate_x)
		coordinateList.append(coordinate_y)
		CircleFit_Coordinates.append(coordinateList)


		highv_mean = dfV.mean()
		higha_mean = dfA.mean()
		

	try:
		#Printing the Coordinates & Calculating Raw Curvature
		
		print(CircleFit_Coordinates)
		PercentList1 = CircleFit_Coordinates
		xc, yc, r, sigma = taubinSVD(CircleFit_Coordinates)
		print(GraphyV)
		print(GraphyA)
		highv_print = highv_mean.values.tolist()
		highv_final = highv_print[0]
		higha_print = higha_mean.values.tolist()
		higha_final = higha_print[0]
		print(highv_print, "is highv print")
		print("highv_mean", highv_mean)
		print("highaa_mean", higha_mean)
		print(xc)
		print(yc)
		print(r)
		print(sigma)
		print(file_name, "succeeded.")
		radiuslist.append(file_name)
		radiuslist.append(r)

		#Update Results_Unfiltered

		f = open(resultsfile1, 'a')
		writer = csv.writer(f)
		data_values = (file_name, r, xc, yc, sigma, highv_final, higha_final)
		writer.writerow(data_values)
		f.close()

		#Making Initial Plot & Saving it
		

		xs = [x[0] for x in CircleFit_Coordinates]
		ys = [x[1] for x in CircleFit_Coordinates]
		plt.plot(xs, ys)

		if KeepPlots == "True":
			os.chdir(FigurePath_Raw)
			savefile_raw = file_name + "_Unfiltered.png"
			plt.savefig(savefile_raw)
			if file_name == VisualizeFile:
				plt.show()
				os.chdir(dir_path)
			else:
				plt.close()
				os.chdir(dir_path)
		else:
			continue

		Box_xs = [x[0] for x in BoxFit_coordinates]
		Box_ys = [x[1] for x in BoxFit_coordinates]
		plt.plot(Box_xs, Box_ys)

		if KeepPlots == "True":
			os.chdir(FigurePath_Raw)
			savefile_raw = file_name + "_boxrange.png"
			plt.savefig(savefile_raw)
			if file_name == VisualizeFile:
				plt.show()
				os.chdir(dir_path)
			else:
				plt.close()
				os.chdir(dir_path)
		else:
			continue

		plt.imshow(data, cmap='gray', interpolation='nearest')
		xs = [x[0] for x in CircleFit_Coordinates]
		ys = [x[1] for x in CircleFit_Coordinates]
		plt.plot(xs, ys, label = "brightest")

		Box_xs_1 = [x[0] for x in BoxFit_coordinates_1]
		Box_ys_1 = [x[1] for x in BoxFit_coordinates_1]
		plt.plot(Box_xs_1, Box_ys_1, label = "inner")

		Box_xs_2 = [x[0] for x in BoxFit_coordinates_2]
		Box_ys_2 = [x[1] for x in BoxFit_coordinates_2]
		plt.plot(Box_xs_2, Box_ys_2, label = "outer")
		plt.legend(loc="upper left")
		plt.fill_betweenx(Box_ys_1, Box_xs_1, Box_xs_2, color='skyblue', alpha=0.2)



		if KeepPlots == "True":
			os.chdir(FigurePath_Raw)
			savefile_raw = file_name + "_shadedrange.png"
			plt.savefig(savefile_raw)
			if file_name == VisualizeFile:
				plt.show()
				os.chdir(dir_path)
			else:
				plt.close()
				os.chdir(dir_path)
		else:
			continue

		plt.imshow(vp, cmap ='gray', interpolation='nearest')

		if KeepPlots == "True":
			os.chdir(FigurePath_Raw)
			savefile_raw = file_name + "_membranesnapshot.png"
			plt.savefig(savefile_raw)
			if file_name == VisualizeFile:
				plt.show()
				os.chdir(dir_path)
			else:
				plt.close()
				os.chdir(dir_path)
		else:
			continue	
		


	finally:
		print("Continuing")

print('\n\n****   Completed!   *****\n\n')

#Show Final PLOT
#if VisualizeFinal == True:
#	plt.show()
#	plt.show()
#	
#else:
#	print('\n\n****   Completed!   *****\n\n')
