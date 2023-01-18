# Generated by Django 4.1.5 on 2023-01-17 16:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("book", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Borrowing",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("borrow_date", models.DateField()),
                ("expected_return_date", models.DateField()),
                ("actual_return_date", models.DateField()),
                (
                    "book",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="Borrowing",
                        to="book.book",
                    ),
                ),
            ],
            options={
                "ordering": ["borrow_date"],
            },
        ),
    ]
