import json
import copy


def getMaskedTransform():

    # Open and read the JSON file
    with open('./digitalTwin/transforms.json', 'r') as file:
        data = json.load(file)

    maskedData = copy.deepcopy(data)

    for i,f in enumerate(maskedData['frames']):
        frame_name = maskedData['frames'][i]["file_path"][-15:-4]
        maskedData['frames'][i]["mask_path"] = f"./digitalTwin/masks/masks/{frame_name}_mask.jpeg" 

    # Serializing json
    json_object = json.dumps(maskedData, indent=4)

    #print(maskedData['frames'][4])
    #error

    # Writing to sample.json
    with open(f"transforms.json", "w") as outfile:
        outfile.write(json_object)

    