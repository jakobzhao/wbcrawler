# !/usr/bin/python
# -*- coding: utf-8 -*-
#
# Created on Oct 16, 2015
# @author:       Bo Zhao
# @email:        bo_zhao@hks.harvard.edu
# @website:      http://yenching.org
# @organization: Harvard Kennedy School

import sys
# numpy
import numpy
# gensim modules
from gensim import utils
from gensim.models.doc2vec import LabeledSentence
from wbcrawler.log import *

reload(sys)
sys.setdefaultencoding('utf-8')


class LabeledLineSentence(object):
    def __init__(self, sources):
        self.sources = sources

        flipped = {}

        # make sure that keys are unique
        for key, value in sources.items():
            if value not in flipped:
                flipped[value] = [key]
            else:
                raise Exception('Non-unique prefix encountered')

    def __iter__(self):
        for source, prefix in self.sources.items():
            with utils.smart_open(source) as fin:
                for item_no, line in enumerate(fin):
                    yield LabeledSentence(utils.to_unicode(line).split(''), [prefix + '_%s' % item_no])

    def to_array(self):
        self.sentences = []
        for source, prefix in self.sources.items():
            with utils.smart_open(source) as fin:
                for item_no, line in enumerate(fin):
                    self.sentences.append(LabeledSentence(utils.to_unicode(line).split(), [prefix + '_%s' % item_no]))
        return self.sentences

    def sentences_perm(self):
        return numpy.random.permutation(self.sentences)


def get_name_from_content(content):
    names = []
    if u'@' not in content:
        return names

    parts = content.split(u"@")

    for part in parts[1:]:
        comma_index = -1
        if u':' in part or u'：' in part:
            if part.find(u':') == -1:
                comma_index = part.find(u'：')
            elif part.find(u'：') == -1:
                comma_index = part.find(u':')
            else:
                if part.find(u':') > part.find(u'：'):
                    comma_index = part.find(u'：')
                else:
                    comma_index = part.find(u':')

        space_index = part.find(u' ')
        if part == parts[-1] and space_index == -1:
            space_index = len(part)

        if comma_index == -1 and space_index == -1:
            name = u'@' + part
        elif comma_index == -1 and space_index != -1:
            name = u'@' + part[:space_index]
        elif comma_index != -1 and space_index == -1:
            name = u'@' + part[:comma_index]
        elif comma_index < space_index:
            name = u'@' + part[:comma_index]
        elif comma_index > space_index:
            name = u'@' + part[:space_index]
        else:
            name = u'@' + part
        names.append(name)

    return names


def preprocess_content(content):
    names = get_name_from_content(content)
    url = ''
    if u'http://t.cn/' in content:
        url_start = content.find(u'http://t.cn/')
        url = content[url_start:url_start + 19]
        # print url

    if len(content) >= 2:
        content = content.split('//')[0]

    content = content.replace(url, '').replace(u'转发微博', '').replace(u'轉發微博', '').replace(u'Repost', '')

    i = 1
    for name in names:
        # content = content.replace(name, u'用户' + unicode(i))
        # content = content.replace(name, u'用户')
        content = content.replace(name, u'')
        i += 1
    while u' ' in content:
        content = content.replace(u' ', u'')
    return content


def seg_sentence(line):
    import jieba
    from wbcrawler.settings import STOP_WORDS
    jieba.load_userdict('wbcrawler/training_set/dict.txt')
    token_list = jieba.cut(preprocess_content(unicode(line)))
    sentence = " ".join(token_list)
    for word in STOP_WORDS:
        if word in sentence:
            if sentence.index(word) == 0:
                sentence = sentence[2:]
            sentence = sentence.replace(u' ' + word, u'')
    return sentence


def seg_sentence_tag(line):
    import jieba
    from wbcrawler.settings import STOP_WORDS
    jieba.load_userdict('wbcrawler/training_set/dict.txt')
    import jieba.posseg
    # print unicode(line)
    a = jieba.posseg.cut(preprocess_content(unicode(line)))
    sentence = u''
    for word, flag in a:
        if 'v' in flag or 'a' in flag:
            if word not in STOP_WORDS:
                sentence += word + u' '
    return sentence
