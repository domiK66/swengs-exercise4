# Today's exercise
1. Download yamod 0.6 from Moodle and replace installation from last time
2. Implement test class ExtendedQueryTests
3. Implement test class MigrationTests
4. Develop your own models covering TV shows, seasons and episodes
5. Write your own tests
6. Optional: extend django admin for the new models + write a custom data migration

# Setup Steps
1. Create a virtual environment
2. Activate the virtual environment
3. Install Django in this virtual environment
4. Create a fresh Django project
5. Unzip the yamod app into the Django project folder
6. Add yamod to INSTALLED_APPS in settings.py
7. Run python manage.py migrate (will add yamod's database tables)
8. Open yamod/tests.py and implement the test methods testing insert/update/deletes on the yamod models
9. run python manage.py test in your project to see, if your tests work