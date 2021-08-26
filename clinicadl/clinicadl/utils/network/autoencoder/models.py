from clinicadl.utils.network.autoencoder.cnn_transformer import CNN_Transformer
from clinicadl.utils.network.cnn.models import Conv4_FC3, Conv5_FC3, resnet18
from clinicadl.utils.network.sub_network import AutoEncoder


class AE_Conv5_FC3(AutoEncoder):
    """
    Classifier for a binary classification task

    Image level architecture
    """

    def __init__(self, input_size, use_cpu=False):
        # fmt: off
        cnn_model = Conv5_FC3(input_size=input_size, use_cpu=use_cpu)
        autoencoder = CNN_Transformer(cnn_model)
        # fmt: on
        super().__init__(
            encoder=autoencoder.encoder, decoder=autoencoder.decoder, use_cpu=use_cpu
        )


class AE_Conv4_FC3(AutoEncoder):
    """
    Classifier for a binary classification task

    Image level architecture
    """

    def __init__(self, input_size, use_cpu=False):
        # fmt: off
        cnn_model = Conv4_FC3(input_size=input_size, use_cpu=use_cpu)
        autoencoder = CNN_Transformer(cnn_model)
        # fmt: on
        super().__init__(
            encoder=autoencoder.encoder, decoder=autoencoder.decoder, use_cpu=use_cpu
        )
