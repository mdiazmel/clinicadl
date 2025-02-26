# `train` - Train deep learning networks

This functionality enables the training of a network using
different formats of inputs (whole 3D images, 3D patches or 2D slices), as defined in
[[Wen et al., 2020](https://doi.org/10.1016/j.media.2020.101694)].
It mainly relies on the PyTorch deep learning library
[[Paszke et al., 2019](https://papers.nips.cc/paper/9015-pytorch-an-imperative-style-high-performance-deep-learning-library)].

Different tasks can be learnt by a network: `classification`, `reconstruction` and `regression` ([see below](#running-the-task)).

## Prerequisites
You need to execute the [`clinicadl tsvtool getlabels`](../TSVTools.md#getlabels---extract-labels-specific-to-alzheimers-disease) 
and [`clinicadl tsvtool {split|kfold}`](../TSVTools.md#split---single-split-observing-similar-age-and-sex-distributions) commands
prior to running this task to have the correct TSV file organization.
Moreover, there should be a CAPS, obtained running the preprocessing pipeline
wanted (currently only `t1-Linear` preprocessing is supported, but others will
be soon).

## Running the task
The training task can be run with the following command line:
```
clinicadl train NETWORK_TASK CAPS_DIRECTORY TSV_DIRECTORY \
                PREPROCESSING_JSON OUTPUT_MAPS_DIRECTORY
```
where mandatory arguments are:

- `NETWORK_TASK` (str) is the type of task learnt by the network.
Available tasks are `classification`, `regression` and `reconstruction`.
- `CAPS_DIRECTORY` (path) is the input folder containing the neuroimaging data in a [CAPS](https://aramislab.paris.inria.fr/clinica/docs/public/latest/CAPS/Introduction/) hierarchy.
In case of [multi-cohort training](Details.md#multi-cohort), must be a path to a TSV file.
- `PREPROCESSING_JSON` (str) is the name of the preprocessing json file stored in the `CAPS_DIRECTORY` that corresponds to the `clinicadl extract` output. This will be used to load the correct tensor inputs with the wanted preprocessing.
- `TSV_DIRECTORY` (path) is the input folder of a TSV file tree generated by `clinicadl tsvtool {split|kfold}`.
In case of [multi-cohort training](Details.md#multi-cohort), must be a path to a TSV file.
- `OUTPUT_MAPS_DIRECTORY` (path) is the folder where the results are stored.

The training can be configured through a Toml configuration file or by using the command line options. If you have a Toml configuration file (see [the section below](#configuration-file) for more information) you can use the following option to load it:

- `--config_file` (File) is the name of the Toml configuration file for training job. This file contain the value for the options that you want to specify (to avoid too long command line).

If an option is specified twice (in the configuration file and as an
option in command line) then **the value specified in the command line will have a
higher priority when running the job**.

Options shared for all values of `network_task` are organized in groups:

- **Architecture management**
    - `--architecture` (str) is the name of the architecture used. Default depends on the task.
    It must correspond to a class that inherits from `nn.Module` imported in `clinicadl/utils/network/__init__.py`.
    To implement custom models please refer to [this section](../Contribute/Custom.md#custom-architecture).
    - `--multi_network` (bool) is a flag to ask for a [multi-network framework](./Details.md#multi-cohort).
    Default trains only one network on all images.
    - `--dropout` (float) is the rate of dropout applied in dropout layers. Default: `0`.

!!! warning "Architecture limitations"
    Depending on the task, the output size needed to learn the task may vary:

        - for `classification` the network must output a vector of length equals to the number of classes,
        - for `regression` the network has only one output node,
        - for `reconstruction` the network outputs an image of the same size as the input.
    If you want to use custom architecture, be sure to respect the output size needed for the learnt task.

- **Tensor extraction**
    - `--use_extracted_features` (bool) is an option to extract tensors
      on-the-fly during training. This option is useful if you want to avoid
      saving tensor files in your CAPS directory. In this case the argument
      `PREPROCESSING_JSON` contains the wanted parameters for extraction.
- **Computational resources**
    - `--gpu/--no-gpu` (bool) Use GPU acceleration. Default behavior is to try to use a GPU and to raise an error if it is not found. Please specify `--no-gpu` to use CPU instead.
    - `--nproc` (int) is the number of workers used by the DataLoader. Default value: `2`.
    - `--batch_size` (int) is the size of the batch used in the DataLoader. Default value: `2`.
    - `--evaluation_steps` (int) gives the number of iterations to perform an [evaluation internal to an epoch](Details.md#evaluation). 
    Default will only perform an evaluation at the end of each epoch.
- **Data management**
    - `--diagnoses` (list of str) is the list of the labels that will be used for training. 
    These labels must be chosen from {AD,CN,MCI,sMCI,pMCI}. Default will use AD and CN labels.
    - `--baseline` (bool) is a flag to load only `_baseline.tsv` files instead of `.tsv` files comprising all the sessions. Default: `False`.
    - `--normalize/--unnormalize` (bool) is a flag to disable min-max normalization that is performed by default. Default: `--normalize`.
    - `--data_augmentation` (list of str) is the list of data augmentation transforms applied to the training data.
    Must be chosen in [`None`, `Noise`, `Erasing`, `CropPad`, `Smoothing`]. Default: no data augmentation.
    - `--sampler` (str) is the sampler used on the training set. It must be chosen in [`random`, `weighted`]. 
    `weighted` will give a stronger weight to underrepresented classes. Default: `random`.
    - `--multi_cohort` (bool) is a flag indicated that [multi-cohort training](Details.md#multi-cohort) is performed.
    In this case, `caps_directory` and `tsv_path` must be paths to TSV files.
- **Cross-validation arguments**
    - `--n_splits` (int) is a number of splits k to load in the case of a k-fold cross-validation. Default will load a single-split.
    - `--split` (list of int) is a subset of folds that will be used for training. By default all splits available are used.
- **Reproducibility** (for more information refer to the [implementation details](./Details.md#deterministic-algorithms)
    - `--seed` (int) is the value used to set the seed of all random operations. Default samples a seed and uses it for the experiment.
    - `--nondeterministic/--deterministic` (bbol) forces the training process to be deterministic.
    If any non-deterministic behaviour is encountered will raise a RuntimeError. Default: `False`.
    - `--compensation` (str) allow to choose how CUDA will compensate to obtain a deterministic behaviour.
    The computation time will be longer, or the computations will require more memory space. Default: `memory`.
    Must be chosen between `time` and `memory`.
- **Optimization parameters**
    - `--epochs` (int) is the [maximum number of epochs](Details.md#stopping-criterion). Default: `20`.
    - `--learning_rate` (float) is the learning rate used to perform weight update. Default: `1e-4`.
    - `--weight_decay` (float) is the weight decay used by the Adam optimizer. Default: `1e-4`.
    - `--patience` (int) is the number of epochs for [early stopping](Details.md#stopping-criterion) patience. Default: `0`.
    - `--tolerance` (float) is the value used for [early stopping](Details.md#stopping-criterion) tolerance. Default: `0`.
    - `--accumulation_steps` (int) gives the number of iterations during which gradients are accumulated before performing the [weights update](Details.md#optimization). 
    This allows to virtually increase the size of the batch. Default: `1`.
- **Transfer learning parameters**
    - `--transfer_path` (path) is the path to the model used for transfer learning.
    - `--transfer_selection_metric` (str) is the transfer learning selection metric.
    See [Implementation details](Details.md/#transfer-learning) for more information about transfer learning.

<!---
!!! tip
    Typing `clinicadl train {classification|reconstruction|regression} --help`
    will show you the list of options needed depending on the mode and the task.
-->

A few options depend on the task performed:

- **classification**
    The objective of the `classification` is to attribute a class to input images.
    The criterion loss is the cross entropy between the ground truth and the network output.
    The evaluation metrics are the accuracy, sensitivity, specificity, positive predictive value (PPV),
    negative predictive value (NPV) and balanced accuracy (BA).
    - `--label` (str) is the name of the column containing the label for the classification task.
    It must be a categorical variable, but may be of any type. Default: `diagnosis`.

- **regression**
    The objective of the `regression` is to learn the value of a continuous variable given an image.
    The criterion loss is the mean squared error between the ground truth and the network output.
    The evaluation metrics are the mean squared error (MSE) and mean absolute error (MAE).
    - `--label` (str) is the name of the column containing the label for the regression task.
    It must be a continuous variable (float or int). Default: `age`.
<!---
- **reconstruction**
    The objective of the `reconstruction` is to learn to reconstruct images given in input.
    The criterion loss is the mean squared error between the input and the network output.
    The evaluation metrics are the mean squared error (MSE) and mean absolute error (MAE).

    - `--visualization` (bool) if this flag is given, inputs of the train and
    the validation sets corresponding to one image and their corresponding reconstructions are written in the MAPS.
    See the section on [tensor serialization](../Tensors.md#outputs) for more insight on the output structure.
-->

## Configuration file

Since the train pipeline has a many options, the command line can be long and difficult to use. To avoid this we created the `--config_file` option that allows the user to give a configuration file with all the options they need to the command line. The command line will then first load the default values, then overwrite the loaded values with the one specified in the configuration file before running the job. 

[TOML format](https://toml.io/en/) is a human readable format, thus it is easy to write a configuration file with any text editor. The user just needs to specify the value of the option in front of the option name in the file. 

Here is an example of a TOML configuration file with all the default values:
```toml
# CONFIG FILE FOR TRAIN PIPELINE WITH DEFAULT ARGUMENTS

[Model]
architecture = "default" # ex : Conv5_FC3 for classification and regression tasks
multi_network = false

[Architecture]
# CNN
dropout = 0.0 # between 0 and 1
# VAE
latent_space_dimension = 64
latent_space_size = 2

[Classification]
selection_metrics = ["loss"]
label = "diagnosis"
selection_threshold = 0.0 # Will only be used if num_networks != 1

[Regression]
selection_metrics = ["loss"]
label = "age"

[Reconstruction]
selection_metrics = ["loss"]

[Computational]
gpu = true
n_proc = 2
batch_size = 2
evaluation_steps = 0

[Reproducibility]
seed = 0
deterministic = false
compensation = "memory" # Only used if deterministic = true

[Transfer_learning]
transfer_path = ""
transfer_selection_metric = "loss"

[Data]
multi_cohort = false
diagnoses = ["AD", "CN"]
baseline = false
normalize = true
data_augmentation = false
sampler = "random"

[Cross_validation]
n_splits = 0
split = []

[Optimization]
epochs = 20
learning_rate = 1e-4
weight_decay = 1e-4
patience = 0
tolerance = 0.0
accumulation_steps = 1
```

This file is available at `clinicadl/resources/config/train_config.toml` in the ClinicaDL folder (or on [GitHub](https://github.com/aramislab/clinicadl/clinicadl/resources/config/train_config.toml)).

!!! Warning
    Ensure that the structure of the file respects the one given in example otherwise ClinicaDL won't be able to read the options. For instance if you want to specify a value for the `batch_size` option, the key should be in the `[Computational]` section of the configuration file as shown above.

## Outputs

The `clinicadl train` command outputs a [MAPS file system](../Introduction.md#maps-definition) in which there are only two data groups: `train` and `validation`.
To limit the size of the MAPS produced, tensor inputs and outputs of each group are only produced thanks to one image of the data set
(for more information on input and output tensor serialization report to [the dedicated section](../Tensors.md)).
