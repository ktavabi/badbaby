#!/usr/bin/env python

"""PANDAS wrapper to return cohort specific data frames."""

import os.path as op
import pandas as pd
from badbaby import defaults as params

static = params.static


def return_dataframes(paradigm, ses=False, longitudinal=False):
    """
    Return available MEG and corresponding CDI datasets.
    Parameters
    ----------
    paradigm:str
        Name of project paradigm. Can be mmn, assr, or ids.
    longitudinal:bool
        Default False. If True then include only Simms-Mann longitudinal cohort.
    ses:bool
        Default False. If True then include only Bezos SES cohort.

    Returns
    -------
    tuple
        Pandas dataframes of available MEG and corresponding CDI datasets.
    """
    # Read excel sheets into pandas dataframes
    xl_meg = pd.read_excel(op.join(static, 'meg_covariates.xlsx'),
                           index_col='subjId',
                           sheet_name=paradigm,
                           converters={'BAD': str})
    xl_meg = xl_meg[(xl_meg.complete == 1)]  # only Ss w complete MEG data
    xl_meg = xl_meg[(xl_meg.behavioral == 1)]  # only Ss w CDI data
    xl_meg.drop(['examDate', 'acq', 'sss',
                 'rejection', 'epoching'], axis=1, inplace=True)
    # Subselect by cohort
    if ses:
        xl_meg = xl_meg[xl_meg['ses'] > 0]  # Bezos cohort
    if longitudinal:
        xl_meg = xl_meg[xl_meg['simmInclude'] == 1]  # SIMMS cohort

    xl_meg = xl_meg.drop('notes', axis=1, inplace=False)
    xl_cdi = pd.read_excel(
        op.join(static, 'behavioral_data.xlsx'),
        sheet_name='Data')
    xl_cdi.drop(['dob', 'gender', 'language', 'cdiForm',
                 'examDate', 'vocabper', 'howuse', 'upstper',
                 'ufutper', 'umisper', 'ucmpper', 'uposper', 'wordend',
                 'plurper',
                 'possper', 'ingper', 'edper', 'irwords', 'irwdper', 'ogwords',
                 'combine', 'combper', 'cplxper'], axis=1, inplace=True)
    return xl_meg, xl_cdi