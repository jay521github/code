'''
    生成日志器的配置
'''
import logging.config


# 路径一定要在调用的地方进行填写，不然会报错。
def get_log(path):
    logging.config.fileConfig(path)
    return logging.getLogger()
