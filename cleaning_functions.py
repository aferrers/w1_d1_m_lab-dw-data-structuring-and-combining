import pandas as pd
import numpy as np

#define function to make all column names in a dataframe lowercase
#would not work without"map"

def make_col_names_lowercase(dataframe: pd.DataFrame) -> pd.DataFrame:
    ''' 
    This function takes dataframe.columns and makes them lowercase
    Inputs:
    dataframe: pd.DataFrame
    Output: pd.DataFrame
    '''
    
    df_copy=dataframe.copy()
    
    df_copy.columns = df_copy.columns.map(str.lower)

    return df_copy

#define function to replace  "_" for " " in all column names in a dataframe lowercase
#would not work with map or with lambda

def remove_blanks_in_col_names(dataframe: pd.DataFrame) -> pd.DataFrame:
    ''' 
    This function removes blank characters in dataframe column names
    Inputs:
    dataframe: pd.DataFrame
    '''
    df_no_blanks=dataframe.copy()
    
    df_no_blanks.columns = df_no_blanks.columns.str.replace(' ','_')
    return df_no_blanks


#define function to fix gender types. Includes a check for strings as some values may have been floats, producing errors.
def fix_gender_types(df: pd.DataFrame) -> pd.DataFrame:
    '''
    this function replaces each record of ender with the first letter of each string.
    Inputs:
    pd: DataFrame
    Outputs: pd.DataFrame
    '''
    df_f=df.copy()
    if 'gender' in df_f.columns:
        df_f['gender'] = list(map(lambda x: x[0].upper() if isinstance(x, str) and x[0].upper() in ['M', 'F'] else None, df_f['gender']))
        return df_f
    else:
        return df_f
    

#define function to fix state values, education, vehicle class. 
#this function is not modular is it does multiple things at once. it was created to practice embedding dictionaries within dictionaries

def fix_state_names_and_education_and_vehicle_class(df: pd.DataFrame) -> pd.DataFrame:
    '''
    this function replaces each abbreviation with the full state name as in the dictionary defined in the function.
    Inputs:
    pd: DataFrame
    Outputs: pd.DataFrame
    '''
    df_f=df.copy()
    replacement_dictionary = {'state': {'Cali': 'California', 'AZ': 'Arizona', 'WA': 'Washington'},
                             'education': {'Bachelors': 'Bachelor'},
                             'vehicle_class': {'Luxury SUV': 'Luxury', 'Sports Car': 'Luxury', 'Luxury Car': 'Luxury'}}
    if 'state' or 'education' in df_f.columns:
        df_f = df_f.replace(replacement_dictionary)
        return df_f
    else:
        return df_f

    
#define function to replace one value for no value in a specific column
#can be used to replace % in the customer lifetime value column

def remove_char_in_rows(df: pd.DataFrame, column_name: str, char: str) -> pd.DataFrame:
    '''
    This function replace one value for no value in a specific column 
    can be used to replace % in the customer lifetime value column
    Inputs:
    dataframe: pd.DataFrame
    '''
    df_f=df.copy()
    
    df_f[column_name] = df[column_name].str.replace(char,'')
    return df_f

# create function to drop na rows

def drop_na_rows(df: pd.DataFrame, *column_names) -> pd.DataFrame:
    '''
    function to drop na rows
    Input:
    DataFrame
    Column names: tuple
    Output:
    DataFrame
    '''
    df_c=df.copy()
    if all(col in df_c.columns for col in column_names):
    #if column_names in df_c.columns:
        df_c=df_c.dropna(subset = column_names)
    else:
        pass
    return df_c



#create function to convert floats to ints
#used apply as applymap is being deprecated
def convert_numeric_col_to_integers (df: pd.DataFrame) -> pd.DataFrame:
    '''
    convert float64 to integers
    Inputs:
    DataFrame
    Output:
    DataFrame
    '''
    
    for column_name in df.columns:
        if isinstance(df[column_name].dtype, pd.Float64Dtype):
       # if df[column_name].dtype in ['float64']:
            df[column_name] = df[column_name].apply(lambda x: int() if x.dtype in ['float64'] else x)
        else:
            pass
    return df




def open_complaints_fix(df: pd.DataFrame, column: str) -> pd.DataFrame:
    '''
    text
    '''
    df2=df.copy()
    if column in df2.columns:
        df2[column] = df2[column].str.split('/', n=2, expand=False).str[1]
    else:
        print("col not found")
    return df2


def open_complaints_fix_len_check(df: pd.DataFrame, column: str) -> pd.DataFrame:
    '''
    text
    '''
    df2=df.copy()
    if column in df2.columns:
        mask = df2[column].apply(lambda x: isinstance(x, str) and len(x) > 1)
        df2.loc[mask, column] = df2.loc[mask, column].str.split('/', n=2, expand=False).str[1]
    else:
        print("col not found")
    return df2


#parent functions to clean up a dataframe

def cleaning_functions_dataframe(df: pd.DataFrame, *column_names) -> pd.DataFrame:
    '''
    This function will take a Pandas DataFrame and it will apply the previous functions in the library
    to clean some columns of the dataframe

    Inputs: 
    df: Pandas DataFrame

    Outputs:
    Another DataFrame
    '''

    df2 = df.copy()
    
    df2 = drop_na_rows(df2, *column_names)
    df2 = make_col_names_lowercase(df2)
    df2 = remove_blanks_in_col_names(df2)
    df2 = fix_gender_types(df2)
    df2 = fix_state_names_and_education_and_vehicle_class(df2)
    df2 = convert_numeric_col_to_integers(df2)

    return df2
