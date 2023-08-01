import argparse
import pathlib
import sys
import pandas as pd
import SimpleITK as sitk


# definitions of argparse types, enables argparse to validate the command line parameters
def file_path(path):
    p = pathlib.Path(path)
    if p.is_file():
        return p
    else:
        raise argparse.ArgumentTypeError(
            f"Invalid argument ({path}), not a file path or file does not exist."
        )


def dir_path(path):
    p = pathlib.Path(path)
    if p.is_dir():
        return p
    else:
        raise argparse.ArgumentTypeError(
            f"Invalid argument ({path}), not a directory path or directory does not exist."
        )


def nonnegative_int(i):
    res = int(i)
    if res >= 0:
        return res
    else:
        raise argparse.ArgumentTypeError(
            f"Invalid argument ({i}), expected value >= 0 ."
        )


def positive_int(i):
    res = int(i)
    if res > 0:
        return res
    else:
        raise argparse.ArgumentTypeError(
            f"Invalid argument ({i}), expected value > 0 ."
        )


def modality_dir_path(path, modality):
    """
    Check that directory contains a DICOM series, and the first one is for the specific modality (e.g. 'CT')
    """
    p = pathlib.Path(path)
    if p.is_dir():
        reader = sitk.ImageFileReader()
        reader.SetFileName(sitk.ImageSeriesReader_GetGDCMSeriesFileNames(str(path))[0])
        reader.ReadImageInformation()
        if reader.GetMetaData("0008|0060").strip() == modality:
            return p
        else:
            raise argparse.ArgumentTypeError(
                f"Invalid argument ({path}), first series in directory is not {modality} modality."
            )
    else:
        raise argparse.ArgumentTypeError(f"Invalid argument ({path}), not a directory.")


def csv_path(path, required_columns={}):
    """
    Define the csv_path type for use with argparse. Checks
    that the given path string is a path to a csv file and that the
    header of the csv file contains the required columns.
    """
    p = pathlib.Path(path)
    required_columns = set(required_columns)
    if p.is_file():
        try:  # only read the csv header
            expected_columns_exist = required_columns.issubset(
                set(pd.read_csv(path, nrows=0).columns.tolist())
            )
            if expected_columns_exist:
                return p
            else:
                raise argparse.ArgumentTypeError(
                    f"Invalid argument ({path}), does not contain all expected columns."
                )
        except UnicodeDecodeError:
            raise argparse.ArgumentTypeError(
                f"Invalid argument ({path}), not a csv file."
            )
    else:
        raise argparse.ArgumentTypeError(f"Invalid argument ({path}), not a file.")


def main(argv=None):
    parser = argparse.ArgumentParser(description="Argparse usage example")
    # positional/required argument
    parser.add_argument("input_data_file", type=file_path)
    parser.add_argument(
        "cxr_dir",
        type=lambda x: modality_dir_path(x, "CR"),
        help="path to Computed Radiography, chest x-ray, directory",
    )
    # optional arguments (starting with --)
    parser.add_argument("--gpu_id", type=nonnegative_int, default=0)
    parser.add_argument("--batch_size", type=positive_int, default=8)
    parser.add_argument("--epochs", type=positive_int, default=100)
    parser.add_argument("--lr", type=float, default=0.0001)
    # use nargs to tell argparse that if the exclude_label flag is given
    # it expects n=N values afterwards (use * for non-fixed number of values)
    # collected into a list.
    parser.add_argument("--exclude_label", type=str, nargs="*")

    args = parser.parse_args(argv)
    print(args)


if __name__ == "__main__":
    # for debugging
    sys.exit(
        main(
            [
                "data/my_data.csv",
                "data",
                "--gpu_id",
                "1",
                "--batch_size",
                "8",
                "--epochs",
                "100",
                "--lr",
                "0.0001",
                "--exclude_label",
                "Cardiomegaly",
                "Pneumonia",
            ]
        )
    )
    # for running the program
    # sys.exit(main(sys.argv[1:]))
