"""Raw data generation
Usage:
  raw_gen.py  --curve_type=<ct>  

Options:
  -h, --help             Show help text.
  -v, --version          Show version.
  --curve_type=<ct>      curve type
"""

import pathlib
import DMT.core
import pandas as pd
import glob
from subprocess import check_call
from docopt import docopt

arguments = docopt(__doc__, version='Technology Generator: 0.1')
curve_type = arguments['--curve_type']


# reading raw data files
sel_files = dict()
cells_dir = pathlib.Path("../sky130_fd_pr/cells")
cell_dir = cells_dir / "nfet_01v8"
data_files = glob.glob(f"{cell_dir}/*.mdm")

if curve_type == "ID_VDS":
    file_ind = "IDVD"

elif curve_type == "ID_VGS":
    file_ind = "IDVG"

for file in data_files:
    if file_ind in file:
        part1 = file.split("(")[1]
        part2 = part1.split(")")[0]
        data = part2.split("_")

        if "D3" in data:
            loc = int(data[0])
            s_pin = 0
            d_pin = int(data[1])
        else:
            loc = int(data[0])
            s_pin = int(data[1])
            d_pin = int(data[2])

        sel_files[file] = ((loc, s_pin, d_pin))
    
index = 1
raw_df = pd.DataFrame()
for mdm_path, name in sel_files.items():
    mdm_path = pathlib.Path(mdm_path)
    measurement = DMT.core.DutMeas(
        database_dir=None,
        dut_type=DMT.core.DutType.device,
        name=mdm_path.stem,
        reference_node="E",
    )

    measurement.add_data(pathlib.Path(mdm_path), key=mdm_path.stem)
    df_read = measurement.data[mdm_path.stem]
    df_read["VGS"] = df_read["VG"] - df_read["VS"]
    df_read["VSB"] = df_read["VS"] - df_read["VB"]
    df_read["VDS"] = df_read["VD"] - df_read["VS"]
    df_read.drop(columns=["VG", "VS", "VD", "VB"], inplace=True)
    df_read["loc"] = name[0]
    df_read["s_pin"] = name[1]
    df_read["d_pin"] = name[2]

    if index == 1:
        raw_df = df_read
    else:
        raw_df = pd.concat([raw_df, df_read])

    index += 1

raw_df.to_csv("raw_data.csv")