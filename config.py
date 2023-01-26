import os
homeDir = (r'\\').join(os.path.abspath(__file__).split('\\')[:-1])
trade_pair = ['BTCUSDT']
admin_list = [1021524873]
BOT_TOKEN = '5825461628:AAFxLcq4B_z927H4JYvM11utplvRcML-_iQ' #@Bin_copy11_bot
db_path = f'{homeDir}\\DB\\db.db'
log_path = f'{homeDir}\\logs\\'
SSL_CERT_FILE = f'{homeDir}\\ssl\\cacert.pem'
