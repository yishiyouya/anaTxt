from util import fileConfig


def getTxt():
    file = open(fileConfig.articles_path + fileConfig.file_name
                , 'r+', encoding=fileConfig.default_encoding)
    txt = file.read()
    file.close()
    return txt