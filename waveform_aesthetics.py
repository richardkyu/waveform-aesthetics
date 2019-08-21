from utils import (check_image_shape,
					make_divisible_rows, 
					row_reducer,
					calculate_column_vector,
					image_transform, 
					create_output,
					export_output)
from cv2 import cv2
import argparse, os, time

#start_time = time.time()

def main(args):
	#Note: In some cases, necessary to convert default BGR pixel values given by CV2 to RGB
	#image is read in as rows of (r,g,b) values, we have x rows and intensity columns of pixels, and each pixel has its own RGB value.
	#We have a list with 3000 elements, with 2491 elements in each element in the 3000, and 3 elements in each list with 2491 elements. (For the picture I'm initially using.)
	image = cv2.imread(args.input) 
	image_2 = cv2.imread(args.input)
	image_2 = make_divisible_rows(image_2, args.row_count)[0] 
	image, args.row_count = check_image_shape(image, args)
	#black to fill in the space not occupied by sine wave
	black = (0,0,0)
	row_width = image.shape[0]//args.row_count #record the row width of the image. image.shape[0] is the number of rows / args.row_count. (3000/100 = 30)
	freq_factor = args.freq_factor * 0.25 + 0.1 # to scale freq_factor, adjust as needed.


	#Apply transformation methods to the image, then use the recorded values transformation to map to an output. Export the output.
	image = row_reducer(image, args.row_count) #returns an image of shape (row_count, num_columns), where row_count is user input, default 100.
	image = image_transform(image, row_width, freq_factor)
	output_img = create_output(image, image_2, black)
	
	export_output(args, output_img)
	



#Run the program
if __name__ == '__main__':	
	parser = argparse.ArgumentParser('Waveform aesthetics - create art using trigonometry! ')
	parser.add_argument('input',
						type=str, help='Input path for image.')
	parser.add_argument('-o', '--output-file', default=None,
						type=str, help='Output path for image')
	parser.add_argument('-n', '--row-count', default=100,
						type=int, help='number of waveforms (rows) in the generated image')
	parser.add_argument('-f', '--freq-factor', default=1/4,
						type=float, help = "f(t) = A sin(wt + phi). The freq_factor is w, or omega.")
	args = parser.parse_args()
	main(args)

	#print("--- %s seconds ---" % (time.time() - start_time))