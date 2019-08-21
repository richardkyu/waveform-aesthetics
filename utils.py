
from os import path
from cv2 import cv2
from tqdm import tqdm
import numpy as np

#Conditionals to ensure numpy array is correct shape
def check_image_shape(image, args):
	
	#If the image rows are within the range of the averaging, the reduce the number of rows.
	row_count = 20 if image.shape[0]<250 else args.row_count

	#Sometimes the image will have length 4 because there is an alpha or transparency value for each pixel included.
	if len(image.shape) == 3 and image.shape[-1] == 4:
		image = image[:, :, :3]
		image_2=image_2[:, :, :3]
		#This makes sure the dimensions of the image are correct. ':3' is used because the last element is a list of size three.
	if len(image.shape) == 3 and image.shape[-1] == 3: #If the dimensions are correct (rows, columns, [R,G,B])
		image = np.sum(image, axis=2) #Sum the values on the last axis, so, convert each of the RGB values into just R+G+B.

	return image, row_count

def make_divisible_rows(image, row_count):
	#These next four lines just ensure that the number of total number of rows is divisble by the user-inputted row_count.
	#We need to do this so we don't get half a waveform, which the program cannot interpret.
	row_width = image.shape[0]//row_count
	col_count = image.shape[1]
	margin_rows = image.shape[0] % row_count
	image = image[margin_rows//2 : margin_rows//2 + row_count * row_width, :] #make sure the number of rows is divisible by row_width, keep column number constant.
	return image, col_count, row_width



def row_reducer(image, row_count):

	image, col_count, row_width = make_divisible_rows(image, row_count)

	reduced_image = np.zeros([row_count, col_count]) #Create a new image with the row_count user input same column number.

	for i in range(row_count):
		#print(np.median(image[i * row_width : (i + 1) * row_width, :]))
		reduced_image[i, :] = (np.median(image[i * row_width : (i + 1) * row_width, :], axis=0)) #axis 0 means take the median value of each column.
		#this is saying the new row entry is equal to the median value (R+G+B) of 30 rows, so the 15th row, the 45th row, the 75th role and so forth.
	
	#This reduced_image has dimension row = row_count (user input), and column = original column number of the image.
	return reduced_image

def calculate_column_vector(f, f_prev, phase_shift, row_width):
	column_vector = np.zeros(row_width) #create a vector of length row_width. This serves as a placeholder for now.
	
	prev_sample = row_width//2 + int((row_width//2) * np.sin(phase_shift)) - 1 #the midpoint of the row_width _+ the midpoint*sin(phase_shift)-1
	intensity = (row_width//2) * np.sin(f + phase_shift) # intensity = midpoint * np.sin(f (the pixel value) + phase_shift, initially 0)
	intensity = intensity + row_width//2 #now add the midpoint of the row_width 
	intensity = intensity.astype(np.int32) #construct 32-bit integer object for intensity, numpy makes default type the type needed to hold all objects in the array.
	column_vector[prev_sample] = 1  #Set the element in the position of the prev_sample equal to 1.

	#Conditionals that store information as 1s and 0s regarding the waveform at some element in a row.
	if intensity > prev_sample:
		column_vector[prev_sample:intensity] = 1
	else:
		column_vector[intensity:prev_sample] = 1
	

	phase_shift = phase_shift+f #phase_shift is basically f_prev
	return column_vector, phase_shift #column_vector now has data with 1s between the values of intensity and prev_sample, and 0s elsewhere.


def image_transform(image, row_width, freq_factor):
	max_freq = 2 * np.pi * freq_factor 
	image = image/image.max()*max_freq #Express all values as a fraction of the maximum (so we normalize the values) then multiply by the max frequency to limit values.
	
	#Creates a placeholder numpy array with dimension rows = rows//row_width *row_width and columns the same, filled with 0.
	waveform_img = np.zeros([row_width * image.shape[0], image.shape[1]]) #multiply number of rows in original matrix by row-width. Keep number of columns constant.
	
	
	#This is a nested for-loop with the usual iterators i, j going from left to right in a row before going down to the next row.
	for i in tqdm(range(image.shape[0])): #Note, there are row_count here.
		row = image[i] #row is equal to the number of the iteration. So we are going down row-by-row at this step.
		phase_shift = 0
		for j in range(len(row)):
			
			f = row[j] # f is equal to the jth element in the row.
			f_prev = f if j==0 else row[j-1] #This is a ternary operator that just says set f = f_prev if it is the first element.
			#print(f, f_prev)
			column_vector, phase_shift = calculate_column_vector(f, f_prev, phase_shift, row_width) # create a tuple column_vector, phase_shift. Note: f = f_prev for the first and second element.

			# Set the previously empty rows equal to the values in the column_vector variable as given by the calculate_column_vector method.
			# Previously 
			waveform_img[i * row_width : (i+1) * row_width, j : j+1] =  column_vector[ : , np.newaxis ]# Make the returned column_vector an actual column vector by adding a dimension (x,) -> (x,1)
	
	return waveform_img


def create_output(image, image_2, color):
	
	output_img = np.zeros((image.shape[0], image.shape[1], 3), dtype='uint8') #Create placeholder numpy array for final_img

	for i in range(3):
		#Color image with original colors in the areas where there are sine waves passing through.
		output_img[:,:,i][image == 0] = color[i] #where image is 0, make the background color white.
		#Where image is true (value exists for sine function at that row), then make the color the same as the original at that point.
		output_img[:,:,i][image == 1] = image_2[:,:,i][image == 1]

	return output_img


def export_output(args, output_img):
	print("Outputting file... please wait.")
	output_file = args.output_file
	if output_file is None:
		output_file = path.join(path.dirname(args.input), 'generated.png')
	cv2.imwrite(output_file, output_img.astype('uint8'))
	print('The output path of the generated image is: ', output_file)
	#return output_file
	