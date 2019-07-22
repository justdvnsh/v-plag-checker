from backend.api import LM


def detect(file=None, text=None):
    lm = LM()
    # text = 'The cat was playing in the garden . I was happy in the way I am'

    if file:
        with open(file, 'r') as fl:
            text = fl.read().lower()
    
    # print(str(text))    

    payload = lm.check_probabilities(text, topk=20)
    payload_string = payload['bpe_strings']
    payload_pred = payload['pred_topk']
    # print(payload)

    count = 0

    for i in range(1,len(payload_string)):
        # print(payload_string[i])
        # print(payload_string[i])
        # print(payload_pred[i-1])
        for pred in payload_pred[i-1]:
            if payload_string[i] == pred[0]:
                # print(payload_string[i], payload_pred[i-1])
                count += 1
            else:
                continue

    if text:
        score = count/len(text.split()) * 100
    else:
        score = count/len(text.split()[:1024]) * 100
    
    print(score)     
    return score           
    