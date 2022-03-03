library(dplyr)
library(fuzzyjoin)
library(assertr)

#setwd("~/Documents/GT Masters/CSE 6242/CSE6242-Project")

fname <- file.choose()
df = read.csv(fname)
#df = read.csv("data/shots_log_location.csv")

complete_df = df[complete.cases(df),]
complete_df$shot_value <- as.character(complete_df$shot_value)

train = sample_n(complete_df, size = round(.80 * nrow(complete_df)))
test = anti_join(complete_df, train)

## Baseline ## 
sum(complete_df$shot_made_numeric)/nrow(complete_df)

### Baseline the probability of a shot going in is 45% ### 

logit.base = glm(shot_made_numeric ~ shot_zone_area + shot_value, data = train, family = "binomial")

complete_df %>% group_by(shot_zone_area) %>% tally()
summary(logit.base)

pred = ifelse(predict(logit.base, type = "response") > 0.50, 1, 0)
table(pred, train$shot_made_numeric)
sum(diag(table(pred, train$shot_made_numeric)))/sum(table(pred, train$shot_made_numeric))


pred_test = ifelse(predict(logit.base, newdata = test, type = "response") > 0.50, 1, 0)
table(pred_test, test$shot_made_numeric)
sum(diag(table(pred_test, test$shot_made_numeric)))/sum(table(pred_test, test$shot_made_numeric))



