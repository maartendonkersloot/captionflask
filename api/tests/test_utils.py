"""
Test class for the utils class
"""
import pickle
import os
import sys
from datetime import datetime, timezone

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import utils  # pylint: disable=import-error, wrong-import-position


def test_cant_post_with_more_than_3_posts_to_bodyswap():
    """
    test if it can post to bodyswap if there are already 3 posts in the past 12 hours.
    should be false
    """
    with open("api/tests/testable.pickle", "rb") as handle:
        test_array = pickle.load(handle)
    datetime_now = datetime.now(timezone.utc)
    utc_time = datetime_now.replace(tzinfo=timezone.utc)
    utc_timestamp = utc_time.timestamp()
    index_checker = 0
    for index in range(0, 3):
        index_checker += 1
        test_array[index].created_utc = utc_timestamp
        test_array[index].subreddit = "bodyswap"
    assert index_checker == 3
    assert utils.can_i_post_to_bodyswap(test_array) is False


def test_cant_post_with_more_than_4_posts_to_bodyswap():
    """
    Tets if it can post to bodyswap if there are already 4 posts in the past 2 hours.
    Should be false.
    """
    with open("api/tests/testable.pickle", "rb") as handle:
        test_array = pickle.load(handle)
    datetime_now = datetime.now(timezone.utc)
    utc_time = datetime_now.replace(tzinfo=timezone.utc)
    utc_timestamp = utc_time.timestamp()
    index_checker = 0
    amount = 4
    for index in range(0, amount):
        index_checker += 1
        test_array[index].created_utc = utc_timestamp
        test_array[index].subreddit = "bodyswap"
    assert index_checker is amount
    assert utils.can_i_post_to_bodyswap(test_array) is False


def test_can_post_with_more_than_4_posts_with_2_bodyswap_to_bodyswap():
    """
    Test if it can post with 2 bodyswap posts in the past 12 hours.
    It should be able to post.
    """
    with open("api/tests/testable.pickle", "rb") as handle:
        test_array = pickle.load(handle)
    datetime_now = datetime.now(timezone.utc)
    utc_time = datetime_now.replace(tzinfo=timezone.utc)
    utc_timestamp = utc_time.timestamp()
    index_checker = 0
    amount = 2
    for index in range(0, amount):
        index_checker += 1
        test_array[index].created_utc = utc_timestamp
        test_array[index].subreddit = "bodyswap"
    assert index_checker is amount
    assert utils.can_i_post_to_bodyswap(test_array) is True


def test_test_if_it_gets_posts():
    """
    Test if it can post, if it goes through the can_i_post_to_bodyswap function.
    """
    assert (
        utils.can_i_post_to_bodyswap() is True
        or utils.can_i_post_to_bodyswap() is False
    )
