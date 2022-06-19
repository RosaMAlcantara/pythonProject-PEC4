import os
import pandas as pd
import numpy as np
import seaborn as sns

pd.options.mode.chained_assignment = None
def read_add_year_gender(filepath: str, gender: str, year: int) -> pd.DataFrame:
    """
    Read the file indicates in filepath var and adds information about gender and year.
     Parameters:
        filepath (str): PathṀs file.
        gender (str)  : Gender (it can be 'M' or 'F').
        year (int)    : The year to which the data corresponds.
                        Four digits for the format.(XXXX).
     Returns:
        (pd.DataFrame): A dataframe with two columns append (gender and year).

    """
    try:
        year_str = str(year)
        year_cad = year_str[2:4]
        wdir = '../'
        data = pd.read_csv(os.path.join(wdir, filepath), header=0, low_memory=False)
        year_num = int(year_cad)
        data[data['age'] == year_num]
        data['gender'] = gender
        data['year'] = year
        return data
    except FileNotFoundError:
        print('Sorry the file we are looking for does not exist')


def join_male_female(path: str, year: int) -> pd.DataFrame:
    """
        Function that creates a single dataframe with the data of the players, with information about the gender
        and the year.
         Parameters:
            path (str): Path's file.
            year (int) : The year to which the data corresponds.
                         Four digits for the format.(XXXX).
         Returns:
            (pd.DataFrame): A dataframe with two columns append (gender and year).

    """
    year_cad = str(year)
    year_str = year_cad[2:4]
    contenido = os.listdir(os.path.join('../', path))
    str_match = [s for s in contenido if year_str in s]
    str_match_f = [s for s in str_match if 'female' in s]
    str_match_m = [s for s in str_match if 'female' not in s]
    data_m = read_add_year_gender(os.path.join(path, str_match_m[0]), 'M', year)
    data_f = read_add_year_gender(os.path.join(path, str_match_f[0]), 'F', year)
    merged_df = data_f.append(data_m)
    return merged_df


def join_datasets_year(path: str, years: list) -> pd.DataFrame:
    """

            A function that reads the information corresponding to soccer players of both genders
            for several years, returning a single dataframe, with information abut gender and year.
                 Parameters:
                    path (str): Path's file.
                    years (int)    : List of years to which the data corresponds.
                                    Four digits for the format.(XXXX).
                 Returns:
                    (pd.DataFrame): A dataframe with two columns append (gender and year).

        """
    df = pd.DataFrame()
    for i in years:
        df = pd.concat([df, join_male_female(path, i)], sort=True)
    return df


def find_max_col(df: pd.DataFrame, filter_col: str, cols_to_return: list) -> pd.DataFrame:
    """

            A function that, given the name of a numeric column, returns the row(s) in
            which its value is maximum. In addition, the function will receive as an argument a list of
            columns.

                 Parameters:
                    df (pd.DataFrame): Dataframe.
                    filter_col(str)    : name of the column from which we want to find out the maximum.
                    cols_to_return: (list) : List of columns to return.
                 Returns:
                    (pd.DataFrame): A dataframe with the rows returned by the function with only these columns.

        """

    seleccion = df.select_dtypes(include=["number"])
    df_1 = pd.DataFrame()
    if filter_col in seleccion:
        for i in cols_to_return:
            value_max = df[i].max()
            if df[i].max() == value_max:
                df_1[i] = df[df[i] == df[i].max()][i]

    return df_1


def find_rows_query(df: pd.DataFrame, query: tuple, cols_to_return: list) -> pd.DataFrame:
    """
         The function will receive a query in tuple form. The first element will be a list of columns on
         which we want filter. The second element will be the list of values that we want to use in the filter.
         If the column is categorical, the value will be a string. If it is numeric, it will be a tuple with the
         value minimum.
                 Parameters:
                     df (pd.DataFrame): Dataframe.
                     query(tuple)     : Query's data.
                     cols_to_return: (list) : List of columns to return.
                 Returns:
                    (pd.DataFrame): The rows returned by the function must contain only these columns.

        """

    # assert cols_to_return not in df.columns.values, 'Hay alguna columna que no está en el dataframe.'
    # The numerical fields in the dataframe are extracted

    seleccion = df.select_dtypes(include=["number"])

    if len(query) == 2:
        name_first = query[0][0], query[1][0]
        if name_first[0] in seleccion:
            df = df.loc[(df[name_first[0]] >= name_first[1][0]) & (df[name_first[0]] <= name_first[1][1])][
                cols_to_return]
        else:
            df = df[df[name_first[0]] == name_first[1]][cols_to_return]
    return df

def show_players_all_years(df: pd.DataFrame) -> None :
    """
        From the data set, show the players of Belgian nationality under 25 years of age with maximum
        potential and the goalkeepers over 28 with an overall greater than 85 in women's soccer.
            Parameters:
                df: (pd.DataFrame): DataFrame.
            Returns:
                None
    """
    data = join_datasets_year("data", [2016, 2017, 2018, 2018, 2019, 2020, 2021, 2022])
    cols = ["short_name", "year", "overall", "potential"]
    data['potential'].max()
    data.query("nationality_name == 'Belgium' and age < 25 and gender == 'M' and  potential == @m")[cols]
    data.query("gender =='F' and age > 28 and overall > 85 and player_positions == 'GK'")[cols]
    return None

