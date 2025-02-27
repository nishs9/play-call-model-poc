## NFL Simulation Engine Playcall Model

output: play_type, play_length
- play_length -> composite column made up of EITHER yards_gained or air_yards on a play (based on play type)

input
---
posteam
posteam_home (boolean)
posteam_away (boolean)
defteam
score_differential
yardline_100
half_seconds_remaining
qtr
down
ydstogo
normal_first_down
first_and_short
first_and_long
second_and_long
second_and_medium
second_and_short
third_and_long
third_and_medium
third_and_short
in_redzone
is_two_minute_drill
is_goal_to_go
curr_length_of_drive (yardline_100 - drive_start_yard_line)
