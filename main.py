import os

from conf import log_conf
from excel import read

if __name__ == '__main__':
    # 创建log对象
    log = log_conf.get_log('./conf/log.ini')
    # 测试用例集合
    cases = list()
    # 读取路径下的测试用例
    for path, dir, files in os.walk('./Test_Case_Data/'):
        for file in files:
            # 获取文件的后缀名
            file_type = os.path.splitext(file)[1]
            file_name = os.path.splitext(file)[0]
            if file_type == '.xlsx':
                case_path = path + file
                cases.append(case_path)
                print(case_path)
            else:
                log.error('文件类型错误：{}'.format(file))
    for case in cases:
        log.info('********正在执行{}文件*********'.format(case))
        read.read(case, log)
