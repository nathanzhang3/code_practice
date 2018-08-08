import logging
import datetime as dt

from market import Market


def create_log():
    lgr = logging.getLogger()
    lgr.setLevel(logging.INFO)
    formatting = '%(levelname)s | %(created)f | %(name)s | %(processName)s ' + \
                 '| %(threadName)s | %(funcName)s | %(message)s'

    # print to console
    # logging.basicConfig(format=formatting)

    # print to log files
    filehandler = logging.FileHandler(filename='code_test_' +
                                      str(dt.datetime.now()) + '.log', mode='w')
    filehandler.setLevel(logging.DEBUG)
    filehandler.setFormatter(logging.Formatter(formatting))
    lgr.addHandler(filehandler)

    return lgr

if __name__ == '__main__':
    logger = create_log()

    m1 = Market('BTCUSD')
    m2 = Market('ETHUSD')

    m1.initialize_api()
    m2.initialize_api()

    m1.create_database()
    m2.create_database()

    while True:
        # Continue streaming data
        m1.stream_data()
        m2.stream_data()
