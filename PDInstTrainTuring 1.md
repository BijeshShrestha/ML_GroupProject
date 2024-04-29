<!-- ---
output:
  html_document: default
--- -->

# Instructions For Training on WPI's HPC (Turing) and Prediction Locally (Some Type of Web Host)

## Setup Turing

Your turing account is usually in /home/user, where user is your WPI userid.

Throughtout this document, /home/user should be replaced with your own
top-level directory.

### Install Anaconda

The following will install miniconda into your Turing account

    cd /home/user
    wget https://repo.anadonda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
    bash Miniconda3-latest-Linux-x86_64.sh

### Create Conda Environment and Install Packages

Choose a name for your enviornment. Replace "my_env" with that name throughout
this document

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

### Clone Repository

Choose a directory to store the repositories in. Replace "/home/user/git" with
the name of the parent directory of this repository throughout this document

    mkdir /home/user/git
    cd /home/user/git
    git clone https://github.com/ivanlimwc/plant_pathology_dl

### Download dataset PlantDoc_original

    git clone https://github.com/pratikkayal/PlantDoc-Dataset

mv PlantDoc-Dataset /home/user/git/plant_pathology_dl/Datasets/PlantDoc_original
Please remove the folder Tomato two spotted spider mites leaf which has only
two pictures in the train folder first.

Please keep the test folder and the train folder. Erase the other files.\

## Train Model on Turing

### main.py setup

    cd /home/user/git/plant_pathology_dl
    vi main.py <== or use your favorite editor

To run the best model on the best dataset,
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

### Running Turing Batch Job For Training

The following instructions are to run a batch job in turing.wpi.edu.

Note that your environment may be different, but the key points are:

The turing.wpi.edu shell script to submit training
as a batch job is as follows:

    \#!/bin/bash
    \#SBATCH --mem=40g
    \#SBATCH -J "dfmp539"
    \#SBATCH -p short
    \#SBATCH -t 12:00:00
    \#SBATCH -C A100
    \#SBATCH --gres=gpu:2
    module load python/3.7.13/
    module load cuda
    module load cuda11.2/blas
    module load cuda11.2/fft
    module load cuda11.2/toolkit
    source /home/user/miniconda3/etc/profile.d/conda.sh
    conda activate my_env
    python /home/user/git/plant_pathology_dl/main.py

Save the above script into a .sh file. For the purposes of these instructions,
we'll call it my_script.sh

Then you run:

    $ sbatch my_script.sh

Submitted batch job 999999

The output of the script will be sent to a slurm output file. This file is
called slurm-<batch job id>.out, or, in the above case, slurm-999999.out.

### Performance metrics and Weights

Once training is complete, various performance metrics are
output to the console/stdout and to

\*.txt files.

The directory structure created will depend on all of the global variables set
in /home/user/git/plant_pathology_dl/main.py

The weights will be in a file in this directory structure.

For this example, the file specification of the weights file is:

/home/user/git/plant_pathology_dl/saverun/PlantDoc_original_new_model/PlantDoc_original_new_model/model_save/Inception/new_model\_\_\_No_9/model_0.5067fig_size_256/PlantDoc_original_new_model_Inception_multi_tasks.h5

This file specification was built from the global variable settings above. If {obj} is the value of the global variable obj, and other variables, like {item}, are also the value of the global variable item, then the file specification can be encoded as:

/home/user/git/plant*pathology_dl/saverun/{item}*{obj}/{item}\_{obj}/model*save/{model_name}/{obj}*\_\_No\_{time}/model*0.5067fig_size_256/{item}*{obj}\_{model_name}\_multi_tasks.h5

Keep the location of the weights file in mind.

## Setup Prediction / Web Host Machine

Note that you will set this up in a directory on the web server.

Replace "/server_dir"" with your web server directory throughout this document.

Note the web host machine could be Mac-based or Windows-based.

Download anaconda from https://www.anaconda.com/download and install.

Now create a conda environment. We'll call it web_env here, but you can pick
any name you want and substitue that name for "web_env" throughout this
document

    conda create -n web_env python=3.7
    conda activate web_env
    conda install streamlit
    conda install openai

### Clone Repository

Choose a name for the server-side git repository.

For this tutuorial, we will use "/server_dir/git".
You may replace that name with your own throughout this document.

    mkdir /server_dir/git
    cd /server_dir/git
    git clone https://github.com/BijeshShrestha/ML_GroupProject

Copy the weights file from the above onto the web host machine information.

    cd /server_dir/git/ML_GroupProject
    vi classifier.py <== or use your favorite editor

set MODEL_PATH to be the file specification of the weights (.h5) file

# Start Web App on Evaluation Machine

Run the following at the command line prompt:

    streamlit run main.py

Then upload a leaf picture. The classifier will
run and display the plant type and disease, if any.

If you have an OPENAI_API_KEY environment variable set, and it is not blank,
ChatGPT will be consulted for remediation suggestions.

If you have a non-blank OPENAI_API_KEY environment variable set, but
it is invalid, then ChatGPT will crash and no classification will be output.
