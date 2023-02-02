import logging
from binance.error import ClientError
import traceback
from Tg_Bot.handlers import send_log
from threading import Thread, Lock


def send_log_thr(txt:str):
    Thread(target=send_log, args=[txt]).start()


def catch_eroor(input_func):
    def output_func(*args, **kwargs):
        ans = ''
        for i in range(3):
            try:
                ans = input_func(*args,**kwargs)
                break
            except ClientError as error:
                txt_err = "Found error. status: {}, error code: {}, error message: {}".format(
                        error.status_code, error.error_code, error.error_message)
                logging.error(txt_err)
                txt = ''
                try:
                    txt = f'{args[0].name_account} -- '
                except:
                    pass
                send_log_thr(txt+f'{input_func.__name__} -- '+ txt_err)
                break
            except:
                logging.error(traceback.format_exc())
        return ans
    return output_func