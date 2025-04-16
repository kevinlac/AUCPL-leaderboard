def time_to_secs(time_string):
    times = time_string.split(":")
    return int(times[0]) * 3600 + int(times[1]) * 60 + int(times[2])

def secs_to_time(time_int):
    hours = str(time_int // 3600)
    time_int %= 3600
    minutes = str(time_int // 60)
    time_int %= 60
    seconds = str(time_int)
    final_string = ""
    if (len(hours) == 1): final_string += "0"
    final_string += hours + ":"
    if (len(minutes) == 1): final_string += "0"
    final_string += minutes + ":"
    if (len(seconds) == 1): final_string += "0"
    final_string += seconds
    return final_string
