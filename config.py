import os
homeDir = (r'\\').join(os.path.abspath(__file__).split('\\')[:-1])
admin_list = [1021524873]
channel_id = -1001262628072
BOT_TOKEN = '5825461628:AAFxLcq4B_z927H4JYvM11utplvRcML-_iQ' #@Bin_copy11_bot
db_path = f'{homeDir}\\DB\\db.db' if homeDir !='' else './DB/db.db'
log_path = f'{homeDir}\\logs\\' if homeDir !='' else './logs/'
SSL_CERT_FILE = f'{homeDir}\\ssl\\cacert.pem' if homeDir !='' else './ssl/cacert.pem'
print(db_path, log_path, SSL_CERT_FILE)