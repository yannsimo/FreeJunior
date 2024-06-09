# Generated by Django 5.0.6 on 2024-06-02 15:29

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('FreeJuniorapp1', '0002_rename_first_name_student_nom_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Program',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='School',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Specialty',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.RenameField(
            model_name='student',
            old_name='Nom',
            new_name='first_name',
        ),
        migrations.RenameField(
            model_name='student',
            old_name='Prenom',
            new_name='last_name',
        ),
        migrations.RemoveField(
            model_name='student',
            name='description',
        ),
        migrations.RemoveField(
            model_name='student',
            name='photo',
        ),
        migrations.AddField(
            model_name='student',
            name='email',
            field=models.EmailField(max_length=254, null=True, unique=True),
        ),
        migrations.AddField(
            model_name='student',
            name='hourly_rate',
            field=models.DecimalField(decimal_places=2, max_digits=6, null=True),
        ),
        migrations.AddField(
            model_name='student',
            name='study_level',
            field=models.CharField(choices=[('Bac+1', 'Bac+1'), ('Bac+2', 'Bac+2'), ('Bac+3', 'Bac+3'), ('Bac+4', 'Bac+4'), ('Bac+5', 'Bac+5'), ('Bac+6', 'Bac+6'), ('Bac+7', 'Bac+7')], max_length=5, null=True),
        ),
        migrations.AlterField(
            model_name='mission',
            name='company',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='missions', to='FreeJuniorapp1.company'),
        ),
        migrations.AlterField(
            model_name='mission',
            name='student',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='missions', to='FreeJuniorapp1.student'),
        ),
        migrations.AddField(
            model_name='student',
            name='program',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='students', to='FreeJuniorapp1.program'),
        ),
        migrations.AddField(
            model_name='program',
            name='school',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='programs', to='FreeJuniorapp1.school'),
        ),
        migrations.AddField(
            model_name='student',
            name='school',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='students', to='FreeJuniorapp1.school'),
        ),
        migrations.AddField(
            model_name='student',
            name='specialty',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='FreeJuniorapp1.specialty'),
        ),
        migrations.CreateModel(
            name='StudentCV',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cv', models.FileField(blank=True, null=True, upload_to='student_cvs/')),
                ('student', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='cv', to='FreeJuniorapp1.student')),
            ],
        ),
        migrations.CreateModel(
            name='StudentDescription',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField()),
                ('student', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='description', to='FreeJuniorapp1.student')),
            ],
        ),
        migrations.CreateModel(
            name='StudentPhoto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('photo', models.ImageField(upload_to='student_photos/')),
                ('student', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='photo', to='FreeJuniorapp1.student')),
            ],
        ),
        migrations.CreateModel(
            name='Subject',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('program', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subjects', to='FreeJuniorapp1.program')),
            ],
        ),
        migrations.AddField(
            model_name='student',
            name='related_subject',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='FreeJuniorapp1.subject'),
        ),
    ]
