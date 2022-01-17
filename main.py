import numpy as np
import folium
import pandas as pd
from geopandas.tools import geocode


table = pd.read_csv("./GlobalLandTemperaturesByState.csv")
print("Введите стартовую и конечную дату")
start_date = input()
end_date = input()
res = table.query("'{0}' <= dt < '{1}'".format(start_date, end_date))

sitys = np.unique(np.array(res["State"]))

flucs = []
for sity in sitys:
    req = res[res.State == sity]
    template = req['AverageTemperature']
    flucs.append(template.max()-template.min())
flucs = np.array(flucs)
MinSity = sitys[flucs.argmin()]
MaxSity = sitys[flucs.argmax()]

print("Наименьшее: {0} {1} Наибольшее: {2} {3}".format(MinSity,flucs.min(),MaxSity, flucs.max()))


MinSity_loc = geocode(MinSity,provider="nominatim" , user_agent = 'my_request')
MaxSity_loc = geocode(MaxSity,provider="nominatim" , user_agent = 'my_request')

mapit = folium.Map( location=[0, 0], zoom_start=1 )
folium.Marker( popup = MaxSity + ' Амплитуда: ' + str(flucs.max()),location=[MaxSity_loc.geometry.iloc[0].y, MaxSity_loc.geometry.iloc[0].x], fill_color='#43d9de', radius=8 ).add_to( mapit )
folium.Marker( popup = MinSity + ' Амплитуда: ' + str(flucs.min()),location=[MinSity_loc.geometry.iloc[0].y, MinSity_loc.geometry.iloc[0].x], fill_color='#43d9de', radius=8 ).add_to( mapit )
mapit.save("map1.html")