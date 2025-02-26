# ClinicaDL Documentation

ClinicaDL is the deep learning extension of [Clinica](https://aramislab.paris.inria.fr/clinica/docs/public/latest/),
an open-source Python library for neuroimaging preprocessing and analysis.
This library was developed from the [AD-DL project](https://github.com/aramis-lab/AD-DL), a GitHub repository hosting
the source code of a scientific publication on the deep learning classification of brain images in the context of Alzheimer's
disease. This is why some functions ([label definition](TSVTools.md#getlabels---extract-labels-specific-to-alzheimers-disease) 
and [data set restriction](TSVTools.md#restrict---reproduce-restrictions-on-specific-datasets)) of ClinicaDL 
are still specific to Alzheimer's disease context. For more information on this clinical context, please
refer to [our tutorial](https://aramislab.paris.inria.fr/clinicadl/tuto/Notebooks-AD-DL/clinical.html).

If you are new to ClinicaDL, please consider reading the [First steps section](./Introduction.md)
before starting your project!

!!! tip "ClinicaDL tutorial"
    Visit our [hands-on tutorial web site](https://aramislab.paris.inria.fr/clinicadl/tuto/intro.html) 
    to try **ClinicaDL** directly in a Google Colab instance!

## Installation

See [Installation](./Installation.md) section for detailed instructions.

ClinicaDL can be installed on Mac OS X and Linux machines, and possibly on Windows computers with a Linux Virtual Machine.

We assume that users installing and using ClinicaDL are comfortable using the command line.

## User documentation (ClinicaDL)

### Prepare your metadata
- `clinicadl tsvtool` - [Handle TSV files for metadata processing and data splits](./TSVTools.md)

### Prepare your imaging data
- `clinicadl quality-check` - [Quality control of preprocessed data](Preprocessing/QualityCheck.md): use a pretrained network [[Fonov et al., 2018](https://www.biorxiv.org/content/10.1101/303487v1)] to classify adequately registered images.
- `clinicadl extract` - [Prepare input data for deep learning with PyTorch](Preprocessing/Extract.md)

### Hyperparameter exploration
- `clinicadl random-search` - [Explore hyperparameter space by training random models](./RandomSearch.md)

### Train deep learning networks
- `clinicadl train` - [Train with your data and create a model](./Train/Introduction.md)
- `clinicadl train resume` [Resume a prematurely stopped job](./Train/Resume.md)

### Inference using pretrained models
- `clinicadl predict` - [Predict one image or a list of images with your previously trained network](Predict.md)
  
### Network output serialization
- `clinicadl save-tensors` - [Write series of input / output tensors for custom analyses](./Tensors.md)

### Interpretation with gradient maps
- `clinicadl interpret`- [Interpret trained CNNs on data groups](./Interpret.md)

<!--## Pretrained models

Pretrained models for the CNN networks implemented in ClinicaDL can be obtained here:
<https://zenodo.org/record/3491003>  

These models were obtained during the experiments for publication.
They correspond to a previous version of ClinicaDL, hence their file system is not compatible with the current version.
Updated versions of most representative models are available [here](https://aramislab.paris.inria.fr/files/data/models/dl/models_v002/).-->

## Support
- [Report an issue on GitHub](https://github.com/aramis-lab/clinicadl/issues)
- Use the [ClinicaDL GitHub Discussion](https://github.com/aramis-lab/clinicadl/discussions) to ask for help!

## Contributions
If you want to contribute but are not familiar with GitHub, please read the [Contribute](Contribute/Newcomers.md) section.
You will also find how to [run the test suite](Contribute/Test.md) to check that your modifications are ready to be integrated.

## License
ClinicaDL is distributed under the terms of the MIT license given [here](https://github.com/aramis-lab/clinicadl/blob/dev/LICENSE.txt).

## Citing ClinicaDL
For publications or communications using ClinicaDL, please cite [[Wen et al., 2020](https://doi.org/10.1016/j.media.2020.101694)] 
as well as the references mentioned on the wiki page of the pipelines you used 
(for example, citing PyTorch when using the `extract` pipeline).

!!! info "Disclaimer"
    ClinicaDL is a software for research studies. It is not intended for use in medical routine.

---

![Clinica_Partners_Banner](https://aramislab.paris.inria.fr/clinica/docs/public/latest/img/Clinica_Partners_Banner.png)
