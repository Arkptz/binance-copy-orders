import os
homeDir = (r'\\').join(os.path.abspath(__file__).split('\\')[:-1])
owners = [1021524873, 828458879]
admin_list = [1021524873, 828458879, 5675395916]
channel_id = -1001262628072 #-1001793924567#
BOT_TOKEN = '5825461628:AAFxLcq4B_z927H4JYvM11utplvRcML-_iQ' #@Bin_copy11_bot #'5593221166:AAEdAfjAiGERdXrFM2ySLsKBFVcSH9h8uFE'#@ukr_tt_bot #
db_path = f'{homeDir}\\DB\\db.db' if homeDir !='' else './DB/db.db'
log_path = f'{homeDir}\\logs\\' if homeDir !='' else '../binance-copy-orders/logs/'
SSL_CERT_FILE = f'{homeDir}\\ssl\\cacert.pem' if homeDir !='' else './ssl/cacert.pem'
