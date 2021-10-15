def countingValleys(steps, path):
    valley_counter = 0
    sea_level_counter = 0
    found_downhill = False
    
    for index, step in enumerate(path):

        if path[index] == "U":
            if found_downhill:
                sea_level_counter += 1
                if sea_level_counter == 0:
                    valley_counter += 1
                    found_downhill = False
                else:
                    continue
            else:
                sea_level_counter += 1
                
        elif path[index] == "D":
            if not found_downhill and sea_level_counter == 0:
                found_downhill = True
            sea_level_counter += -1
    
    return valley_counter
