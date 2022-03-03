library(dplyr)

player_ids = read.csv("~/Documents/GT Masters/CSE 6242/CSE6242-Project/data/player_id.csv")
player_ids <- player_ids %>% distinct(id) %>% .$id

### Need to run the fetch_shots_by_player.R file first ### 
setwd("~/Documents/GT Masters/CSE6242-Project/project/shots_2015")
for (i in player_ids){
  
  tryCatch({
    #print(i)
    shots <- fetch_shots_by_player_id_and_season(
      player_id = i, 
      season = "2015-16"
    )
    shots <- shots$player
    if (nrow(shots)>0){
            data.table::fwrite(shots, paste0(i, ".csv"))
      }
    Sys.sleep(5)
  }, 
  
  error = function(e) {
    print(paste0("Could Not Find Player: ", i))
    #missing_shots <- paste0("Could Not Find Player: ", i)
    
  })
  
}

setwd("~/Documents/GT Masters/CSE 6242/project/")

path = "shots_2015/"
out.file<-""
file.names <- dir(path, pattern =".csv")
for(i in 1:length(file.names)){
  file <- read.table(paste0("shots/", file.names[i]),header=TRUE, sep=",", stringsAsFactors=FALSE)
  out.file <- rbind(out.file, file)
}

data.table::fwrite(out.file, "shot_location_2015.csv")
out.file <- out.file %>% filter(!is.na(player_id), game_event_id != "")

out.file$game_event_id <- as.numeric(out.file$game_event_id)
out.file$player_id <- as.numeric(out.file$player_id)
out.file$team_id <- as.numeric(out.file$team_id)
out.file$period <- as.numeric(out.file$period)
out.file$minutes_remaining <- as.numeric(out.file$minutes_remaining)
out.file$seconds_remaining <- as.numeric(out.file$seconds_remaining)
out.file$shot_distance <- as.numeric(out.file$shot_distance)
out.file$loc_x <- as.numeric(out.file$loc_x)
out.file$loc_y <- as.numeric(out.file$loc_y)
out.file$shot_attempted_flag <- as.numeric(out.file$shot_attempted_flag)
out.file$shot_made_numeric <- as.numeric(out.file$shot_made_numeric)
out.file$shot_value <- as.numeric(out.file$shot_value)




shot_csv = read.csv("/Users/adam/Documents/GT Masters/CSE 6242/CSE6242-Project/data/shots_log_location.csv")
                    

shots = bind_rows(shot_csv, out.file)

data.table::fwrite(shots, "/Users/adam/Documents/GT Masters/CSE 6242/CSE6242-Project/data/shots_log_location_v2.csv")




