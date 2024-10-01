import json,os,re
import numpy as np

dir = "C:/Users/pc/Desktop/F_gholami/1/"
dir_list = ["C:/Users/pc/Desktop/F_gholami/1/annotations.1.json", "C:/Users/pc/Desktop/F_gholami/2/annotations.2.json",
             "C:/Users/pc/Desktop/F_gholami/3/annotations.3.json", "C:/Users/pc/Desktop/F_gholami/4/annotations.4.json",
             "C:/Users/pc/Desktop/F_gholami/5/annotations.5.json"]
#with open(os.path.join(dir,"annotations.1.json"))as f:
#    label = json.load(f)

def retrieve_labels(dir_list:list, maxclass:int):
    json_lis = []
    coords = []
    names = []
    ## Loading the json file
    for dir in dir_list:
        with open(dir) as f:
            label = json.load(f)
            # Turns out you can't iterate json loaded files in a for-loop. Every fix I found suggested appending into a list.
            json_lis.append(label)
    ## Making a copy to not mess with the indexing of the original list.
    json_lis_copy = json_lis.copy()
    ## Making sure the signature of annotation app is gone by deleting the version key,value pair.
    for idx, label in enumerate(json_lis):
        for image_name in json_lis_copy[idx].copy():
            if image_name == "___sa_version___":
                label.pop("___sa_version___")
            else:
                pass
    ## Parsing the labels of each image to get coordinates for each class
    for label in json_lis:
        for image_name in label:
            ## Defining as many temp_lists as needed
            """
            Assuemed that there can only be as much as 10 points for a singla patient.
            So the default maximum number of catheters is set at 10.
            """
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
    
    # Sorting the names list and simultaneously pairing with coords
    sorted_pairs = sorted(zip(names, coords), key=lambda x: [int(text) if text.isdigit() else text.lower() for text in re.split('([0-9]+)', x[0])])
    # Unzipping the sorted pairs
    names, coords = zip(*sorted_pairs)
    return names, coords

def sequencer(seq_window:int, reverse:bool, train_rate:float, val_rate:float):
    names, coords = retrieve_labels(dir_list,11)
    train_sequences = []
    train_coords = []
    valid_sequences = []
    valid_coords = []
    test_sequences = []
    test_coords = []
    # Let's go through names and check slice numbers to see which subsample it belongs to.
    for idx, name in enumerate(names):
        # checking which idx is the threshold for our train set
        if (idx/len(names)>=train_rate) and (names[idx-1].split("_")[0] != name.split("_")[0]):
            train_lim = idx
            patient_slices = []
            coord_slices = []
            # Creating the list of slice names for a patient
            for i in range(idx):
                patient_slices.append(names[i])
                coord_slices.append(coords[i])
            # Step 1: Generate sequences based on the sorted names list
            for i in range(len(patient_slices) - seq_window + 1):
                sequence = patient_slices[i:i + seq_window]
                coord_sequence = coord_slices[i:i + seq_window]
                train_sequences.append(sequence)
                train_coords.append(coord_sequence)
                # Step 2: Add reverse sequences if reverse=True
                if reverse:
                    train_sequences.append(list(reversed(sequence)))
                    train_coords.append(list(reversed(sequence)))
            ## Validation sequences
            for index in range(idx,len(names)):
                #print("first condition :    ", train_rate<(index/len(names)), "-"*4,index/len(names))
                #print("second condition :    ", (index/len(names))>train_rate+val_rate)
                #print("third condition :    ", names[index-1].split("_")[0] != names[index].split("_")[0], names[index-1],"\n")
                if train_rate<(index/len(names)) and (index/len(names))>train_rate+val_rate and names[index-1].split("_")[0] != names[index].split("_")[0]:
                # Write sth to further increase the "index" in order to fit the if condition above
                    valid_lim = index
                    patient_slices = []
                    coord_slices = []
                    # Creating the list of slice names for a patient
                    for i in range(idx,index):    #************** PROBLEM!! Reduce train list from patient slices!!
                        patient_slices.append(names[i])
                        coord_slices.append(coords[i])
                    # Step 1: Generate sequences based on the sorted names list
                    for i in range(len(patient_slices) - seq_window + 1):
                        sequence = patient_slices[i:i + seq_window]
                        coord_sequence = coord_slices[i:i + seq_window]
                        valid_sequences.append(sequence)
                        valid_coords.append(coord_sequence)
                        # Step 2: Add reverse sequences if reverse=True
                        if reverse:
                            valid_sequences.append(list(reversed(sequence)))
                            valid_coords.append(list(reversed(coord_sequence)))
                    #----------------------------------------------------------------------------------    
                    # Deciding the test set using the last index and the remainings of the 'names' list
                    #----------------------------------------------------------------------------------
                    for idx in range(index,len(names)):
                        # Creating the list of slice names for a patient
                        patient_slices.append(names[idx])
                        # Step 1: Generate test sequences based on the sorted names list
                        for i in range(len(patient_slices) - seq_window + 1):
                            sequence = patient_slices[i:i + seq_window]
                            coord_sequence = coord_slices[i:i + seq_window]
                            test_sequences.append(sequence)
                            test_coords.append(test_sequences)
                            # Step 2: Add reverse sequences if reverse=True
                            if reverse:
                                test_sequences.append(list(reversed(sequence)))
                                test_coords.append(list(reversed(coord_sequence)))
                        break
            break
        else:
            pass
    return train_sequences, train_coords, valid_sequences, valid_coords, test_sequences, test_coords, train_lim, valid_lim
# Check what conditions mess with validation data when setting it larger than 0.3
train_sequences, train_coords, valid_sequences, valid_coords, test_sequences, test_coords, train_lim , valid_lim = sequencer(seq_window=6, reverse=True, train_rate=0.6, val_rate= 0.2)
print(len(train_sequences),len(valid_sequences),len(test_sequences))
print(len(train_coords),len(valid_coords),len(test_coords))