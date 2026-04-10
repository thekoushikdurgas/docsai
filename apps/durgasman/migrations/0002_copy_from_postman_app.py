"""
Data migration: copy existing postman_app rows into durgasman tables.
Safe to run multiple times (uses get_or_create by name + postman_id).
"""

from django.db import migrations


def copy_postman_data(apps, schema_editor):
    # Source models (postman_app)
    try:
        PostmanCollection = apps.get_model("postman_app", "PostmanCollection")
        PostmanEnvironment = apps.get_model("postman_app", "PostmanEnvironment")
    except LookupError:
        # postman_app not present or already removed — nothing to copy
        return

    DurgasmanCollection = apps.get_model("durgasman", "DurgasmanCollection")
    DurgasmanEnvironment = apps.get_model("durgasman", "DurgasmanEnvironment")

    for col in PostmanCollection.objects.all():
        DurgasmanCollection.objects.get_or_create(
            postman_id=col.postman_id or "",
            s3_file_key=col.s3_file_key,
            defaults=dict(
                name=col.name,
                description=col.description,
                schema_version=col.schema_version,
                s3_bucket_id=col.s3_bucket_id,
                item_count=col.item_count,
                request_count=col.request_count,
                size_bytes=col.size_bytes,
                uploaded_at=col.uploaded_at,
                uploaded_by=col.uploaded_by,
            ),
        )

    for env in PostmanEnvironment.objects.all():
        DurgasmanEnvironment.objects.get_or_create(
            postman_id=env.postman_id or "",
            s3_file_key=env.s3_file_key,
            defaults=dict(
                name=env.name,
                s3_bucket_id=env.s3_bucket_id,
                variable_count=env.variable_count,
                size_bytes=env.size_bytes,
                uploaded_at=env.uploaded_at,
                uploaded_by=env.uploaded_by,
            ),
        )


def noop(apps, schema_editor):
    pass  # no reverse migration needed


class Migration(migrations.Migration):
    dependencies = [
        ("durgasman", "0001_initial"),
        # postman_app removed from INSTALLED_APPS — do not depend on its migrations.
        # copy_postman_data() uses try/except LookupError when postman_app models are absent.
    ]

    operations = [
        migrations.RunPython(copy_postman_data, noop),
    ]
