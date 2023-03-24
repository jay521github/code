# 读取ini配置文件的模块
import configparser
# 读取配置文件中的内容
def ReadIni(path, section, option):
    conf = configparser.ConfigParser()
    conf.read(path)
    value = conf.get(section, option)
    return value
