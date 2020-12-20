# -*-coding:utf-8 -*-
"""
    功能：绘制词云
"""
from os import path
from scipy.misc import imread
import matplotlib.pyplot as plt
from wordcloud import WordCloud, ImageColorGenerator

# 获取当前文件路径
# __file__ 为当前文件路径

d = path.dirname(__file__)

back_coloring_path = "background_image1.jpg"                  # 设置背景图片路径
text_path = 'output\\output_word_divide\\word_8468163.text'  # 设置要分析的文本路径
font_path = 'D:\\Fonts\\simkai.ttf'                           # 为matplotlib设置中文字体路径
imgname1 = "WordCloudDefautColors.png"                        # 保存的图片名1(只按照背景图片形成)
imgname2 = "WordCloudColorsByImg.png"                         # 保存的图片名2(颜色按照背景图片颜色布局生成)

back_coloring = imread(path.join(d, back_coloring_path))      # 设置背景图片

# 设置词云属???
wc = WordCloud(
               font_path=font_path,              # 设置字体
               background_color="white",         # 背景颜色
               max_words=200,                    # 词云显示的最大词数
               mask=back_coloring,               # 设置背景图片
               max_font_size=200,                # 字体最大值
               random_state=42,
               width=500, height=430, margin=2,  # 设置图片默认的大小,但是如果使用背景图片的话,那么保存的图片大小将会按照其大小保存,margin为词语边缘距??
               )

text = open(text_path,encoding= 'utf-8').read()

# 生成词云, 可以用generate输入全部文本(wordcloud对中文分词支持不??,建议启用中文分词),也可以我们计算好词频后使用generate_from_frequencies函数
wc.generate(text)

# wc.generate_from_frequencies(txt_freq)
# txt_freq例子为[('词a', 100),('词b', 90),('词c', 80)]
# 从背景图片生成颜色???
image_colors = ImageColorGenerator(back_coloring)

plt.figure()
# 以下代码显示图片
plt.imshow(wc)
plt.axis("off")
plt.show()
# 绘制词云

# 保存图片
wc.to_file(path.join(d, imgname1))

image_colors = ImageColorGenerator(back_coloring)

plt.imshow(wc.recolor(color_func=image_colors))
plt.axis("off")
# 绘制背景图片为颜色的图片
plt.figure()
plt.imshow(back_coloring, cmap=plt.cm.gray)
plt.axis("off")
plt.show()
# 保存图片
wc.to_file(path.join(d, imgname2))
