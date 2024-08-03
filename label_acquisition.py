import json,os
import numpy as np
dir = "C:/Users/pc/Desktop/F_gholami/1/"
dir_list = ["C:/Users/pc/Desktop/F_gholami/1/annotations.1.json"]
with open(os.path.join(dir,"annotations.1.json"))as f:
    label = json.load(f)

def retrieve_labels(dir_list:list, maxclass:int):
    coords = []
    names = []
    ## Loading the json file
    for dir in dir_list:
        with open(dir) as f:
            label = json.load(f)
    ## Making sure the signature of annotation app is gone.
        for image_name in list(label):
            image_labels = []
            if image_name == "___sa_version___":
                label.pop("___sa_version___")
            else:
                pass
            
    ## Parsing the labels of each image to get coordinates for each class
        for image_name in list(label):
            ## Defining as many temp_lists as needed
            temp_list1, temp_list2, temp_list3, temp_list4, temp_list5, temp_list6, temp_list7, temp_list8, temp_list9, temp_list10, temp_list11 = ([] for i in range(maxclass))
            names.append(image_name) 
            ## Iterating through instances to change values of temp_lists to the existing values from annotation json
            for instance in label[image_name]["instances"]:
                if instance["classId"] == 1:
                    temp_list1 = [instance["x"],instance["y"]]
                elif instance["classId"] == 2:
                    temp_list2 = [instance["x"],instance["y"]]
                elif instance["classId"] == 3:
                    temp_list3 = [instance["x"],instance["y"]]
                elif instance["classId"] == 4:
                    temp_list4 = [instance["x"],instance["y"]]
                elif instance["classId"] == 5:
                    temp_list5 = [instance["x"],instance["y"]]
                elif instance["classId"] == 6:
                    temp_list6 = [instance["x"],instance["y"]]
                elif instance["classId"] == 7:
                    temp_list7 = [instance["x"],instance["y"]]
                elif instance["classId"] == 8:
                    temp_list8 = [instance["x"],instance["y"]]
                elif instance["classId"] == 9:
                    temp_list9 = [instance["x"],instance["y"]]
                elif instance["classId"] == 10:
                    temp_list10 = [instance["x"],instance["y"]]            
                elif instance["classId"] == 11:
                    temp_list11 = [instance["x"],instance["y"]]
                temp_list = [temp_list1, temp_list2, temp_list3, temp_list4, temp_list5, temp_list6, temp_list7, temp_list8, temp_list9, temp_list10, temp_list11]
            for idx,i in enumerate(temp_list):
                if len(i)==0:
                    temp_list[idx] = [0,0]
                else:
                    pass
            coords.append(temp_list)
        
        ## Here's the sorting block.
        # The problem was the name strings were a combination of strings and numbers so the 3 digits was preceding the 2 digit elements.
        # So we just kept the number part of each name string and the created the sorting indices using np.argsort
        # Then it was easy to sort all the names and coords lists and also change them to numpy arrays.
        nums = []
        for i in names:
            num = i.split("_")[1]
            num = num.split(".")[0]
            num = int(num)
            nums.append(num)
        sort_map = np.argsort(nums)
        np.array(nums)[sort_map]
        coords = np.array(coords)[sort_map]
        names = np.array(names)[sort_map]
        for idx,j in enumerate(names):
            if idx<3:
                print("The name is:    ", j,"\n The arrays are as following:    ",coords[idx], "\n")
                
        #print("Length of names list:    ",len(names),"\n coordinates are:    ", len(coords))
            ## Now only sorting the names and sequences // use stackoverflow links in bookmarks.
retrieve_labels(dir_list,11)

#for att in label["JAHANGIRI, MAHBOOBEH_184.jpg"]["instances"]:
#    print(att)