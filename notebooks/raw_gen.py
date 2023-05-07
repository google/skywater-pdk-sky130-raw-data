import pathlib
import DMT.core
import pandas as pd
import glob
from subprocess import check_call
from docopt import docopt

# reading raw data files
curve_type = ["ID_VDS", "ID_VGS"]
cells_dir = pathlib.Path("../sky130_fd_pr/cells")
cell_dir = cells_dir / "nfet_01v8"
data_files = glob.glob(f"{cell_dir}/*.mdm")

sel_files_vd = dict() 
sel_files_vg = dict() 

for file in data_files:
    
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
    
    if "IDVD" in file:
        sel_files_vd[file] = ((loc, s_pin, d_pin))
    elif "IDVG" in file:
        sel_files_vg[file] = ((loc, s_pin, d_pin))
    
total_sel_files = [sel_files_vd, sel_files_vg]
for sel_files in total_sel_files:
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

    if sel_files == sel_files_vd:
        raw_df.to_csv(f"{cell_dir}/raw_data_idvd.csv")
    elif sel_files == sel_files_vg:
        raw_df.to_csv(f"{cell_dir}/raw_data_idvg.csv")