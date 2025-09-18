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
    totpages = len(corpus.keys())
    transit_model = dict(zip(corpus.keys(),[(1-damping_factor)/totpages for _ in range(totpages)]))
    if len(corpus[page]):
        indi_prob = damping_factor/len(corpus[page])
    else:
        indi_prob = 0
    for i in corpus[page]:
        transit_model[i] += indi_prob
    return transit_model


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    all_pages = list(corpus.keys())
    pagerank_dict = dict(zip(all_pages,[0 for _ in range(len(all_pages))]))
    page = random.choice(all_pages)
    pagerank_dict[page] += 1
    for _ in range(n-1):
        transit = transition_model(corpus,page,damping_factor)
        choices = list(transit.keys())
        page = random.choices(choices,weights=[transit[i] for i in choices],k=1)[0]
        pagerank_dict[page] += 1
    for i in pagerank_dict:
        pagerank_dict[i] /= n
    return pagerank_dict

def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    N = len(corpus)
    for i in corpus:
        if len(corpus[i]) == 0:
            corpus[i] = set(corpus.keys()) 
    delta = 0.001
    pagerank_dict_prev = dict(zip(corpus.keys(),[1/N for _ in range(N)]))
    pagerank_dict_next = pagerank_dict_prev.copy()
    status = dict(zip(corpus.keys(),[False for _ in range(N)]))
    while not all(status.values()):
        for i in pagerank_dict_next:
            if not status[i]:
                pagerank_dict_next[i] = (1-damping_factor)/N + damping_factor*sum([pagerank_dict_prev[j]/len(corpus[j]) for j in pagerank_dict_prev if i in corpus[j]])
                if abs(pagerank_dict_next[i]-pagerank_dict_prev[i]) < delta:
                    status[i] = True
        if not all(status.values()):
            pagerank_dict_prev = pagerank_dict_next.copy()
    return pagerank_dict_prev



if __name__ == "__main__":
    main()
