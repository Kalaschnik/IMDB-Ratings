import time
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from get_id import get_series_id

# start counting execution time
start_time = time.time()

# import ratings
df_rating = pd.read_csv("data//ratings.tsv", sep="\t")

# import episodes
df_episodes = pd.read_csv("data//episode.tsv", sep="\t")

# merge both
df = pd.merge(df_episodes, df_rating, on='tconst', how='inner')

# get rid over elements having no seasonNumber and episodeNumber. No of trash items: 10.995
df = df[(df["seasonNumber"] != "\\N") | (df["episodeNumber"] != "\\N")]

# prepare for Season×Episode-Notation (SXXEXX) by adding leading zeros:
df['seasonNumber'] = df['seasonNumber'].apply('{:0>2}'.format)
df['episodeNumber'] = df['episodeNumber'].apply('{:0>2}'.format)

# Merge seasonNumber and episodeNumber to seasonEpisodeNumber
df["seasonEpisodeNumber"] = df["seasonNumber"] + df["episodeNumber"]

# Delete old columns
df = df.drop('seasonNumber', axis=1)
df = df.drop('episodeNumber', axis=1)

# reorder columns
df = df[['tconst', 'parentTconst', 'seasonEpisodeNumber', 'averageRating', 'numVotes']]

# we don’t need that anymore since we added leading zeros, which will not destroy the sorting
# since seasonNumber and episodeNumber contained alphanumeric stuff, we need to change it now to numeric only:
# df[['seasonNumber', 'episodeNumber']] = df[['seasonNumber', 'episodeNumber']].apply(pd.to_numeric)

# print(get_series_id("Breaking Bad"))  # Breaking Bad = tt0903747
df_single = df[df["parentTconst"] == "tt0903747"]
# sort by seasonEpisodeNumber
df_single = df_single.sort_values('seasonEpisodeNumber')

print(df_single)

x = df_single["seasonEpisodeNumber"]
y = df_single["averageRating"]
# print(type(x))
# print(type(y))


# visualize

sns.set_style("darkgrid")  # white, whitegrid, dark, darkgrid
fig, ax = plt.subplots()
fig.dpi = 100

# Pandas’ dataframe is optimized for matplotlibs x,y arguments. so you don’t need to convert using list()
# ax.plot(df_single["seasonEpisodeNumber"], df_single["averageRating"])

# ax.legend()  # matplotlib tries to set legend the best way, alternatively use: loc=1, loc=2,... =4
# ax.set_ylim([0, 11])
ax.set_title("Breaking Bad")
ax.set_xlabel("Season Number × Episode Number")
ax.set_ylabel("IMDB average Rating")

# fig.savefig("graphic.png", transparent=True)
ax.plot(x, y, '.')



# # lin. regression
x = x.tolist()
y = y.tolist()
x = list(map(int, x))
y = list(map(float, y))
print(x)
print(y)
# fit with np.polyfit
fit = np.polyfit(x, y, 1)
fit_fn = np.poly1d(fit)
ax.plot(x, y, 'yo', x, fit_fn(x), '--k')



plt.show()

print("--- %s seconds ---" % (time.time() - start_time))
