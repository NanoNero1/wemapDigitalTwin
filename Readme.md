<p align="center">
  <img src="https://getwemap.com/images/logo-wemap.svg" width="15%"/>
</p>

# Running the code

In order to run the pipeline, you need to specify the path where the data is stored.

```bash
python main.py C:\Users\Dimitri\Documents\wemap\pipeline\pipelineData\wemap-office-one-room-v1\wemap-office-one-room-v1
```


## Step 1: Preprocessing, Collecting Masks and Inpainting

## Step 2: Converting Data To Nerfstudio set

## Step 3: 



### Known Problems:
- sometimes you can run out of memory so it's best to run this alone and close other applications



### To-do:
- if we already have the data processed, skip this step
- list like *[process,train,render]*

- add a requirements file, explaining what libraries
you need and how to set them up

To fix out of CUDA memory:
pip uninstall tinycudann
git ninja install+...tinycuda...


- add saving of the checkpoints,
- log saying it will be saved to this path

- one script to process&train
- second script to visualize


### Visualization From Server Execution

See the link

https://wandb.ai/balbul/nerfstudio-project

Feel free to check loss function and output metrics curve on wandb.

You can see some samples of model performance in Section Eval Images



