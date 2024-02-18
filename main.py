import pandas as pd
from traceback import print_exc
from random import uniform
from time import perf_counter
from typing import List

def transform_scores(score: str):
    try:
        # If data is a number we return the number
        return float(score)
    except ValueError:
        if '–' in score:
            # Some data is in format n–m so we put in that cell an average of n and m
            lower_score, upper_score = map(float, score.split('–'))

            return lower_score + upper_score / 2
        else:
            # If data cannot be transformed to number just return it
            return score

def get_overall_scores_data(file_path: str) -> pd.Series:
    universities_df = pd.read_csv(file_path)

    # As we need only one column, we use Pandas Series
    overall_scores_column = universities_df['Overall scores'].astype(str)

    # Transform values to numbers if possible 
    overall_scores = overall_scores_column.apply(transform_scores)

    # Convert values to numeric, coerce non-numeric values to NaN
    overall_scores = pd.to_numeric(overall_scores, errors='coerce')

    # Drop NaN values
    numeric_values = overall_scores.dropna()

    # Calculate mean of numeric values
    mean = numeric_values.mean()

    # Fill NaN values with mean 
    overall_scores.fillna(value=mean, inplace=True)

    return overall_scores


def fractional_interval_method(data: pd.Series, n: int):
    N = len(data)

    a = N / n

    alpha = uniform(1.0, a)

    sample = [data[int(alpha + i * a)] for i in range(n)]

    return sample

if __name__ == '__main__':
    try:
        overall_scores = get_overall_scores_data('./data/universities_data.csv')

        m = 10

        n = 5

        sample_len = max(1, int(len(overall_scores) * n / 100))

        samples = []

        method_work_time = 0

        for i in range(m):
            if i:
                sample = fractional_interval_method(overall_scores, sample_len)
            else:
                # Calculate method work time
                start_time = perf_counter()

                sample = fractional_interval_method(overall_scores, sample_len)

                end_time = perf_counter()

                method_work_time = end_time - start_time

            samples.append(pd.Series(sample))

        general_mean = overall_scores.mean()

        sample_means = [sample.mean() for sample in samples]

        samples_std = pd.concat(samples).std()

        print(f'General mean: {general_mean}')
        print(f'Sample means: {sample_means}')
        print(f'Samples std: {samples_std}')
    except Exception as e:
        print('Error occurred:')
        print_exc()