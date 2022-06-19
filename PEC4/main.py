import pandas as pd
import seaborn as sns
from functions import (
    read_add_year_gender,
    join_male_female,
    join_datasets_year,
    find_max_col,
    find_rows_query,
    calculate_bmi,
    players_dict,
    clean_up_players_dict,
    top_average_column,
    grafico_BMI_pais,
    grafico_BMI_comparativa,
)



def main(path_female_players_16, path_female_players_17, path_female_players_18, path_female_players_19,
         path_female_players_20, path_female_players_21, path_female_players_22, path_players_16,
         path_players_17, path_players_18, path_players_19, path_players_20, path_players_21, path_players_22,
         path_female_player_18_24):
    """Main function that runs all the expected analyses listed in ES-PEC4-enun.ipynb."""
    #########################################
    ########## Exercise 1 .A###################
    #########################################
    print('Bienvenid@s')
    data = read_add_year_gender(path_female_players_16, 'F', 2016)
    data.head()

    #########################################
    ########## Exercise 1.B ###################
    #########################################
    df = join_male_female("data", 2016)
    df.head()
    df.tail()

    #########################################
    ########## Exercise 1.C###################
    #########################################
    df = join_datasets_year('data', [2016, 2018, 2020])
    print(df)

    #########################################
    ########## Exercise 2.A###################
    #########################################
    filtered_df = find_max_col(path_players_20, "potential", ["potential"])
    filtered_df.head()

    #########################################
    ########## Exercise 2.B ###################
    #########################################
    filtered_df2 = find_rows_query(path_female_players_22, (["gender"], ["F"]), ["short_name", "gender"])
    filtered_df2.head()
    #########################################
    ########## Exercise 3.A ###################
    #########################################
    male_bmi = calculate_bmi(data, "M", 2021, ["short_name"])
    print(male_bmi)

    #########################################
    ########## Exercise 3.B ###################
    #########################################
    data = join_datasets_year("data", [2016, 2017, 2018, 2022])
    grafico_BMI_pais(data, 'M', 2022)

    #########################################
    ########## Exercise 3.C ###################
    #########################################
    data = sns.load_dataset(path_female_players_18)
    grafico_BMI_comparativa(data )

    #########################################
    ########## Exercise 4.A ###################
    #########################################
    data = join_datasets_year( "data" , [2016 , 2017 , 2018] )
    ids = [192476, 230566]
    columns_of_interest = ["short_name", "year"]
    data_dict = players_dict(data, ids, columns_of_interest)
    print(data_dict)

    #########################################
    ########## Exercise 4.B ###################
    #########################################
    data = join_datasets_year("data", [2016, 2017, 2018])
    ids = [176580, 168542]
    columns_of_interest = ["overall", "player_positions"]
    data_dict = players_dict(data, ids, columns_of_interest)
    data_dict = clean_up_players_dict(data_dict, [("player_positions", "del_rep")])

    #########################################
    ########## Exercise 5 A###################
    #########################################
    top_shooting = top_average_column(data_dict, "short_name", "shooting", 2)

    #########################################
    ########## Exercise 5 B###################
    #########################################
    if __name__ == "__main__":
            path_female_players_16 = "../data/female_players_16.csv"
            path_female_players_17 = "../data/female_players_17.csv"
            path_female_players_18 = "../data/female_players_18.csv"
            path_female_players_19 = "../data/female_players_19.csv"
            path_female_players_20 = "../data/female_players_20.csv"
            path_female_players_21 = "../data/female_players_21.csv"
            path_female_players_22 = "../data/female_players_22.csv"
            path_players_16 = "../data/players_16.csv"
            path_players_17 = "../data/players_17.csv"
            path_players_18 = "../data/players_18.csv"
            path_players_19 = "../data/players_19.csv"
            path_players_20 = "../data/players_20.csv"
            path_players_21 = "../data/players_21.csv"
            path_players_22 = "../data/players_22.csv"
            path_female_player_18_24 = "../data/female_player_18_24.csv"

    main( path_female_players_16, path_female_players_17, path_female_players_18, path_female_players_19,
              path_female_players_20, path_female_players_21, path_female_players_22, path_players_16,
              path_players_16, path_players_17, path_players_18,
              path_players_19, path_players_20, path_players_21, path_players_22, path_female_player_18_24)


