import folium
import pandas

map = folium.Map(location=[68,79],zoom_start=6)

fgv = folium.FeatureGroup(name="Volcanoes") #hotels,destinations,recreation centres,agriculture farms,manufacturing firms

data = pandas.read_csv("volcanoes.txt")
lat = list(data["LAT"])
lon = list(data["LON"])
elv = list(data["ELEV"])
name = list(data["NAME"])

def colorProducer(elevation):
    if elevation < 1000:
        return 'green'
    elif 1000<= elevation <= 3000:
        return 'orange'
    else:
        return 'red'

html = """<h4>Volcano information:</h4>
<a href="https://www.google.com/search?q=%%22%s%%22" target="_blank">%s</a><br>
Height: %s m
"""

for lt,ln,el,name in zip(lat,lon,elv,name):
    iframe = folium.IFrame(html=html % (name, name, el), width=200, height=100)
    fgv.add_child(folium.CircleMarker(location=[lt,ln],
                                     popup=folium.Popup(iframe),radius=10,fill_color=colorProducer(el),
                                     fill_opacity=0.7,color ='grey'))

fgp = folium.FeatureGroup(name="Population") #Clans,Chiefdoms,Kingdoms,Governance

fgp.add_child(folium.GeoJson( data=open('world.json','r',encoding="utf-8-sig").read(),
    style_function=lambda x: {'fillColor':'green' if x['properties']['POP2005'] < 10000000
    else 'orange' if 10000000 <= x['properties']['POP2005'] < 20000000 else 'red'}))
map.add_child(fgv)
map.add_child(fgp)
map.add_child(folium.LayerControl())
map.save("map1.html")
