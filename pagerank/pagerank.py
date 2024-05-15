import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    trans_mod = dict()

    num_files = len(corpus)

    num_links = len(corpus[page])

    if num_links != 0:
        rand_prob = (1-damping_factor)/num_files
        spec_prob = damping_factor/num_links
    else:
        rand_prob = (1-damping_factor)/num_files
        spec_prob = 0

    for file in corpus:
        if len(corpus[page]) == 0:
            trans_mod[file] = 1/num_files
        else:
            if file not in corpus[page]:
                trans_mod[file] = rand_prob
            else:
                trans_mod[file] = spec_prob+rand_prob

    if round(sum(trans_mod.values()),5) != 1:
        print(f'ERROR! Probabiliies add up to {sum(trans_mod.values())}')
    else:
        return trans_mod


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    redict = dict()
    pages = list(corpus.keys())
    rand_page = random.choice(pages)
    prob_next_sample = transition_model(corpus, rand_page, damping_factor)



def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    redict = dict()
    pages = list(corpus.keys())
    for page in pages:
        pr = 1/len(pages)



if __name__ == "__main__":
    main()
