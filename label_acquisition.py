import json,os,re
import numpy as np

dir = "C:/Users/pc/Desktop/F_gholami/1/"
dir_list = ["C:/Users/pc/Desktop/F_gholami/1/annotations.1.json", "C:/Users/pc/Desktop/F_gholami/2/annotations.2.json"]
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
    json_lis_copy = json_lis.copy()
    ## Making sure the signature of annotation app is gone.
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
    valid_sequences = []
    test_sequences = []
    # Let's go through names and check slice numbers to see if it fits our window
    for idx, name in enumerate(names):
        base_index = 0
        # checking which idx is the threshold for our name set (where does the current patient end)
        if (idx/len(names))<=train_rate and names[idx-1].split("_")[0] != name.split("_")[0]:
            patient_slices = []
            # Creating the list of slice names for a patient ************** PROBLEM!!
            for i in range(idx):
                patient_slices.append(names[i])
            #---------------------------------------------------------------
            ## Took care of intra-patient sequence creation defining a list that includes all slices of a patient.
            #---------------------------------------------------------------
            
            #---------------------------------------------------------------
            # Code the thresholding and sampling based on percentage share for each subsample.
            ## So far I know the percentage should only be checked via "len(names)" as the denominator!
            ## Also, I guess implementing the percentage if/else condition should be checked in the patient threshold if!
            #---------------------------------------------------------------

            # Step 1: Generate sequences based on the sorted names list
            for i in range(len(patient_slices) - seq_window + 1):
                sequence = patient_slices[i:i + seq_window]
                train_sequences.append(sequence)
                # Step 2: Add reverse sequences if reverse=True
                if reverse:
                    train_sequences.append(list(reversed(sequence)))
        
        ## Validation sequences
        elif train_rate<(idx/len(names)) and (idx/len(names))<train_rate+val_rate and names[idx-1].split("_")[0] != name.split("_")[0]:
            patient_slices = []
            # Creating the list of slice names for a patient
            for i in range(idx):    #************** PROBLEM!! Reduce train list from patient slices!!
                patient_slices.append(names[i])

            # Step 1: Generate sequences based on the sorted names list
            for i in range(len(patient_slices) - seq_window + 1):
                sequence = patient_slices[i:i + seq_window]
                valid_sequences.append(sequence)
                # Step 2: Add reverse sequences if reverse=True
                if reverse:
                    valid_sequences.append(list(reversed(sequence)))
        
            # Time to reset
            #----------------------------------------------------
            # first make sure the coords can be used by sequences of names.
            #----------------------------------------------------
        else:
            patient_slices = []
            # Creating the list of slice names for a patient
            for i in range(idx): #************** PROBLEM!! Reduce train and validation list from patient slices!!
                patient_slices.append(names[i]) 
            # Step 1: Generate sequences based on the sorted names list
            for i in range(len(patient_slices) - seq_window + 1):
                sequence = patient_slices[i:i + seq_window]
                test_sequences.append(sequence)
                # Step 2: Add reverse sequences if reverse=True
                if reverse:
                    test_sequences.append(list(reversed(sequence)))
    return train_sequences, valid_sequences, test_sequences

train_sequences, valid_sequences, test_sequences = sequencer(seq_window=6, reverse=True, train_rate=0.7, val_rate= 0.2)
print(len(test_sequences))
#for att in label["JAHANGIRI, MAHBOOBEH_184.jpg"]["instances"]:
#    print(att)