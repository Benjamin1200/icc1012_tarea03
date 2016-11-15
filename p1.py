from nltk import word_tokenize
import time
import json
import operator
import collections
import sys

def separate_records(filename):
    with open(filename, 'r') as fo:
        filename_three_plus_stars = "data_three_plus_stars.json"
        filename_two_minus_stars = "data_two_minus_stars.json"
        data_three_plus_stars = open(filename_three_plus_stars, 'w')
        data_two_minus_stars = open(filename_two_minus_stars, 'w')
        b = 0
        errors = 0
        while True:
            line = fo.readline()
            b += 1
            if line is None or line is "":
                break
            try:
                data = json.loads(line)
                if data['stars'] >= 3.0:
                    data_three_plus_stars.write(line)
                else:
                    data_two_minus_stars.write(line)
            except:
                errors += 1
        data_three_plus_stars.close()
        data_two_minus_stars.close()

def obtain_top_twenty_words(filename):
        filename_three_plus_stars = "data_three_plus_stars.json"
        filename_two_minus_stars = "data_two_minus_stars.json"
        #separate_records(filename)
        top_words = get_twenty_most_used_words(filename_three_plus_stars)
        print "Top 20 words for 3+ Stars ratings.\n"
        for word, times in top_words:
            print word, times
        print "\nTop 20 words for 2- Stars ratings.\n"
        top_words = get_twenty_most_used_words(filename_two_minus_stars)
        for word, times in top_words:
            print word, times

def get_twenty_most_used_words(filename):
    #words = {}
    with open(filename, 'r') as fo:
        counter = collections.Counter()
        while True:
            line = fo.readline()
            if line is None or line is "":
                break
            data = json.loads(line)
            tokenized_words = set(word_tokenize(data['text'].lower()))
            for token in tokenized_words:
                counter[token] += 1
                #try:
                #    words[token] += 1
                #except:
                #    words[token] = 1
        #top_words = sorted(words.items(), key=operator.itemgetter(1), reverse=True)[0:20]
        top_words = counter.most_common(20)
        return top_words

if __name__ == '__main__':
    time_start = time.clock()
    filename = "yelp_academic_dataset_review.json" # only useful for separation.
    # Write output to file in write mode.
    _fo = open("p1_summary2.txt", 'w')
    sys.stdout = _fo
    obtain_top_twenty_words(filename)
    time_end = time.clock()
    print "\nTime taken to completion of the metric: {0} in processor time".format(time_end - time_start)
    _fo.close()
