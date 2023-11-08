# Generated by Django 4.2.7 on 2023-11-07 23:27

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        (
            "intercambio",
            "0003_remove_evento_año_evento_anio_santa_destinatario_and_more",
        ),
    ]

    operations = [
        migrations.AddField(
            model_name="evento",
            name="fecha_ultimo_sorteo",
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="evento",
            name="sorteo_realizado",
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name="evento",
            name="anio",
            field=models.IntegerField(
                choices=[(2022, 2022), (2023, 2023), (2024, 2024)], verbose_name="Año"
            ),
        ),
    ]
