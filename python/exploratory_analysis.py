#
# This script performs exploratory analysis that was not part of the pre-registration.
# It generates additional graphs in "out/".
#
# The working directory must be the directory containing the python/data/out folders.
#

import numpy as np
import pandas as pd
import json
from scipy.stats import ttest_ind
from scipy.stats import ttest_1samp
from scipy.stats import mannwhitneyu
from statsmodels.graphics.gofplots import qqplot
import matplotlib
import matplotlib.pyplot as plt
from statistics import mean, stdev
from math import sqrt

from load_process import load_data, process_data

def valid_data_histogram(gameCondition, toolCondition):
    plt.clf()
    bins = np.linspace(0, 1, 20)
    plt.hist(gameCondition['proportion_of_valid_data'], bins, alpha=0.5, label="Game")
    plt.hist(toolCondition['proportion_of_valid_data'], bins, alpha=0.5, label="Tool")
    plt.suptitle('')
    plt.title("")
    plt.legend(loc='upper right')
    plt.savefig('out/valid_data_hist+'+dataset+'.pdf', bbox_inches='tight')

def enjoyment_histogram(gameCondition, toolCondition):
    plt.clf()
    bins = np.linspace(0, 5, 25)
    plt.hist(gameCondition['imi_enjoyment'], bins, alpha=0.5, label="Game")
    plt.hist(toolCondition['imi_enjoyment'], bins, alpha=0.5, label="Tool")
    plt.suptitle('')
    plt.title("")
    plt.legend(loc='upper right')
    plt.savefig('out/enjoyment_hist+'+dataset+'.pdf', bbox_inches='tight')

def valid_data_qq_plot(gameCondition, toolCondition):
    plt.clf()
    qqplot(gameCondition['proportion_of_valid_data'], line='s')
    plt.suptitle('')
    plt.title("")
    plt.savefig('out/valid_data_game_qq+'+dataset+'.pdf', bbox_inches='tight')
    qqplot(toolCondition['proportion_of_valid_data'], line='s')
    plt.suptitle('')
    plt.title("")
    plt.savefig('out/valid_data_tool_qq+'+dataset+'.pdf', bbox_inches='tight')

def non_parametric_valid_data_test(cat1, cat2):
    print("""Hypothesis 2: Proportion of valid data (DV2(a)) will be lower in the game condition than the
    task condition. A two-tailed two-sample t-test will be used to test whether the mean scores of
    DV2(a) is less in the game condition than the task condition. α = 0.05""")
    c0 = cat1['proportion_of_valid_data']
    c1 = cat2['proportion_of_valid_data']
    alpha = 0.05
    mwu = mannwhitneyu(c0, c1)
    n0 = len(c0)
    n1 = len(c1)
    cond0 = (n0 - 1) * (stdev(c0) ** 2)
    cond1 = (n1 - 1) * (stdev(c1) ** 2)
    pooledSD = sqrt((cond0 + cond1) / (n0 + n1 - 2))
    cohens_d = (mean(c0) - mean(c1)) / pooledSD
    print("Game mean" ,mean(c0), "sd" ,stdev(c0))
    print("mean Tool" ,mean(c1), "sd", stdev(c1))
    print("Mann-Whitney U test: p =", mwu.pvalue, "; U =",mwu.statistic, "; significant =",(mwu.pvalue < alpha), "; d =",cohens_d, "\n\n")

dataset = 'data'
print("Analysing dataset", dataset, "\n")
rawData = load_data("data/"+dataset)
df = process_data(rawData)

gameCondition = df[df['version']=='Game']
toolCondition = df[df['version']=='Tool']
valid_data_histogram(gameCondition, toolCondition)
valid_data_qq_plot(gameCondition, toolCondition)
enjoyment_histogram(gameCondition, toolCondition)

non_parametric_valid_data_test(gameCondition, toolCondition)
