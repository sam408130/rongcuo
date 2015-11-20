#!/usr/bin/env python  
#-*-coding:utf-8 -*- 
import time
import sys
import re
import daopai
import pinyin


# The Trie data structure keeps a set of words, organized with one node for
# each letter. Each node has a branch for each letter that may follow it in the
# set of words.
class TrieNode:
    def __init__(self):
        self.word = None
        self.children = {}

        #global NodeCount
        #NodeCount += 1

    def insert( self, word ):
        node = self

        for letter in word:
            if letter not in node.children: 
                node.children[letter] = TrieNode()

            node = node.children[letter]

        node.word = word


def search( word, maxCost):

    # build first row
    currentRow = range( len(word) + 1 )

    results = []

    # recursively search each branch of the trie
    for letter in trie.children:
        searchRecursive( trie.children[letter], letter, word, currentRow, 
            results, maxCost )

    return results

# This recursive helper is used by the search function above. It assumes that
# the previousRow has been filled in already.
def searchRecursive( node, letter, word, previousRow, results, maxCost ):

    columns = len( word ) + 1
    currentRow = [ previousRow[0] + 1 ]

    # Build one row for the letter, with a column for each letter in the target
    # word, plus one for the empty string at column 0
    for column in xrange( 1, columns ):

        insertCost = currentRow[column - 1] + 1
        deleteCost = previousRow[column] + 1
        if word[column - 1] == letter or pinyin.get(word[column - 1])==pinyin.get(letter):
            replaceCost = previousRow[ column - 1 ] 
        else:                
            replaceCost = previousRow[ column - 1 ] + 1

        currentRow.append( min( insertCost, deleteCost, replaceCost ) )
    # if the last entry in the row indicates the optimal cost is less than the
    # maximum cost, and there is a word in this trie node, then add it.
    if currentRow[-1] <= maxCost and node.word != None:
        results.append( [node.word, currentRow[-1]]  )

    # if any entries in the row are less than the maximum cost, then 
    # recursively search each branch of the trie
    if min( currentRow ) <= maxCost:
        for letter in node.children:
            searchRecursive( node.children[letter], letter, word, currentRow, 
                results, maxCost )


def main(TARGET,MAX_COST,tag):
    global trie
    trie=TrieNode()
    names=daopai.search(TARGET,tag)
    #print len(names)
    #for i in names:print i.decode('utf-8')
    for word in names:
        #WordCount += 1
        tempmat=re.compile('##').split(word)
        try:
            insert_word=tempmat[0].decode('utf-8')
            trie.insert( insert_word )
        except:
            continue    
    results = search( TARGET.decode('utf-8'), MAX_COST )
    return results


if __name__=='__main__':
    TARGET = '乡村音乐'
    MAX_COST = 2

    # Keep some interesting statistics
    NodeCount = 0
    WordCount = 0

    global trie
    # read dictionary file into a trie
    trie = TrieNode()
    names=open('tags.txt','r').readlines()
    start = time.time()
    #names=daopai.search(TARGET)
    #names=['cat','cats','bat','ict']
    for word in names:
        WordCount += 1
        tempmat=re.compile('##').split(word)
        try:
            insert_word=tempmat[0].decode('utf-8')
            trie.insert( insert_word )
        except:
            continue

    

    '''
    for i in trie.children:
        print i ,trie.children[i]
    print "Read %d words into %d nodes" % (WordCount, NodeCount)
    # The search function returns a list of all words that are less than the given
    # maximum distance from the target word
    
    
    
    pool=multiprocessing.Pool(processes=3)
    poolresult=[]
    for i in xrange(100):
        poolresult.append(pool.apply_async(test))
    pool.close()
    pool.join()
    '''
    results=search( TARGET.decode('utf-8'), MAX_COST )
    end = time.time()
    for result in results:
        print result[0],result[1]
    print "Search took %g s" % (end - start)
    #for result in results: print result[0]  
