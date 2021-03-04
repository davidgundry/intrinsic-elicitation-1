#
# This script performs the pre-registered analysis for "data/data.json". It saves graphs in "out/".
#
# The working directory must be the directory containing the python/data/out folders.
#
# Requires pandas, scipy, statsmodels, matplotlib. Get them using
#  `pip install pandas scipy statsmodels matplotlib`

import numpy as np
from scipy.stats import ttest_ind
from scipy.stats import ttest_1samp
from scipy.stats import mannwhitneyu
from statsmodels.graphics.gofplots import qqplot
import matplotlib
import matplotlib.pyplot as plt
from statistics import mean, stdev
from math import sqrt

import seaborn as sns
sns.set(style="ticks", font_scale=1.5)
import ptitprince as pt

from load_process import load_data, process_data

def hypothesis_test_1(cat1, cat2):
    print("""Hypothesis 1: Enjoyment (DV1) will be greater in the game condition than the task condition.
    A one-tailed two-sample t-test will be used to test whether the mean scores of DV1 is greater
    in the game condition than the task condition. α = 0.05.""")
    alpha = 0.05
    c0 = cat1['imi_enjoyment']
    c1 = cat2['imi_enjoyment']
    ttest = ttest_ind(c0,c1)
    n0 = len(c0)
    n1 = len(c1)
    cond0 = (n0 - 1) * (stdev(c0) ** 2)
    cond1 = (n1 - 1) * (stdev(c1) ** 2)
    pooledSD = sqrt((cond0 + cond1) / (n0 + n1 - 2))
    cohens_d = (mean(c0) - mean(c1)) / pooledSD
    p = ttest.pvalue/2 # because it's a one tailed test, we also check that ttest.statistic has the correct sign
    print("Game mean" ,mean(c0), "sd" ,stdev(c0))
    print("mean Tool" ,mean(c1), "sd", stdev(c1))
    print("one tailed t test: p =", p, "; t =",ttest.statistic, "; significant =",(p < alpha) and (ttest.statistic > 0), "; d =",cohens_d, "\n\n")

def hypothesis_test_2(cat1, cat2):
    print("""Hypothesis 2: Proportion of valid data (DV2(a)) will be lower in the game condition than the
    task condition. A two-tailed two-sample t-test will be used to test whether the mean scores of
    DV2(a) is less in the game condition than the task condition. α = 0.05""")
    c0 = cat1['proportion_of_valid_data']
    c1 = cat2['proportion_of_valid_data']
    alpha = 0.05
    ttest = ttest_ind(c0, c1)
    n0 = len(c0)
    n1 = len(c1)
    cond0 = (n0 - 1) * (stdev(c0) ** 2)
    cond1 = (n1 - 1) * (stdev(c1) ** 2)
    pooledSD = sqrt((cond0 + cond1) / (n0 + n1 - 2))
    cohens_d = (mean(c0) - mean(c1)) / pooledSD
    print("Game mean" ,mean(c0), "sd" ,stdev(c0))
    print("mean Tool" ,mean(c1), "sd", stdev(c1))
    print("two tailed t test: p =", ttest.pvalue, "; t =",ttest.statistic, "; significant =",(ttest.pvalue < alpha), "; d =",cohens_d, "\n\n")

def hypothesis_test_3(cat1, cat2):
    print("""Hypothesis 3: Proportion of valid data-providing mechanic actuations (DV2(b)) will be greater
    in the game condition than what would be expected if ordering was random. A two-tailed one-sample
    t-test will be used to compare DV2 for the game condition against the theoretical mean expected if
    players provided word orderings that were completely random. This is given below. α = 0.05

    Theoretical random proportion = (valid permutations / total permutations of 3 words) = 1/6 = 16.67%""")
    alpha = 0.05
    c0 = cat1['proportion_of_valid_data_providing_mechanic_actuations_hasnoun']
    ttest = ttest_1samp(c0, 1/6)
    cohens_d = (mean(c0) - (1/6)) / stdev(c0)
    print("Game mean" ,mean(c0), "sd" ,stdev(c0))
    print("two tailed, 1 sample t test: p =", ttest.pvalue, "; t =", ttest.statistic, "; significant =", (ttest.pvalue < alpha), "; d =",cohens_d, "\n\n")

def enjoyment_box_plot(df):
    plt.clf()
    boxplot = df.boxplot(column='imi_enjoyment', by='version', grid=False)
    plt.suptitle('')
    plt.title("")
    boxplot.set_xlabel("")
    boxplot.set_ylabel("IMI Enjoyment subscale")
    plt.savefig('out/imi_enjoyment_per_condition+'+dataset+'.pdf', bbox_inches='tight')


