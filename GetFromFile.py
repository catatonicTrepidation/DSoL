import json
import sys

def get_comments(inpath):
    with open(inpath) as data_file:
        comments = json.load(data_file)
    comments_formatted = []
    for c in comments:
            comments_formatted.append(c["commentText"]) # push each comment into list
    return comments_formatted

def get_vocab(type):
    with open("vocabulary/"+type+"_formatted.txt") as vocab:
        vocab_formatted = []
        for v in vocab:
            vocab_formatted.append(v[:-1]) # push each vocabulary word into list
        return vocab_formatted


if __name__ == "__main__":
    out_name = 'adverbs'
    if len(sys.argv) > 1:
        out_name = sys.argv[1]
    output = open('vocabulary/' + out_name + '_formatted.txt','w')
    with open("vocabulary/" + out_name + ".txt") as vocab:
        for v in vocab:
            output.write(v.lower()) # push each vocabulary word into list

