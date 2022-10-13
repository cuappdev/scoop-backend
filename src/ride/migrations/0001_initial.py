
# Generated by Django 4.0.2 on 2022-09-21 21:52


from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('path', '0001_initial'),
        ('person', '0002_person_profile_pic_url'),
    ]

    operations = [
        migrations.CreateModel(
            name='Ride',
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("max_travelers", models.IntegerField(default=1)),
                ("min_travelers", models.IntegerField(default=1)),
                ("departure_datetime", models.DateTimeField()),
                ("description", models.TextField(default=None, null=True)),
                ("is_flexible", models.BooleanField(default=False)),
                ("estimated_cost", models.FloatField(default=None, null=True)),
                (
                    "type",
                    models.CharField(
                        choices=[
                            ("rideshare", "Rideshare"),
                            ("studentdriver", "Student Driver"),
                        ],
                        max_length=20,
                    ),
                ),
                (
                    "creator",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="creator",
                        to="person.person",
                    ),
                ),
                (
                    "driver",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="driver",
                        to="person.person",
                    ),
                ),
                (
                    "path",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="path.path"
                    ),
                ),
                ("riders", models.ManyToManyField(to="person.Person")),
            ],
        ),
    ]
