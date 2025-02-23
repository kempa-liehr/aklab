import ipynbname
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as cm
import matplotlib.image as image
import pandas as pd
from pathlib import Path
import seaborn as sns

sns.set_palette('tab20')
colors = [cm.to_hex(plt.cm.tab20(i)) for i in range(20)]

def list2color(data, cmap=plt.cm.jet):
    return dict(zip(data, cmap(np.linspace(0, 1, len(data))
                               )
                    )
                )

def savefig(label, suffix='pdf', path=None):
    notebookID = ipynbname.name().split('__')[0] + '__'
    if path is None:
        try:
            notebook_path = ipynbname.path()
        except FileNotFoundError:
            notebook_path = Path.cwd()
        if notebook_path.parent.name == 'notebooks':
            path = notebook_path.parent / 'results' / 'figs'
        else:
            path = notebook_path / 'figs'
    if not path.exists():
        path.mkdir(parents=True)
    fn = f'{notebookID}{label}.{suffix}'
    plt.savefig(path / fn, bbox_inches='tight')
    return fn


def distribution(series, log_transformed=False,
                 swarmplot=False,
                 bins='auto'):
    '''
    Visualize distribution of pandas.Series as combination of histogram and boxplot

    :param series: pandas.Series
    :return: fig
    '''
    gridkw = dict(height_ratios=[5, 1])
    fig, (ax1, ax2) = plt.subplots(2, 1, gridspec_kw=gridkw, sharex=True)
    if log_transformed:
        feature = pd.Series(np.log(series),
                           name = 'log({})'.format(series.name)
                           )
    else:
        feature = series
    sns.histplot(x=feature, ax=ax1, kde=False, bins=bins) #array, top subplot
    sns.boxplot(x=feature, ax=ax2, width=.4) #bottom subplot
    if swarmplot:
        sns.swarmplot(feature, ax=ax2,
                      size=2, color=".3", linewidth=0)

    ax1.set_xlabel('')
    ax1.text(1.05, 0.95,
             feature.describe().to_string(),
             transform=ax1.transAxes, fontsize=14,
             verticalalignment='top')
    #http://stackoverflow.com/questions/29813694/how-to-add-a-title-to-seaborn-facet-plot
    fig.subplots_adjust(top=0.9)
    fig.suptitle(feature.name, fontsize=16)
    return  fig, (ax1, ax2)


def distributions(series, species, log_transformed=False,
                 both_series=False, bins='auto', colors=colors):
    '''
    Visualize distribution of pandas.Series as combination of histogram and boxplot

    :param series: pandas.Series
    :return: fig
    '''
    # ENGSCI762 Data Science module
    # http://stackoverflow.com/questions/40070093/gridspec-on-seaborn-subplots
    gridkw = dict(height_ratios=[5, 1, 1])
    fig, (ax1, ax2, ax3) = plt.subplots(3, 1, gridspec_kw=gridkw, sharex=True)

    labels = np.unique(species)
    if log_transformed:
        feature = pd.Series(np.log(series),
                           name = 'log({})'.format(series.name)
                           )
    else:
        feature = series
    if not both_series:
        A = feature[species == labels[0]]
        B = feature[species == labels[1]]
        Alabel = labels[0]
        Blabel = labels[1]
    else:
        A = feature
        B = species
        Alabel = feature.name
        Blabel = species.name

    sns.histplot(x=A, ax=ax1,
                 kde=False,
                 label=Alabel,
                 color=colors[1],
                 bins=bins
                 ) #array, top subplot
    sns.histplot(x=B, ax=ax1,
                 kde=False,
                 label=Blabel,
                 color=colors[3],
                 bins=bins)  # array, top subplot
    ax1.legend()
    ax1.set_xlabel('')
    sns.boxplot(x=A, ax=ax2, width=.4,
                color=colors[1])  # middle subplot
    ax2.set_xlabel('')

    current_palette = colors
    sns.boxplot(x=B, ax=ax3, width=.4,
                color=colors[3]
                )  # bottom subplot
    return fig, (ax1, ax2, ax3)

