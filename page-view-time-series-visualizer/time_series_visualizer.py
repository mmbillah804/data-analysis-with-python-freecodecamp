import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

# Import data (Make sure to parse dates. Consider setting index column to 'date'.)
df = pd.read_csv('fcc-forum-pageviews.csv', parse_dates=['date'], index_col='date')

# Clean data
df = df[
    (df['value'] >= df['value'].quantile(0.025)) &
    (df['value'] <= df['value'].quantile(0.975))
]


def draw_line_plot():
    # Draw line plot
    fig, ax = plt.subplots(figsize=(14, 6))
    ax.plot(df.index, df['value'], color='r')
    ax.set_title('Daily freeCodeCamp Forum Page Views 5/2016-12/2019')
    ax.set_xlabel('Date')
    ax.set_ylabel('Page Views')

    # Save image and return fig
    fig.savefig('line_plot.png')
    return fig


def draw_bar_plot():
    # Copy and modify data for monthly bar plot
    df_bar = df.copy()
    df_bar['year'] = df_bar.index.year
    df_bar['month'] = df_bar.index.strftime('%B')  # Full month name

    # Order months correctly
    month_order = [
        'January', 'February', 'March', 'April',
        'May', 'June', 'July', 'August',
        'September', 'October', 'November', 'December'
    ]
    df_bar['month'] = pd.Categorical(df_bar['month'], categories=month_order, ordered=True)

    # Group by year and month and get average page views
    df_bar = df_bar.groupby(['year', 'month'])['value'].mean().unstack()

    # Draw bar plot
    fig = df_bar.plot(kind='bar', figsize=(14, 8)).figure
    plt.xlabel('Years')
    plt.ylabel('Average Page Views')
    plt.legend(title='Months', bbox_to_anchor=(1.05, 1), loc='upper left')

    plt.tight_layout()

    # Save image and return fig
    fig.savefig('bar_plot.png')
    return fig


def draw_box_plot():
    # Prepare data for box plots (this part is done!)
    df_box = df.copy()
    df_box.reset_index(inplace=True)
    df_box['year'] = [d.year for d in df_box.date]
    df_box['month'] = [d.strftime('%b') for d in df_box.date]

    # Custom order for months
    df_box['month'] = pd.Categorical(df_box['month'],
                                     categories=[
                                         'Jan', 'Feb', 'Mar', 'Apr',
                                         'May', 'Jun', 'Jul', 'Aug',
                                         'Sep', 'Oct', 'Nov', 'Dec'
                                     ],
                                     ordered=True)

    # Draw box plots (using Seaborn)
    fig, axes = plt.subplots(1, 2, figsize=(20, 8))

    # Year-wise box plot
    sns.boxplot(x='year', y='value', data=df_box, ax=axes[0])
    axes[0].set_title('Year-wise Box Plot (Trend)')
    axes[0].set_xlabel('Year')
    axes[0].set_ylabel('Page Views')

    # Month-wise box plot
    sns.boxplot(x='month', y='value', data=df_box, ax=axes[1])
    axes[1].set_title('Month-wise Box Plot (Seasonality)')
    axes[1].set_xlabel('Month')
    axes[1].set_ylabel('Page Views')

    # Save image and return fig
    fig.savefig('box_plot.png')
    return fig
    