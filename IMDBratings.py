import os
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

# todo tconst in funktion auslagern get_id(user_input) bspw. – making sense?
# todo implement getting the slope directly http://www.statsmodels.org/stable/index.html
# todo make categorial color binning for regplot
# todo only allow years that are listed for duplocate titles

if os.path.exists(os.getcwd() + "//raw//" + "dataframe.csv"):
    print("IMDB dataframe found! Reading...")
    # , dtype={'sxxexx': str})
    df = pd.read_csv("raw//dataframe.csv", sep="\t")
else:
    print("Please run IMDBratings_setup.py first!")

while True:
    print("-----------------------------------------------------------------")
    input_title = input("Enter a series title: ")
    print("-----------------------------------------------------------------")
    tconst = df.loc[(df["type"] == "tvSeries") & (df["title"] == input_title), "tconst"]

    if len(tconst) == 0:
        print(
            "Nothing found! Does the spelling of the title match with IMDB’s spelling on their website?"
        )
    else:
        break

# get the year now
tconst = df.loc[
    (df["type"] == "tvSeries") & (df["title"] == input_title), ["tconst", "year"]
]
if len(tconst) > 1:
    print(
        "The title '"
        + input_title
        + "' was found more than once. Here is a list of release years: "
    )

    for index, row in tconst.iterrows():
        print(row["year"])

    input_year = input("When was the release year of 'your' " + input_title + "? ")

    tconst = df.loc[
        (df["type"] == "tvSeries")
        & (df["title"] == input_title)
        & (df["year"] == int(input_year)),
        "tconst",
    ]
else:
    tconst = df.loc[(df["type"] == "tvSeries") & (df["title"] == input_title), "tconst"]

# convert tconst to single string
tconst = tconst.to_string(index=False)
tconst = tconst.strip()
print(input_title + " (IMDB id: " + tconst + ") found.")
print("URL: http://www.imdb.com/title/" + tconst + "/")

rating = df.loc[(df["type"] == "tvSeries") & (df["tconst"] == tconst), "rating"]
rating = rating.to_string(index=False)
print(input_title + " has an overall rating of " + str(rating) + ".")
rating = float(rating)

# sxxexx = df.loc[(df['type'] == 'tvEpisode') & (df['parent'] == tconst), 'sxxexx']
# sxxexx = sxxexx.sort_values()
# # sxxexx = sxxexx.apply('{:0>2}'.format)
# # sxxexx = sxxexx.tolist()


# Visualize Episode rating over time
# retrieving user request...
df_eps_rating = df[(df["type"] == "tvEpisode") & (df["parent"] == tconst)]

# it’s important to sort data before we plot them. Since we want to plot ratings over time
# ... we sort the df by Series and Episodes (sxxexx) notation
df_eps_rating = df_eps_rating.sort_values("sxxexx")


# print(df_episodes.info())


# plot
# subplot extraction
fig, ax = plt.subplots()
fig.dpi = 80  # choose a low value only for testing, export it at least > 150 dpi


ax.set_ylim([0, 10])
ax.set_title(input_title + " – Overall rating: " + str(rating))

# last_ep = df_eps_rating['sxxexx'].iloc[-1]
# ax.set_xlim([0, last_ep])

sns.despine()
sns.set(style="ticks", color_codes=True)
sns.set_style("darkgrid")  # white, whitegrid, dark, darkgrid
sns.regplot("sxxexx", "rating", df_eps_rating)  # x_jitter=last_ep
print(df_eps_rating[["rating", "sxxexx"]])

# Strip plot offers no linear regression, yet it auto bins the seasons...
# sns.stripplot(x='sxxexx', y='rating', data=df_eps_rating).set_title(input_title + " – Overall rating: " + str(rating))

plt.show()
