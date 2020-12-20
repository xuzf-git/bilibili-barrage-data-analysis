# -*-coding:utf-8 -*-
"""
    功能：利用jieba分词库进行中文分词；
          根据词性，停用词表进行筛选过滤

"""
import os
import time
import jieba
import jieba.posseg as pseg
import jieba.analyse


# 待分词文件列表
file_list = []


"""
    加载本地字典：
    【1】自定义字典
    【2】停用词字典
"""
local_dic_name = './data/userdict.txt'
local_stopwords_name = './data/stopwords_dic.txt'
jieba.load_userdict(local_dic_name)
jieba.load_userdict(local_stopwords_name)


"""
    函数功能：创建停用词list
    参数：
        filepath：停用词典地址
    返回：
         停用词list
"""


def stopwordslist(local_stopwords_name):
    stopwords = [line.strip() for line in open(local_stopwords_name, 'r', encoding='utf-8').readlines()]
    return stopwords


"""
    函数功能：利用 jieba 进行分词
    参数：
        filename：需要进行分词的文件名
    返回：
         未过滤的分词结果
"""


def divide_words(filename):
    os.chdir('./data/generated')
    if os.path.exists(filename):
        with open(filename, 'r', encoding='utf-8') as f:
            str1 = f.read()
            result = pseg.cut(str1)
        return result
    else:
        pass


"""
    函数功能：对词语进行过滤、降噪处理
    参数：
        result：未过滤的分词结果
    返回：
         body：过滤的分词结果（字符串）
"""


def word_filter(result):
    stopwords = stopwordslist(local_stopwords_name)
    body = ''
    for w in result:
        if w.flag != 'x' and w.flag != 'r' and w.flag != 'ul' \
                and w.flag != 'uj' and w.flag != 'y' and w.flag != 'q'\
                and w.flag != 'd' and w.flag != 'm' and w.flag != 'eng':
            if w.word not in stopwords:
                body += w.word + '\n'
    # 提取关键词
    tag = jieba.analyse.extract_tags(body, 5)
    print(tag)
    # 生成关键词比重词典
    # key = jieba.analyse.textrank(body, topK=100, withWeight=True)
    # keywords = dict()
    # for i in key:
    #    keywords[i[0]] = i[1]
    # print(keywords)
    return body


if __name__ == '__main__':
    input_mode = input('==选择爬取模式==\n 1.单文件分词\n 2.多文件分词\n =============\n选择模式：')
    print('=============')
    if input_mode == '1':
        file_list = [input('输入文件名(不包含扩展名)：')]
        print('=============\n')
    elif input_mode == '2':
        with open('D:\\Python\\project\\bilibili\\av_number.txt') as f:
            file_list = [x.replace('\n', '') for x in f.readlines()]
    for filename in file_list:
        filename = filename + '.text'
        result = divide_words(filename)
        body = word_filter(result)
        # 创建输出文件夹
        """
        if not os.path.isdir('output_word_divide'):
            os.mkdir('output_word_divide')
        # 输出格式化后的结果
        filename = 'word_' + filename
        with open(f'output_word_divide/{filename}', 'w', encoding="utf-8") as f:
            f.write(body)
        """
        # 输出格式化后的结果
        filename = 'word_' + filename
        with open(f'{filename}', 'w', encoding="utf-8") as f:
            f.write(body)
    print('=============\n')
    print(u'分词完成...')
    print(u'2秒后自动退出程序...')
    time.sleep(2)
