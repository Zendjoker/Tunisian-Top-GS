# Generated by Django 5.0.2 on 2024-06-09 20:52

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Rank',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, unique=True)),
                ('icon', models.ImageField(default='default_tag_image.png', upload_to='ranks_icons')),
                ('points', models.IntegerField(default=0)),
            ],
        ),
    ]
