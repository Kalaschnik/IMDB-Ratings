import os
import pandas as pd

# raw path
imdb_raw = os.getcwd() + "//raw//"

# raw table names
tbl_basics = "basics.tsv"
tbl_episode = "episode.tsv"
tbl_ratings = "ratings.tsv"


# check if dataframe.csv exist
if not os.path.exists(os.getcwd() + "//raw//" + "dataframe.csv"):

    # these imports are only needed for the first time
    import urllib.request
    import gzip
    import shutil

    print(
        "\t\t\t+++ WELCOME TO THE SET UP +++\n"
        "The script needs to download some IMDB data from the IMDB servers. \n"
        "Note: If you continue a folder 'raw' will be created (if there is none) within the location"
        " of this script file.\n"
        "The download size will be approx 160mb. The final size on your hard drive—after removing unnecessary files—is approx. 26mb.\n"
        "Do you want to continue?"
    )
    cont = input("To abort use random key. To continue type 'Y': ").lower()
    if cont == "y":
        if not os.path.exists(imdb_raw):
            print("Create 'raw' folder in " + os.getcwd())
            os.makedirs("raw")
        else:
            print("Raw folder already exists but w/o the correct csv. Continuing ...")

        ##############################
        ####### DOWNLOAD FILES #######
        ##############################

        print("Download IMDB basic information (~120 mb) ...")
        url = "https://datasets.imdbws.com/title.basics.tsv.gz"
        urllib.request.urlretrieve(url, os.getcwd() + "//raw//" + tbl_basics + ".gz")
        print("Done.")

        print("Download IMDB episodes list (~30 mb) ...")
        url = "https://datasets.imdbws.com/title.episode.tsv.gz"
        urllib.request.urlretrieve(url, os.getcwd() + "//raw//" + tbl_episode + ".gz")
        print("Done.")

        print("Downloading...")
        print("Download IMDB user ratings (~7 mb) ...")
        url = "https://datasets.imdbws.com/title.ratings.tsv.gz"
        urllib.request.urlretrieve(url, os.getcwd() + "//raw//" + tbl_ratings + ".gz")
        print("Done.")

        print("Downloads finished. Extracting tsv (tab separated values) files...")

        ##############################
        ###### EXTRACTING FILES ######
        ##############################

        print("Extracting " + tbl_basics + "...")
        with gzip.open(imdb_raw + tbl_basics + ".gz", "rb") as f_in:
            with open(imdb_raw + tbl_basics, "wb") as f_out:
                shutil.copyfileobj(f_in, f_out)

        print("Extracting " + tbl_episode + "...")
        with gzip.open(imdb_raw + tbl_episode + ".gz", "rb") as f_in:
            with open(imdb_raw + tbl_episode, "wb") as f_out:
                shutil.copyfileobj(f_in, f_out)

        print("Extracting " + tbl_ratings + "...")
        with gzip.open(imdb_raw + tbl_ratings + ".gz", "rb") as f_in:
            with open(imdb_raw + tbl_ratings, "wb") as f_out:
                shutil.copyfileobj(f_in, f_out)

        ##############################
        ###### REMOVE .GZ FILES ######
        ##############################

        print("All files extracted. Cleaning ...")
        os.remove(imdb_raw + tbl_basics + ".gz")
        os.remove(imdb_raw + tbl_episode + ".gz")
        os.remove(imdb_raw + tbl_ratings + ".gz")

        ##############################
        ###### CREATE BASIC DF #######
        ##############################

        print("Cleaning done. Preprocessing tables ...")

        print("Reading " + tbl_basics + "...")
        # we don’t need all columns from this table
        columns_of_interest = ["tconst", "titleType", "primaryTitle", "startYear"]
        # IMDB uses \N for missing values. Here we convert that to NaN (escaping the \)
        df_basics = pd.read_csv(
            imdb_raw + tbl_basics,
            sep="\t",
            usecols=columns_of_interest,
            na_values=["\\N"],
        )
        # generating a type summary maybe for later
        # type_summary = df_basics.groupby('titleType')['tconst'].nunique()
        # kick out all types that are not tvSeries and tvEpisodes since we all go for Ratings for tv episodes
        df_basics = df_basics[
            (df_basics["titleType"] == "tvSeries")
            | (df_basics["titleType"] == "tvEpisode")
        ]
        # convert Year from float to int and replacing NaNs with 0 to store int
        # df_basics['startYear'] = df_basics['startYear'].fillna(0).astype(int)
        # drop rows with NaN in Year, should be fine and only trouble making for super rare unknown series...
        df_basics = df_basics.dropna(subset=["startYear"])
        # convert startYear to ints
        df_basics["startYear"] = df_basics["startYear"].astype(int)

        ##############################
        ###### CREATE EPISODE DF #####
        ##############################

        print(tbl_basics + " captured. Reading " + tbl_episode + "...")
        df_episode = pd.read_csv(
            imdb_raw + tbl_episode,
            sep="\t",
            na_values=["\\N"],
            dtype={"seasonNumber": str, "episodeNumber": str},
        )
        # get rid of elements having no seasonNumber and episodeNumber, since they are unplotable anyway
        # OLD: df_episode = df_episode[(df_episode["seasonNumber"] != "\\N") | (df_episode["episodeNumber"] != "\\N")]
        df_episode = df_episode.dropna(subset=["seasonNumber", "episodeNumber"])
        print("Append leading 0, if series/episode has only one digit.")
        df_episode["seasonNumber"] = df_episode["seasonNumber"].apply("{:0>2}".format)
        df_episode["episodeNumber"] = df_episode["episodeNumber"].apply("{:0>2}".format)
        print("Combining vectors: Series × Episode Notation: SxxExx")
        df_episode["sxxexx"] = df_episode["seasonNumber"] + df_episode["episodeNumber"]
        print("Delete single series and episode columns...")
        df_episode = df_episode.drop("seasonNumber", axis=1)
        df_episode = df_episode.drop("episodeNumber", axis=1)

        ##############################
        ###### CREATE RATINGS DF #####
        ##############################

        print(tbl_episode + " captured. Reading " + tbl_ratings + "...")
        # Ratings got no NaNs
        df_ratings = pd.read_csv(imdb_raw + tbl_ratings, sep="\t", na_values=["\\N"])

        ##############################
        ###### MERGE DATAFRAMES ######
        ##############################

        print("All files captured. Merging tables ...")
        # This complex. There Are many ways to do this...
        # Note what I thought: There are 809.029 lines in ratings. Within ratings there are some
        # ... types (short, video, etc) that we don’t need. Since we already cleaned basics to contain only
        # ... tvSeries and tvEpisodes it is safe to inner merge (SQL’s inner join), this uses intersection of keys
        # ... from both frames, see:
        # https://pandas.pydata.org/pandas-docs/stable/merging.html#brief-primer-on-merge-methods-relational-algebra
        # So, by merging Ratings and Basics we end with all tvSeries and tvEpisodes that definitely have a rating!
        # Let’s do this here:
        df_basics_ratings = pd.merge(df_basics, df_ratings, on="tconst", how="inner")

        # So far so good. Inner merging df basics/rating with df episode would results in losing tvSeries, therefore
        # ... we’re using SQL likes left outer join:
        df = pd.merge(df_basics_ratings, df_episode, on="tconst", how="left")

        ##############################
        ########## Tidy up ###########
        ##############################

        print("Merging done. Tidy up ...")
        # rename some headers to be more clean
        df.columns = [
            "tconst",
            "type",
            "title",
            "year",
            "rating",
            "votes",
            "parent",
            "sxxexx",
        ]

        print("Storing CSV ...")
        df.to_csv(imdb_raw + "dataframe.csv", index=False, sep="\t")

        print(
            "Do you want to delete the raw files (*.tsv)?\n"
            "If you want to inspect them, they are in your raw folder.\n"
            "However, they take up approx. 700mb on your hard drive, and are not needed anymore."
        )
        remove_raw = input("Remove raw files? To remove them type 'Y': ").lower()
        if remove_raw == "y":
            print("Deleting files...")
            os.remove(imdb_raw + tbl_basics)
            os.remove(imdb_raw + tbl_episode)
            os.remove(imdb_raw + tbl_ratings)
            print("Files deleted.")
        else:
            print(
                "Raw files remain untouched under " + imdb_raw + ". Happy inspecting."
            )

        print(
            "A CSV file has been stored in your raw folder. This file is important, if you delete this file\n"
            "you need to rerun the setup since the script will look for this file. \n"
            "\t\tYour System is now set up to analyze and plot IMDB data.\n"
            "\t\t\t\tPlease run IMDBratings.py"
        )

    else:
        print("Execution aborted by user.")

else:
    print("Your system is already set up. Please start IMDBratings.py.")
