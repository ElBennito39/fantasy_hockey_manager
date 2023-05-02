
#Utility for handling various NHL api time outputs
#takes MM:SS MMM:SS MMMM:SS and gives seconds

def convert_mintime_to_seconds(time_str):
    if time_str is None:
        return 0
    minutes, seconds = time_str.split(':')
    return int(minutes) * 60 + int(seconds)
