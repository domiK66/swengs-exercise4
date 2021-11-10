import datetime
from typing import cast

from django.test import TestCase
from . import models

class YamodBaseTest(TestCase):

    def setUp(self):
        self.genres=["Action","Horror","Scifi","Drama","Comedy"]
        self.movies = [
            ("Blade Runner", datetime.date(year=1982,month=6,day=25),"Scifi",100),
            ("Blade Runner 2049", datetime.date(year=2017,month=10,day=6),"Scifi",150),
            ("Nomadland", datetime.date(year=2020,month=9,day=11),"Drama",110),
            ("The French Dispatch", datetime.date(year=2021,month=7,day=12),"Comedy",100),
            ("Rushmoore", datetime.date(year=1998,month=9,day=17),"Comedy",95)
        ]
        # Setup database
        [models.Genre.objects.create(name=name) for name in self.genres]
        [models.RoleType.objects.create(name=name) for name in ["Actor","Producer","Director"]]
        [models.Movie.objects.create(movie_title=movie_title,
                                     released=released,
                                     original_title=movie_title,
                                     runtime=runtime) for movie_title,released, genre,runtime in self.movies]    
        # Updates
        for movie_title,released, genre,runtime in self.movies:
            models.Movie.objects.get(movie_title=movie_title).genre.add(models.Genre.objects.get(name=genre))


class YamodModelTest(YamodBaseTest):

    def test_create_genre(self):
        # Create a new model instance for model "Genre" with name "Comedy"
        # YOUR CODE HERE:
        genre = models.Genre.objects.create(name="Comedy")
        # /ENDYOURCODE
        self.assertEqual(genre.name,"Comedy")

    def test_delete_genre(self):
        # YOUR CODE HERE: Delete Genre instance with name "Action"
        models.Genre.objects.filter(name="Action").delete()
        # /ENDYOURCODE
        self.assertEqual(models.Genre.objects.count(),4)

    def test_filter_movie_by_year(self):
        # Filter all movies, that were released after 2000 (store results of query in variable movies_2000)
        # YOUR CODE HERE:
        movies_2000 = models.Movie.objects.filter(released__year__gte=2000)
        # /ENDYOURCODE        
        self.assertEqual(movies_2000.count(),3)

    def test_filter_movie_by_runtime(self):
        # Filter all movies with a runtime <= 100 (FIXED: runtime < 100)
        # YOUR CODE HERE:
        movies_90 = models.Movie.objects.filter(runtime__lte=100)
        # /ENDYOURCODE
        self.assertEqual(movies_90.count(),3)

    def test_filter_movie_starting_with_b(self):
        # Filter all movies that start with letter B
        # YOUR CODE HERE:
        movies_with_b = models.Movie.objects.filter(movie_title__startswith="B")
        # /ENDYOURCODE
        self.assertEqual(movies_with_b.count(),2)

    def test_filter_movie_containing_blade(self):
        # Filter all movies that contain "Blade" in its title
        # YOUR CODE HERE:
        movies_containing_blade = models.Movie.objects.filter(movie_title__contains="Blade")
        # /ENDYOURCODE
        self.assertEqual(movies_containing_blade.count(),2)

    def test_genre_to_str(self):        
        # Implement the __str__ method of model class Genre and Movie
        # Genre should return the name and Movie should return the movie_title
        # (Implementation is done in models.py)
        for movie_title,released,genre,runtime in self.movies:
            self.assertEqual(str(models.Movie.objects.get(movie_title=movie_title)),movie_title)


    def test_update_role_type(self):
        # Load the model instance "Actor" of model "RoleType"
        # and update the name of the RoleType to "Actor/Actress"
        # YOUR CODE HERE:
        actor = models.RoleType.objects.get(name="Actor")
        actor.name="Actor/Actress"
        actor.save()
        # /ENDYOURCODE
        self.assertEqual(models.RoleType.objects.filter(name="Actor/Actress").count(),1)

    def test_get_or_create_role_type(self):
        # The following call results in an error, as a role type "Producer"
        # already exists. Modify the "create" method accordingly, so this 
        # test can pass
        # MODIFY CODE HERE
        models.RoleType.objects.get_or_create(name="Producer")
        # /ENDYOURCODE
        self.assertEqual(models.RoleType.objects.count(),3)
        self.assertEqual(models.RoleType.objects.filter(name="Producer").count(),1)

