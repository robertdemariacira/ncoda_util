import os
import pathlib

import numpy as np

M = 2161
N = 1051
L = 34
DATA_FILE_SIZE = M * N * L * 4  # Data(3D) record length in bytes
COORD_FILE_SIZE = M * N * 4  # Coordinate(2D) record length in bytes

MISSING = -999.0
MISSING_ATOL = 1e-6

IN_DTYPE = ">f4"


def read_data(filename: pathlib.Path) -> np.ndarray:
    _validate_file_size(DATA_FILE_SIZE, filename)

    data_3d = _read_raw_data(filename)
    data_3d = data_3d.reshape((L, N, M))  # change the order here
    data_3d = np.transpose(
        data_3d, (2, 1, 0)
    )  # transpose the data to get the correct order

    _convert_missing_to_nan(data_3d)

    return data_3d


def _convert_missing_to_nan(data: np.ndarray) -> None:
    data[np.isclose(data, MISSING, atol=MISSING_ATOL)] = np.nan


def read_coord(filename: pathlib.Path) -> np.ndarray:
    _validate_file_size(COORD_FILE_SIZE, filename)

    coord_2d_deg = _read_raw_data(filename)
    coord_2d_deg = coord_2d_deg.reshape((N, M))  # change the order here
    coord_2d_deg = np.transpose(coord_2d_deg, (1, 0))

    return coord_2d_deg


def _read_raw_data(filename: pathlib.Path) -> np.ndarray:
    with open(filename, "rb") as file:
        return np.fromfile(file, dtype=IN_DTYPE)


def _validate_file_size(min_size: int, filename: pathlib.Path) -> None:
    size = os.path.getsize(filename)

    if size < min_size:
        msg = f"Found file with size: {size} smaller than size: {min_size}: {filename}"
        raise ValueError(msg)
