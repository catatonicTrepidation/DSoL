from GetFromFile import get_comments
from GetFromFile import get_vocab


adverbs = get_vocab("adverbs")
preps = get_vocab("prepositions")
nouns = get_vocab("nouns")

subjects = "i you he she we they".split()
subjects.extend(get_vocab("names"))

#adjectives = "my your his her our their".split()
adjectives = get_vocab("adjectives")

verbs = "is was been".split() # would do well to have all irregular verb conjugations
verbs.extend(get_vocab("verbs"))

articles = "the a an some one few my your his her our their".split()


conjunctions = "and-but-than-rather than-whether-though-which-who-whose-whom-whomever-how".split("-")


def msc(s):
    g = True
    w = s.lower().replace(',','').split()
    vc = 0
    for i in range(len(w)):
        tg = False
        #print(w[i])
        if w[i] in subjects or w[i] in nouns:
            #print("subject or noun!")
            v = expverb(w[i+1:],vc)
            tg = v or expprep(w[i+1:])
            if v:
                vc = (vc+1)%2
        if w[i] in verbs or w[i] in articles or w[i] in conjunctions:
            #print("verb!")
            tg = tg or expnoun(w[i+1:])
        if w[i] == "that":
            #print(w[i+1:])
            tg = tg or msc(" ".join(w[i+1:]))
            return tg
        g = tg and g
    #print("-",g)
    return g


def expverb(w,vc):
    for i in range(len(w)):
        if w[i] not in adverbs:
            return w[i] in verbs
    return vc == 1

def expprep(w):
    return len(w) != 0 and w[0] in preps

def expadv(w):
    return True

def expnoun(w):
    #print(w)
    for i in range(len(w)):
        s = w[i]
        s = s.replace("ing", "")
        t = w[i]
        t = t.replace("'s", "")
        if w[i] not in adjectives:
            return s in verbs or t in nouns
    return False

def page_stats(comments):
    stats = [0,0,0,0,0,0]*2
    total_sentences = 0
    total_correct = 0
    total_words = 0
    for c in comments:
        total_sentences+=1
        if msc(c):
            total_correct+=1
        c_stats = comment_stats(c)
        total_words += c_stats[1] # number of words
        s_stats = c_stats[0] # number of subjects, nouns, etc
        for i in range(len(s_stats)):
            stats[2*i] += s_stats[i]
    unknown = total_words
    for i in range(len(s_stats)):
        stats[2*i+1] = stats[2*i]*100/total_words
        unknown -= stats[2*i]
    stats.extend([unknown, unknown*100/total_words])
    return (stats,total_correct/total_sentences,total_words)

def comment_stats(c):
    words = c.split()
    word_types = [subjects, nouns, adjectives, verbs, adverbs, preps]
    c_stats = [0,0,0,0,0,0]
    total = 0
    for w in words:
        for i in range(len(c_stats)):
            c_stats[i] += 1 if w in word_types[i] else 0
        total+=1
    return (c_stats,total)


def output_stats(file_name,stats,output):
    
    print("-" + file_name + "-")
    print("%.0f subjects (%.1f%%) \n%.0f nouns (%.1f%%) \n%.0f adjectives (%.1f%%) \n%.0f verbs (%.1f%%) \n%.0f adverbs (%.1f%%) \n%.0f prepositions (%.1f%%) \n%.0f unknown words (%.1f%%)" % tuple(stats[0]))
    print(stats[2], "words total\n")
    print("%f%% of comments were marked as grammatically correct\n" % (100*stats[1]))
    
    output.write("-" + file_name + "-\n")
    output.write("%.0f subjects (%.1f%%) \n%.0f nouns (%.1f%%) \n%.0f adjectives (%.1f%%) \n%.0f verbs (%.1f%%) \n%.0f adverbs (%.1f%%) \n%.0f prepositions (%.1f%%) \n%.0f unknown words (%.1f%%)\n" % tuple(stats[0]))
    output.write(str(stats[2]) + " words total\n\n")
    output.write("%f%% of comments were marked as grammatically correct\n\n" % (100*stats[1]))


if __name__ == "__main__":
    output_number = 6
    output = open('output/output' + str(output_number) + '.txt', 'w')
    
    print("----------STATS----------\n")
    output.write("----------STATS----------\n")
    
    
    """https://www.youtube.com/watch?v=R36F8CWAi2k"""
    poset_comments = get_comments('/users/miaow/Desktop/DSoL/comments/posetcomments.json')
    poset_stats = page_stats(poset_comments)
    output_stats("poset_comments",poset_stats,output)
    
    """https://www.youtube.com/watch?v=I3kVxW8IriA"""
    doge_comments = get_comments('/users/miaow/Desktop/DSoL/comments/dogecomments.json')
    doge_stats = page_stats(doge_comments)
    output_stats("doge_comments",doge_stats,output)
    
    """https://www.youtube.com/watch?v=Fj-o3gYhSyc"""
    poset_comments = get_comments('/users/miaow/Desktop/DSoL/comments/hotelcomments.json')
    poset_stats = page_stats(poset_comments)
    output_stats("spanish_comments",poset_stats,output)
    
    """https://www.youtube.com/watch?v=Q8savTZOzY0"""
    poset_comments = get_comments('/users/miaow/Desktop/DSoL/comments/schrodingercomments.json')
    poset_stats = page_stats(poset_comments)
    output_stats("japanese_comments",poset_stats,output)


    output.close()
