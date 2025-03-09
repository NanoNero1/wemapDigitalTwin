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


    file_path = "images/frame_00237.png"
    
    #! maybe it's the wrong type of matrix?
    transform_matrix = [
                    [
                        -0.2714771797283373,
                        0.16060999804562984,
                        -0.9489491922197578,
                        0.017548072811172644
                    ],
                    [
                        -0.960328538314223,
                        0.020146637017384877,
                        0.2781424302693817,
                        0.08782567456780599
                    ],
                    [
                        0.06379059010556412,
                        0.9868123132311801,
                        0.1487690124633197,
                        0.005655566625667207
                    ],
                    [
                        0.0,
                        0.0,
                        0.0,
                        1.0
                    ]
                ]
    
    # Open and read the JSON file
    with open('./digitalTwin/test_folder/test_transforms.json', 'r') as file:
        data = json.load(file)

    print(data['frames'][4])

    for idx,f in enumerate(data['frames']):
        getRenderFromPose(f['transform_matrix'],f['file_path'],device,pipeline,idx,modelName)

    print('IT WORKEDDD')


def getRenderFromPose(pose,path,device,pipeline,idx,modelName):

    ### NEED TO RE-STRUCTURE THIS
    #camera_to_worlds = torch.tensor([[0.1576458912421872, 0.001432504239621657, 0.9874946687988042, -0.1502362906932832], 
    #                             [ 0.98749570137543, -0.00011438947221609208, -0.1576458901465443, 3.7798531274000803], 
    #                             [-0.00011286941201377187, 0.9999989674227929, -0.0014326248091246496, -0.007071613542939272]
    #                             ]).to(device)


    #camera_toF_worlds = torch.tensor(np.array(pose[:-1])).to(device)


    #pose = [[0.0, 0.0, 0.0, 0.0],[0.0, 0.0, 0.0, 0.0],[float(idx),0.0, 0.0, 0.0],[0.0, 0.0, 0.0, 1.0]]

    swapAxes = np.array([[1.0, 0.0, 0.0, 0.0],
                         [0.0, 0.0, -1.0, 0.0],
                         [0.0, 1.0, 0.0, 0.0],
                         [0.0, 0.0, 0.0, 1.0]])

    import json

    with open(f'./outputs/digitalTwin/{modelName}/dataparser_transforms.json') as f:
        dataTransform = json.load(f)

    dataMatrix = np.array(dataTransform['transform'])
    dataScale = np.array(dataTransform['scale'])


    #pose = np.array(pose)[]

    #print(dataMatrix)
    #print(pose)
    #error
    #pose = dataMatrix[:,:3] @ (pose + dataMatrix[:,3])
    #print(o)
    #pose = pose * dataScale

    #camera_to_worlds = torch.tensor(  np.array(pose[:-1]) ) .to(device)
    #camera_to_worlds=pose[:-1,:]

    pose = swapAxes @ pose
    pose = dataMatrix @ pose
    pose[:3,3] *= dataScale

    #pose[:3,:3] = pose[:3,:3].T
    #pose[:3,3] =  -1*pose[:3,3] 

    #print('laaaaaaaaaaaaaaaa')
    #print(pose.shape)
    #print(pose)
    #error
    camera_to_worlds=torch.tensor(pose).to(device)

    #print(camera_to_worlds.shape)
    #placeHolder = copy.deepcopy(camera_to_worlds[:,2])
    #camera_to_worlds[:,2] = camera_to_worlds[:,1]
    #camera_to_worlds[:,1] = placeHolder

    #print(camera_to_worlds)

    #print(camera_to_worlds.shape)
    
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