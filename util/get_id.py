import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


def get_series_id(series_title):
    # Checks if auxiliary files are already local
    first_run = not os.path.isfile("df.pkl" and "df_basics.pkl")
    if first_run:
        columns_of_interest = ['tconst', 'titleType', 'primaryTitle']
        # pandas starts interpreting year as int, yet later some \N will occur,
        # so we treat year as str, for now: dtype={"startYear": str}
        df_basics = pd.read_csv("data//basics.tsv", sep="\t", usecols=columns_of_interest)
        # save it for later in pickle file:
        df_basics.to_pickle("df_basics.pkl")  # where to save it, usually as a .pkl
    else:  # load pickle local pickle file
        df_basics = pd.read_pickle("df_basics.pkl")

    # get distribution summary based on titleType
    # df_summary = df_basics.groupby('titleType')['tconst'].nunique()
    # print(df_summary)
    # fig, ax = plt.subplots()
    # fig.dpi = 300
    # sns.set_style("whitegrid")
    # df_summary.plot.bar()
    # fig.savefig("imdb-type-distribution.png", transparent=True)
    # plt.show()
    # # all IMDB entries:
    # print(len(df_basics)) # 4.832.632 as of February 25, 2018


    # CLEANING. We only need this df for the allocation of a given series title to its id (tconst)
    # ... and since we want to allocate only tv series with tv episodes (later) we can get rid of everything else
    if first_run:
        # getting all type that match with tvSeries and tvEpisoded
        df = df_basics[(df_basics["titleType"] == "tvSeries") | (df_basics["titleType"] == "tvEpisode")]
        # get rid of all but tvSeries
        # df = df_basics[df_basics["titleType"] == "tvSeries"]
        df.to_pickle("df.pkl")
        df.to_csv("df.csv", index=False, sep="\t")  # just for checking
    else:
        df = pd.read_pickle("df.pkl")

    # find user title and return id (tconst)
    # max() return the pandas series as a string, not sure if this the best solution
    series_id = df.loc[df["primaryTitle"] == series_title, 'tconst'].max()
    return series_id

# TODO see: https://stackoverflow.com/questions/14262433/large-data-work-flows-using-pandas