def calculate_bmi(df: pd.DataFrame , gender: str , year: int , cols_to_return: list) -> pd.DataFrame:
    """

            A function that receives a dataframe with the data, a gender and a year and returns a dataframe that
            includes a column with the mass index (BMI) of each soccer player.
                 Parameters:
                     df (pd.DataFrame): Dataframe.
                     gender:(str) Gender (it can be 'M' or 'F').
                     year (int)    : The year to which the data corresponds.
                                    Four digits for the format.(XXXX).
                      cols_to_return: (list) : List of columns to return.
                 Returns:
                    (pd.DataFrame): A dataframe with two columns append (gender and year).

        """
    df = df.loc[(df['gender'] == gender) &
                (df['year'] == year)]
    BMI = (df['weight_kg']) / ((df['height_cm'] / 10) * (df['height_cm'] / 10))*100
    df['BMI'] = BMI

    return df

def grafico_BMI_pais (data: pd.DataFrame, gender: str, year: int ) -> None:

     """

            A function that receives a dataframe with the data, a gender and a year and returns a dataframe that
            includes a column with the mass index (BMI) of each soccer player.
                 Parameters:
                     df (pd.DataFrame): Dataframe.

                 Returns:
                    None:

        """
     df_sin = calculate_bmi(data, gender, year, ["club_flag_url", 'BMI'])
     df_sin = df_sin.fillna('No Value.')
     df_sin['BMI'] = round(df_sin['BMI'], 2)
     df_sin['PAIS'] = df_sin.club_flag_url.str[29:31]
     df_sin.sort_values('PAIS')
     df_o = df_sin.groupby(by=['PAIS']).BMI.max().reset_index()
     df_o['category'] = np.where(df_o['BMI'] < 18.5, 'Underweight',
                        np.where(df_o['BMI'] < 25, 'Normal weight',
                        np.where(df_o['BMI'] < 30, 'Overweight', 'Obese')))

     # Prepare size and  style
     sns.set(rc={'figure.figsize': (12, 10)})
     sns.set_style("whitegrid")

     # Crete the figure
     p = sns.barplot(data=df_o, y='PAIS', x='BMI', hue='category', orient='h')
     p.set_title('Máximo BMI por país')
     return


def grafico_BMI_comparativa(data: pd.DataFrame) -> None:
    """

           A function that receives a dataframe with the data, a gender and a year and returns a dataframe that
           includes a column with the mass index (BMI) of each soccer player.
                Parameters:
                    df (pd.DataFrame): Dataframe.

                Returns:
                   None:

       """
    # Prepare size and  style
    sns.set(rc={'figure.figsize': (12, 10)})
    sns.set_style("whitegrid")

    # Crete the figure
    p = sns.barplot(data=data, y='total', x='category', hue='category', orient='v',
                        palette=["#9b59b6", "#ff0000", "#00f0f0", "#00ff00"])
    p.set_title('Comparativa Mujeres españolas de 18 a 24 años y resto del mundo')
    return

def players_dict(df: pd.DataFrame , ids: list , cols: list) -> dict:
    """

            A function that returns a dictionary where the keys are the values of the column “sofifa_id”
            contained in the “ids” list and the associated values  dictionaries with the information
            correspondent.
                 Parameters:
                    df (dataframe): A dictionary
                    ids (list)    :  sofifa_id list.
                    cols (list)   : columns to save in the dataframe.
                 Returns:
                    (dict): dictionary where the keys are the values of the column “sofifa_id”.

        """
    f = {}
    cols_1 = ['sofifa_id']
    df_1 = df.query("sofifa_id in @ids").sort_values('sofifa_id')[cols_1]
    df_2 = df.query("sofifa_id in @ids").sort_values('sofifa_id')[cols]
    df_2['sofifa_id'] = df_1['sofifa_id']
    f = dict.fromkeys(ids, )
    for i in ids:
        df_3 = df_2.loc[df_2['sofifa_id'] == i][cols]
        d3 = df_3.to_dict('list')
        f[i] = d3
    return f



def clean_up_players_dict(data_dict: dict , col_query: list) -> list:
    """

          A function that removes the redundant information.
                 Parameters:
                    player_dict (dict) : players_dict format dictionary.
                    col_query (list)   : tuples list with details about the information to simplify
                 Returns:
                    (dict): A dictionary with a determinate format.

    """

    total = len(col_query)
    for i in range(total):
        for element in col_query:
            print(element[i])
            if (element[i] == 'one'):
                for k, v in data_dict.items():
                    data_dict[k][element[0]] = data_dict[k][element[0]][0].strip('"')

            if element[i] == 'del_rep':
                for k, v in data_dict.items():
                    lst = [*data_dict[k][element[0]]]
                    data_dict[k][element[0]] = lst[2].split()

    return data_dict


def top_average_column(data: dict , identifier: str , col: str , threshold: int) -> list:
    """

            A function for each sofifa_id, compute the average value of the col feature if you have
            threshold information or more years
                 Parameters:
                    data (dict) : A clean dictionary with several sofifa_id.
                    identifier(str) : column/key to be used as identifier.
                    col (str) : name of a column/numeric key.
                    threshold (int)    : Minimum number of data needed.
                 Returns:
                    (list): Return a list of tuples consisting of three elements: column value
                            identifier; characteristic average; and a dictionary composed of the key
                            year containing the list of years corresponding to the values the key value
                            with those values

        """
    return