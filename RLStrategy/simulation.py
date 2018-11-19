import logging
import os
import settings
from policy_learner import PolicyLearner
import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('MODEL', type=int, help="trained model name?")
    parser.add_argument('COIN', type=str, help="coin type?")
    parser.add_argument('BALANCE', type=int, help="initial balance?")

    args = parser.parse_args()
    MODEL = args.MODEL
    COIN = args.COIN
    BALANCE = args.BALANCE

    log_dir = os.path.join(settings.BASE_DIR, 'logs/%s' % 'bitcoin_min')
    timestr = settings.get_time_str()
    file_handler = logging.FileHandler(filename=os.path.join(
        log_dir, "%s_%s.log" % ('bitcoin_min', timestr)), encoding='utf-8')
    stream_handler = logging.StreamHandler()
    file_handler.setLevel(logging.DEBUG)
    stream_handler.setLevel(logging.INFO)
    logging.basicConfig(format="%(message)s",
        handlers=[file_handler, stream_handler], level=logging.DEBUG)

    policy_learner = PolicyLearner(
                coin_code=COIN, coin_chart=None, training_data=None,
                min_trading_unit=0.01, max_trading_unit=0.03)

    policy_learner.trade(balance=BALANCE,
                         model_path=os.path.join(settings.BASE_DIR, 'models/{}/model_{}.h5'.format('bitcoin_min',MODEL)))
