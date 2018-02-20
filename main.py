from bs4 import BeautifulSoup
from collections import defaultdict

import urllib2, string, os, shutil

import numpy as np
import matplotlib.pyplot as plt

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
            #elif os.path.isdir(file_path): shutil.rmtree(file_path)
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

    print 'Done!'



# ---------------------------------------------------------------------------
# Plot takes the information and uses matplotlib to visualize the information
# ---------------------------------------------------------------------------
def plot():
    # plot the information
    index = np.arange(len(sorted_list.keys()))
    plt.bar(index, sorted_list.values())
    plt.xlabel('Language', fontsize=5)
    plt.ylabel('Count', fontsize=5)
    plt.xticks(index, sorted_list.keys(), fontsize=10, rotation=90)
    plt.title('Usage of Programming Language words in Hacker News Posts')
    plt.show()


# ---------------------
# Start of Main Routine
# ---------------------

folder = 'pages'
url_list_file = open('url_list.txt', 'r')
sorted_list = dict()
counts = dict()
languages=[ 'python',
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
# Loop through file for urls, print some comments from it
for the_file in os.listdir(folder):
    with open('pages\\'+the_file, 'r') as f:
        soup = BeautifulSoup(f.read(), 'html.parser')

        comments = soup.find_all("span", class_="c00")
        for comment in comments:
            text = comment.p.get_text().encode('utf-8')
            for word in text.split():
                lw = word.lower()
                if lw.rstrip('.') in languages:
                    if lw in counts:
                        counts[lw] += 1
                    else:
                        counts[lw] = 1
    print '.',
print 'Sorting...'

for key, value in sorted(counts.iteritems(), key=lambda (k,v): (v,k)):
    sorted_list[key] = value


print 'Plotting...'
plot()
