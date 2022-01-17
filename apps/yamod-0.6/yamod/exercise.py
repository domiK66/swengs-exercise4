from . import models

def create_genre():
    # Create a new model instance for model "Genre" with name "Comedy"
    # YOUR CODE HERE:
    genre = models.Genre.objects.create(name = "Comedy")
    # /ENDYOURCODE
    return genre

def delete_genre():
    # Delete Genre instance with name "Action"
    # YOUR CODE HERE: 
    genre = models.Genre.objects.filter(name = "Action").delete()
    # /ENDYOURCODE

def filter_movie_by_year():
    # Filter all movies, that were released after 2000 (store results of query in variable movies_2000)
    # YOUR CODE HERE:
    movies_2000 = models.Movie.objects.filter(released__gt = "2000-01-01")
    # /ENDYOURCODE        
    return movies_2000

def filter_movie_by_runtime():
    # Filter all movies with a runtime < 100
    # YOUR CODE HERE:
    movies_90 = models.Movie.objects.filter(runtime__lte = 100)
    # /ENDYOURCODE
    return movies_90

def filter_movie_starting_with_b():
    # Filter all movies that start with letter B
    # YOUR CODE HERE:
    movies_with_b = models.Movie.objects.filter(movie_title__startswith = "B")
    # /ENDYOURCODE
    return movies_with_b

def filter_movie_containing_blade():
    # Filter all movies that contain "Blade" in its title
    # YOUR CODE HERE:
    movies_containing_blade = models.Movie.objects.filter(movie_title__contains = "Blade")
    # /ENDYOURCODE
    return movies_containing_blade
     
# Implement the __str__ method of model class Genre and Movie
# Genre should return the name and Movie should return the movie_title
# (Implementation is done in models.py)
    
def update_role_type():
    # Load the model instance "Actor" of model "RoleType"
    # and update the name of the RoleType to "Actor/Actress"
    # YOUR CODE HERE:
    actor = models.RoleType.objects.get(name = "Actor")
    actor.name="Actor/Actress"
    actor.save()
    # /ENDYOURCODE


def get_or_create_role_type():
    # The following call results in an error, as a role type "Producer"
    # already exists. Modify the "create" method accordingly, so this 
    # test can pass
    # MODIFY CODE HERE
    models.RoleType.objects.get_or_create(name = "Producer")
    # /ENDYOURCODE
    
    
# EXERCISE 4
def test_and_query():
    # Filter all movies where the name starts with a B
    # AND that were released after 1980
    # YOUR CODE HERE:
    movies_with_b_after_1980 = models.Movie.objects.filter(movie_title__startswith="B", released__year__gte=1980)
    # /ENDYOURCODE
    return movies_with_b_after_1980

def test_or_query():
    # Filter all movies that were released after 2020 OR have genre comedy
    # YOUR CODE HERE:
    from django.db.models import Q
    movies = models.Movie.objects.filter(Q(genre__name="Comedy") | Q(released__year__gt=2020))
    # /ENDYOURCODE
    return movies
