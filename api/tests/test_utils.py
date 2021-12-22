import os, sys
from datetime import datetime
from datetime import timezone

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import utils
import pickle


def test_cant_post_with_more_than_3_posts_to_bodyswap():
    with open("api/tests/testable.pickle", "rb") as handle:
        b = pickle.load(handle)
    dt = datetime.now(timezone.utc)
    utc_time = dt.replace(tzinfo=timezone.utc)
    utc_timestamp = utc_time.timestamp()
    index_checker = 0
    for index in range(0, 3):
        index_checker += 1
        b[index].created_utc = utc_timestamp
        b[index].subreddit = "bodyswap"
    assert index_checker == 3
    assert utils.can_i_post_to_bodyswap(b) == False


def test_cant_post_with_more_than_4_posts_to_bodyswap():
    with open("api/tests/testable.pickle", "rb") as handle:
        b = pickle.load(handle)
    dt = datetime.now(timezone.utc)
    utc_time = dt.replace(tzinfo=timezone.utc)
    utc_timestamp = utc_time.timestamp()
    index_checker = 0
    amount = 4
    for index in range(0, amount):
        index_checker += 1
        b[index].created_utc = utc_timestamp
        b[index].subreddit = "bodyswap"
    assert index_checker == amount
    assert utils.can_i_post_to_bodyswap(b) == False


def test_can_post_with_more_than_4_posts_with_2_bodyswap_to_bodyswap():
    with open("api/tests/testable.pickle", "rb") as handle:
        b = pickle.load(handle)
    dt = datetime.now(timezone.utc)
    utc_time = dt.replace(tzinfo=timezone.utc)
    utc_timestamp = utc_time.timestamp()
    index_checker = 0
    amount = 2
    for index in range(0, amount):
        index_checker += 1
        b[index].created_utc = utc_timestamp
        b[index].subreddit = "bodyswap"
    assert index_checker == amount
    assert utils.can_i_post_to_bodyswap(b) == True


def test_test_if_it_gets_posts():
    assert (
        utils.can_i_post_to_bodyswap() == True
        or utils.can_i_post_to_bodyswap() == False
    )
