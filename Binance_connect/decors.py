import logging
from binance.error import ClientError
import traceback


def catch_eroor(input_func):
    def output_func(*args, **kwargs):
        ans = ''
        try:
            ans = input_func(*args,**kwargs)
        except ClientError as error:
            logging.error(
                "Found error. status: {}, error code: {}, error message: {}".format(
                    error.status_code, error.error_code, error.error_message
                )
            )
        except:
            logging.error(traceback.format_exc())
        return ans
    return output_func