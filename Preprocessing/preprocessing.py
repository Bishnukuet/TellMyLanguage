"""
This is a simple program to identify the language of written text. The corpus is non-standared wiki content. However,
easily extended to large standared corpus.
Authror: Bishnu Sarker, Erasmus Mundus Master in Data Mining and Knowledge Management DMKM. bishnukuet@gmail.com
"""
import os
import sys
import numpy
import math
import operator
import numpy as np


indexDict=dict()
lang_full="English French German Italian Spanish Bengali".split()
lang_nick="en fr de it es bn".split()
count=dict()
RootPath=os.path.split(os.getcwd())[0]

class preprocess(object):
    def __init__(self):
        self.total_words=0
        pass
    def __str__(self):
        pass
    def tokenize(self,text,lang):
        '''
        This fucntion takes a txt file and a language it was written, and tokenize and
        append the new words to the dictionary
        :param text: Filepath of the text corpus
        :param lang:  two digit language code of the language it was written
        :return: None
        '''
        with open(text) as datafile:
            for line in datafile:
                for word in line.split():
                    word=word.strip('(),: ][{} ;."').lower()
                    if word=="":
                        continue

                    if not indexDict.__contains__(word):
                        d=dict()
                        d[lang]=1
                        indexDict.__setitem__(word,d)

                    else:
                        termD=indexDict[word]
                        if termD.__contains__(lang):
                            indexDict[word][lang] += 1
                        else:
                            indexDict[word][lang]=1



    def find_voca_stat(self,vocab):
        '''
        Find the general Statistics about the dictionary
        :param vocab: Dictionary built from corpus
        :return: Dictionary of Language wise word counts and total word count
        '''
        language=lang_nick
        full_lang=lang_full
        total_words=len(indexDict)
        self.total_words=total_words

        for lang in language:
            count[lang]=0
        for term in vocab.keys():
            lang_keys=vocab[term].keys()
            for key in lang_keys:
                count[key]=count[key]+int(vocab[term][key])
        print '---------------------------Langauge Statistics------------------\n'
        #for lange_name in zip(language,full_lang):
        #    print lange_name[1],':',float(count[lange_name[0]])/(total_word)*100,'%','\n'

        return count,total_words
    def get_term_freq(self,token,lang_nick):
        '''
        This function computes the term frequency per language
        :param token: Term
        :param lang_nick: lang
        :return: total terms in Language lang_nick, term counts in lang_nick
        '''
        term_per_lang=1
        total_count=count[lang_nick]
        if indexDict.__contains__(token):
            lang=indexDict[token]
            l=lang.keys()
            for keys in l:

                #total_count=total_count+indexDict[token][keys]
                if keys==lang_nick:
                    term_per_lang+=indexDict[token][lang_nick]
            #print 'lang','total count','term/lang\n'
            #print lang_nick,total_count,term_per_lang
            return total_count,term_per_lang

        else:
            return total_count ,term_per_lang

    def compute_term_prob(self,token,lang):
        '''
        This function computes the term probability for a given term for given language
        :param token: term to be considered
        :param lang: Givn language
        :return: term probability
        '''
        term_count,term_per_lang=self.get_term_freq(token,lang)
        #print lang,term_count,term_per_lang,self.total_words
        return float(term_per_lang)/(term_count+self.total_words)
    def compute_log_likelihood(self,tokens,lang):
        '''
        This computes the total likelihood of text to belongs to a particular language
        :param tokens: List of terms
        :param lang: given language
        :return: likelihood value
        '''
        token_prob=1.0
        for token in tokens:
            term=token.strip('(),: ][{} ;."').lower()
            token_prob=token_prob+np.log(self.compute_term_prob(term,lang))
            #print token_prob
        return token_prob
    def identify_lang(self,text):
        '''
        This is function identify the language given text. For simplicity this function only considered texts.
        It can be extended for entire file processing
        :param text: plain text
        :return: likelihood values for different language
        '''

        tokens=text.split()
        likelihood=dict()
        for lang in lang_nick:
            logs=self.compute_log_likelihood(tokens,lang)
            likelihood[lang]=logs

        max_sim=max(likelihood.iteritems(), key=operator.itemgetter(1))[0]

        print 'Most Probable Language is:', max_sim,'----->',likelihood[max_sim]

        return  likelihood
    def learn_dictionary(self, LangList):
        '''
        This function learns the dictionary
        :param LangList: List of language codes
        :return: None
        '''
        for lang in LangList:
            filePath=os.path.join(RootPath,"Data\Wiki Data\\"+lang+"\\"+lang+'.txt')

            self.tokenize(filePath,lang)

if __name__ == '__main__':
    #filePath=os.pathjoin( RootPath,"Data\\Wiki Data\\en\\en.txt")

    process=preprocess()

    process.learn_dictionary(lang_nick)

    stat, total=process.find_voca_stat(indexDict)
    print "----------------Statistics-------------------------------\n"
    print "Total Word Count:",total,"\n"
    print "Language wise word counts\n"
    print stat
    print '------------------------------------------------------------\n'

    prob_like=process.identify_lang("was a global war that lasted")

    print '\n\n-----------Complete Probability List------------------\n'
    print prob_like

    #import operator
