import logging

def config_logger():
    logger = logging.getLogger('hoho_logger')
    logger.setLevel(logging.DEBUG)

    ## 将log写入文件
    # dir_path = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'log')
    # if not os.path.exists(dir_path):
    #     os.makedirs(dir_path)
    # log_filename = os.path.join(dir_path, f'hoho_log_{int(time.time())}.log')
    # fh = logging.FileHandler(log_filename)
    # fh.setLevel(logging.DEBUG)

    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)

    formatter = logging.Formatter('[%(asctime)s][%(filename)s][line:%(lineno)d][%(levelname)s] %(message)s')

    # fh.setFormatter(formatter)
    ch.setFormatter(formatter)

    # logger.addHandler(fh)
    logger.addHandler(ch)

    return logger


LOGGER = config_logger()
