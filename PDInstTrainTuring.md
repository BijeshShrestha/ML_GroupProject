<!-- ---
output:
  html_document: default
title:
  Instructions for Training on WPI's HPC (Turing) and Prediction Locally
--- -->

Please note that this tutorial is for a Linux environment only 
(Turing is a Linux environment, but your local machine may not be). 
However, if you are familiar with Windows or Mac command-line, 
then adapting these instructions should not be too much trouble.

# Setup Turing

Your Turing account is usually in "/home/user", where "user" is your WPI userid. 
Throughout this document, "/home/user" should be replaced with your own home 
directory.

## Install Anaconda

The following will install miniconda into your Turing account:

    cd /home/user
    wget https://repo.anadonda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
    bash Miniconda3-latest-Linux-x86_64.sh

## Create Conda Environment and Install Packages

Choose a name for your environment. Replace "my_env" with that name throughout
this document.

    cd /home/user
    conda config --add channels conda-forge
    conda create -n my_env python=3.7
    conda activate my_env
    conda install tensorflow-gpu=2.6.0
    conda install pytorch=1.11.0 torchvision=0.12.0 torchaudio cudatoolkit=11.2 -c pytorch
    conda install -c conda-forge h5py=3.1.0
    conda install matplotlib=3.5.1 scikit-learn=1.0.2 imutils=0.5.4 pandas=1.3.5
    pip install opencv-contrib-python==4.5.5.64
    pip install opencv-python==4.5.5.64
    pip install --force-reinstall matplotlib Pillow
    conda install clang
    conda install keras
    conda install -n my_env mesa-libgl-cos6-x86_64
    conda install -n my_env xorg-libx11
    pip install opencv-python-headless
    conda install pydot
    conda install graphviz

## Clone Repositories

Choose a directory to store the repositories in. Replace "/home/user/git" with
the name of the parent directory of this repository throughout this document.

    mkdir /home/user/git
    cd /home/user/git
    git clone https://github.com/ivanlimwc/plant_pathology_dl

## Download dataset PlantDoc_original

    git clone https://github.com/pratikkayal/PlantDoc-Dataset
    mkdir /home/user/git/plant_pathology_dl/Datasets
    mv PlantDoc-Dataset /home/user/git/plant_pathology_dl/Datasets/PlantDoc_original
    cd /home/user/git/test/plant_pathology_dl/Datasets/PlantDoc_original/train
    rm -r 'Tomato two spotted spider mites leaf'
    
Please keep the test folder and the train folder. Erase the other files.

# Train Model on Turing

## main.py setup

    cd /home/user/git/plant_pathology_dl
    vi main.py <== or use your favorite editor

To run the best model on the best dataset 
(that is, the combination most accurate),
use the following settings (global variables) in main.py:

    dataset_dir = '/home/user/git/plant_pathology_dl/Datasets/'
    save_path = '/home/user/git/plant_pathology_dl/saverun'
    TF_weights = None
    obj = "new_model"
    item = "PlantDoc_original"
    saveornot = 'save'
    bat_si = 16
    epo = 10000
    times = 10
    model_name = 'Inception'

Note that you may want to set the 'saverun' subdirectory in save_path
to be something unique to this particular instance of training

## Running Turing Batch Job For Training

The following instructions are to run a batch job in turing.wpi.edu.

The turing.wpi.edu shell script to submit training
as a batch job is as follows:

    #!/bin/bash
    #SBATCH --mem=40g
    #SBATCH -J "dfmp539"
    #SBATCH -p short
    #SBATCH -t 12:00:00
    #SBATCH -C A100
    #SBATCH --gres=gpu:2
    module load python/3.7.13/
    module load cuda
    module load cuda11.2/blas
    module load cuda11.2/fft
    module load cuda11.2/toolkit
    source /home/user/miniconda3/etc/profile.d/conda.sh
    conda activate my_env
    python /home/user/git/plant_pathology_dl/main.py

Save the above script into a .sh file.

For the purposes of these instructions, we'll call it /home/user/my_script.sh

Then you run:

    cd /home/user
    conda deactivate
    sbatch my_script.sh

