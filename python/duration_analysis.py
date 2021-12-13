#
# This script generates the analysis for "data/duration.csv". It saves
# output data and graphs in "out/".
#


import numpy as np
import pandas as pd
import json
from scipy.stats import ttest_ind
from scipy.stats import ttest_1samp
import matplotlib
import matplotlib.pyplot as plt
from statistics import mean, stdev
from math import sqrt
from scipy.stats import mannwhitneyu

def duration_histogram(gameCondition, toolCondition):
    plt.clf()
    bins = np.linspace(0, 720, 24)
    plt.hist(gameCondition['duration'], bins, alpha=0.5, label="Game")
    plt.hist(toolCondition['duration'], bins, alpha=0.5, label="Tool")
    plt.suptitle('')
    plt.title("")
    plt.legend(loc='upper right')
    plt.savefig('out/duration_hist+'+dataset+'.pdf', bbox_inches='tight')

def duration_boxplot(df):
    plt.clf()
    boxplot = df.boxplot(column='duration', by='version', grid=False)
    plt.suptitle('')
    plt.title("")
    boxplot.set_xlabel("")
    boxplot.set_ylabel("Duration")
    plt.savefig('out/duration_per_condition+'+dataset+'.pdf', bbox_inches='tight')


dataset = 'duration'
print("Analysing dataset", dataset, "\n")
df=  pd.read_csv("data/"+dataset+".csv", names=["version","duration"])

gameCondition = df[df['version']=='Normal']
toolCondition = df[df['version']=='Tool']

duration_histogram(gameCondition,toolCondition)
duration_boxplot(df)

cAll = df['duration']
c0 = gameCondition['duration']
c1 = toolCondition['duration']
alpha = 0.05
ttest = ttest_ind(c0, c1)
n0 = len(c0)
n1 = len(c1)
cond0 = (n0 - 1) * (stdev(c0) ** 2)
cond1 = (n1 - 1) * (stdev(c1) ** 2)
pooledSD = sqrt((cond0 + cond1) / (n0 + n1 - 2))
cohens_d = (mean(c0) - mean(c1)) / pooledSD

print("all data: mean", mean(cAll), "sd", stdev(cAll))
print("game condition: mean", mean(c0), "sd", stdev(c0))
print("tool condition: mean", mean(c1), "sd", stdev(c1))
print(ttest)

mwu = mannwhitneyu(c0, c1)
print("Mann-Whitney U test:", mwu)

print("cohens d =", cohens_d)

m0 = mean(c0)
print("\n\nGame mean:", m0)
print("This in seconds per input (20 inputs):", (m0/20))
print("This in inputs per second:", (20/m0))
print("This in inputs per 8 minutes:", (8*60) * (20/m0))

m1 = mean(c1)
print("\n\nTool mean:", m1)
print("This in seconds per input (20 inputs):", (m1/20))
print("This in inputs per second:", (20/m1))
print("This in inputs per 8 minutes:", (8*60) * (20/m1))

twoSDUp = mean(c0) + 2.5*stdev(c0)
print("\n\n2.5 standard deviations above game mean", twoSDUp)
print("This in seconds per input (20 inputs):", (twoSDUp/20))
print("This in inputs per second:", (20/twoSDUp))
print("This in inputs per 8 minutes:", (8*60) * (20/twoSDUp))