# Generated by Django 2.2.6 on 2020-03-22 11:59

import core.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0011_update_proxy_permissions'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('email', models.EmailField(max_length=255, unique=True)),
                ('slug', models.SlugField(blank=True, default='', max_length=255, null=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='InsertUpdate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Inserted_On', models.DateTimeField(default=django.utils.timezone.now)),
                ('Updated_On', models.DateTimeField(blank=True, null=True)),
                ('Inserted_By', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='inserted_byy', to=settings.AUTH_USER_MODEL)),
                ('Updated_By', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='updated_byy', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='SetupTable',
            fields=[
                ('insertupdate_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='core.InsertUpdate')),
                ('Name', models.CharField(max_length=255)),
                ('Description', models.TextField(max_length=500)),
                ('Is_Active', models.BooleanField(default=True)),
                ('System_Used', models.BooleanField(default=False)),
            ],
            bases=('core.insertupdate', models.Model),
        ),
        migrations.CreateModel(
            name='AddressType',
            fields=[
                ('setuptable_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='core.SetupTable')),
            ],
            bases=('core.setuptable',),
        ),
        migrations.CreateModel(
            name='City',
            fields=[
                ('setuptable_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='core.SetupTable')),
            ],
            options={
                'verbose_name_plural': 'Cities',
            },
            bases=('core.setuptable',),
        ),
        migrations.CreateModel(
            name='Country',
            fields=[
                ('setuptable_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='core.SetupTable')),
            ],
            options={
                'verbose_name_plural': 'Countries',
            },
            bases=('core.setuptable',),
        ),
        migrations.CreateModel(
            name='Gender',
            fields=[
                ('setuptable_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='core.SetupTable')),
            ],
            bases=('core.setuptable',),
        ),
        migrations.CreateModel(
            name='ProfileStatus',
            fields=[
                ('setuptable_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='core.SetupTable')),
            ],
            options={
                'verbose_name_plural': 'Profile Statuses',
            },
            bases=('core.setuptable',),
        ),
        migrations.CreateModel(
            name='UserType',
            fields=[
                ('setuptable_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='core.SetupTable')),
            ],
            bases=('core.setuptable',),
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('insertupdate_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='core.InsertUpdate')),
                ('Full_Name', models.CharField(max_length=50)),
                ('CNIC', models.BigIntegerField(blank=True, null=True)),
                ('DOB', models.DateField(blank=True, null=True)),
                ('contact', models.BigIntegerField(blank=True, null=True)),
                ('other_contacts', models.TextField(blank=True, max_length=1000, null=True)),
                ('Shop_Name', models.CharField(blank=True, max_length=255, null=True)),
                ('WhatsApp', models.BooleanField(default=False)),
                ('image', models.ImageField(default='pics_default/default_user.png', upload_to=core.models.profile_image_file_path)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('Address_Types', models.ManyToManyField(blank=True, to='core.AddressType')),
                ('Profile_Status', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='core.ProfileStatus')),
                ('User_Type', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='core.UserType')),
                ('city', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='core.City')),
                ('country', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='core.Country')),
                ('gender', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='profile_gender', to='core.Gender')),
            ],
            bases=('core.insertupdate', models.Model),
        ),
        migrations.AddField(
            model_name='city',
            name='countryy',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='city', to='core.Country'),
        ),
    ]
