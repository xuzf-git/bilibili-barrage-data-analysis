# -*-coding:utf-8 -*-

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.neighbors import KNeighborsClassifier
from numpy import mean
import os


"""
    功能：加载语料数据
    参数：无
    返回：储存文件的词语矩阵
"""


def load_x_files():
    # 语料
    b = os.path.dirname(__file__)
    # 获取文件夹下的所有文件名
    file_name_list = os.listdir("output\\output_word_divide")
    # 语料矩阵容器
    x_corpus = []
    # 遍历每个文件并将语料存储于corpus中
    for file_name in file_name_list:
        file_name = "output\\output_word_divide\\" + file_name
        f = open(file_name, 'r', encoding="utf-8", errors='ignore')
        str_in_file = f.read()
        x_corpus.append(str_in_file)
        f.close()
    return x_corpus


def load_y_files():
    # 语料
    b = os.path.dirname(__file__)
    # 获取文件夹下的所有文件名
    file_name_list = os.listdir("label_data")
    # 语料矩阵容器
    y_corpus = []
    # 遍历每个文件并将语料存储于corpus中
    for file_name in file_name_list:
        file_name = "label_data\\" + file_name
        f = open(file_name, 'r', encoding="utf-8", errors='ignore')
        str_in_file = f.read()
        y_corpus.append(str_in_file)
        f.close()
    return y_corpus


"""
    功能：将词语转换为tf-idf矩阵
    参数：词语列表corpus
    返回：文件的词语向量矩阵
"""


def transformer_vector(corpus):
    # 将文本中的词语转换为词频矩阵
    vectorizer = CountVectorizer()
    # 计算个词语出现的次数
    X = vectorizer.fit_transform(corpus)
    # 获取词袋中所有文本关键词
    word = vectorizer.get_feature_names()
    # print(word)
    # 查看词频结果
    # print(X.toarray())
    # 类调用
    transformer = TfidfTransformer()
    # print(transformer)
    # 将词频矩阵X统计成TF-IDF值
    tfidf = transformer.fit_transform(X)
    # 查看数据结构 tfidf[i][j]表示i类文本中的tf-idf权重
    # print(tfidf.toarray())
    return tfidf


def knn_classifier():
    # 导入X数据
    x_corpus = load_x_files()
    # 导入Y数据
    y_corpus = load_y_files()
    tfidf = transformer_vector(x_corpus)
    x_train_data = tfidf.toarray()[:700]
    y_train_data = y_corpus[:700]
    val_x = tfidf.toarray()[700:1000]
    val_y = y_corpus[700:1000]

    neigh = KNeighborsClassifier(n_neighbors=3)
    neigh.fit(x_train_data, y_train_data)

    predictions = neigh.predict(x_train_data)
    acc = mean(predictions == y_train_data)
    print(acc)

    clf = MultinomialNB()
    clf.fit(x_train_data, y_train_data)
    print(y_train_data)
    predictions = clf.predict_proba(val_x)
    # print(clf)
    print(predictions)
    # multiclass_logloss(val_y, predictions)

    # acc = mean(predictions == val_y)
    # print(acc)


if __name__ == '__main__':
    knn_classifier()