def enjoyment_raincloud(df):
    dy="imi_enjoyment"; dx="version"; ort="v"; pal = sns.color_palette(n_colors=2)
    f, ax = plt.subplots(figsize=(7, 5))
    ax=pt.half_violinplot( x = dx, y = dy, data = df, palette = pal, bw = .2, cut = 0.,
                        scale = "area", width = .6, inner = None, orient = ort, order=["Game","Tool"])
    ax=sns.stripplot( x = dx, y = dy, data = df, palette = pal, edgecolor = "white",
                    size = 3, jitter = 1, zorder = 0, orient = ort, order=["Game","Tool"])
    ax=sns.boxplot( x = dx, y = dy, data = df, color = "black", width = .15, zorder = 10,\
                showcaps = True, boxprops = {'facecolor':'none', "zorder":10},\
                showfliers=True, whiskerprops = {'linewidth':2, "zorder":10},\
                saturation = 1, orient = ort, order=["Game","Tool"])
    plt.xticks(plt.xticks()[0], ["Game","Control"])
    ax.set_xlabel("")
    ax.set_ylabel("IMI Enjoyment")
    plt.savefig('out/imi_enjoyment_per_condition_raincloud+'+dataset+'.pdf', bbox_inches='tight')


def valid_proportion_all_data_boxplot(df):
    plt.clf()
    boxplot = df.boxplot(column='proportion_of_valid_data', by='version', grid=False)
    plt.suptitle('')
    plt.title("")
    boxplot.set_xlabel("")
    boxplot.set_ylabel("Proportion of Valid Data")
    plt.savefig('out/prop_valid_data_per_condition+'+dataset+'.pdf', bbox_inches='tight')


def valid_proportion_all_data_raincloud(df):
    dy="proportion_of_valid_data"; dx="version"; ort="v"; pal = sns.color_palette(n_colors=2)
    f, ax = plt.subplots(figsize=(7, 5))
    ax=pt.half_violinplot( x = dx, y = dy, data = df, palette = pal, bw = .2, cut = 0.,
                        scale = "area", width = .6, inner = None, orient = ort, order=["Game","Tool"])
    ax=sns.stripplot( x = dx, y = dy, data = df, palette = pal, edgecolor = "white",
                    size = 3, jitter = 1, zorder = 0, orient = ort, order=["Game","Tool"])
    ax=sns.boxplot( x = dx, y = dy, data = df, color = "black", width = .15, zorder = 10,\
                showcaps = True, boxprops = {'facecolor':'none', "zorder":10},\
                showfliers=True, whiskerprops = {'linewidth':2, "zorder":10},\
                saturation = 1, orient = ort, order=["Game","Tool"])
    plt.xticks(plt.xticks()[0], ["Game","Control"])
    ax.set_xlabel("")
    ax.set_ylabel("Proportion of Valid Data")
    plt.savefig('out/prop_valid_data_per_condition_raincloud+'+dataset+'.pdf', bbox_inches='tight')


def valid_proportion_actuations_boxplot(df):
    plt.clf()
    boxplot = df.boxplot(column='proportion_of_valid_data_providing_mechanic_actuations_hasnoun', by='version', grid=False)
    plt.suptitle('')
    plt.title("")
    boxplot.set_xlabel("")
    boxplot.set_ylabel("Proportion of valid data providing mechanic actuations (has noun)")
    plt.savefig('out/prop_valid_data_providing_actuations_per_condition+'+dataset+'.pdf', bbox_inches='tight')

def gaming_frequency_bar_plot(df):
    plt.clf()
    boxplot = df['gaming_frequency'].value_counts().plot.bar(grid=False)
    plt.suptitle('')
    plt.title("")
    #boxplot.set_xlabel("Gaming Frequency")
    boxplot.set_ylabel("Count")
    plt.savefig('out/gaming_frequency+'+dataset+'.pdf', bbox_inches='tight')

dataset = 'data'
print("Analysing dataset", dataset, "\n")
rawData = load_data("data/"+dataset)
df = process_data(rawData)

gameCondition = df[df['version']=='Game']
toolCondition = df[df['version']=='Tool']

hypothesis_test_1(gameCondition, toolCondition)
hypothesis_test_2(gameCondition, toolCondition)
hypothesis_test_3(gameCondition, toolCondition)
enjoyment_box_plot(df)
enjoyment_raincloud(df)
valid_proportion_all_data_boxplot(df)
valid_proportion_all_data_raincloud(df)
valid_proportion_actuations_boxplot(df)
gaming_frequency_bar_plot(df)
print(df['gaming_frequency'].value_counts())
