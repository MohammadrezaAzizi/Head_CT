import json,os
dir = "C:/Users/pc/Desktop/F_gholami/1/"
with open(os.path.join(dir,"annotations.1.json"))as f:
    label = json.load(f)

#for idx,image_name in enumerate(label.copy()):
#    if image_name == "___sa_version___":
#        label = label.pop("___sa_version___",None)
#    else:
#        pass
for image_name in list(label):
    if image_name == "___sa_version___":
        label.pop("___sa_version___")
    else:
        pass
    #if image_name.lower().endswith('.jpg') == False:
        ################
        #delete the "___sa_version___" from the begining of the loaded json file.
        ################

for att in label["JAHANGIRI, MAHBOOBEH_184.jpg"]["instances"]:
    print(att)