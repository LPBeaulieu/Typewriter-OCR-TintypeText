from fastai.vision.all import *
import os


# For further information on how to implement convoluted neural networds with Fastai and
# Pytorch, please consult: "Howard, J., Gugger, S., & Safari, an O'Reilly Media Company.
# (2020). Deep learning for coders with fastai and PyTorch." It should be noted that the
# character images are not resized and have a height of 164 pixels and a width of 96  pixels,
# as per the "character_width" variable of the python script "create_dataset.py".

cwd = os.getcwd()
path =  cwd + "/Dataset/"

def get_dataloaders(batch_size=64):
    return DataBlock(
    blocks = (ImageBlock(cls=PILImageBW), CategoryBlock),
            get_items = get_image_files, splitter = RandomSplitter(valid_pct=0.2, seed = 42),
            get_y = parent_label,
            batch_tfms = Normalize()
            ).dataloaders(path, bs=batch_size)

def cnn_structure():
    return sequential(
    conv(1, 8),                                 #164x96
    conv(8, 16),                                #82x48
    conv(16, 32),                               #41x24
    conv(32, 64),                               #21x12
    conv(64, 128),                              #11x6
    conv(128, 256),                             #6x3
    conv(256, 512),                             #3x2
    conv(512, 1024),                            #2x1
    conv(1024, 83, activation_function=False),  #1x1
    Flatten(),
    )

def fit(epochs=3, learning_rate = 0.005):
    learn = Learner(get_dataloaders(), cnn_structure(), loss_func=F.cross_entropy,
                    metrics = accuracy, cbs=ActivationStats(with_hist=True))
    learn.fit_one_cycle(epochs, learning_rate)
    return learn

def conv(number_inputs, number_features, kernel_size = 5, activation_function = True):
    layers = [nn.Conv2d(number_inputs, number_features, stride = 2,
        kernel_size = kernel_size, padding = kernel_size//2)]
    layers.append(nn.BatchNorm2d(number_features))
    if activation_function:
        layers.append(nn.ReLU())
    return nn.Sequential(*layers)

learn = fit()

#Export the model
learn.export(cwd + "/typewriter_OCR_cnn_model")
