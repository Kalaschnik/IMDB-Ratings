# Plot TV Series Rating Based on IMDb User Ratings

> Scatter plot a TV series listed within the *Internet Movie Database* (IMDb).

## ℹ Note
A more recent web app approach is offered by [ratingraph.com](https://www.ratingraph.com/tv-shows/).

## How-to

Start by downloading the setup file `IMDBratings_setup.py` and the execution file `IMDBratings.py`. 

### Setup

Run `python IMDBratings_setup.py`. The CLI will guide you through the setup:
1. The script will create a `raw` folder within the current directory, then
2. it will download three datasets from https://datasets.imdbws.com/. Specifically, (1) `title.basics.tsv.gz`, (2) `title.episode.tsv.gz`, and (3) `title.ratings.tsv.gz`.
3. Thereafter, it will extract the files and merge the tables.
4. Lastly, the script removes the gz files, and you end up with a csv file being approx. 26 MB


### Series Exploration
Run `python IMDBratings.py`. The CLI will guide you through the setup:
1. You can enter an arbitrary series (it needs to be listed in IMDb).
2. In case there are multiple series sharing the same name, you get asked to enter a release year to specify your selection.
3. The script returns a scatter plot with a linear regression of your series.


## Demos

### Setup
![test](util/imdb-series-ratings-setup.gif)

### Series Exploration
![test](util/imdb-series-ratings.gif)




## About

This project was part of the lecture *Introduction to Digital Humanities* during the term 2017/2018, held by Dr. Francesco Mambrini ([@francescomambrini](https://github.com/francescomambrini)) at Leipzig University. There is also a not so serious project report as [PDF](util/It's-in-the-Slope-Linear-Regression-of-IMDb-Series.pdf).

