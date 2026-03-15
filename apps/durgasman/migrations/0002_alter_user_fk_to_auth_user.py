# Migrate FK from core.User (users table) to auth.User (auth_user) before core.0004_delete_user

from django.db import migrations, models
import django.db.models.deletion


def null_user_fks(apps, schema_editor):
    """Set user_id to NULL so we can alter FK to auth.User (old ids pointed to core users)."""
    from django.db import connection
    with connection.cursor() as c:
        c.execute("UPDATE durgasman_collection SET user_id = NULL")
        c.execute("UPDATE durgasman_environment SET user_id = NULL")
        c.execute("UPDATE durgasman_requesthistory SET user_id = NULL")


def noop(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('durgasman', '0001_initial'),
        ('core', '0003_alter_user_managers_alter_user_theme_preference_and_more'),
    ]

    operations = [
        # Allow NULL so we can clear references to core users before switching to auth.User
        migrations.AlterField(
            model_name='collection',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='core.user'),
        ),
        migrations.AlterField(
            model_name='environment',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='durgasman_environments', to='core.user'),
        ),
        migrations.AlterField(
            model_name='requesthistory',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='core.user'),
        ),
        migrations.RunPython(null_user_fks, noop),
        migrations.AlterField(
            model_name='collection',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='auth.user'),
        ),
        migrations.AlterField(
            model_name='environment',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='durgasman_environments', to='auth.user'),
        ),
        migrations.AlterField(
            model_name='requesthistory',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='auth.user'),
        ),
    ]
