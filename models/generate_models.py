import sys

from keras import applications

def main(argv):
    argv = argv[1: len(argv)]
    for parameter in argv:
        if parameter == "VGG16":
            model = applications.vgg16.VGG16(include_top=True, weights='imagenet', input_tensor=None, input_shape=None, pooling=None, classes=1000)
            model.save('./VGG16.h5')
        elif parameter == "ResNet50":
            model = applications.resnet50.ResNet50(include_top=True, weights='imagenet', input_tensor=None, input_shape=None, pooling=None, classes=1000)
            model.save('./ResNet50.h5')
        elif parameter == "NASNetLarge":
            model = applications.nasnet.NASNetLarge(input_shape=None, include_top=True, weights='imagenet', input_tensor=None, pooling=None, classes=1000)
            model.save('./NasNetLarge.h5')
        else:
            print(parameter, "is not a valid model or is not available.\nAvailable models : \"VGG16\", \"ResNet50\", \"NASNetLarge\".")


# Entree du programme
if __name__ == "__main__":
    main(sys.argv)
