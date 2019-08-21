# Description
This algorithm outputs an image using the RGB values of a given input image's pixel as a basis for the frequency of a sine wave occupying a row of the image.

The program is based around the observation that for a function f: 
`f(t) = A sin (wt + f)` 
Consider that from this, we can use averaged RGB values normalized to 0 to 2π to generate a waveform, if we take the set of those RGB values as the variable t, to create the above function for a row.

# Visual Results

  Before Image Transformation                |  After Image Transformation                 | 
:-------------------------------------------:|:-------------------------------------------:|
![before](https://i.imgur.com/1sa3N9S.jpg)   |  ![after](https://i.imgur.com/FsjJjgm.jpg)


  Closeup                                     | 
  :------------------------------------------:|
  ![closeup](https://i.imgur.com/Ofurja8.jpg)

Photo by Amanda Dalbjörn on Unsplash


  Before Image Transformation                |  After Image Transformation                 | 
:-------------------------------------------:|:-------------------------------------------:|
![before](https://i.imgur.com/fH9cdO1.jpg)   |  ![after](https://i.imgur.com/E9PhNB3.png)


  Closeup                                     | 
  :------------------------------------------:|
  ![closeup](https://i.imgur.com/UlnPEav.png)


Photo by Ben Scott on Unsplash


All photos downloadable in repository.

# Program Execution
**Instructions:**
Download the repository and run the python command while in the local folder. The argparse implementation requires you to attach the path of the photo that you want to process as an input. Additionally, there are three optional arguments you can designate after the required input which are the output path, the row count, and the frequency factor.

In bash:

`python waveform_aesthetics.py PATH_TO_IMG `

The program will run and display a progress bar which corresponds to the creation of data for where to plot the waveform if everything is done correctly.


# Code Structure and Methods
The code is broken up into a [utils.py](utils.py) file which contains all the definitions for modification, and a main execution file called [waveform_aesthetics.py](waveform_aesthetics.py), responsible for running and implementing the methods in utils.

There are seven methods that handle the process of image transformation. Here is a brief explanation on how they work.

| Method Name  | Functionality   |
| :------------- | :---------- |
|check_image_shape | When we read in an image using numpy.asarray along with cv2, sometimes the image does not conform to the shape (rows, columns, 3) and sometimes the image is too small for processing. For instance, the shape may be (row, column, 4) if there is an transparency or alpha value in addition to the RGB values.  |
| make_divisible_rows  | The user may input the number of rows of waveforms they want the picture to represented in, with the default value being 100. Since the total number of rows may not be divisible by 100 or the user's input, we must include a method that discards a few rows in order to make sure that we do not end up with half a row, a case that the algorithm cannot handle. |
| row_reducer  | If the original shape of the image is represented by numpy.shape as (row,column,3), then row_reducer reduces the rows to the row_count value given by the user as an input such that the returned shape is (100, column, 3) by default. The 100 rows are a sample of the median rows.|
| calculate_column_vector | This calculates the column vector of shape (row/100, ). Note that row will divide evenly into 100 because we had processed it with the make_divisible_rows method prior. |
| image_transform | The iterative method that adds a unique column vector for every element in the row_reduced image matrix, expanding the shape from (100,column, 3) back to (row, column, 3), with the new numpy array containing 0s and 1s indicating if a pixel at that position is part of the waveform or not.|
|  create_output | Reading in the binary information along with an original copy of the picture in image_2 (which contains the preserved color information) to give the appropriate RGB values for each point on the generated waveform. |
|  export_output | Output the file to the specified output path, the same directory as the input file by default. |


Finally, the background color can be modified by changing the tuple associated with the variable "black" in the execution file, in case we want to render against a picture with a mainly white background.
