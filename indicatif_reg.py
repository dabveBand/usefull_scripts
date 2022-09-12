#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# File     : indicatif_regionaux.py
# Author   : daBve, dabve@gmail.com
# Created  :
# Desc     :
# -----------------------------------------------------


from terminaltables import AsciiTable

"""
indicatif
"""
wilaya = [
    'Adrar', 'Chlef', 'Laghouat', 'Oum-El-Boughi', 'Batna', 'Bejaia', 'Biskra', 'Bechar', 'Blida', 'Bouira', 'Tamanrasat',
    'Tebessa', 'Telemcen', 'Tiarer', 'Tizi-Ouzou', 'Alger', 'Djelfa', 'Jijel', 'Setif', 'Saida', 'Skikda', 'Sidi-Bel-Abbes',
    'Annaba', 'Guelma', 'Constantine', 'Medea', 'Mostaganem', 'M\'sila', 'Mascara', 'Ouargla', 'Oran', 'Le-Baydah', 'Illizi',
    'Bordj-Bou-Arreridj', 'Boumerdes', 'Le-Taref', 'Tindouf', 'Tissemsilt', 'Le-Oued', 'Khenchela', 'Souk-Ahras', 'Tipaza',
    'Mila', 'Ain-Defla', 'Naama', 'Ain-Timouchent', 'Ghardaia', 'Relizane'
]

indicatif = [
    '049', '027', '029', '032', '033', '034', '033', '049', '025', '026', '029', '037', '043', '046', '026', '021', '027', '034',
    '036', '048', '038', '048', '038', '037', '031', '025', '045', '035', '045', '029', '041', '049', '029', '035', '024', '038',
    '049', '046', '032', '032', '037', '024', '031', '027', '049', '043', '029', '046'
]

postal = [
    '01000', '02000', '03000', '04000', '05000', '06000', '07000', '08000', '09000', '10000', '11000', '12000', '13000', '14000',
    '15000', '16000', '17000', '18000', '19000', '20000', '21000', '22000', '23000', '24000', '25000', '26000', '27000', '28000',
    '29000', '30000', '31000', '32000', '33000', '34000', '35000', '36000', '37000', '38000', '39000', '40000', '41000', '42000',
    '43000', '44000', '45000', '46000', '47000', '48000'
]

table_data = [
    ['Code', 'Wilaya', 'Indicatif', 'Code Postal'],
]

for i in range(48):
    region = [str(i + 1), wilaya[i], indicatif[i], postal[i]]
    table_data.append(region)

table_instance = AsciiTable(table_data)
print(table_instance.table)
