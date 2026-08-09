from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('fuelrequests', '0007_fuelrequests_tags'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='fuelrequests',
            name='tags',
        ),
    ]