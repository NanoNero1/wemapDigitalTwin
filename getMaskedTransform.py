import json
import copy
import os


def getMaskedTransform():

    # Open and read the JSON file
    with open('./digitalTwin/transforms.json', 'r') as file:
        data = json.load(file)

    maskedData = copy.deepcopy(data)

    for i,f in enumerate(maskedData['frames']):
        frame_name = maskedData['frames'][i]["file_path"][-15:-4]
        maskedData['frames'][i]["mask_path"] = f"./masks/masks/{frame_name}_mask.jpeg" 

    # Serializing json
    json_object = json.dumps(maskedData, indent=4)

    #print(maskedData['frames'][4])
    #error
    #os.remove("./transforms.json")

    # Writing to sample.json
    with open(f"./digitalTwin/transforms.json", "w") as outfile:
        #json.dump(maskedData, f, indent=4)
        outfile.write(json_object)

    