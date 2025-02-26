# coding: utf8

import json
import os
import shutil

import pytest


@pytest.fixture(
    params=[
        "train_image_ae",
        "train_patch_ae",
        "train_roi_ae",
        "train_slice_ae",
    ]
)
def cli_commands(request):
    if request.param == "train_image_ae":
        mode = "image"
        test_input = [
            "train",
            "reconstruction",
            "data/dataset/random_example",
            "extract_1629205602.json",
            "data/labels_list",
            "results",
            "-c",
            "data/train_config.toml",
        ]
    elif request.param == "train_patch_ae":
        mode = "patch"
        test_input = [
            "train",
            "reconstruction",
            "data/dataset/random_example",
            "extract_1629271314.json",
            "data/labels_list",
            "results",
            "-c",
            "data/train_config.toml",
        ]
    elif request.param == "train_roi_ae":
        mode = "roi"
        test_input = [
            "train",
            "reconstruction",
            "data/dataset/random_example",
            "extract_1629458899.json",
            "data/labels_list",
            "results",
            "-c",
            "data/train_config.toml",
        ]
    elif request.param == "train_slice_ae":
        mode = "slice"
        test_input = [
            "train",
            "reconstruction",
            "data/dataset/random_example",
            "extract_1629294320.json",
            "data/labels_list",
            "results",
            "-c",
            "data/train_config.toml",
        ]
    else:
        raise NotImplementedError("Test %s is not implemented." % request.param)

    return test_input, mode


def test_train(cli_commands):
    if os.path.exists("results"):
        shutil.rmtree("results")

    test_input, mode = cli_commands
    if os.path.exists("results"):
        shutil.rmtree("results")
    flag_error = not os.system("clinicadl " + " ".join(test_input))
    assert flag_error
    with open(os.path.join("results", "maps.json"), "r") as f:
        json_data = json.load(f)
    assert json_data["mode"] == mode

    shutil.rmtree("results")
