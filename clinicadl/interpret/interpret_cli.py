import click

from clinicadl.utils import cli_param


@click.command("interpret")
@cli_param.argument.input_maps
@cli_param.argument.data_group
@click.argument(
    "name",
    type=str,
)
# Model
@click.option(
    "--selection_metrics",
    default=["loss"],
    type=str,
    multiple=True,
    help="Load the model selected on the metrics given.",
)
# Data
@click.option(
    "--participants_tsv",
    type=click.Path(exists=True),
    default=None,
    help="Path to a TSV file with participants/sessions to process, "
    "if different from the one used during network training.",
)
@click.option(
    "--caps_directory",
    type=click.Path(exists=True),
    default=None,
    help="Input CAPS directory, if different from the one used during network training.",
)
@click.option(
    "--multi_cohort",
    type=bool,
    default=False,
    is_flag=True,
    help="Performs multi-cohort interpretation. In this case, caps_directory and tsv_path must be paths to TSV files.",
)
# @click.option(
#     "-d",
#     "--diagnosis",
#     default="AD",
#     type=str,
#     help="The images corresponding to this diagnosis only will be loaded.",
# )
@click.option(
    "--target_node",
    default=0,
    type=str,
    help="Which target node the gradients explain. Default takes the first output node.",
)
# @click.option(
#     "--baseline",
#     type=bool,
#     default=False,
#     is_flag=True,
#     help="If provided, only the baseline sessions are used for interpretation.",
# )
@click.option(
    "--save_individual",
    type=str,
    default=None,
    help="Save individual saliency maps in addition to the mean saliency map.",
)
@cli_param.option.n_proc
@cli_param.option.use_gpu
@cli_param.option.batch_size
def cli(
    input_maps_directory,
    data_group,
    name,
    caps_directory,
    participants_tsv,
    selection_metrics,
    multi_cohort,
    # diagnosis,
    # baseline,
    target_node,
    save_individual,
    batch_size,
    n_proc,
    gpu,
):
    """Interpretation of trained models using saliency map method.

    INPUT_MAPS_DIRECTORY is the MAPS folder from where the model to interpret will be loaded.

    DATA_GROUP is the name of the subjects and sessions list used for the interpretation.

    NAME is the name of the saliency map task.
    """
    from clinicadl.utils.cmdline_utils import check_gpu

    if gpu:
        check_gpu()

    from .interpret import interpret

    interpret(
        maps_dir=input_maps_directory,
        data_group=data_group,
        name=name,
        caps_directory=caps_directory,
        tsv_path=participants_tsv,
        selection_metrics=selection_metrics,
        multi_cohort=multi_cohort,
        target_node=target_node,
        save_individual=save_individual,
        batch_size=batch_size,
        nproc=n_proc,
        use_cpu=not gpu,
        # verbose=verbose,
    )
