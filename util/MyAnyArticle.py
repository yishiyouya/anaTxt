import jieba
import matplotlib.pyplot as plt
import wordcloud
import networkx as nx
import matplotlib
import jieba.posseg as psg

from util import fileConfig

matplotlib.rcParams['font.sans-serif'] = ['SimHei']


class AnyArticle(object):
    file_name = ''
    stop_name = ''
    names = []

    def __init__(self, fileName, stopName, names=list):
        self.file_name = fileName
        self.stop_name = stopName
        self.names = names

    # 读取文本
    def read_txt(self):
        file = open(self.file_name, 'r+', encoding=fileConfig.default_encoding)
        txt = file.read()
        file.close()
        return txt

    # 词性统计（写入文档）
    def sda(self):
        text = open(self.file_name, encoding=fileConfig.default_encoding, errors='ignore').read()
        seg = psg.cut(text)
        file = open("词性.txt", 'a+')
        for ele in seg:
            file.writelines(ele)

    # 停词文档
    def stopwordslist(self, stopName):
        stopwords = [line.strip() for line in open(stopName, 'r', encoding=fileConfig.default_encoding).readlines()]
        return stopwords

    # 分词生成人物（写入文档）
    def write_txt(self):
        # 使用精确模式对文本进行分词counts = {}     # 通过键值对的形式存储词语及其出现的次数
        words = jieba.lcut(self.read_txt())
        counts = {}
        countCharacters = {}
        stopwords = self.stopwordslist(self.stop_name)
        for word in words:
            if len(word) == 1:  # 单个词语不计算在内
                continue
            elif word not in stopwords:
                counts[word] = counts.get(word, 0) + 1  # 遍历所有词语，每出现一次其对应的值加 1
            elif word in self.names:
                countCharacters[word] = countCharacters.get(word, 0) + 1  # 遍历所有词语，每出现一次其对应的值加 1
        items = list(counts.items())
        items.sort(key=lambda x: x[1], reverse=True)  # 根据词语出现的次数进行从大到小排序

        f = open("词频统计.txt", "w")  # 写入文件
        for i in range(len(items)):
            word, count = items[i]
            f.writelines("{0:<5}{1:>5}\n".format(word, count))
        f.close()

        items = list(countCharacters.items())
        items.sort(key=lambda x: x[1], reverse=True)  # 根据词语出现的次数进行从大到小排序

        f = open("词频统计——character.txt", "w")  # 写入文件
        for i in range(len(items)):
            word, count = items[i]
            f.writelines("{0:<5}{1:>5}\n".format(word, count))
        f.close()

    # 生成词云
    def creat_wordcloud(self):
        f_0 = open("词频统计.txt", 'r')
        bg_pic = plt.imread('张国荣.jpg')
        text = f_0.read()
        f_0.close()
        wcloud = wordcloud.WordCloud(font_path=r"D:\simhei.ttf",
                                     background_color="white", width=1000,
                                     max_words=500,
                                     mask=bg_pic,
                                     height=860,
                                     margin=2,
                                     ).generate(text)

        wcloud.to_file("连城诀cloud.jpg")
        plt.imshow(wcloud)
        plt.axis('off')
        plt.show()

    # 生成人物关系图（全按书上抄的）
    def creat_relationship(self):
        Names = self.names
        relations = {}
        lst_para = (self.read_txt()).split('\n')  # lst_para是每一段
        for text in lst_para:
            for name_0 in Names:
                if name_0 in text:
                    for name_1 in Names:
                        if name_1 in text and name_0 != name_1 and (name_1, name_0) not in relations:
                            relations[(name_0, name_1)] = relations.get((name_0, name_1), 0) + 1
        maxRela = max([v for k, v in relations.items()])
        relations = {k: v / maxRela for k, v in relations.items()}
        # return relations

        plt.figure(figsize=(15, 15))
        G = nx.Graph()
        for k, v in relations.items():
            G.add_edge(k[0], k[1], weight=v)
        # 筛选权重大于0.6的边
        elarge = [(u, v) for (u, v, d) in G.edges(data=True) if d['weight'] > 0.6]
        # 筛选权重大于0.3小于0.6的边
        emidle = [(u, v) for (u, v, d) in G.edges(data=True) if (d['weight'] > 0.3) & (d['weight'] <= 0.6)]
        # 筛选权重小于0.3的边
        esmall = [(u, v) for (u, v, d) in G.edges(data=True) if d['weight'] <= 0.3]
        # 设置图形布局
        pos = nx.spring_layout(G)
        # 设置节点样式
        nx.draw_networkx_nodes(G, pos, alpha=0.8, node_size=1200)
        # 设置大于0.6的边的样式
        nx.draw_networkx_edges(G, pos, edgelist=elarge, width=2.5, alpha=0.9, edge_color='g')
        # 0.3~0.6
        nx.draw_networkx_edges(G, pos, edgelist=emidle, width=1.5, alpha=0.6, edge_color='y')
        # <0.3
        nx.draw_networkx_edges(G, pos, edgelist=esmall, width=1, alpha=0.4, edge_color='b', style='dashed')
        nx.draw_networkx_labels(G, pos, font_size=12)

        plt.axis('off')
        plt.title("连城诀人物权重图")
        plt.show()

    def start(self):
        self.write_txt()
        self.creat_wordcloud()
        self.creat_relationship()


def main():
    any = AnyArticle(fileConfig.articles_path + fileConfig.file_name,
                     fileConfig.stop_name,
                     fileConfig.names)
    any.start()


if __name__ == '__main__':
    main()