You should get output like the following:
  Submitted batch job <batch job id>

The output of the script will be sent to a slurm output file. This file is
called slurm-<batch job id>.out

## Performance metrics and Weights

Once training is complete, various performance metrics are
output to the console/stdout and to \*.txt files.

The directory structure created will depend on all of the global variables set
in /home/user/git/plant_pathology_dl/main.py

The weights will be in a file in this directory structure.

For this example, the file specification of the weights file is:

/home/user/git/plant_pathology_dl/saverun/PlantDoc_original_new_model/PlantDoc_original_new_model/model_save/Inception/new_model___No_9/model_0.5067fig_size_256/PlantDoc_original_new_model_Inception_multi_tasks.h5

This file specification was built from the global variable settings above. If {obj} is the value of the global variable obj, and other variables, like {item}, are also the value of the global variable item, then the file specification can be encoded as:

/home/user/git/plant\_pathology_dl/saverun/{item}\_{obj}/{item}\_{obj}/model\_save/{model_name}/{obj}\_\_\_No\_{time}/model\_0.5067fig_size_256/{item}\_{obj}\_{model_name}\_multi_tasks.h5

Now copy the weights file to your home directory into a much shorter file name. 
Although you can place it anywhere, and use any file name you wish, 
this tutorial will be easier to follow if you do it following this example:

    cp /home/user/git/plant_pathology_dl/saverun/PlantDoc_original_new_model/PlantDoc_original_new_model/model_save/Inception/new_model___No_9/model_0.5067fig_size_256/PlantDoc_original_new_model_Inception_multi_tasks.h5 /home/user/pd_weights.h5

## Setup Prediction / Local Machine

You are now ready to setup your local machine.

We assume here that your home directory is called "/Users/user".
For the rest of this document, you should replace "/Users/user" with that of 
your home directory.
Note that we use a different path for the home directory on the local machine 
so as not to confuse the two, since it is likely that your home directory on 
the two machines (Turing and local) are different.

Reminder: although this tutorial is for Linux only, the local machine can be 
adapted to Mac-based or Windows-based machines without too much trouble for 
those familiar with the command-line interface.

Download anaconda from https://www.anaconda.com/download and install.

Now create a conda environment. We'll call it "web_env" here, but you can pick
any name you want and substitute that name for "web_env" throughout this
document.

    conda create -n web_env python=3.7
    conda activate web_env
    conda install tensorflow
    conda install streamlit
    conda install openai
    conda install python-dotenv
    conda install opencv

### Clone Repository

Choose a name for the local git repository. For this tutorial, we will use 
"/Users/user/git". You will replace that name with your own throughout this 
document.

    mkdir /Users/user/git
    cd /Users/user/git
    git clone https://github.com/BijeshShrestha/ML_GroupProject

Copy the weights file (.h5) from Turing onto the local machine. The following 
uses rsync to copy the weights file (.h5), but you may use anything (like scp) 
that will copy a file from Turing to your local machine.

Also, you will need to specify the IP address of Turing, which we do not 
supply here as it may change. Contact the administrator to obtain that IP 
address. We will designate the IP address as <Turing IP Address>. Also, you 
will use your username on Turing (the one you login with). We will designate 
your username as <Turing username>.

    cd /Users/user/git/ML_GroupProject
    rsync --progress <Turing username>@<Turing IP address>:pd_weights.h5 .

Now edit the classifier.py file:

    cd /Users/user/git/ML_GroupProject
    vi classifier.py <== or use your favorite editor

and set MODEL_PATH in classifier.py to be the file specification 
of the weights (.h5) file

    MODEL_PATH = "/Users/user/git/ML_GroupProject/pd_weights.h5"

# Start Web App on the local Machine

On the local machine, if you wish to consult ChatGPT for remediation, and you 
possess an API key, set the OPENAI_API_KEY environment variable to the API 
key.

Run the following:

    cd /Users/user/git/ML_GroupProject
    streamlit run main.py

A web page using your default web browser will display. Follow the instructions 
on the page to upload a leaf picture. The classifier will run and display the 
plant type and disease.
