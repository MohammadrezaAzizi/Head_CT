import json,os
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
            temp_list1, temp_list2, temp_list3, temp_list4, temp_list5, temp_list6, temp_list7, temp_list8, temp_list9, temp_list10 = ([] for i in range(maxclass))
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
                temp_list = [temp_list1, temp_list2, temp_list3, temp_list4, temp_list5, temp_list6, temp_list7, temp_list8, temp_list9, temp_list10]

            for idx,i in enumerate(temp_list):
                if len(i)==0:
                    temp_list[idx] = [0,0]
                else:
                    pass
            coords.append(temp_list)
        print("Length of names list:    ",len(names),"\n coordinates are:    ", len(coords))
            ## Now only sorting the names and sequences and writing functions to gather all annotations and reading the images remains.
retrieve_labels(dir_list,10)

#for att in label["JAHANGIRI, MAHBOOBEH_184.jpg"]["instances"]:
#    print(att)