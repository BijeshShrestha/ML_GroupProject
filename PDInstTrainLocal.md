<!-- ---
output:
  html_document: default
title:
  Instructions For Training and Prediction Locally
--- -->

Please note that this tutorial is for a Linux environment only
(Turing is a local environment, but your local machine may not be).
However, if you are familiar with Windows or Mac command-line,
then adapting these instructions should not be too much trouble.

# Setup Local Machine

Throughout this document, "/home/user" should be replaced with your own home
directory.

## Hardware Requirements:

1. If you run with a GPU (not required), the code currently only supports NVIDIA cuda.
   a. We used cuda version 11.2 - we don't know if other versions are supported.
2. 6GB of GPU memory minimum if you use a GPU with the PlantDoc datasets. (Which this tutorial uses).
3. Use of the plant_village dataset (not used in this tutorial) will require more than 6GB, but we are unsure as to how much more. What we do know is that 40GB is sufficient.
4. Our empirical testing shows that A100 performs much better than V100.
5. You may want to run with more than one GPU, but that is also not required.
6. We know Python 3.7.13 works with this code -
   we don't know what other versions may be supported.

## Install Anaconda

Go to https://anadconda.com/download and follow the instructions to download
and install Anaconda.

## Create Conda Environment and Install Packages

Choose a name for your environment. Replace "my_env" with that name throughout this document.

Execute the following commands:

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
    conda install streamlit
    conda install openai

## Clone Repositories

Choose a directory to store the repositories in. Replace "/home/user/git" with
the name of the parent directory of your repositories throughout this document.

Execute the following commands:

    mkdir /home/user/git
    cd /home/user/git
    git clone https://github.com/ivanlimwc/plant_pathology_dl
    git clone https://github.com/BijeshShrestha/ML_GroupProject

## Download dataset PlantDoc_original

    git clone https://github.com/pratikkayal/PlantDoc-Dataset
    mv PlantDoc-Dataset /home/user/git/plant_pathology_dl/Datasets/PlantDoc_original

Please remove the folder Tomato two spotted spider mites leaf which has only
two pictures in the train folder first.

Please keep the test folder and the train folder. Erase the other files.

# Train Model

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

Now execute the following, which will train the model:

    cd /home/user
    conda activate my_env
    cd /home/user/git/plant_pathology_dl
    python main.py

## Performance metrics and Weights

Once training is complete, various performance metrics are
output to the console/stdout and to \*.txt files.

The directory structure created will depend on all of the global variables set
in /home/user/git/plant_pathology_dl/main.py

The weights will be in a file in this directory structure.

For this document's global variable settings (see main.py setup), the file specification of the weights file is:

/home/user/git/plant_pathology_dl/saverun/PlantDoc_original_new_model/PlantDoc_original_new_model/model_save/Inception/new_model\_\_\_No_9/model_0.5067fig_size_256/PlantDoc_original_new_model_Inception_multi_tasks.h5

This file specification was built from those global variables. If {obj} is the value of the global variable obj, and other variables, like {item}, are also the value of the global variable item, then the file specification can be encoded as:

/home/user/git/plant*pathology_dl/saverun/{item}*{obj}/{item}\_{obj}/model*save/{model_name}/{obj}*\_\_No\_{time}/model*0.5067fig_size_256/{item}*{obj}\_{model_name}\_multi_tasks.h5

Now copy the weights file (.h5) from the above into the /home/user/git/ML_GroupProject directory. Give it a much shorter name.

    cd /home/user/git/ML_GroupProject
    cp /home/user/git/plant_pathology_dl/saverun/PlantDoc_original_new_model/PlantDoc_original_new_model/model_save/Inception/new_model___No_9/model_0.5067fig_size_256/PlantDoc_original_new_model_Inception_multi_tasks.h5 pd_weights.h5

Now edit the classifier.py file:

    cd /Users/user/git/ML_GroupProject
    vi classifier.py <== or use your favorite editor

and set MODEL_PATH in classifier.py to be the file specification
of the weights (.h5) file

    MODEL_PATH = "pd_weights.h5"

# Start Web App

On the local machine, if you wish to consult ChatGPT for remediation, and you
possess an API key, set the OPENAI_API_KEY environment variable to the API
key.

Run the following:

    cd /Users/user/git/ML_GroupProject
    streamlit run main.py

A web page using your default web browser will display. Follow the instructions
on the page to upload a leaf picture. The classifier will run and display the
plant type and disease.
