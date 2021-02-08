import pandas as pd
import json

def load_data(filename):
    rawData = []
    with open(filename+".json") as f:
        content = f.read()
        rawData = json.loads(content)
    return rawData

def process_data(rawData):
    data, language, version = [], [], [],
    excludedPIDs = []
    for d in rawData:
        data.append(d["data"])
        language.append(d["data"]["answers"][0])
        dVersion = d["data"]["gameVersion"]
        if (dVersion == "Normal"):
            dVersion = "Game"
        version.append(dVersion)
            
    duration, gaming_frequency = [], []
    imi1, imi2, imi3, imi4, imi5, imi6, imi7, imi_enjoyment = [], [], [], [], [], [], [], []
    grammatical_moves, moves_with_noun, total_moves = [], [] ,[]
    proportion_of_valid_data, proportion_of_valid_data_providing_mechanic_actuations = [], []
    for i, d in enumerate(data):
        gaming_frequency.append(d["answers"][1])

        # Calculate IMI Enjoyment subscale mean
        # Scores for questions 3 and 4 are reversed
        a = [int(numeric_string) for numeric_string in d["answers"][2:]]
        imi1.append(a[0])
        imi2.append(a[1])
        imi3.append(a[2])
        imi4.append(a[3])
        imi5.append(a[4])
        imi6.append(a[5])
        imi7.append(a[6])
        imi_value = (a[0] + a[1] + (6-a[2]) + (6-a[3]) + a[4] + a[5] + a[6])/7
        imi_enjoyment.append(imi_value)

        # Calculate proportions of valid moves:
        count_gram = sum([is_grammatical(a) and has_noun(a) for a in d["moves"]])
        count_w_noun = sum([has_noun(a) for a in d["moves"]])
        count_all = len(d["moves"])
        total_moves.append(count_all)
        grammatical_moves.append(count_gram)
        moves_with_noun.append(count_w_noun)
        proportion_of_valid_data.append(count_gram/count_all)
        proportion_of_valid_data_providing_mechanic_actuations.append(count_gram/count_w_noun)
    d = { 
            "version": version,
            "language": language,
            "gaming_frequency": gaming_frequency,
            "imi1": imi1, "imi2": imi2, "imi3": imi3, "imi4": imi4, "imi5": imi5, "imi6": imi6, "imi7": imi7,
            "imi_enjoyment": imi_enjoyment,
            "total_moves" : total_moves,
            "moves_with_noun": moves_with_noun,
            "grammatical_moves": grammatical_moves,
            "proportion_of_valid_data" : proportion_of_valid_data,
            "proportion_of_valid_data_providing_mechanic_actuations": proportion_of_valid_data_providing_mechanic_actuations
        }
    df = pd.DataFrame(data=d)
    return df

def is_grammatical(array):
    a = []
    adj1 = ["big", "small"]
    adj2 = ["empty", "filled"]
    adj3 = ["red", "blue", "green"]
    nouns = ["square","circle","triangle"]
    for word in array:
        if word in adj1:
            a.append(1)
        if word in adj2:
            a.append(2)
        if word in adj3:
            a.append(3)
        if word in nouns:
            a.append(4)
    return (a[0] < a[1] < a[2])

def has_noun(array):
    nouns = ["square","circle","triangle"]
    for word in array:
        if word in nouns:
            return True
    return False
