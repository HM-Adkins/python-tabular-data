#! /usr/bin/env python3

import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats

def filter_species(input_file, species_column):
    """
    Filter a data frame by species and return a list of data frames.
    The input file must contain a column with species names for filtering.

     Parameters
    ----------
    input_file : str
        A csv file to be filtered.

    species_column : str
        The column that contains the species names.

     Returns
    -------
    list
        A list of data frames. Each data frame contains the information from a 
        single species. The number of data frames in the list is equal to the 
        number of species in the input file.
    """
    dataframe = pd.read_csv(input_file)
    species = dataframe[species_column].unique()
    species_df_list = []
    for sp in species:
        species_df_list.append(dataframe[dataframe.species == sp])

    # Map species names to dataframes
    species_df_dict = {name: df for name, df in zip(species, species_df_list)}

    return species_df_dict

def species_regress(species_df_dict):
    for key, value in species_df_dict.items():
        x = value.petal_length_cm
        y = value.sepal_length_cm
        regression = stats.linregress(x, y)
        slope = regression.slope
        intercept = regression.intercept
        plt.scatter(x, y, label = 'Data')
        plt.plot(x, slope * x + intercept, color = "orange", label = 'Fitted line')
        plt.xlabel("Petal length (cm)")
        plt.ylabel("Sepal length (cm)")
        plt.legend()
        plt.savefig(f"{key}_regress.png")
        plt.close()

if __name__ == '__main__':
    input_file = "iris.csv"
    filter_column = "species"