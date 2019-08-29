#!/usr/bin/env python

"""plot_grand_average.py: viz grand averaged ERF data.
    Does per age:
        1. plot topographic maps of odball ERFs
        2. plot compare oddball ERFs GFP
"""

__author__ = "Kambiz Tavabi"
__copyright__ = "Copyright 2019, Seattle, Washington"
__license__ = "MIT"
__version__ = "1.0.1"
__maintainer__ = "Kambiz Tavabi"
__email__ = "ktavabi@uw.edu"
__status__ = "Production"

import os
from os import path as op
from pathlib import Path

import matplotlib.pyplot as plt
import mne
from meeg_preprocessing import config

from badbaby import defaults

plt.style.use('ggplot')

# parameters
workdir = defaults.datapath
analysis = 'Oddball'
conditions = ['standard', 'deviant']
tmin, tmax = defaults.epoching
lp = defaults.lowpass
ages = [2, 6]
window = defaults.peak_window  # peak ERF latency window

evoked_dict = dict()
picks_dict = dict()
for aix in ages:
    evoked_dict[aix] = dict()
    picks_dict[aix] = dict()
    for ci, cond in enumerate(conditions):
        evo_in = op.join(workdir, '%s_%d_%dmos_grp-ave.fif' % (cond, lp, aix))
        if not op.isfile(evo_in):
            os.system(op.join(Path(__file__).parents[0],
                              'processing/compute_grand_average.py'))
        # Peak ERF gradiometer activity
        grandavr = mne.read_evokeds(evo_in)[0]
        ch, lat = grandavr.get_peak(ch_type='grad', tmin=window[0],
                                    tmax=window[1])
        picks_dict[aix][cond] = ch
        evoked_dict[aix][cond] = grandavr
        if cond in ['all', 'deviant']:
            print('     %s peak at:\n'
                  '         %s at %0.3fms' % (cond, ch, lat))
        # plot group ERF topography
        timing = [lat - .1, lat]
        hs = grandavr.plot_joint(title=cond, times=timing,
                                 ts_args=config.TS_ARGS,
                                 topomap_args=config.TOPOMAP_ARGS)
        for ii, hh in enumerate(hs):
            hh.savefig(op.join(defaults.figsdir,
                               op.basename(evo_in)[:-4] +
                               '_%d.png' % ii), bbox_inches='tight')
    #  compare group ERF time courses at peak locations
    pick = [grandavr.ch_names.index(kk) for kk in
            set(list(picks_dict[aix].values()))]
    hs = mne.viz.plot_compare_evokeds(evoked_dict[aix],
                                      show_sensors=True, gfp=True)
    for hh, kind in zip(hs, ['grad', 'mag']):
        hh.savefig(op.join(defaults.figsdir,
                           '%s_%d_%s_grp-ave.png' % (analysis, lp, kind)),
                   bbox_inches='tight')
