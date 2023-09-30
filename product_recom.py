import pandas as pd
import random

# Create a mock movie dataset
movie_data = {
'MovieID': range(1, 21),
'Title': ['Movie {}'.format(i) for i in range(1, 21)],
'Genre': [random.choice(['Action', 'Comedy', 'Drama', 'Sci-Fi']) for _ in range(20)],
'Popularity': [random.randint(1, 100) for _ in range(20)]  # Add popularity values here
}

movie_df = pd.DataFrame(movie_data)
movie_df.set_index('MovieID', inplace=True)

# Create a mock user-movie interaction dataset
user_data = {
'UserID': range(1, 11),
'MovieIDs': [random.sample(range(1, 21), 5) for _ in range(10)]
}

user_df = pd.DataFrame(user_data)
user_df.set_index('UserID', inplace=True)

from deap import creator, tools, algorithms, base

# Create fitness and individual classes
creator.create("FitnessMulti", base.Fitness, weights=(1.0, 1.0, 1.0, -1.0))
creator.create("Individual", list, fitness=creator.FitnessMulti)

# Define the toolbox with genetic operators
toolbox = base.Toolbox()

# Define the movie recommendation as an individual (a list of MovieIDs)

toolbox.register("movie", random.sample, range(1, 21), 5)
toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.movie, n=1)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)

# Define the evaluation function (fitness function)

def calculate_user_satisfaction(user_df, movie_df, movie_ids):
    """
    Calculate user satisfaction based on the selected movie recommendations.

    Parameters:
    - user_df: DataFrame containing user data.
    - movie_df: DataFrame containing movie data.
    - movie_ids: List of recommended movie IDs.

    Returns:
    - user_satisfaction: User satisfaction score.
    """
    user_satisfaction = 0.0

    # Calculate user satisfaction based on user-movie interactions and movie properties
    for user_id, row in user_df.iterrows():
        user_movie_ids = row['MovieIDs']
        intersection = len(set(user_movie_ids).intersection(movie_ids))
        user_satisfaction += intersection / len(user_movie_ids)

    return user_satisfaction

def calculate_diversity(movie_df, movie_ids):
    """
    Calculate diversity of movie recommendations.

    Parameters:
    - movie_df: DataFrame containing movie data.
    - movie_ids: List of recommended movie IDs.

    Returns:
    - diversity: Diversity score.
    """
    diversity = 0.0

    # Calculate diversity based on movie properties (e.g., genre)
    selected_genres = movie_df.loc[movie_ids]['Genre']
    unique_genres = set(selected_genres)
    diversity = len(unique_genres) / len(movie_ids)

    return diversity

def calculate_novelty(user_df, movie_ids):
    """
    Calculate novelty of movie recommendations.

    Parameters:
    - user_df: DataFrame containing user data.
    - movie_ids: List of recommended movie IDs.

    Returns:
    - novelty: Novelty score.
    """
    novelty = 0.0

    # Calculate novelty based on the popularity of recommended movies
    total_movie_popularity = movie_df['Popularity'].sum()  # You should have a 'Popularity' column in your movie_df
    selected_movie_popularity = movie_df.loc[movie_ids]['Popularity'].sum()
    novelty = 1.0 - (selected_movie_popularity / total_movie_popularity)

    return novelty

def calculate_accuracy(user_df, movie_df, movie_ids):
    """
    Calculate accuracy of movie recommendations.

    Parameters:
    - user_df: DataFrame containing user data.
    - movie_df: DataFrame containing movie data.
    - movie_ids: List of recommended movie IDs.

    Returns:
    - accuracy: Accuracy score.
    """
    accuracy = 0.0

    # Calculate accuracy based on user-movie interactions and movie properties
    for user_id, row in user_df.iterrows():
        user_movie_ids = row['MovieIDs']
        intersection = len(set(user_movie_ids).intersection(movie_ids))
        accuracy += intersection / len(movie_ids)

    return accuracy
def evaluate(individual):
    movie_ids = individual[0]

    # Calculate user satisfaction, diversity, novelty, and accuracy based on movie_ids

    user_satisfaction = calculate_user_satisfaction(user_df, movie_df, movie_ids)
    diversity = calculate_diversity(movie_df, movie_ids)
    novelty = calculate_novelty(user_df, movie_ids)
    accuracy = calculate_accuracy(user_df, movie_df, movie_ids)

    return user_satisfaction, diversity, novelty, accuracy

toolbox.register("evaluate", evaluate)
toolbox.register("mate", tools.cxBlend, alpha=0.5)
toolbox.register("mutate", tools.mutShuffleIndexes, indpb=0.2)
toolbox.register("select", tools.selNSGA2)

if __name__ == "__main__":
    # Create a population of recommendations
    population = toolbox.population(n=100)
    # population = [toolbox.individual() for _ in range(100)]

    # Run NSGA-II

    algorithms.eaMuPlusLambda(population, toolbox, mu=50, lambda_=100, cxpb=0.7, mutpb=0.2, ngen=50, stats=None,
                              halloffame=None, verbose=True)

    # Extract the Pareto front solutions
    pareto_front = tools.sortNondominated(population, len(population), first_front_only=True)[0]

    # Print the Pareto front solutions
    for ind in pareto_front:
        print("User Satisfaction:", ind.fitness.values[0])
        print("Diversity:", ind.fitness.values[1])
        print("Novelty:", ind.fitness.values[2])
        print("Accuracy:", ind.fitness.values[3])
        print("Recommended Movie IDs:", ind[0])
        print()