class ExtendedQueryTests(YamodBaseTest):

    def test_and_query(self):
        # Filter all movies where the name starts with a B
        # AND that were released after 1980
        # YOUR CODE HERE:
        movies_with_b_after_1980 = models.Movie.objects.filter(movie_title__startswith="B", released__year__gte=1980)
        # /ENDYOURCODE
        self.assertEqual(movies_with_b_after_1980.count(),2)

    def test_or_query(self):
        # Filter all movies that were released after 2020 OR have genre comedy
        # YOUR CODE HERE:
        from django.db.models import Q
        movies = models.Movie.objects.filter(Q(genre__name="Comedy") | Q(released__year__gt=2020))
        # /ENDYOURCODE
        self.assertEqual(movies.count(),2)

    def test_filter_relation(self):
        # Filter all movies where the genre ends with character "y"
        # YOUR CODE HERE:
        results = models.Movie.objects.filter(genre__name__endswith="y")
        # /ENDYOURCODE
        self.assertEquals(results.count(),2)

    def test_add_persons_to_movie(self):
        # Go to Wikipedia and select (a) the director and (b) 
        # the lead actor of "Blade runner 2049".
        # Create two person model instances and add them to the 
        # movie "Blade runner 2049"
        #
        # Note: the model class "Person" has a many-to-many relation 
        # with model class "Movie"; Unlike the many-to-many relation 
        # Movie --> Genre, it uses an intermediate relation "Role".
        # The reason is: we need to provide more information on what
        # a person has actually done in a movie which is expressed through
        # the intermediate model "Role" - the intermediate role is provided 
        # through the "through" argument in
        #
        # participates_in = models.ManyToManyField(Movie,through="Role")
        #
        # In this case, you cannot use the person.participates_in.add method 
        # as we have seen on the slides in the genre case. You have to create 
        # the model instances using their respective .objects.create method.
        #
        # YOUR CODE HERE:
        movie1 = models.Movie.objects.get(movie_title="Blade Runner 2049")
        director = 	models.Person.objects.create(credited_name="Denis Villeneuve",year_of_birth=1967,gender="M")
        lead_actor = models.Person.objects.create(credited_name="Ryan Gosling",year_of_birth=1967,gender="M")
        models.Role.objects.create(person=director, movie=movie1, role=models.RoleType.objects.get(name="Director"))
        models.Role.objects.create(person=lead_actor, movie=movie1, role=models.RoleType.objects.get(name="Actor"))
        # /ENDYOURCODE      
        self.assertEqual(director.participates_in.all().count(),1)
        self.assertEqual(lead_actor.participates_in.all().count(),1)

class MigrationTests(YamodBaseTest):
    '''
    The goal of these tests, is to practice the use of the migrations 
    concept of Django. 
    
    Extend the data model of models.py to include the concept of 
    TV shows. The data model should at least provide models for 

    - TV shows (should have at least a title and a release date)
    - Seasons (should provide the possibility to add a regular cast referencing the Person model)
    - Episodes (should have at least a title and a length in minutes)

    and appropriate relations between them. Develop iterativley, 
    thus extend the data model one by one (always running 
    migrations between them) and implement the following test. 

    You can add further relations (e.g. tv shows and seasons 
    might have a link to genres) as you see fit.

    Optional: try to write a custom data migration (see slides)
    that populates the development databases with following pre-defined 
    list of genres:

    ["Action","Horror","Scifi","Drama","Comedy"]    

    Optional: add custom django admin classes for the newly generated 
    models TV shows, seasons and episodes.

    '''

    def test_tv_show(self):
        '''
        Go to models.py and create a new model "TVShow". 
        Write appropriate tests that show case how a new 
        model instance ist created, updated and deleted.
        '''
        tv_show = models.TvShow.objects.create(title="South Park",released = "1998-01-01")
        self.assertEqual(tv_show.title,"South Park")
        self.assertEqual(tv_show.released,"1998-01-01")

        tv_show.title="South Park Extreme"
        tv_show.save()
        self.assertEqual(models.TvShow.objects.filter(title="South Park Extreme").count(),1)

        models.TvShow.objects.filter(title="South Park Extreme",released = "1998-01-01").delete()
        self.assertEqual(models.TvShow.objects.count(),0)

        
    def test_tv_show_season(self):
        '''
        Go to models.py and create a new model "Season".
        Write appropriate tests that show case how a new 
        model instance ist created, updated and deleted.        
        '''
        tv_show1 = models.TvShow.objects.create(title="South Park", released = "1998-01-01")

        person1 = models.Person.objects.create(credited_name="Kenny", year_of_birth=1967, gender="M")
        person2 = models.Person.objects.create(credited_name="Cartman", year_of_birth=1967, gender="M")
        season1 = models.Season.objects.create(number=1, tv_show=tv_show1)
        season1.cast.add(person1)
        season1.cast.add(person2)
        self.assertEqual(season1.cast.count(), 2)

        season2 =  models.Season.objects.get(tv_show=tv_show1)
        season2.number = 2
        season2.save()
        self.assertEqual(models.Season.objects.get(tv_show=tv_show1).number, 2)

        models.Season.objects.get(tv_show=tv_show1).delete()
        self.assertEqual(models.Season.objects.count(),0)


    def test_tv_show_episode(self):
        '''
        Go to models.py and create a new model "Episode".
        Write appropriate tests that show case how a new 
        model instance ist created, updated and deleted.        
        '''
        
        

    