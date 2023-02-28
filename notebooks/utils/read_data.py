import os
import os.path as op
import pandas as pd
import numpy as np
from pandas import DataFrame
from typing import Union, List, Tuple
from strenum import StrEnum
from collections import namedtuple
import re

DUTinfo = namedtuple('DUTinfo', 'die mod idx flavor W L meas_mode VG VD VB T')
IDVGpattern = r'Die(\d+)_(\d+)-(\d+)_(\w+)_W(\d+)_L(\d+)_(\w+)_Vd(.+)Vb(.+)_T(\d+)K.csv'
IDVDpattern = r'Die(\d+)_(\d+)-(\d+)_(\w+)_W(\d+)_L(\d+)_(\w+)_Vg(.+)Vb(.+)_T(\d+)K.csv'
DATApath = op.join(op.abspath(__file__), '..', '..', '..', 'sky130_fd_pr', 'epfl')


class MeasureentMode(StrEnum):
    IDVG = 'idvg'
    IDVD = 'idvd'


def decode_iv_file_name(
        filename: str) -> DUTinfo:
    """Decode IV measurement filename."""
    if MeasureentMode.IDVG in filename:
        res = re.findall(IDVGpattern, filename)[0]
        die, mod, idx, flavor, w, l, meas_mode, vd, vb, temp = res
        return DUTinfo(
            die=int(die), mod=mod, idx=int(idx), flavor=flavor,
            W=np.round(float(w)*1e-9, 9), L=np.round(float(l)*1e-9, 9), meas_mode=meas_mode,
            VD=float(vd.replace('V', '.')), VB=float(vb.replace('V', '.')),
            T=float(temp), VG=None
        )
    elif MeasureentMode.IDVD in filename:
        res = re.findall(IDVDpattern, filename)[0]
        die, mod, idx, flavor, w, l, meas_mode, vg, vb, temp = res
        return DUTinfo(
            die=int(die), mod=mod, idx=int(idx), flavor=flavor,
            W=np.round(float(w)*1e-9, 9), L=np.round(float(l)*1e-9, 9), meas_mode=meas_mode,
            VG=float(vg.replace('V', '.')), VB=float(vb.replace('V', '.')),
            T=float(temp), VD=None
        )
    else:
        raise ValueError(f"Filename {filename} can not be decoded.")


def read_iv(
        mod: Union[int, str],
        idx: Union[list, int],
        meas_mode: Union[MeasureentMode, str],
        vg: Union[float, list, None] = None,
        vd: Union[float, list, None] = None,
        vb: Union[float, list, None] = None,
        temp: Union[float, list, None] = None
) -> List[Tuple[DUTinfo, DataFrame]]:
    """Read IV measurement.

    :param mod: Module index.
    :param idx: DUT index
    :param meas_mode: Measurement mode.
    :param vg: Gate voltage.
    :param vd: Drain voltage.
    :param vb: Bulk voltage.
    :param temp: Temperature.
    """
    out = []
    folder = None
    mod = str(mod)
    idx = [idx] if isinstance(idx, int) else idx
    vg = [vg] if isinstance(vg, float) else vg
    vd = [vd] if isinstance(vd, float) else vd
    vb = [vb] if isinstance(vb, float) else vb
    temp = [temp] if isinstance(temp, float) else temp

    for f in os.listdir(DATApath):
        if f.endswith(mod):
            folder = f
            break

    filename_list = os.listdir(op.join(DATApath, folder))
    for file in filename_list.copy():
        info = decode_iv_file_name(filename=file)
        if info.idx not in idx:
            filename_list.remove(file)
            continue

        if info.meas_mode != meas_mode:
            filename_list.remove(file)
            continue

        if vg:
            if info.VG not in vg:
                filename_list.remove(file)
                continue
        if vd:
            if info.VD not in vd:
                filename_list.remove(file)
                continue
        if vb:
            if info.VB not in vb:
                filename_list.remove(file)
                continue

        if temp:
            if info.T not in temp:
                filename_list.remove(file)
                continue

    for f in filename_list:
        f_info = decode_iv_file_name(f)
        df = pd.read_csv(op.join(DATApath, folder, f), index_col=0)
        out.append((f_info, df))
    return out
