import pandas as pd
import numpy as np


def clean(file_name):
    df = pd.read_csv(file_name)

    # Author column
    df['author'] = df['author'].str.replace('Writtenby:', '')


    # Narrator
    df['narrator'] = df['narrator'].str.replace('Narratedby:', '')
    

    # Time column - split to Hour and Minutes
    df['time'] = df['time'].str.strip()
    df[['hour', 'minutes']] = df['time'].str.split(' and ', expand=True)

    # Hour column
    # Convert all value into minutes then cast to INTEGER type
    df['hour'] = df['hour'].apply(lambda x: int(x.replace(' hrs', '').strip()) * 60 if x.endswith('hrs')
                                            else int(x.replace(' hr', '').strip()) * 60 if x.endswith('hr')
                                            else int(x.replace(' mins', '').strip()) if x.endswith('mins')
                                            else int(x.replace(' min', '').strip()) if x.endswith('min')   
                                            else 1 if x == 'Less than 1 minute'
                                            else x)
    
    # Minutes column
    # Replace NULL with STRING 0
    df['minutes'] = df['minutes'].fillna('0')
    # Cast to INTEGER type
    df['minutes'] = df['minutes'].apply(lambda x: int(x.replace(' mins', '').strip()) if x.endswith('mins')
                                        else int(x.replace(' min', '').strip()) if x.endswith('min')   
                                        else 0 if x == '0'
                                        else x)
    
    # Create new column named 'duration_mins', hour + minutes
    df['duration_mins'] = df['hour'] + df['minutes']



    # Release date column - convert to DATETIME type
    df['releasedate'] = pd.to_datetime(df['releasedate'])


    # Language column - capitalize all languages
    df['language'] = df['language'].apply(lambda x: 'Mandarin Chinese' if x == 'mandarin_chinese' 
                                                else x.title())
    

    # Price column - cast to FLOAT type
    df['price'] = df['price'].str.replace(',', '')
    df['price'] = df['price'].str.replace('Free', '0')
    df['price'] = df['price'].astype(float)


    # Stars column - split to Star and Ratings
    df[['star', 'ratings']] = df['stars'].str.split('stars', expand=True)

    # Star
    df['star'] = df['star'].str.replace(' out of 5', '')
    df['star'] = df['star'].str.replace('Not rated yet', '0')
    df['star'] = df['star'].astype(float)
    df['star'] = df['star'].replace(0.0, np.nan)

    # Ratings
    df['ratings'] = df['ratings'].str.replace('ratings', '')
    df['ratings'] = df['ratings'].str.replace('rating', '')
    df['ratings'] = df['ratings'].str.replace(',', '')
    df['ratings'] = df['ratings'].fillna('0')
    df['ratings'] = df['ratings'].astype(int)


    # Drop uncessary columns and Rename
    df = df.drop(['time', 'stars', 'hour', 'minutes'], axis=1)
    df = df.rename(
        columns={
            'releasedate': 'released_date',
            'language': 'languages',
            'star': 'stars'
        }
    )


    df.to_csv("cleaned_audible.csv", header=True, index=False)


clean("raw_audible.csv")

