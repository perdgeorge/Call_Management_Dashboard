from src.data.seed_data import calls


def get_all_calls():
    return [call for call in calls if not call["is_archived"]]
