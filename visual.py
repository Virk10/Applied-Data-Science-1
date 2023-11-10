import pandas as pd
import matplotlib.pyplot as plt
import os
def merge_climate_data(urls, columns):
    """
    Merge climate data from multiple URLs into a single DataFrame.

    Parameters:
    - urls (list): A list of URLs containing climate data.
    - columns (list): A list of column names corresponding to each URL.

    Returns:
    - pd.DataFrame: Merged DataFrame with 'year' as the common column and specified columns from each URL.
    """
    dfs = []
    for url, column in zip(urls, columns):
        df = pd.read_csv(url, skiprows=5, sep='\s+')
        df = df[['year', 'ann']]
        df.rename(columns={"ann": column}, inplace=True)
        dfs.append(df)

    merged_df = dfs[0]
    for df in dfs[1:]:
        merged_df = pd.merge(merged_df, df, on="year")

    return merged_df

def plot_moving_averages(df, columns, window=20, title="Rising Temperature", xlabel="Year", ylabel="Mean Temperature"):
    """
    Create a line plot for the specified columns with 20-year moving averages.

    Parameters:
    - df (pd.DataFrame): The DataFrame containing the data.
    - columns (list): A list of column names to plot.
    - window (int): The size of the moving average window (default is 20).
    - title (str): The title of the plot (default is "Rising Temperature").
    - xlabel (str): The label for the x-axis (default is "Year").
    - ylabel (str): The label for the y-axis (default is "Mean Temperature").

    Returns:
    - None
    """
    for column in columns:
        df[column] = df[column].rolling(window=window).mean()
        plt.plot(df["year"], df[column], label=column)

    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)

    plt.legend(loc="upper left")
    plt.show()

def plot_unclaimed_estates(file_path, date_format="%m/%d/%Y"):
    """
    Load data from a CSV file containing information about unclaimed estates,
    filter the data to include only years after 1999, and create a bar chart
    showing the count of unclaimed estates per year.

    Parameters:
    - file_path (str): The file path of the CSV file containing unclaimed estates data.
    - date_format (str): The format of the date column in the CSV file (default is "%m/%d/%Y").

    Returns:
    - None
    """
    data = pd.read_csv(file_path, encoding='ISO-8859-1')
    
    # Convert the 'Date of Death' column to datetime using the specified format
    data['Year of Death'] = pd.to_datetime(data['Date of Death'], format=date_format).dt.year
    
    filtered_data = data[data['Year of Death'] > 1999]
    yearly_counts = filtered_data['Year of Death'].value_counts().sort_index()

    plt.figure(figsize=(10, 6))
    plt.bar(yearly_counts.index, yearly_counts.values, color='skyblue', width=0.6)
    plt.xlabel('Unclaimed Year')
    plt.ylabel('Count')
    plt.title('Unclaimed House since 2000')

    plt.xticks(yearly_counts.index, rotation=45)
    plt.tight_layout()
    plt.show()

def plot_marital_status_distribution(file_path, threshold=0.03):
    """
    Plot the distribution of marital status, grouping small categories as "Other" if their percentage is below the threshold.

    Parameters:
    - data (pd.DataFrame): The DataFrame containing the marital status data.
    - threshold (float): The threshold percentage to determine small categories (default is 0.03).

    Returns:
    - None
    """
    data = pd.read_csv(file_path, encoding='ISO-8859-1')
    marital_status_counts = data['Marital Status'].value_counts()
    small_categories = marital_status_counts[marital_status_counts / marital_status_counts.sum() < threshold].index
    data['Marital Status'] = data['Marital Status'].apply(lambda x: 'Other' if x in small_categories else x)
    marital_status_counts = data['Marital Status'].value_counts()

    plt.figure(figsize=(8, 8))
    plt.pie(marital_status_counts, labels=marital_status_counts.index, autopct='%1.1f%%', startangle=140)
    plt.title('Distribution of Marital Status')
    plt.axis('equal')
    plt.show()


def main():
    """
    Execute all the functions to load and visualize data.
    """
    url_list = [
        'https://www.metoffice.gov.uk/pub/data/weather/uk/climate/datasets/Tmean/date/England.txt',
        'https://www.metoffice.gov.uk/pub/data/weather/uk/climate/datasets/Tmean/date/Wales.txt',
        'https://www.metoffice.gov.uk/pub/data/weather/uk/climate/datasets/Tmean/date/Scotland.txt',
        'https://www.metoffice.gov.uk/pub/data/weather/uk/climate/datasets/Tmean/date/Northern_Ireland.txt'
    ]
    column_names = ['england', 'wales', 'scotland', 'northern']

    result_df = merge_climate_data(url_list, column_names)
    columns_to_plot = ['england', 'scotland', 'wales', 'northern']
    plot_moving_averages(result_df, columns_to_plot)
    date_format = "%d/%m/%Y"
    # Get the current working directory of the script
    current_directory = os.getcwd()
    file_path = "UnclaimedEstatesList.csv"
    plot_unclaimed_estates(file_path,date_format=date_format)
    plot_marital_status_distribution(file_path)

# Call the main function to execute all the functions
main()
