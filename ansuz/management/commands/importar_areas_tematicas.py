import os
import pandas as pd
from django.core.management import BaseCommand
from ansuz.models import Area


class Command(BaseCommand):
    def handle(self, *args, **kwargs,):
        df_areas = pd.read_json(os.path.join('ansuz', 'fixtures', 'eixos_tematicos.json', ), encoding='utf-8')

        for index, row in df_areas.iterrows():
            Area.objects.create(id=row['id'], nome=row['nome'])
            print(f"Área {row['nome']} importada.")
        print(f'Áreas importadas com sucesso!')