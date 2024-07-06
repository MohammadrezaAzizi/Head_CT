import PIL.Image
import SimpleITK as sitk
import os
import matplotlib.pyplot as plt
import numpy as np
import PIL.Image as Image

dir = "C:/Users/pc/Desktop/F_gholami/MR.data/1"
def dicom_to_jpeg(input_directory, output_directory):
    for filename in os.listdir(dir):
        if filename.lower().endswith('dcm'):
            image = sitk.ReadImage(os.path.join(input_directory, filename))
            ## Rescale intensity to [0,255] cast to uint8 for JPEG
            image = sitk.Cast(sitk.RescaleIntensity(image, outputMinimum=0, outputMaximum=255),sitk.sitkUInt8)
            ## Save the jpeg format
            output_path = os.path.join(output_directory,filename.replace('.dcm','.jpg'))
            image = sitk.GetArrayViewFromImage(image)
            image = np.squeeze(image,axis=0)
            #image = np.squeeze(image)
            image = Image.fromarray(image)
            image.save(output_path,'JPEG')
            print(f"saved {output_path}")
        else:
            break
dicom_to_jpeg(dir,dir)