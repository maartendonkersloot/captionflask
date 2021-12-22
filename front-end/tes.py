import praw
import pickle

reddit = praw.Reddit(
    client_id="dBbawnq6RJY_zdl-TiEoHg",
    client_secret="RWjFvyIseJMGt1hQuKCCQAe-0P_63Q",
    password="Esmeralda1",
    user_agent="script by guy on SO",
    username="swapper_rp",
)
posts = reddit.redditor("swapper_rp").submissions.new(limit=5)
time_array = []
for post in posts:
    time_array.append(post)
with open("testable.pickle", "wb") as handle:
    pickle.dump(posts, handle, protocol=pickle.HIGHEST_PROTOCOL)

with open("testable.pickle", "rb") as handle:
    b = pickle.load(handle)
