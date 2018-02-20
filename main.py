from bs4 import BeautifulSoup
from collections import defaultdict

import urllib2, string, os, shutil

import numpy as np
import matplotlib.pyplot as plt

# Matt McDade
# This program downloads news.ycombinator.com "Who's Hiring" posts
# and analyzes the usage of popular programming languages to see
# what are the most in-demand languages to young companies

# In the future, this program will display the change of each language
# over time to track the pop


# ---------------------------------------------------------
# Download pages goes through the url text file to download
#      recent copies of the corresponding html files
# ---------------------------------------------------------
def download_pages():

    # Open the file containing the urls for reading
    url_list_file = open('url_list.txt', 'r')


    # Delete old files
    print 'Deleting old files...'
    for the_file in os.listdir(folder):
        file_path = os.path.join(folder, the_file)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
        except Exception as e:
            print(e)

    # Loop through file for urls, print some comments from it
    print 'Downloading new html files...'
    for url in url_list_file:
        filename = 'pages\\' + url[-8:].rstrip('\n') + '.html'
        response = urllib2.urlopen(url)
        soup = BeautifulSoup(response.read(), 'html.parser')
        with open(filename, 'w') as file:
            file.write(str(soup))
        print '.',
    print 'Done!'



# ---------------------------------------------------------------------------
# Plot takes the information and uses matplotlib to visualize the information
# ---------------------------------------------------------------------------
def plot():
    # plot the information
    index = np.arange(len(counts.keys()))
    plt.bar(index, counts.values())
    plt.xlabel('Language', fontsize=15)
    plt.ylabel('Count', fontsize=15)
    plt.xticks(index, counts.keys(), fontsize=10, rotation=80)
    plt.title('Usage of Programming Language words in Hacker News Posts')
    plt.tight_layout() # Automagically sets boundaries to be tight af
    plt.show()



# ---------------------
# Start of Main Routine
# ---------------------

# Assign initial variables -
# folder = directory of html files,
# url_list_file = pretty self-explanatory
# counts = dictionary language and number of times seen
# languages = list of all languages to look for and plot
folder = 'pages'
url_list_file = open('url_list.txt', 'r')
counts = dict()
languages = [ 'python',
            'javascript',
            'react',
            'c++',
            'php',
            'java',
            'c',
            'c#',
            'html',
            'css',
            'r',
            'go',
            'swift',
            'android',
            'ios',
            'ruby',
            'perl',
            'scala',
            'sql',
            'typescript',
            'visualbasic',
            'haskell',
            'rust',
            'clojure',
            'redux',
            'redis',
            'elixir',
            'node.js',
            'rails']


# Ask to download pages or not
answer = raw_input('Download new files? (y/n) ')
if answer == 'y':
    download_pages()

print 'Finding languages...'
for the_file in os.listdir(folder):
    with open('pages\\'+the_file, 'r') as f:
        soup = BeautifulSoup(f.read(), 'html.parser')

        # Looking through the html files, I found all the comments are span tags with class c00
        comments = soup.find_all("span", class_="c00")
        for comment in comments:
            text = comment.p.get_text().encode('utf-8')
            for word in text.split():             # Loop through every word in the comment.
                lw = word.lower().strip('.')      # Change word to lower case, and remove any periods.
                if lw in languages:               # If word exists in languages, continue.
                    if lw in counts:              # If the language exists in the dictionary, increment it.
                        counts[lw] += 1
                    else:                         # If it doesnt, add a new key with value 1.
                        counts[lw] = 1
    print '.', # Print a dot every time it finishes
               # an html file before looping again

print '\nPlotting...'
plot()
