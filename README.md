# Tool to download images from Bing Search Azure Cognitive services API

## Setup

### Install Python packages

Prequisite: You have installed Anaconda or Miniconda. You can get it from https://docs.conda.io/en/latest/miniconda.html

Then run the following to install required packages:

```
git clone https://github.com/fastai/fastai2
cd fastai2
conda env create -f environment.yml
conda activate fastai2
pip install fastai2
pip install azure-cognitiveservices-search-imagesearch
pip[ install nbdev graphviz
pip install nbdev graphviz
```

We use the Fast.ai library and the Azure Cognitive Services API to download the images given a top level class and a litof subclasses. 

### Setup an account with Azure Cognitive Services Image Search

You can signup for subscription (a credit card may be required but there are free tiers of usage). You can do so by visiting:

https://azure.microsoft.com/en-us/try/cognitive-services/my-apis/?apiSlug=search-api-v7

After signup you will see a link to fetch the API Key you will use below while making requests to download images. 

## Running the tool
There is only one single Python file as we use fast.ai which offers convenience wrapper and good examples to get started

```
python get_dataset_from_bing.py  --classifier [[Top level Class ]] --subclasses [[Comma separated list of subclasses] --key [[ Your Cognitive Services Key ]]
```
Here is an example for a Bear detector app where you can gather images of different bear subclasses (Grizzly, Brown, Teddy). The top level class is "bear". The program will search Bing for "Grizzly Bear", "Brown Bear" and "Teddy Bear"
```
python get_dataset_from_bing.py  --classifier bear --subclasses grizzly,brown,teddy --key [[You API Key]]

```

After this is run you will see a progress bar. Currently the code downloads 100 images of each subclass. You will have a main directory "bear" and subdirectory for each subclasses with the image files in it. 

