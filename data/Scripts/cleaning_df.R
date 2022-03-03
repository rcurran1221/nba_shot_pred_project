library(dplyr)
library(fuzzyjoin)
library(assertr)

setwd("~/Documents/GT Masters/CSE 6242/project")
df1 = read.csv("shot_logs.csv")


df %>% head(5) 

## We are looking for distinct player_name ##

distinct_names <- df %>% distinct(player_name)

### We are going to find the playerid by player name #### 

ids <- apply(distinct_names, 1, find_player_id_by_name)
distinct_names$ids <- ids 

missing_names <- distinct_names %>% filter(is.na(ids)) %>% select(player_name)
missing_names$player_name <- as.character(missing_names$player_name)
### Some manually cleaning is going to need to be done ####

missing.df.1 <- stringdist_left_join(missing_names, 
                          available_players, 
                          by = c(player_name = "lower_name"))

still.missing <- missing.df.1 %>% filter(is.na(person_id))

missing.df.1[which(missing.df.1$player_name == "otto porter"), "person_id"] = 203490
missing.df.1[which(missing.df.1$player_name == "nene hilario"), "person_id"] = 2403
missing.df.1[which(missing.df.1$player_name == "jose juan barea"), "person_id"] = 200826
missing.df.1[which(missing.df.1$player_name == "james ennis"), "person_id"] = 203516

### Check That This Is 0 Rows #### 
stopifnot(missing.df.1 %>% filter(is.na(person_id)) %>% nrow()  == 0)

distinct_names <- distinct_names %>% left_join(., 
                             missing.df.1 %>% select(player_name, person_id),
                             by = c("player_name" = "player_name"))

distinct_names <- distinct_names %>% mutate(final_ids = coalesce(ids, person_id)) %>% 
  select(player_name, final_ids) %>% 
  rename(player_id = final_ids)

### Check that they are all unique ids ####
stopifnot(distinct_names %>% distinct(., ) %>% nrow() == nrow(distinct_names))

df <- df %>% left_join(.,
                 distinct_names) 


#### Default Season: 2014-15 #### 

player_ids <- df %>% distinct(player_id) %>% .$player_id
for (i in player_ids[140:length(player_ids)]){
  
  tryCatch({
  #print(i)
  shots <- fetch_shots_by_player_id_and_season(
    player_id = i, 
    season = "2014-15"
  )
  shots <- shots$player
  data.table::fwrite(shots, paste0("shots/", i, ".csv"))
  Sys.sleep(5)
  }, 
  
   error = function(e) {
     print(paste0("Could Not Find Player: ", i))
     #missing_shots <- paste0("Could Not Find Player: ", i)
     
   })
  
}

                    
path = "shots/"
out.file<-""
file.names <- dir(path, pattern =".csv")
for(i in 1:length(file.names)){
  file <- read.table(paste0("shots/", file.names[i]),header=TRUE, sep=",", stringsAsFactors=FALSE)
  out.file <- rbind(out.file, file)
}

data.table::fwrite(out.file, "shot_location.csv")
out.file <- out.file %>% filter(!is.na(player_id))

out.file <- out.file[2:nrow(out.file), ]

out.file = out.file %>% group_by(player_id, game_id) %>% mutate(shot_id = seq(n())) 
out.file = out.file %>% ungroup()

df <- df %>% group_by(player_id, GAME_ID) %>% mutate(shot_id = seq(n()))

out.file <- out.file %>% rename(GAME_ID = game_id)
location_df <- out.file
location_df$GAME_ID = as.numeric(location_df$GAME_ID)
location_df$player_id = as.numeric(location_df$player_id)
location_df$player_name <- NULL
shots_with_location <- df %>% left_join(., location_df)

shots_with_location %>% filter(FGM == shot_made_numeric) %>% nrow()
View(shots_with_location %>% filter(FGM != shot_made_numeric))

shots_with_location %>% data.table::fwrite(., "shots_log_location.csv")
# write.table(out.file, file = "cand_Brazil.txt",sep=";", 
#             row.names = FALSE, qmethod = "double",fileEncoding="windows-1252")

  




