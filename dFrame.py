import requests
import pandas as pd

def fetch_api_data(url):
    """
    Fetches data from a given API URL and returns it as a pandas DataFrame.
    """
    try:
        response = requests.get(url)
        response.raise_for_status()  
        data = response.json()
        
        if not data:  
            print(f"No data found at {url}")
            return pd.DataFrame()

        return pd.DataFrame(data)
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from {url}: {e}")
        return pd.DataFrame()  

def preprocess_data(df):
    """
    Cleans and preprocesses the given DataFrame.
    """
    if df.empty:
        return df

    for col in df.columns:
        if df[col].apply(lambda x: isinstance(x, list)).any():  
            df[col] = df[col].apply(lambda x: str(x) if isinstance(x, list) else x)  
    
    df = df.drop_duplicates()  
    

    df = df.fillna("Unknown")  


    if 'date' in df.columns:
        df['date'] = pd.to_datetime(df['date'], errors='coerce')  
    df.columns = [col.lower() for col in df.columns]  
    
    return df

def main():
    christians_url = 'http://127.0.0.1:8000/christians'
    events_url = 'http://127.0.0.1:8000/events'

    # Fetch and preprocess data
    christians_df = fetch_api_data(christians_url)
    events_df = fetch_api_data(events_url)

    if christians_df.empty or events_df.empty:
        print("One or more datasets are empty. Exiting.")
        return

    christians_df = preprocess_data(christians_df)
    events_df = preprocess_data(events_df)

    
    print("Shape of Christians DataFrame:", christians_df.shape)
    print("Shape of Events DataFrame:", events_df.shape)

    print("\nChristians DataFrame - Describe:")
    print(christians_df.describe(include='all'))  
    print("\nChristians DataFrame - Info:")
    print(christians_df.info())

    print("\nEvents DataFrame - Describe:")
    print(events_df.describe(include='all'))  
    print("\nEvents DataFrame - Info:")
    print(events_df.info())

    print("Christians DataFrame columns:", christians_df.columns)
    print("Events DataFrame columns:", events_df.columns)

    events_df = events_df.rename(columns={'id': 'event_id'})

    # Check if 'event_id' exists in both dataframes before merging
    if 'event_id' not in christians_df.columns or 'event_id' not in events_df.columns:
        print("Error: 'event_id' column missing from one or both DataFrames.")
        return

    merged_df = pd.merge(christians_df, events_df, on="event_id", how="inner")

    print("\nMerged DataFrame - Describe:")
    print(merged_df.describe(include='all'))
    print("\nMerged DataFrame - Info:")
    print(merged_df.info())

    merged_df.to_csv("merged_data.csv", index=False)

    print(f"Merged data saved to 'merged_data.csv'.")

if __name__ == "__main__":
    main()
