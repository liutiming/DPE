#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 19 12:18:40 2018

@author: ben
"""

import numpy as np
import pandas as pd

from . utilities import estimate_bins

"""R_C := cases; R_N := non-cases; Mix := mixture"""


def load_diabetes_data(metric):

    dataset = 'data/biobank_mix_WTCC_ref.csv'
    headers = {'diabetes_type': 'group', 't1GRS': 'T1GRS', 't2GRS': 'T2GRS'}

    if metric == 'T1GRS':
        # bin_width = 0.006  # 0.005
        # bin_min = 0.095
        # bin_max = 0.350

        # TODO: Derive this from the scores (this is close to but not equal to the R_C_median)
        median = 0.23137931525707245  # Type 2 population (0.231468353)

    elif metric == 'T2GRS':
        # bin_width = 0.1
        # bin_min = 4.7
        # bin_max = 8.9

        median = 6.78826

    else:
        raise ValueError(metric)
    binning_method = 'fd'

    data = pd.read_csv(dataset)
    data.rename(columns=headers, inplace=True)
    # print(data.describe())

    scores = {}
    means = {}
    p_C = None

    # Arrays of metric scores for each group
    scores = {'R_C': data.loc[data['group'] == 1, metric].values,
              'R_N': data.loc[data['group'] == 2, metric].values,
              'Mix': data.loc[data['group'] == 3, metric].values}
    # Try creating a "ground truth" by combining both reference populations
              # 'Mix': np.r_[data.loc[data['group'] == 1, metric].values,
              #              data.loc[data['group'] == 2, metric].values]}

    # if metric == 'T1GRS':
    #     p_C = len(scores['R_C'])/(len(scores['R_C']) + len(scores['R_N']))

    means = {'R_C': scores['R_C'].mean(),
             'R_N': scores['R_N'].mean()}

    medians = {"R_C": np.median(scores["R_C"]),
               "R_N": median}

    # if False:
    #     sns.jointplot(x='T1GRS', y='T2GRS', data=data)
    # #    f, ax = plt.subplots(1, 3)
    #     sns.jointplot(x='T1GRS', y='T2GRS', color='r', data=data.loc[data["group"]==1])
    #     sns.jointplot(x='T1GRS', y='T2GRS', color='b', data=data.loc[data["group"]==2])
    #     sns.jointplot(x='T1GRS', y='T2GRS', color='g', data=data.loc[data["group"]==3])
    # #    sns.JointGrid(x='T1GRS', y='T2GRS', data=data)

    # --------------------------- Bin the data -------------------------------
    print("Diabetes Data [{}]".format(metric))
    # print("=====================")
    # print("Chosen: width = {}".format(bin_width))
    hist, bins = estimate_bins(scores)
    chosen_bins = bins[binning_method]
    chosen_bins["method"] = binning_method
    return scores, chosen_bins, means, medians, p_C


def load_renal_data():
    '''Load individuals with Type 2 Diabetes GRS and renal disease (microalbuminuria)
    Group: 1 is controls;
    2 is non insulin treated type 2;
    3 is mixture (microalbuminuria) in all individuals not on insulin.
    Truth is 7.77'''

    metric = 'T2GRS'

    # dataset = 'data/renal_data.csv'
    # headers = {'t2d_grs_77': 'T2GRS', 'group': 'group'}
    dataset = 'data/renal_final_data_mixture_2_type_1_1.xls'
    headers = {"T2GRS": "T2GRS", "Group": "group"}
    p_C = 0.0758
    binning_method = 'fd'  # TODO: Take max over R_C, R_N?

    # New "enriched" data set
    # dataset = 'data/renal_data_new.csv'
    # headers = {'T2_GRS': 'T2GRS', "Group (1 t2, 2 control, 3 mixture)": 'group'}
    # p_C = 0.1053

    # bin_width = 0.128  # 0.1
    # bin_min = 4.7
    # bin_max = 8.9

#    data = pd.read_csv(dataset)
    data = pd.read_excel(dataset)
    data.rename(columns=headers, inplace=True)
    data.dropna(inplace=True)  # Remove empty entries
    # print(data.describe())

    scores = {}
    means = {}

    # Arrays of metric scores for each group
#    scores = {#'R_C': data.loc[data['group'] == 1, metric].sample(n=100000).values,
##              'R_C': data.loc[data['group'] == 1, metric].values,
#              'R_C': data.loc[data['group'] == 2, metric].values,
##              'R_N': data.loc[data['group'] == 1, metric].sample(n=100000).values,
#              'R_N': data.loc[data['group'] == 1, metric].sample(n=10000, random_state=42).values,
#              # 'R_N': data.loc[data['group'] == 2, metric].values,
#              'Mix': data.loc[data['group'] == 3, metric].values}

    prev_data = pd.read_csv('data/renal_data.csv')
    prev_data.rename(columns={'t2d_grs_77': 'T2GRS', 'group': 'group'}, inplace=True)

    scores = {'R_C': data.loc[data['group'] == 1, metric].values,
              'R_N': prev_data.loc[prev_data['group'] == 1, metric].sample(n=10000, random_state=42).values,
              'Mix': data.loc[data['group'] == 2, metric].values}

    means = {'R_C': scores['R_C'].mean(),
             'R_N': scores['R_N'].mean()}

    medians = {"R_C": np.median(scores['R_C']),
               "R_N": np.median(scores['R_N'])}

    # --------------------------- Bin the data -------------------------------
    print("Renal Data")
    # print("==========")
    # print("Chosen: width = {}".format(bin_width))
    hist, bins = estimate_bins(scores)
    chosen_bins = bins[binning_method]
    chosen_bins["method"] = binning_method
    return scores, chosen_bins, means, medians, p_C


def load_coeliac_data():
    '''
    non-cases 1,
    cases 2,
    mixture 3
    '''

    dataset = 'data/new_data_control_1_cases_2_mixture_3.csv'
    p_C = 0.139  # Not ground truth - 13.9% report a diagnosis of coeliac so our analysis shows there is no undiagnosed coeliac within a gluten free cohort
    binning_method = 'fd'

    data = pd.read_csv(dataset, header=None, names=['GRS', 'group'])
    data.dropna(inplace=True)  # Remove empty entries

    scores = {'R_C': data.loc[data['group'] == 2, 'GRS'].values,
              'R_N': data.loc[data['group'] == 1, 'GRS'].values,
              'Mix': data.loc[data['group'] == 3, 'GRS'].values}

    means = {'R_C': scores['R_C'].mean(),
             'R_N': scores['R_N'].mean()}

    medians = {"R_C": np.median(scores['R_C']),
               "R_N": np.median(scores['R_N'])}

    print("Coeliac Data")
    # print("==========")
    # print("Chosen: width = {}".format(bin_width))
    hist, bins = estimate_bins(scores)
    chosen_bins = bins[binning_method]
    chosen_bins["method"] = binning_method
    return scores, chosen_bins, means, medians, p_C


def generate_dataset(p_C):

    assert 0.0 <= p_C <= 1.0

    n_ref_1 = 5000
    n_ref_2 = 5000
    n_mix = 5000

    ref1 = np.random.normal(loc=1, scale=0.2, size=n_ref_1)
    bump = int(np.ceil(0.1 * n_ref_2))
    ref2 = np.concatenate((np.random.normal(loc=1.2, scale=0.2, size=n_ref_2-bump),
                           np.random.normal(loc=1.6, scale=0.05, size=bump)))
    mix_n_ref_1 = int(round(p_C * n_mix))
    mix_n_ref_2 = n_mix - mix_n_ref_1
    mix = np.concatenate((np.random.choice(ref1, mix_n_ref_1, replace=True),
                          np.random.choice(ref2, mix_n_ref_2, replace=True)))

    scores = {'Ref1': ref1,
              'Ref2': ref2,
              'Mix': mix}
    return scores


def save_dataset(scores, filename, codes=None):
    if codes is None:
        codes = {'Ref1': 1, 'Ref2': 2, 'Mix': 3}
    groups = np.concatenate((np.ones_like(scores['Ref1'], dtype=int) * codes['Ref1'],
                             np.ones_like(scores['Ref2'],
                                          dtype=int) * codes['Ref2'],
                             np.ones_like(scores['Mix'], dtype=int) * codes['Mix']))
    grs = np.concatenate((scores['Ref1'], scores['Ref2'], scores['Mix']))
    data = pd.DataFrame(data={'Group': groups, 'GRS': grs})
    data.to_csv(filename, header=True, index=False)


def load_dataset(filename, codes=None):
    if codes is None:
        codes = {'Ref1': 1, 'Ref2': 2, 'Mix': 3}
    data = pd.read_csv(filename)  # , header=['Group', 'GRS'])
    data.dropna(inplace=True)  # Remove any empty entries
    scores = {'Ref1': data.loc[data['Group'] == codes['Ref1'], 'GRS'].values,
              'Ref2': data.loc[data['Group'] == codes['Ref2'], 'GRS'].values,
              'Mix': data.loc[data['Group'] == codes['Mix'], 'GRS'].values}
    return scores
