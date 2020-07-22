# Inspired by https://github.com/simonwillcock/RipReddit/
import os
import getopt
import sys
import json
import requests
import codecs

# The main cmd


def get_items(subreddit, sort='hot', count: int = 1000):
    """ Returns a list of items from the given subreddit, sorted by hot, new, controversial, or top. """
    url = 'http://www.reddit.com/r/{}/{}.json?limit={}'.format(
        subreddit, sort, count)
    header = {'User-Agent': 'Amazing script'}
    try:
        request = requests.get(url, headers=header)
        json_data = request.json()
        return [x['data'] for x in json_data['data']['children']]
    except:
        print('Error: Subreddit ' + subreddit + ' did not resolve')
        return []


def demo():
    """ Runs a quick demo by getting posts from /r/wallpaper and printing them to the console. """
    print("Recent items from the Wallpaper subreddit:")
    items = get_items('wallpaper', count=10)
    for item in items:
        print('\t{} - {}'.format(item['title'], item['url']))

    print("\nRecent items from the Wallpaper subreddit, sorted by Top:")
    items = get_items('wallpaper', 'top')
    for item in items:
        print('\t{} - {}'.format(item['title'], item['url']))


# Command Line Options code below:

HELP_STR = """Usage:
    python3 ripreddit.py <subreddit 1> <subreddit 2> ...
\nCommand Line Options:
    -h --help: Prints this. Ignores all other options
    -d --demo: Runs a quick demo. Ignores all other options
    -c --clean: Deletes the default directory. Ignores all other options
    -i --inputfile: Defines a list of subreddits (1 per line) to go through (instead of args)
    -o --outputdir: The output directory. ./reddit by default
    -l --limit: The maximum links to get. Will usually return much less. 1000 by default
    -s --single: All outputs be concaternated into a single file (reddit.txt)
    -a --append: Appends instead of overwriting existing files
"""


def main(argv):
    subreddits = []
    outputdir = 'reddit'
    single = False
    write_char = 'w'
    limit = '1000'

    # Go through subreddits (stop once an arg starts with -)
    for arg in argv.copy():
        if arg.startswith('-'):
            break
        subreddits.append(arg)
        argv.remove(arg)

    # Attempt parsing args
    try:
        opts, args = getopt.getopt(argv, "hdci:o:l:sa", [
                                   "help", "demo", "clean", "inputfile=", "outputfile=", "limit=", "single", "append"])
    except:
        print(HELP_STR)
        sys.exit(2)

    # Go through args
    for opt, arg in opts:
        if opt in ('-h', '--help'):
            print(HELP_STR)
            sys.exit(0)
        elif opt in ('-d', '--demo'):
            demo()
            sys.exit(0)
        elif opt in ('-c', '--clean'):
            if os.path.exists(outputdir):
                import shutil
                shutil.rmtree(outputdir)
            sys.exit(0)
        elif opt in ('-s', '--single'):
            single = not single
        elif opt in ('-a', '--append'):
            write_char = 'a'
        elif opt in ('-o', '--outputdir'):
            # TODO: Check if valid directory
            outputdir = arg
        elif opt in ('-l', '--limit'):
            limit = int(arg)
        elif opt in ('-i', '--inputfile'):
            if not os.path.exists(arg):
                print('Input file invalid!')
                sys.exit(2)
            with open(arg, 'r') as file:
                for line in file.readlines():
                    subreddits.append(line.replace('\n', ''))
    if len(subreddits) <= 0:
        print("Error: No subreddits given.\n" + HELP_STR)
        sys.exit(2)

    # Actually do the work now
    # If mode isn't append and it's in single mode, clear reddit.txt (so we can append later)
    if single and 'w' in write_char:
        singleFile = os.path.join(outputdir, 'reddit.txt')
        if os.path.exists(singleFile):
            os.remove(singleFile)

    # Make working directory
    if not os.path.exists(outputdir):
        os.makedirs(outputdir)

    # Loop through all subreddits and save them
    for subreddit in subreddits:
        postList = get_items(subreddit, count=limit)
        urlList = [t['url'] for t in postList]

        # Save it
        if single:
            with codecs.open(os.path.join(outputdir, 'reddit.txt'), 'a+', 'utf-8-sig') as file:
                # Check for whitespace and add it
                if file.readable():
                    contents = file.read()
                    if len(contents > 0) and not contents.endswith('\n'):
                        file.write('\n')

                # Write actual content
                file.write('\n'.join(urlList))
        else:
            with codecs.open(os.path.join(outputdir, str(subreddit) + '.txt'), write_char + '+', 'utf-8-sig') as file:
                # Check for whitespace and add it
                if 'a' in write_char and file.readable():
                    contents = file.read()
                    if len(contents) > 0 and not contents.endswith('\n'):
                        file.write('\n')

                # Write actual content
                file.write('\n'.join(urlList))
    # We're done here


if __name__ == "__main__":
    main(sys.argv[1:])
