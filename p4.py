from nltk import word_tokenize
from nltk.corpus import stopwords
import matplotlib.pyplot as plt
import numpy as np
import time
import json
import operator
import collections
import sys

def separate_records(filename):
    with open(filename, 'r') as fo:
        filename_three_plus_stars = "medium_three_plus_stars.json"
        filename_two_minus_stars = "medium_two_minus_stars.json"
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
    filename_three_plus_stars = "medium_three_plus_stars.json"
    filename_two_minus_stars = "medium_two_minus_stars.json"
    #separate_records(filename)
    top_words = get_twenty_most_used_words(filename_three_plus_stars)
    print "Top 20 words for 3+ Stars ratings.\n"
    figures_three = []
    for word, tupl in top_words:
        times = tupl[0]
        times_by_stars = tupl[1]
        # Graphics
        figure = plt.figure()

        # fixed bin size
        bins = np.arange(2, 7, 1)
        x = times_by_stars[0]*[3.0]
        # the histogram of the data
        plt.hist(x, bins=bins, alpha=0.8, align='left')

        x = times_by_stars[1]*[4.0]
        # the histogram of the data
        plt.hist(x, bins=bins, alpha=0.8, align='left')

        x = times_by_stars[2]*[5.0]
        # the histogram of the data
        plt.hist(x, bins=bins, alpha=0.8, align='left')

        plt.xticks(bins[1:-1])
        plt.xlabel('Stars')
        plt.ylabel('Frequency')
        plt.title(r'Word="{}"'.format(word))

        figures_three.append(figure)
        print word, times, times_by_stars
    i = 0
    for figure in figures_three:
        figure.savefig("plot_three_medium{}.png".format(i))
        i += 1
    print "\nTop 20 words for 2- Stars ratings.\n"
    top_words = get_twenty_most_used_words(filename_two_minus_stars)
    figures_two = []
    for word, tupl in top_words:
        times = tupl[0]
        times_by_stars = tupl[1]
        # Graphics
        figure = plt.figure()

        # fixed bin size
        bins = np.arange(0, 4, 1)
        x = times_by_stars[0]*[1.0]
        # the histogram of the data
        plt.hist(x, bins=bins, alpha=0.8, align='left')

        x = times_by_stars[1]*[2.0]
        # the histogram of the data
        plt.hist(x, bins=bins, alpha=0.8, align='left')

        plt.xticks(bins[1:-1])
        plt.xlabel('Stars')
        plt.ylabel('Frequency')
        plt.title(r'Word="{}"'.format(word))

        figures_two.append(figure)
        print word, times, times_by_stars
    i = 0
    for figure in figures_two:
        figure.savefig("plot_two_medium{}.png".format(i))
        i += 1

def get_twenty_most_used_words(filename):
    with open(filename, 'r') as fo:
        words = {}
        while True:
            line = fo.readline()
            if line is None or line is "":
                break
            data = json.loads(line)
            tokenized_words = [i for i in set(word_tokenize(data['text'].lower())) if i not in stopwords.words('english')]
            for token in tokenized_words:
                try:
                    if data['stars'] == 3:
                        words[token] = (words[token][0] + 1, [words[token][1][0] + 1, words[token][1][1], words[token][1][2]])
                    elif data['stars'] == 4:
                        words[token] = (words[token][0] + 1, [words[token][1][0], words[token][1][1] + 1, words[token][1][2]])
                    elif data['stars'] == 5:
                        words[token] = (words[token][0] + 1, [words[token][1][0], words[token][1][1], words[token][1][2] + 1])
                    elif data['stars'] == 2:
                        words[token] = (words[token][0] + 1, [words[token][1][0], words[token][1][1] + 1])
                    else:
                        words[token] = (words[token][0] + 1, [words[token][1][0] + 1, words[token][1][1]])
                except:
                    if data['stars'] == 3:
                        words[token] = (1, [1, 0, 0])
                    elif data['stars'] == 4:
                        words[token] = (1, [0, 1, 0])
                    elif data['stars'] == 5:
                        words[token] = (1, [0, 0, 1])
                    elif data['stars'] == 2:
                        words[token] = (1, [0, 1])
                    else:
                        words[token] = (1, [1, 0])
        top_words = sorted(words.items(), key=lambda x: x[1][0], reverse=True)[0:20]
        #top_words = counter.most_common(20)
        return top_words

if __name__ == '__main__':
    time_start = time.clock()
    filename = "yelp_medium.json" # only useful for separation.
    # Write output to file in write mode.
    _fo = open("p4_summary1.txt", 'w')
    sys.stdout = _fo
    obtain_top_twenty_words(filename)
    time_end = time.clock()
    print "\nTime taken to completion of the metric: {0} in processor time".format(time_end - time_start)
    _fo.close()
