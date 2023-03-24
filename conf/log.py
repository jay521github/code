import logging


class Logger:
    def get_logger(self):
        # 创建日志对象
        logger = logging.getLogger('logger')
        logger.setLevel(logging.DEBUG)
        if not logger.handlers:
            sh = logging.StreamHandler()
            fmt = logging.Formatter(fmt='[%(filename)s]:%(asctime)s - %(levelname)s - %(message)s')
            fh = logging.FileHandler('./mylog.txt', encoding='utf-8')
            fmt1 = logging.Formatter(fmt='[%(filename)s]:%(asctime)s - %(levelname)s - %(message)s')
            fh.setFormatter(fmt1)
            fh.setLevel(logging.DEBUG)
            sh.setFormatter(fmt)
            sh.setLevel(logging.DEBUG)
            logger.addHandler(sh)
            logger.addHandler(fh)
        return logger