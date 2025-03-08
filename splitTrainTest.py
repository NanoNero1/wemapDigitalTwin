import json
import copy
import numpy as np

# Open and read the JSON file
with open('./hopeWorks/transforms.json', 'r') as file:
    data = json.load(file)

# Print the data
#print(data['frames'][0])


sortFrames = sorted(data['frames'], key=lambda x: x["file_path"], reverse=False)