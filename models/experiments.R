setwd("D:/CSE6242-PROJECT")
shots_data <- read.csv("data/shots_log_location.csv", header = TRUE)

if(!require('DescTools')) install.packages('DescTools')

library(DescTools)

model <- glm(SHOT_RESULT ~ CLOSE_DEF_DIST + SHOT_DIST, data = shots_data, family = 'binomial')

summary(model)

PseudoR2(model)
