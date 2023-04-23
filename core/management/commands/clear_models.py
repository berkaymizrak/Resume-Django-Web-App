import time
from django.core.management.base import BaseCommand, CommandError
from .utils import Progress
from core import models as core_models
from frontend import models as fr_models
from user import models as user_models

clear_models = [
    core_models.GeneralSetting,
    core_models.ImageSetting,
    core_models.Document,
    core_models.Message,
    fr_models.Skill,
    fr_models.SocialMedia,
]


class Command(BaseCommand):
    help = 'Clear all data in showed models. This command is generated for example of usage of colorful Django management command.'

    def handle(self, *args, **options):
        self.stdout.write(self.style.MIGRATE_HEADING(
            "\nThis command will clear all models' data."
            "\nThe models that is going to be affected:"
        ))
        for model in clear_models:
            self.stdout.write(self.style.SUCCESS(model.__name__))
        self.stdout.write(self.style.WARNING(
            "You may prefer run this command at your local with a copy of this DB then insert django dump to production.\n"
        ))
        r = input("Would you like to continue? (y/N): ")
        if r not in ("y", "Y"):
            raise CommandError("Command exited.")

        for model in clear_models:
            self.clear_model_data(model)

        self.stdout.write(self.style.HTTP_SERVER_ERROR("\nCleaning is completed!\n"))

    def clear_model_data(self, django_model):
        # Progress parameters for user-friendly progressbar:
        count = 0
        progress = Progress()
        now = time.time()
        objs_count = django_model.objects.count()
        time.sleep(0.1)

        # Loop in queryset:
        all_objs = django_model.objects.all()
        self.stdout.write(self.style.HTTP_SERVER_ERROR("\nCleaning starting for: %s" % django_model.__name__))
        for enum, obj in enumerate(all_objs):
            count += 1
            progress.progress(enum + 1, objs_count, now, self, message='In progress... %s object(s) deleted.' % count)

            obj.delete()

        """
        This process can be just done with:
        
        >> python manage.py flush
        
        OR:
        
        >> django_model.objects.all().delete()
        
        However this command is created only for example of usage of Progress and Django management command.
        """

        self.stdout.write(self.style.SUCCESS(
            "Cleaning completed for %s. Affected number of data: %s" % (django_model.__name__, count)
        ))
