from backend.api import LM


def detect(file=None, text=None):
    lm = LM()
    # text = 'The cat was playing in the garden . I was happy in the way I am'

    if file:
        with open(file, 'r') as fl:
            data = fl.read().lower()
    else:
        data = text
    # print(str(text))    

    payload = lm.check_probabilities(data, topk=20)
    payload_string = payload['bpe_strings']
    payload_pred = payload['pred_topk']
    # print(payload)

    count = 0

    for i in range(1,len(payload_string)):
        for pred in payload_pred[i-1]:
            if payload_string[i] == pred[0]:
                count += 1
            else:
                continue

    if text:
        if count > len(data.split()):
            score = 100
        else:
            score = count/len(data.split()) * 100
    else:
        if count > len(data.split()):
            score = 100
        else:            
            score = count/len(data.split()[:1024]) * 100
    
    print(score)     
    return score           
    
# detect(file='../../shake_1.txt')    