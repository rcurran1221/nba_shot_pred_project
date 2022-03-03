library(dplyr)

fname <- file.choose()
### READ IN SHOT LOG LOCATION ###
data <- read.csv(fname)

View(table(data$shot_zone_area, data$loc_x))

zones = (data %>% group_by(shot_zone_area) %>% 
  summarize(min_x = min(loc_x),
         max_x = max(loc_x), 
         min_y = min(loc_y), 
         max_y = max(loc_y)) %>% 
    filter(!is.na(max_x)))

zones %>% data.table::fwrite(., "/Users/adam/Documents/GT Masters/CSE 6242/CSE6242-Project/data/zone_lookup.csv")
