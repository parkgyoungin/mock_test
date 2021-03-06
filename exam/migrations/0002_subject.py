# Generated by Django 2.2.4 on 2019-08-16 03:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('exam', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Subject',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order', models.PositiveIntegerField()),
                ('name', models.CharField(max_length=50)),
                ('certificate', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subjects', to='exam.Certificate')),
            ],
        ),
    ]
