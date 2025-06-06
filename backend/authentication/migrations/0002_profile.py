# Generated by Django 3.0.5 on 2025-05-20 04:25

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('authentication', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=255)),
                ('height', models.FloatField(blank=True, help_text='Height in cm', null=True)),
                ('weight', models.FloatField(blank=True, help_text='Weight in kg', null=True)),
                ('age', models.PositiveIntegerField(blank=True, null=True)),
                ('gender', models.CharField(blank=True, choices=[('male', 'Male'), ('female', 'Female'), ('other', 'Other'), ('prefer_not_to_say', 'Prefer not to say')], max_length=20, null=True)),
                ('fitness_goal', models.CharField(blank=True, choices=[('weight_loss', 'Weight Loss'), ('muscle_gain', 'Muscle Gain'), ('endurance', 'Endurance'), ('general_fitness', 'General Fitness'), ('other', 'Other')], max_length=50, null=True)),
                ('activity_level', models.CharField(blank=True, choices=[('sedentary', 'Sedentary'), ('lightly_active', 'Lightly Active'), ('moderately_active', 'Moderately Active'), ('very_active', 'Very Active'), ('extremely_active', 'Extremely Active')], max_length=50, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
