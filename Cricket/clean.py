import pandas as pd

def clean(file_name):
    """
    Clean data to answer 5 questions as follows:
        -> What is the Average Career Length
        -> AVG Batting_Strike_Rate for cricketers who played over 10 years
        -> Find number of cricketers who played before 1960
        -> Max Highest Inns Score by Country
        -> Hundreds, Fifties, Ducks (0) AVG by Country
    """

    df = pd.read_csv(file_name)


    # Drop uncessary columns and rename
    df = df.drop(['Mat', 'NO', 'Runs', 'Ave', 'BF', '4s', '6s'], axis=1)
    df = df.rename(columns={
        'HS':'Highest_Inns_Score', 
        'SR':'Batting_Strike_Rate', 
        '100':'Hundreds', 
        '50':'Fifties', 
        '0':'Ducks'
    })


    # Drop duplicates
    drop_dup = df.drop_duplicates().reset_index(drop=True)

    # to guarantee that the number of rows after dropping duplicates is correct
    # Before drop - 66 rows, After drop must be 62 rows
    assert len(drop_dup) == len(df) - df.duplicated().sum(), \
    "The number of rows after dropping duplicates are not consistent"

    df = drop_dup


    # Drop Null
    df['Batting_Strike_Rate'] = df['Batting_Strike_Rate'].fillna(df['Batting_Strike_Rate'].mean().round(2))


    # Player column
    df['Country'] = df['Player'].str.split('(').str[1] \
                                    .str.split(')').str[0] \
                                        .str.strip()

    df['Player'] = df['Player'].str.split('(').str[0] \
                                    .str.strip()
    

    # Span column
    df['Span'] = df['Span'].str.strip()
    df[['Start_Career', 'Retire_Career']] = df['Span'].str.split('-', expand=True)
    df['Start_Career'] = df['Start_Career'].astype(int)
    df['Retire_Career'] = df['Retire_Career'].astype(int)
    df = df.drop('Span', axis=1)


    # Highest_Inns_Score column
    df['Highest_Inns_Score'] = df['Highest_Inns_Score'].str.extract(r'(\d+)')
    df['Highest_Inns_Score'] = df['Highest_Inns_Score'].astype(int)

    df.to_csv("cleaned_cricket.csv", header=True, index=False)


clean("raw_cricket.csv")

