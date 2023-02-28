from matplotlib.pyplot import rcParams

default = {
    'axes.formatter.limits': (-3, 3),
    'axes.labelsize': 9,
    'axes.titlesize': 20,
    'axes.titleweight': 'bold',
    'axes.formatter.use_mathtext': True,
    'axes.linewidth': 1.,
    'axes.autolimit_mode': "round_numbers",
    'axes.xmargin': 0.,
    'axes.ymargin': .0,
    "figure.dpi": 100,
    'savefig.dpi': 1200,
    'xtick.labelsize': 8,
    'ytick.labelsize': 8,
    'font.size': 8,
    'legend.fontsize': 8,
    'legend.framealpha': 0.5,
    'legend.frameon': False,
    'figure.figsize': [4, 3],
    'lines.linestyle': '-',
    'lines.markersize': 4,
    'lines.markerfacecolor': "white",
    'xtick.direction': "in",
    'ytick.direction': "in",
    'figure.autolayout': False,
    'figure.constrained_layout.use': False,
}


def rcParams_update(kwargs: dict = None, theme: str = None):
    if theme is None:
        d = default
    else:
        raise ValueError
    if kwargs:
        for key, val in kwargs.items():
            d[key] = val
    rcParams.update(d)