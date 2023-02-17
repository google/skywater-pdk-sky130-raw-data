from matplotlib import pyplot as plt
from matplotlib.pyplot import Axes
from pandas import DataFrame
from typing import Union, Tuple


def plot_idvg(
        df: DataFrame,
        axes: Union[Tuple[Axes, Axes], None] = None,
        dev_type='n',
        **kwargs
) -> Tuple[Axes, Axes]:

    if axes is None:
        ax = plt.gca()
        axt = ax.twinx()
    else:
        ax, axt = axes

    try:
        df.VS
    except AttributeError:
        df['VS'] = 0
        print("Can't find VS in data, set VS = 0 V")

    if dev_type == 'n':
        x = df.VG - df.VS
        y = df.ID
        ax.set_xlabel('$V_{GS}$ (V)')
        ax.set_ylabel('$I_D$ (A)')
        axt.set_ylabel('$I_D$ (A)')
    else:
        x = df.VS - df.VG
        y = -df.ID
        ax.set_xlabel('$V_{SG}$ (V)')
        ax.set_ylabel('$-I_D$ (A)')
        axt.set_ylabel('$-I_D$ (A)')

    ax.plot(x, y, marker='o', mfc='w', markevery=0.1, **kwargs)
    ax.set_yscale('log')

    axt.plot(x, y, marker='o', mfc='w', markevery=0.1)

    ax.legend(loc=2)

    return ax, axt


def plot_idvd(
        df: DataFrame,
        ax: Union[Axes, None] = None,
        dev_type='n',
        **kwargs
) -> Tuple[Axes, Axes]:
    if ax is None:
        ax = plt.gca()

    try:
        df.VS
    except AttributeError:
        df['VS'] = 0
        print("Can't find VS in data, set VS = 0 V")

    if dev_type == 'n':
        x = df.VD - df.VS
        y = df.ID
        ax.set_xlabel('$V_{DS}$ (V)')
        ax.set_ylabel('$I_D$ (A)')
    else:
        x = df.VS - df.VD
        y = -df.ID
        ax.set_xlabel('$V_{SD}$ (V)')
        ax.set_ylabel('$-I_D$ (A)')

    ax.plot(x, y, marker='o', mfc='w', markevery=0.1, **kwargs)

    ax.legend(loc=0)

    return ax