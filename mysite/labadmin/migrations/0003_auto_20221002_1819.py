# Generated by Django 3.2.15 on 2022-10-02 12:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('labadmin', '0002_remove_patient_testpres'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='appointment',
            name='testpres',
        ),
        migrations.RemoveField(
            model_name='feedback',
            name='customer',
        ),
        migrations.RemoveField(
            model_name='slot',
            name='astrength',
        ),
        migrations.RemoveField(
            model_name='slot',
            name='status',
        ),
        migrations.RemoveField(
            model_name='slot',
            name='time',
        ),
        migrations.AddField(
            model_name='appointment',
            name='compstatus',
            field=models.CharField(default='begin', max_length=20),
        ),
        migrations.AddField(
            model_name='feedback',
            name='email',
            field=models.EmailField(default='rghanasyam9@gmail.com', max_length=254),
        ),
        migrations.AddField(
            model_name='feedback',
            name='name',
            field=models.CharField(default='shyam', max_length=25),
        ),
        migrations.AddField(
            model_name='feedback',
            name='subject',
            field=models.CharField(default='general', max_length=25),
        ),
        migrations.AddField(
            model_name='slot',
            name='end',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='slot',
            name='start',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='slot',
            name='t1',
            field=models.CharField(default='AM', max_length=5),
        ),
        migrations.AddField(
            model_name='slot',
            name='t2',
            field=models.CharField(default='AM', max_length=5),
        ),
        migrations.AlterField(
            model_name='feedback',
            name='message',
            field=models.CharField(max_length=100),
        ),
        migrations.CreateModel(
            name='Day',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('start', models.PositiveIntegerField(default=0)),
                ('end', models.PositiveIntegerField(default=0)),
                ('t1', models.CharField(max_length=5)),
                ('t2', models.CharField(max_length=5)),
                ('strength', models.PositiveIntegerField(default=0)),
                ('astrength', models.PositiveIntegerField(default=0)),
                ('status', models.CharField(max_length=15)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='labadmin.category')),
            ],
        ),
    ]
