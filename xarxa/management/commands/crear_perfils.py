from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone
from faker import Faker
from datetime import timedelta
from random import randint
import datetime

from ...models import *

faker = Faker(["es_ES"])

class Command(BaseCommand):
    help = "Crea perfils N perfils (indicat per paràmetre) amb posts, comentaris i notificacions, i afegeix relacions de seguiment de forma aleatòria."
    def add_arguments(self, parser):
        parser.add_argument(
            "num_profiles",
            type=int,
            help="Nombre de perfils a crear.",
        )
    def handle(self, *args, **options):
        num_profiles = options["num_profiles"]
        if num_profiles <= 0:
            raise CommandError("El nombre de perfils ha de ser un nombre positiu.")

        added_users = []

        for _ in range(num_profiles):
            username = faker.user_name()
            email = faker.email()
            password = faker.password()
            profile_picture = faker.image_url(width=200, height=200)
            location = faker.city()
            bio = faker.text(max_nb_chars=200)
            user = User.objects.create_user(username=username, email=email, password=password)
            user.first_name = faker.first_name()
            user.last_name = faker.last_name()
            user.date_joined = timezone.now() - timedelta(days=randint(1, 365))  # Usuari creat en el darrer any
            user.save()

            profile = None
            ## sqlite3.IntegrityError: UNIQUE constraint failed: xarxa_profile.user_id
            if Profile.objects.filter(user=user).exists():
              profile = user.profile
              profile.bio = bio
              profile.profile_picture = profile_picture
              profile.location = location
              profile.save()
            else:
              profile = Profile.objects.create(user=user, bio=bio, profile_picture=profile_picture, location=location)


            # Crear posts
            for _ in range(randint(1, 5)):
                content = faker.sentence(nb_words=randint(5, 30))
                Post.objects.create(author=user, content=content)

            # Crear comentaris
            posts = Post.objects.filter(author=user)
            for post in posts:
                for _ in range(randint(0, 3)):
                    text = faker.sentence(nb_words=randint(5, 20))
                    Comment.objects.create(post=post, author=user, text=text)

            # Crear notificacions
            for _ in range(randint(0, 3)):
                notification_type = faker.random_element(Notification.NOTIFICATION_TYPES)[0]
                Notification.objects.create(
                    to_user=user,
                    from_user=faker.random_element(User.objects.all()),
                    post=faker.random_element(posts),
                    notification_type=notification_type,
                )
            added_users.append(user)

        for user in added_users:
            # Afegir relacions de seguiment aleatòries
            all_users = User.objects.exclude(id=user.id)
            for _ in range(randint(0, 5)):
                follower = faker.random_element(all_users)
                if follower != user and not profile.followers.filter(id=follower.id).exists():
                    profile.followers.add(follower)

        self.stdout.write(self.style.SUCCESS(f"{num_profiles} perfils creats amb èxit."))
