import sqlalchemy, pyodbc, os
import pandas as pd
import inspect
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
import numpy as np
from mwbe import QUERY_TXT

def get_data():
    Source_InstanceName = 'MU19PRODDB1'
    Source_DB_Name = 'munprod'
    # change below Instance & Database name
    Source_conn =sqlalchemy.create_engine(f'mssql+pyodbc://{Source_InstanceName}/{Source_DB_Name}?trusted_connection=yes&driver=ODBC Driver 17 for SQL Server')

    query = inspect.cleandoc(QUERY_TXT)

    df = pd.read_sql(query, con=Source_conn)
    df.to_csv('mwbe.csv', index=False)
    print(df.shape)
    

def get_df():
    df = pd.read_csv('mwbe.csv')
    return df
    
    
if __name__ == '__main__':
    df = get_df()
    
    


    # Assuming 'df' is your DataFrame and it has been loaded correctly.
    # Group by 'apih_je_year' and sum 'LineCost'
    yearly_totals = df.groupby('apih_je_year')['LineCost'].sum().reset_index()

    # Sort by year to ensure the bar chart is ordered correctly
    yearly_totals = yearly_totals.sort_values(by='apih_je_year')

    # Format function to convert numbers to millions with 'm' suffix
    def millions(x, pos):
        return '%1.1f m' % (x * 1e-6)

    # Set up the plot
    plt.figure(figsize=(10, 6))

    # Plot the bar chart
    plt.bar(yearly_totals['apih_je_year'], yearly_totals['LineCost'])

    # Label the axes
    plt.xlabel('Fiscal Year')
    plt.ylabel('Total LineCost (in millions)')

    # Set the title
    plt.title('Total LineCost per Fiscal Year')

    # Rotate the x-axis labels for better readability
    plt.xticks(rotation=45)

    # Format the Y-axis to show values in millions
    formatter = FuncFormatter(millions)
    plt.gca().yaxis.set_major_formatter(formatter)

    # Show the plot
    plt.tight_layout()  # Adjust layout to prevent clipping of tick-labels
    plt.show()