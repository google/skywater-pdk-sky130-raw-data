from matplotlib import pyplot as plt
from matplotlib.pyplot import Axes
from pandas import DataFrame
from typing import Union, Tuple


def plot_idvg(
        df: DataFrame,
        axes: Union[Tuple[Axes, Axes], None] = None
) -> Tuple[Axes, Axes]:
    if axes is None:
        ax = plt.gca()
        axt = ax.twinx()
    else:
        ax, axt = axes

    ax.plot(df.VG, abs(df.ID), marker='o', mfc='w', markevery=0.2)
    ax.set_yscale('log')

    axt.plot(df.VG, abs(df.ID), marker='o', mfc='w', markevery=0.2)

    ax.set_xlabel('$V_G$ (V)')
    ax.set_ylabel('$I_D$ (A)')
    axt.set_ylabel('$I_D$ (A)')

    return ax, axt


def plot_idvd(
        df: DataFrame,
        ax: Union[Axes, None] = None
) -> Tuple[Axes, Axes]:
    if ax is None:
        ax = plt.gca()

    ax.plot(df.VD, abs(df.ID), marker='o', mfc='w', markevery=0.2)

    ax.set_xlabel('$V_D$ (V)')
    ax.set_ylabel('$I_D$ (A)')

    return ax