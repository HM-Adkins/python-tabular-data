#! /usr/bin/env python3

import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats


def filter_species(input_file, species_column):
    """
    Filter a data frame by species and return a dictionary of
    species name : data frame pairs. The input file must contain a column with
    species names for filtering.

     Parameters
    ----------
    input_file : str
        A csv file to be filtered.

    species_column : str
        The column that contains the species names.

     Returns
    -------
    dict
        A dictionary of species name : data frame pairs. Each data frame
        contains the information from a single species. The number of pairs is
        equal to the number of species in the input file.
    """
    dataframe = pd.read_csv(input_file)
    species = dataframe[species_column].unique()
    species_df_list = []
    for sp in species:
        species_df_list.append(dataframe[dataframe.species == sp])

    # Map species names to dataframes
    species_df_dict = {name: df for name, df in zip(species, species_df_list)}

    return species_df_dict


def species_regress(species_df_dict, 
                    predictor,
                    response):
    """
    Performs and plots regressions for specified predictor and response
    variables from data frames provided in a dictionary of
    species name : data frame pairs.

     Parameters
    ----------
    species_df_dict : dict
        A dictionary of species name : data frame pairs generated using the
        filter_species function.

    pred_var : str
        The column that contains the predictor (independent) variable values.

    res_var : str
        The column that contains the response (dependent) variable values.

     Returns
    -------
    image file
        png image of the plotted data and regression line for a single species.
        The number of images generated is equal the number of pairs in the dict.
        
    """
    for key, value in species_df_dict.items():
        x = value[predictor]
        y = value[response]
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
        print(f"{key}_regress.png created in working directory")


if __name__ == '__main__':
    species_df_dict = filter_species(input_file = "iris.csv",
                                     species_column = "species")
    species_regress(species_df_dict = species_df_dict,
                    predictor = "petal_length_cm",
                    response = "sepal_length_cm")
