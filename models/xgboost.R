library(xgboost)
library(fastDummies)

shot_csv = read.csv("/Users/adam/Documents/GT Masters/CSE 6242/CSE6242-Project/data/shots_log_location_v2.csv")


y = shot_csv$shot_made_numeric
X = fastDummies::dummy_cols(shot_csv %>% select(shot_zone_area, attacker_height, defender_height ))
X[, c("shot_zone_area", "attacker_height", "defender_height")] <- NULL

X = cbind.data.frame(X, shot_csv$shot_distance, shot_csv$shot_value)
X = X[-bad_index, ]
y = y[-bad_index]

X = cbind.data.frame(X, y)
set.seed(7)
X<-X[sample(nrow(X)),]

y = X$y
X$y <- NULL

folds <- cut(seq(1,nrow(X)),breaks=5,labels=FALSE)

scores = c()
for(i in 1:5){

  testIndexes <- which(folds==i,arr.ind=TRUE)
  
  testData <- X[testIndexes, ]
  trainData <- as.matrix(X[-testIndexes, ])
  
  trainLabels <- y[-testIndexes]
  testLabels <- y[testIndexes]
  
  ## train the model 
  xgb = xgboost(data = trainData, label = trainLabels, nrounds = 20, objective = "binary:logistic")
  predicted_label = ifelse(predict(xgb, as.matrix(testData)) > 0.5, 1, 0)
  
  z <- (table(predicted_label, testLabels))
  
  scores[i] <- sum(diag(z))/sum(z)
  #Use the test and train data partitions however you desire...
}

mean(scores)






y = shot_csv$shot_made_numeric
#X = shot_csv %>% select(shot_zone_area, shot_distance, shot_value, attacker_height, defender_height)

X = fastDummies::dummy_cols(shot_csv %>% select(shot_zone_area, attacker_height, defender_height ))
X[, c("shot_zone_area", "attacker_height", "defender_height")] <- NULL

X = cbind.data.frame(X, shot_csv$shot_distance, shot_csv$shot_value)
X = X[-bad_index, ]
y = y[-bad_index]

X<-X[sample(nrow(X)),]
set.seed(7)

folds <- cut(seq(1,nrow(X)),breaks=5,labels=FALSE)

null_scores = c()
for(i in 1:5){
  
  testIndexes <- which(folds==i,arr.ind=TRUE)
  
  testData <- X[testIndexes, ]
  trainData <- as.matrix(X[-testIndexes, ])
  
  trainLabels <- y[-testIndexes]
  testLabels <- y[testIndexes]
  
  ## train the model 
  xgb = xgboost(data = trainData, label = trainLabels, nrounds = 20, objective = "binary:logistic")
  predicted_label = ifelse(predict(xgb, as.matrix(testData)) > 0.5, 1, 0)
  
  z <- (table(predicted_label, testLabels))
  
  null_scores[i] <- sum(diag(z))/sum(z)
  #Use the test and train data partitions however you desire...
}

### 0.5462062 is the null model 
mean(null_scores)

t.test()