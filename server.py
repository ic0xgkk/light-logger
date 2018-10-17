import light_logger.common as core

try:
    import light_logger.common
    import light_logger.io
    import light_logger.net
    import Crypto
    import pymysql
except Exception as e:
    print("Loading modules failed : " + str(e))

core.main()
