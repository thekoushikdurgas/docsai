# Migrate FK from core.User to auth.User before core.0004_delete_user

from django.db import migrations, models
import django.db.models.deletion


def null_user_fks(apps, schema_editor):
    from django.db import connection
    with connection.cursor() as c:
        c.execute("UPDATE json_store SET created_by_id = NULL")


def noop(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('json_store', '0001_initial'),
        ('core', '0003_alter_user_managers_alter_user_theme_preference_and_more'),
    ]

    operations = [
        migrations.RunPython(null_user_fks, noop),
        migrations.AlterField(
            model_name='jsonstore',
            name='created_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='json_stores', to='auth.user'),
        ),
    ]
