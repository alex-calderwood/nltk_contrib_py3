# Natural Language Toolkit: Parsers
#
# Copyright (C) 2001-2007 NLTK Project
# Author: Steven Bird <sb@csse.unimelb.edu.au>
#         Edward Loper <edloper@gradient.cis.upenn.edu>
# URL: <http://www.nltk.org/>
# For license information, see LICENSE.TXT
#

"""
Classes and interfaces for producing tree structures that represent
the internal organization of a text.  This task is known as X{parsing}
the text, and the resulting tree structures are called the text's
X{parses}.  Typically, the text is a single sentence, and the tree
structure represents the syntactic structure of the sentence.
However, parsers can also be used in other domains.  For example,
parsers can be used to derive the morphological structure of the
morphemes that make up a word, or to derive the discourse structure
for a set of utterances.

Sometimes, a single piece of text can be represented by more than one
tree structure.  Texts represented by more than one tree structure are
called X{ambiguous} texts.  Note that there are actually two ways in
which a text can be ambiguous:

    - The text has multiple correct parses.
    - There is not enough information to decide which of several
      candidate parses is correct.

However, the parser module does I{not} distinguish these two types of
ambiguity.

The parser module defines C{ParseI}, a standard interface for parsing
texts; and two simple implementations of that interface,
C{ShiftReduce} and C{RecursiveDescent}.  It also contains
three sub-modules for specialized kinds of parsing:

  - C{nltk.parser.chart} defines chart parsing, which uses dynamic
    programming to efficiently parse texts.
  - C{nltk.parser.probabilistic} defines probabilistic parsing, which
    associates a probability with each parse.
"""


##//////////////////////////////////////////////////////
##  Parser Interface
##//////////////////////////////////////////////////////
class ParseI(object):
    """
    A processing class for deriving trees that represent possible
    structures for a sequence of tokens.  These tree structures are
    known as X{parses}.  Typically, parsers are used to derive syntax
    trees for sentences.  But parsers can also be used to derive other
    kinds of tree structure, such as morphological trees and discourse
    structures.
    
    """
    def parse(self, sent):
        """
        Derive a parse tree that represents the structure of the given
        sentences words, and return a Tree.  If no parse is found,
        then output C{None}.  If multiple parses are found, then
        output the best parse.

        The parsed trees derive a structure for the subtokens, but do
        not modify them.  In particular, the leaves of the subtree
        should be equal to the list of subtokens.

        @param sent: The sentence to be parsed
        @type sent: L{list} of L{string}
        """
        raise NotImplementedError()

    def get_parse(self, sent):
        """
        @return: A parse tree that represents the structure of the
        sentence.  If no parse is found, then return C{None}.

        @rtype: L{Tree}
        @param sent: The sentence to be parsed
        @type sent: L{list} of L{string}
        """

    def get_parse_list(self, sent):
        """
        @return: A list of the parse trees for the sentence.  When possible,
        this list should be sorted from most likely to least likely.

        @rtype: C{list} of L{Tree}
        @param sent: The sentence to be parsed
        @type sent: L{list} of L{string}
        """

    def get_parse_probs(self, sent):
        """
        @return: A probability distribution over the parse trees for the sentence.

        @rtype: L{ProbDistI}
        @param sent: The sentence to be parsed
        @type sent: L{list} of L{string}
        """

    def get_parse_dict(self, sent):
        """
        @return: A dictionary mapping from the parse trees for the
        sentence to numeric scores.

        @rtype: C{dict}
        @param sent: The sentence to be parsed
        @type sent: L{list} of L{string}
        """

##//////////////////////////////////////////////////////
##  Abstract Base Class for Parsers
##//////////////////////////////////////////////////////
class AbstractParse(ParseI):
    """
    An abstract base class for parsers.  C{AbstractParse} provides
    a default implementation for:

      - L{parse} (based on C{get_parse})
      - L{get_parse_list} (based on C{get_parse})
      - L{get_parse} (based on C{get_parse_list})

    Note that subclasses must override either C{get_parse} or
    C{get_parse_list} (or both), to avoid infinite recursion.
    """
    def __init__(self):
        """
        Construct a new parser.
        """
        # Make sure we're not directly instantiated:
        if self.__class__ == AbstractParse:
            raise AssertionError("Abstract classes can't be instantiated")

    def parse(self, sentence):
        return self.get_parse_list(sentence.split())

    def grammar(self):
        return self._grammar

    def get_parse(self, tokens):
        trees = self.get_parse_list(list(tokens))
        if len(trees) == 0: return None
        else: return trees[0]
    
    def get_parse_list(self, tokens):
        tree = self.get_parse(tokens)
        if tree is None: return []
        else: return [tree]

    def batch_test(self, filename):
        f = open(filename)
        for line in f:
            line = line.strip()
            if not line: continue 
            if line.startswith('#'):
                print(line)
                continue
            print(("Sentence:", line))
            parses = self.parse(line)
            print(("%d parses." % len(parses)))
            for tree in parses: print(tree)

from nltk.parse import *
