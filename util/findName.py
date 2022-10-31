from LAC import LAC

from util import fileConfig


def lac_username(sentences: str) -> list:
    # 装载LAC模型
    user_name_list = []
    lac = LAC(mode="lac")
    lac_result = lac.run(sentences)
    for index, lac_label in enumerate(lac_result[1]):
        if lac_label == "PER":
            user_name_list.append(lac_result[0][index])
    return user_name_list


def readName():
    file = open(fileConfig.articles_path + fileConfig.file_name
                , 'r+', encoding=fileConfig.default_encoding)
    txt = file.read()
    file.close()
    lac_user = lac_username(txt)
    res = list(set(lac_user))
    res.sort()
    print(res)


if __name__ == '__main__':
    readName()
