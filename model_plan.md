## NFL Simulation Engine Playcall Model

output: play_type, play_length
- play_length -> composite column made up of EITHER yards_gained or air_yards on a play (based on play type)

input
---
- posteam
- posteam_home (boolean)
- posteam_away (boolean)
- defteam
- score_differential
- yardline_100
- half_seconds_remaining
- qtr
- down
- ydstogo
- normal_first_down (1st + 7-10)
- first_and_short (1st + 6 or less)
- first_and_long (1st + 10+)
- second_and_long (2nd + 8+)
- second_and_medium (2nd + 4-7)
- second_and_short (2nd + 3 or less)
- third_and_long (3rd + 8+)
- third_and_medium (3rd + 4-7)
- third_and_short (3rd + 3 or less)
- in_redzone
- is_two_minute_drill
- is_goal_to_go
- curr_length_of_drive (yardline_100 - drive_start_yard_line)
