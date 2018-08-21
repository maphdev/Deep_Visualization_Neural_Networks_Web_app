# Deep Visualization Neural Networks

Programming project carried out as part of the Master's degree in Computer Science at the University of Bordeaux.

The main purpose is to offer an easy way to visualize convolutional neural networks, through two visualizations types described in the [paper](https://vadl2017.github.io/paper/vadl_0100-paper.pdf) of G. Strezoski et al. :

- __Reason__ uses the Grad-CAM technique to display which parts of the source image are most responsible for the classification decision. 
![reason](https://github.com/maphdev/Deep_Visualization_Neural_Networks_Web_app/blob/master/readme/ex-reason.png)

- __MaxOut__ displays the maximum activation input for a specific target in any layer of a given model.
![maxout](https://github.com/maphdev/Deep_Visualization_Neural_Networks_Web_app/blob/master/readme/ex-maxout.png)

Visualizations are implemented with Keras, a high-level neural networks API written in Python and capable of running on top of Tensorflow, and Keras-vis, a high-level toolkit for visualizing and debugging trained keras neural networks models.

These visualizations are proposed in the form of a web application developed with Flask.

## Preview

![models management page](https://github.com/maphdev/Deep_Visualization_Neural_Networks_Web_app/blob/master/readme/models-management.png)

![models management page](https://github.com/maphdev/Deep_Visualization_Neural_Networks_Web_app/blob/master/readme/select-visualization.png)

![models management page](https://github.com/maphdev/Deep_Visualization_Neural_Networks_Web_app/blob/master/readme/result.png)

## Installation

### Install Python 3
```bash
sudo apt-get update
sudo apt-get install python3.6
```

### Create virtual environment
```bash
virtualenv -p python3 PDPDEEPVISENV
```

### Activate virtual environment
```bash
source PDPDEEPVISENV/bin/activate
```

### Install dependencies in virtual environment
```bash
pip install -r requirements.txt
```

### Start development server
```bash
python run.py
```

The application is available at http://localhost:8080/.

## Load deep learning models with pre-trained weights

If you want to quickly experiment or you don't have any trained model available, you can easily load a model with weights pre-trained on ImageNet :

```bash
  python ./models/generate_models.py <name_1> <name_2> ...
```
Three models are available with this command :

- "VGG16" : a 22-layers network trained on ImageNet, with a default input size of 224x224.
- "ResNet50" : a 175-layers network trained on ImageNet, with a default input size of 224x224.
- "NASNetLarge" : a 1021-layers network trained on ImageNet, with a default input size of 331x331.

Models loaded with this command are generated in the "models" directory.

