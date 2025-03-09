# Imports
from nerfstudio.utils.eval_utils import eval_setup
from nerfstudio.pipelines.base_pipeline import Pipeline
from pathlib import Path
from nerfstudio.cameras.cameras import Cameras, CameraType, RayBundle

import torch
from PIL import Image
import numpy as np
import json
from utils import makeFolder
import copy



def renderTestImages(modelName):

    makeFolder("./digitalTwin/test_render")
    makeFolder(f"./digitalTwin/test_render/nerfacto/")
    makeFolder(f"./digitalTwin/test_render/depth-nerfacto/")
    makeFolder(f"./digitalTwin/test_render/{modelName}")
    #error
    # The path
    #load_config = Path("C:/Users/Dimitri/Documents/wemap/code/separate/ratp-gambetta-split/ratp-gambetta-split/outputs/hopeWorks/nerfacto/2025-03-06_115207/config.yml")
    load_config = Path(f"./outputs/digitalTwin/{modelName}/config.yml")
    
    #eval_num_rays_per_chunk=eval_num_rays_per_chunk,

    # Get the pipeline
    _, pipeline, _, _ = eval_setup(
                load_config,
                test_mode="inference",
            )
    
    #error

    """
    "w": 720,
        "h": 720,
        "fl_x": 623.5382907247958,
        "fl_y": 623.5382907247958,
        "cx": 360.0,
        "cy": 360.0,
    """
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    
    # Open and read the JSON file
    with open('./digitalTwin/test_folder/test_transforms.json', 'r') as file:
        data = json.load(file)

    print(data['frames'][4])

    for idx,f in enumerate(data['frames']):
        getRenderFromPose(f['transform_matrix'],f['file_path'],device,pipeline,idx,modelName)


def getRenderFromPose(pose,path,device,pipeline,idx,modelName):

    swapAxes = np.array([[1.0, 0.0, 0.0, 0.0],
                         [0.0, 0.0, -1.0, 0.0],
                         [0.0, 1.0, 0.0, 0.0],
                         [0.0, 0.0, 0.0, 1.0]])

    import json

    with open(f'./outputs/digitalTwin/{modelName}/dataparser_transforms.json') as f:
        dataTransform = json.load(f)

    dataMatrix = np.array(dataTransform['transform'])
    dataScale = np.array(dataTransform['scale'])

    pose = swapAxes @ pose
    pose = dataMatrix @ pose
    pose[:3,3] *= dataScale

    camera_to_worlds=torch.tensor(pose).to(device)
    
    # Create Cameras instance, define your camera intrinsics 
    cameras = Cameras(
        camera_to_worlds=camera_to_worlds,
        camera_type=CameraType.PERSPECTIVE,
        fx=623.5382907247958,
        fy=623.5382907247958,
        cx=360.0,
        cy=360.0,
        width=720,
        height=720)

    # Render the single frame using the given camera pose
    outputs = pipeline.model.get_outputs_for_camera(cameras)
    rgba = pipeline.model.get_rgba_image(outputs=outputs, output_name="rgb")
    outputs["rgba"] = rgba
    output_image = outputs["rgba"]
    output_image = output_image.detach().cpu().numpy()

    # Convert NumPy array to PIL Image and save
    output_image = (output_image * 255).astype(np.uint8)  # Rescale to 0-255 for saving
    output_image_pil = Image.fromarray(output_image)

    #output_image_path = os.path.join(output_dir, 'rendered_image.png')
    print(path[-15:-4])
    #print()
    save_path = f"./digitalTwin/test_render/{modelName}/{path[-15:-4]}_testRender.png"
    #error
    
    output_image_pil.save(save_path)