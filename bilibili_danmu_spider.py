# -*-coding:utf-8 -*-
"""
    功能介绍：利用requests中的get方法抓取网页，
              运用正则的方法解析网页获取弹幕，并保存。
"""
import requests
import time
import re
import os
import json
from bs4 import BeautifulSoup

# 视频AV号列表
av_list = []


'''
函数功能：获取指定UP主的视频av号
参数：
    mid:用户编号 
    size:单次拉取数目 
    page:页数
返回：
    无
'''


def getAllAVList(mid, size, page):
    # 获取UP主视频列表
    for n in range(1, page + 1):
        url = "http://space.bilibili.com/ajax/member/getSubmitVideos?mid=" + \
              str(mid) + "&pagesize=" + str(size) + "&page=" + str(n)
        r = requests.get(url)
        text = r.text
        json_text = json.loads(text)
        # 遍历JSON格式信息，获取视频aid
        for item in json_text["data"]["vlist"]:
            av_list.append(item["aid"])
    # print(av_list)
    return av_list


'''
函数功能：获取弹幕文件的xml地址
参数：
    av_num：视频av号list
返回：
    无
'''


def get_xml_file(av_list):
    count = 1

    for av_num in av_list:
        url = 'https://www.bilibili.com/video/av' + str(av_num)
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                          ' (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36 Edge/15.15063'
        }
        html_code = requests.get(url, headers=headers).text
        # 获取视频标签
        label_list = ''
        soup = BeautifulSoup(html_code, features="lxml")
        label_link = soup.find_all('li', class_="tag")
        for label in label_link:
            tag = label.text
            label_list = tag + '\n' + label_list
        # print(label_list)
        # 正则匹配cid编号, 视频标题
        if not re.match(f'.*"cid=(\d+)&aid={av_num}', html_code):
            print(f'[{count}] not found')
            continue
        cid_num = re.match(f'.*"cid=(\d+)&aid={av_num}', html_code).group(1)
        title = re.match(f'.*"title":"(.*)","pubdate"', html_code).group(1)
        xml_url = 'http://comment.bilibili.com/' + cid_num + '.xml'
        xml_data = str(requests.get(xml_url, headers=headers).content, encoding="utf-8")

        # 格式化xml文件
        xml_format(av_num, xml_data, title, label_list)
        # print(f'[{count}] {title} done')
        print('done')
        count += 1
        time.sleep(0.5)


'''
函数功能：格式化xml弹幕文件
参数：
    av_num：视频av号
    xml_data：需要格式化的xml的字符串
    title: 视频名称
    label_list：视频标签
返回：
    无
'''


def xml_format(av_num, xml_data, title, label_list):
    # 正则匹配各级标签
    head = re.match('(<\?xml.+?>)', xml_data).group(1)
    tag_i = re.findall('</*i>', xml_data)
    danmu_list = re.findall('">(.*?)</d>', xml_data)
    body = ''
    # 对标签进行换行和缩进
    for i, tag in enumerate(danmu_list):
        if i == 0:
            body += '\n\t' + tag.replace(head + tag_i[0], '') + '\n\t'
        elif i == len(danmu_list) - 1:
            body += tag + '\n'
        else:
            body += tag + '\n\t'
    """
    # 创建输出文件夹
    if not os.path.isdir('output'):
        os.mkdir('output')
    if not os.path.isdir('label_data'):
        os.mkdir('label_data')

    # 输出格式化后的结果
    result = head + '\n' + 'title:' + title + '\n' + tag_i[0] + body + tag_i[1]
    with open(f'output/{av_num}.text', 'w', encoding="utf-8") as f:
        f.write(result)
    with open(f'label_data/{av_num}.text', 'w', encoding="utf-8") as f:
        f.write(label_list)
    """
    with open(f'label_data/{av_num}.text', 'w', encoding="utf-8") as f:
        f.write(label_list)


def main():
    input_mode = input('==选择爬取模式==\n 1.单视频爬取\n 2.多视频爬取\n 3.爬取指定UP主视频弹幕\n=============\n选择模式：')

    print('=============')
    if input_mode == '1':
        av_list = [input('输入视频av号：')]
        print('=============\n')
    elif input_mode == '2':
        with open('av_number.txt') as f:
            av_list = [x.replace('\n', '') for x in f.readlines()]
    elif input_mode == '3':
        mid = input('输入指定UP主mid:')
        size = int(input('输入单次拉取数目:'))
        page = int(input('输入页数:'))
        av_list = getAllAVList(mid, size, page)
        if av_list is []:
            print(" this UP's mid is not found")

    get_xml_file(av_list)
    with open(f'av_number.txt', 'a', encoding="utf-8") as f:
        for i in av_list:
            temp = str(i) + '\n'
            f.write(temp)

    print('=============\n')
    print(u'弹幕爬取完成...')
    print(u'2秒后自动退出程序...')
    time.sleep(2)


if __name__ == '__main__':
    main()

