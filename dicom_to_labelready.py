import SimpleITK as sitk
import os, cv2
import matplotlib.pyplot as plt
import numpy as np
import PIL.Image as Image
import pydicom
from skimage.filters.thresholding import threshold_otsu
from skimage.measure import regionprops
from skimage.filters.thresholding import threshold_multiotsu


def mean_normalization(image):
    # Might be a good idea to write a unit test for the type.
    image = sitk.GetArrayFromImage(image)
    print("Dimensions are:   ",image.shape)
    mask = np.where(image != 0)
    desired_img = image[mask]
    mean = np.mean(desired_img)
    std = np.std(desired_img)
    final_image = (image - mean)/ std
    return final_image

def processed_image_export(input_image, output_dir, filename):
    #if type(binary_input) != np.uint8:
    #    print("type of binary_input is  ", str(type(binary_input)), "... Converting to np.uint8")
    #    binary = np.asarray(binary_input, dtype=np.uint8)
    thresh = threshold_multiotsu(input_image)
    binary = input_image>thresh[1]
    for i in range(512):
        for j in range(512):
            if input_image[i][j]<thresh[0]:
                input_image[i][j]=0
            elif input_image[i][j]<thresh[1]:
                input_image[i][j]=thresh[0]
            else:
                input_image[i][j]=255
    ## +++ add a fix for filename from jupyternotebook
    plt.imsave(fname="C:/Users/pc/Desktop/F_gholami/MR.data/1/00000140_binary.jpg" ,arr=binary, format='jpg', cmap = 'gray', dpi=300)
    plt.imsave(fname="C:/Users/pc/Desktop/F_gholami/MR.data/1/00000140_fuzzy.jpg",arr=input_image, format='jpg', cmap='gray', dpi=300)
    clahe_filename = output_dir+filename.split(".")[0]+"_"+"clahe"+".jpg"
    fuzzy_filename = output_dir+filename.split(".")[0]+"_"+"fuzzy"+".jpg"
    plt.imsave(fname=clahe_filename ,arr=binary, format='jpg', cmap = 'gray', dpi=300)
    plt.imsave(fname=fuzzy_filename,arr=input_image, format='jpg', cmap='gray', dpi=300)


dir = "C:/Users/pc/Desktop/F_gholami/MR.data/1"
def dicom_to_jpeg(input_directory, output_directory):
    # Give all dicom files in a directory the ".dcm" suffix
    for filename in os.listdir(input_directory):
        if not filename.lower().endswith('dcm'):
            os.rename(os.path.join(input_directory, filename), os.path.join(input_directory,filename,".dcm"))

    for filename in os.listdir(dir):
        if filename.lower().endswith('dcm'):
            image = sitk.ReadImage(os.path.join(input_directory, filename))
            # Image normalization (zero-centered)
            image = mean_normalization(image)
            image = np.squeeze(image, axis=0)
            clahe_img = image.astype(dtype=np.uint16)
            clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
            clahe_img = clahe.apply(clahe_img) + 30

            ## Rescale intensity to [0,255] cast to uint8 for JPEG
            image = sitk.Cast(sitk.RescaleIntensity(mn_image, outputMinimum=0, outputMaximum=255),sitk.sitkFloat32)
            corrector = sitk.N4BiasFieldCorrectionImageFilter()
            output = corrector.Execute(image)
            ## Save the jpeg format
            #output_path = os.path.join(output_directory,filename.replace('.dcm','.dcm'))
            sitk.WriteImage(output,os.path.join(output_directory,filename))

            ## Open the standard image using pydicom and using pillow to save it in jpeg format.
            image = pydicom.dcmread(os.path.join(input_directory, filename))
            output_path = os.path.join(output_directory,filename.replace('.dcm','.jpg'))
            image= image.pixel_array
            image = Image.fromarray(image)
            image.save(output_path,'JPEG')
            print(f"saved {output_path}")
        else:
            pass
dicom_to_jpeg(dir,dir)

def dicom_2_jpg_using_pydicom(input_directory, output_directory):
    for filename in os.listdir(dir):
        if filename.lower().endswith('dcm'):
            image = pydicom.dcmread(os.path.join(input_directory, filename))
            output_path = os.path.join(output_directory,filename.replace('.dcm','.jpg'))
            image= image.pixel_array

            print("printing info",image.size)

            ## Rescale intensity to [0,255] cast to uint8 for JPEG
            min_value = np.min(image)
            max_value = np.max(image)
            image = ((image-min_value)/(max_value-min_value)*255).astype(np.uint8)
            ## Save the jpeg format
            output_path = os.path.join(output_directory,filename.replace('.dcm','.png'))
            #image = np.squeeze(image)
            image = Image.fromarray(image)
            image.save(output_path,'PNG')
            print(f"saved {output_path}")
        else:
            pass
#dicom_2_jpg_using_pydicom(dir,dir)