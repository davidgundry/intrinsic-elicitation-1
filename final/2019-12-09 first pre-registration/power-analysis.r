
library("pwr")
# These calculations are to determine the required sample size for the Enjoyment and Data Quality experiment,
# comparing the adjective game that has been developed against an implementation of a standard (non-game)
# experimental paragidm using the same interface.
#
# Three hypotheses will be tested, each independent of the others and with an alpha of 0.05. The first, that
# players will experience more enjoyment in the game condition. The second, that players will provive poorer
# quality data in the game condition. And third, data quality will be better in the game than would be expected
# if answering was purely random (assessed theoretically). 

playtestUserDataQualityMeansSD <- read.csv(file="data/playtest/playtest-user-data-quality-means-sd.csv", header=TRUE, sep=",")
observedSDGameCondition <- sd(playtestUserDataQualityMeansSD$mean)
estimatedSDToolCondition <- observedSDGameCondition
pooledSD <- sqrt((observedSDGameCondition*observedSDGameCondition+estimatedSDToolCondition*estimatedSDToolCondition)/2)
observedMeanGameCondition <- mean(playtestUserDataQualityMeansSD$mean)

# Enjoyment
alt <- "greater" # We are interested in whether the game is more enjoyable than the tool/experiment version.
                 # There are reasons why the tool may be more enjoyable (eg. enjoying contributing to citizen science)
                 # But this would still just be a failure of the game to be enjoyable. Being equal or worse to the
                 # tool condition makes no difference: from both we would conclude that the game does not satisfy
                 # our definition of an 'applied game' (needs to be enjoyable) that motivates its use in our reserach.
estimatedEffectSizeEnjoyment <- cohen.ES(test = "t", size = "medium")$effect.size
                 # Designing an applied game is a significant investment of effort. It is only justifiable as a
                 # methodology if it leads to a fairly substantial effect on participant motivation (which we
                 # are operationalising here as enjoyment). Less than a medium effect size would indicate that the game
                 # is not particularly useful as a replacement for a standard experimental setup. Whether it has
                 # a small, or no effect (or negative effect) makes no difference with regards to whether
                 # is is an ecologically valid example of a (practically useful) 'applied game'.
pwr.t.test(d = estimatedEffectSizeEnjoyment, sig.level = 0.05, power = 0.8, alternative = alt)


# Data Quality
alt <- "less" # Whether the game collects equal or better data to the tool/experiment version makes no difference
              # for our research: either way we would conclude that it is 'good enough'. The tool implements a
              # standard experimental paradigm, but we could not argue that by beating the tool the game has
              # demonstrated anything meaningful that extends beyond one particular limited implementation.
              # Whereas by performing worse than the tool, it shows that the data qaulity is definitely poor.
              # The tool is, in other words, only useful as a lower bound. 
estimatedMeanToolCondition = 0.9
              # Estimating that 90% of the time in an experimental context, people use the grammatical form.
              # So long as participants are acting like they would in a face-to-face experiment: eg. not rushing
              # and putting in reasonable care.
estimatedDelta <- observedMeanGameCondition - estimatedMeanToolCondition
estimatedEffectSize <- estimatedDelta / pooledSD
              # Formula for Cohens d (for equal group sizes) is:
              #     d = (Mean1 - Mean2) / PooledSD
              # where 
              #     PooledSD = sqrt((SD1^2 + SD2^2) / 2)
pwr.t.test(d = estimatedEffectSize, sig.level = 0.05, power = 0.8, alternative = alt)


# Data Quality vs. Random
alt <- "two.sided" # It would be of interest if players perform worse than random as they might result from
                   # an (ungrammatical) answering strategy, such as noun-first.
meanRandom = 1/6 # Data quality is determined by whether the permutation of 3 words supplied by the player is correct.
                 # There are 6 possible permutations of 3 elements (3*2*1). Only one is correct, therefore the
                 # theoretical mean in a random condition is 1/6 = 1.66..
estimatedDeltaVsRandom <- observedMeanGameCondition - meanRandom
estimatedEffectSizeVsRandom <- estimatedDeltaVsRandom / pooledSD
pwr.t.test(d = estimatedEffectSizeVsRandom, sig.level = 0.05, power = 0.8, type = "one.sample")

# Largest sample size required is 50.15 per group. We will round this to 50, making an overall required sample size of 100.