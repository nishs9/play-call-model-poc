import pandas as pd
import numpy as np

features = ["pos_team", "posteam_home", "posteam_away", "def_team", "score_differential", "yardline_100", "half_seconds_remaining", "qtr",
            "down", "ydstogo", "normal_first_down", "first_and_short", "first_and_long", "second_and_short", "second_and_medium", "second_and_long",
            "third_and_short", "third_and_medium", "third_and_long", "in_redzone", "is_two_minute_drill", "is_goal_to_go", "curr_drive_length"] 

output_columns = ["play_type", "play_length"]

def convert_drive_start_to_raw_yards(drive_start_label: str, posteam: str) -> int:
    if (drive_start_label == "50"):
        return 50
    drive_start_label_split = drive_start_label.split(" ")
    side_of_field = drive_start_label_split[0].strip()
    relative_yardline = int(drive_start_label_split[1])
    if (posteam == side_of_field):
        return int(100 - int(relative_yardline))
    else:
        return posteam, int(relative_yardline)
    
def pre_process_training_data(year: int = 2024, save_data: bool = False) -> tuple[pd.DataFrame, pd.Series, pd.Series, pd.DataFrame]:
    df = pd.read_csv(f"raw_pbp_data/{year}_NFL.csv", low_memory=False)
    df['year'] = year
    df = df[df['season_type'] == 'REG']
    df = df[df['down'].isin([1,2,3])]
    df = df[df['play_type'].isin(['pass', 'run'])]
    df = df[~((df['air_yards'] == 0) & (df['play_type'] == 'pass'))]
    df = df[~((df['air_yards'].isna()) & (df['play_type'] == 'pass'))]
    df = df[~(df['drive_start_yard_line'].isna())]

    df["pos_team"] = df["posteam"]
    df["def_team"] = df["defteam"]

    df[["posteam", "drive_start_yard_line_100"]] = df[["posteam", "drive_start_yard_line"]].apply(lambda row: convert_drive_start_to_raw_yards(row["drive_start_yard_line"], row["posteam"]), axis=1, result_type='broadcast')

    df["curr_drive_length"] = df["drive_start_yard_line_100"] - df["yardline_100"]

    df['posteam_home'] = (df['posteam'] == df['home_team']).astype(int)
    df['posteam_away'] = (df['posteam'] != df['home_team']).astype(int)

    df['normal_first_down'] = ((df['down'] == 1) & (df['ydstogo'] <= 10) & (df['ydstogo'] >= 7)).astype(int)
    df['first_and_short'] = ((df['down'] == 1) & (df['ydstogo'] < 5)).astype(int)
    df['first_and_long'] = ((df['down'] == 1) & (df['ydstogo'] > 10)).astype(int)
    df['second_and_short'] = ((df['down'] == 2) & (df['ydstogo'] <= 3)).astype(int)
    df['second_and_medium'] = ((df['down'] == 2) & (df['ydstogo'] > 3) & (df['ydstogo'] <= 7)).astype(int)
    df['second_and_long'] = ((df['down'] == 2) & (df['ydstogo'] > 7)).astype(int)
    df['third_and_short'] = ((df['down'] == 3) & (df['ydstogo'] <= 3)).astype(int)
    df['third_and_medium'] = ((df['down'] == 3) & (df['ydstogo'] > 3) & (df['ydstogo'] <= 7)).astype(int)
    df['third_and_long'] = ((df['down'] == 3) & (df['ydstogo'] > 7)).astype(int)
    df['is_two_minute_drill'] = ((df['half_seconds_remaining'] <= 120) & 
                                    ((df['qtr'] == 2) | (df['qtr'] == 4))).astype(int)
    df['in_redzone'] = (df['yardline_100'] <= 20).astype(int)
    df['is_goal_to_go'] = ((df['in_redzone'] == 1) & (df['ydstogo'] == df['yardline_100'])).astype(int)

    df['play_length'] = np.where(
            df['play_type'].isin(['pass']), df['air_yards'], 
            df['yards_gained']
        )
    
    if (save_data):
        saved_df = df[features + output_columns]
        saved_df.to_csv(f"training_data/{year}_NFL.csv", index=False)
    
    X = df[features]
    y_play_type = df["play_type"]
    y_play_length = df["play_length"]

    return X, y_play_type, y_play_length, df

if __name__ == "__main__":
    for year in range(2017, 2025):
        print(f"Cleaning and processing training data for {year}...")
        X, y_play_type, y_play_length, df = pre_process_training_data(year=year, save_data=True)