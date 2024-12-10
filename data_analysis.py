import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.stats import ttest_ind
import argparse


def plot_distribution_of_numeric_cols(df):
    numeric_columns = df.select_dtypes(include='number').columns

    for col in numeric_columns:
        plt.figure()
        plt.hist(df[col], bins=10, edgecolor='k', alpha=0.7)
        plt.title(f'Histogram of {col}')
        plt.xlabel(col)
        plt.ylabel('Frequency')
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        plt.show()

def visualize_engagement_boxplot(df, engagement_metric=None):
    """
    Visualizes the engagement for toxic vs. non-toxic posts using a box plot.
    """
    if engagement_metric is None:
        df['engagement'] = df['like_count'] + df['quote_count'] + df['repost_count']
        sns.boxplot(data=df, x='toxic', y='engagement')
        plt.title('Engagement for Toxic vs. Non-Toxic Posts')
        plt.xlabel('Toxicity (1 = Toxic, 0 = Non-Toxic)')
        plt.ylabel('Engagement (Likes + Quotes + Reposts)')
        plt.show()

    else:
        sns.boxplot(data=df, x='toxic', y=engagement_metric)
        plt.title(f"{engagement_metric} for Toxic vs. Non-Toxic Posts")
        plt.xlabel('Toxicity (1 = Toxic, 0 = Non-Toxic)')
        plt.ylabel(f"{engagement_metric}")
        plt.show()


def scatter_with_regression(df):
    """
    Creates scatter plots of sentiment vs. like, quote, and repost counts with regression lines.
    """
    metrics = ['like_count', 'quote_count', 'repost_count']
    for metric in metrics:
        sns.lmplot(data=df, x='sentiment', y=metric, height=5, aspect=1.5, ci=None)
        plt.title(f'Sentiment vs. {metric.replace("_", " ").title()}')
        plt.xlabel('Sentiment')
        plt.ylabel(metric.replace('_', ' ').title())
        plt.show()


def compute_summary_statistics(df):
    """
    Computes mean engagement and other summary statistics for toxic vs. non-toxic posts.
    """
    df['engagement'] = df['like_count'] + df['quote_count'] + df['repost_count']
    summary = df.groupby('toxic')['engagement'].agg(['mean', 'median', 'std', 'count'])
    print("Summary Statistics for Engagement by Toxicity:")
    print(summary)
    return summary


def perform_t_test(df):
    """
    Performs a t-test between toxic and non-toxic posts on engagement.
    """
    df['engagement'] = df['like_count'] + df['quote_count'] + df['repost_count']
    toxic_engagement = df[df['toxic'] == 1]['engagement']
    non_toxic_engagement = df[df['toxic'] == 0]['engagement']
    t_stat, p_value = ttest_ind(toxic_engagement, non_toxic_engagement, equal_var=False)
    print(f"T-Test Results:\nT-Statistic: {t_stat}, P-Value: {p_value}")
    return t_stat, p_value


def load_df(csv_path, toxic_threshold=-0.95):
    try:
        # Load the CSV into a DataFrame
        df = pd.read_csv(csv_path)
        df['toxic'] = df['sentiment'] < toxic_threshold
        return df
    except FileNotFoundError:
        print(f"File not found: {csv_path}")
    except Exception as e:
        print(f"An error occurred: {e}")


def interaction_regression(twitter_df, bluesky_df):
    """
    :param twitter_df: twitter dataframe, should have toxic and sentiment cols
    :param bluesky_df: bluesky dataframe, shoudl have toxic and sentiment cols
    :return: beta_0, beta_1, beta_2, beta_3, and t: test statistic for beta_3, and p-value of t
    """
    return


def main():
    parser = argparse.ArgumentParser(description="Analyze Twitter and Bluesky sentiment data.")
    parser.add_argument("--csv_path", type=str, default="./datasets/asian_10000_20241128_012508.csv", help="Path to the CSV file containing the dataset.")
    parser.add_argument("--threshold", type=float, default=-0.95, help="Threshold for determining toxicity based on sentiment.")
    args = parser.parse_args()

    # Load data
    df = load_df(args.csv_path, args.threshold)

    if df is not None:
        # Perform analysis
        visualize_engagement_boxplot(df)
        scatter_with_regression(df)
        compute_summary_statistics(df)
        perform_t_test(df)


if __name__ == "__main__":
    main()
