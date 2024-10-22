
def calculate_percent(cons : dict, sum_of_cons : int) -> dict:
    new_dict = dict()
    for key, value in cons.items():
        new_dict[key] = round((value / sum_of_cons) * 100)
    return new_dict