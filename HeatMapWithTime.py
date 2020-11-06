import pandas as pd
import geopandas as gpd
import folium as folium

def highlight_function(feature):
    return {
        'fillColor': '#ffaf00',
        'color': 'green',
        'weight': 3,
        'dashArray': '5, 5'
    }
def style_function(feature):
    return {
        'fillColor': '#ffaf00',
        'color': 'blue',
        'weight': 1.5,
        'dashArray': '5, 5'
    }

#Load some of my flight data into a datafram
flights_df = pd.read_csv(r"C:\Users\Gareth.Ahern\Desktop\NonCommercialOver1000\Attempt2\13.csv")                                    
flights13 = gpd.GeoDataFrame(flights_df, geometry=gpd.points_from_xy(flights_df.Longitude, flights_df.Latitude))
              
flights_df = pd.read_csv(r"C:\Users\Gareth.Ahern\Desktop\NonCommercialOver1000\Attempt2\14.csv")
flights14 = gpd.GeoDataFrame(flights_df, geometry=gpd.points_from_xy(flights_df.Longitude, flights_df.Latitude))
              
flights_df = pd.read_csv(r"C:\Users\Gareth.Ahern\Desktop\NonCommercialOver1000\Attempt2\15.csv")
flights15 = gpd.GeoDataFrame(flights_df, geometry=gpd.points_from_xy(flights_df.Longitude, flights_df.Latitude))
                                    
flights_df = pd.read_csv(r"C:\Users\Gareth.Ahern\Desktop\NonCommercialOver1000\Attempt2\16.csv")
flights16 = gpd.GeoDataFrame(flights_df, geometry=gpd.points_from_xy(flights_df.Longitude, flights_df.Latitude))

flights_df = pd.read_csv(r"C:\Users\Gareth.Ahern\Desktop\NonCommercialOver1000\Attempt2\17.csv")
flights17 = gpd.GeoDataFrame(flights_df, geometry=gpd.points_from_xy(flights_df.Longitude, flights_df.Latitude))

flights_df = pd.read_csv(r"C:\Users\Gareth.Ahern\Desktop\NonCommercialOver1000\Attempt2\18.csv")
flights18 = gpd.GeoDataFrame(flights_df, geometry=gpd.points_from_xy(flights_df.Longitude, flights_df.Latitude))

flights_df = pd.read_csv(r"C:\Users\Gareth.Ahern\Desktop\NonCommercialOver1000\Attempt2\19.csv")
flights19 = gpd.GeoDataFrame(flights_df, geometry=gpd.points_from_xy(flights_df.Longitude, flights_df.Latitude))

#I then merge all my geopanda'd dataframs into one mega-dataframe
frames = [flights13,flights14,flights15,flights16,flights17,flights18,flights19]
result = pd.concat(frames) 

map_data = result.copy()

#Can only use .dt accessor with datetimelike values
map_data['Position_DateTime']= pd.to_datetime(map_data['Position_DateTime'])

#I want to only group the data by day, not by datetime
map_data['Date'] = map_data['Position_DateTime'].apply(lambda x: x.date())

#This is how thick each data point is
#If the lines are all red, then make this smaller, if there is no red then make it a bigger number
map_data["Weight"] = 1

#Group the data by Date (switch in Position_DateTime if you want to include hours in the heatmap)
map_data = map_data.groupby("Date").apply(lambda x: x[["Latitude","Longitude","Weight"]].sample(int(len(x))).values.tolist())

#Not really sure what this bit does
#seems important as these are the only two variables used to create the heatmap!
date_hour_index = [x.strftime("%m/%d/%Y, %H:%M:%S") for x in map_data.index]
date_hour_data = map_data.tolist()

from folium.plugins import HeatMapWithTime
from shapely.geometry import Polygon
#Create a datafram with some lat/lons for some airports
airports_df = pd.DataFrame({'Latitude': [51.88926, 51.87999, 51.470020, 51.157925, 51.278755, 51.75], 
              'Longitude': [0.262703, -0.37627178, -0.454295, -0.163917, -0.770607, -1.58361],
              'Airport': ['Stansted', 'Luton', 'Heathrow', 'Gatwick','Farnborough','Brize Norton']})

#Stick the datafram data into a set of series
lat = airports_df["Latitude"]
lon = airports_df["Longitude"]
air = airports_df["Airport"]

#Create our map
flight_map_time = folium.Map(location =[51.5, -1],zoom_start=10)

#Add our airport series into the map
for i in range(len(lat)):
    folium.Marker((lat[i],lon[i]),popup =air[i]).add_to(flight_map_time)

#ATZs are cirlces with radius of 2NM (which is 1852m)
rad = 1852 * 2
folium.Circle(location=[51.61166667, -0.808333333], popup='Wycombe ATZ', fill_color='#000', radius=rad, weight=2, color="#000").add_to(flight_map_time)
folium.Circle(location=[51.65250556, 0.156008333], popup='Stapleford ATZ', fill_color='#000', radius=rad, weight=2, color="#000").add_to(flight_map_time)
folium.Circle(location=[51.655825, -0.32585], popup='Elstree ATZ', fill_color='#000', radius=rad, weight=2, color="#000").add_to(flight_map_time)
folium.Circle(location=[51.34802778, -0.558708333], popup='Fairoaks ATZ', fill_color='#000', radius=rad, weight=2, color="#000").add_to(flight_map_time)
folium.Circle(location=[51.32388889, -0.8475], popup='Blackbushe ATZ', fill_color='#000', radius=rad, weight=2, color="#000").add_to(flight_map_time)
folium.Circle(location=[51.50065833, 0.774833333], popup='White Waltham ATZ', fill_color='#000', radius=rad, weight=2, color="#000").add_to(flight_map_time)
folium.Circle(location=[51.588425, -0.512994444], popup='Denham ATZ', fill_color='#000', radius=rad, weight=2, color="#000").add_to(flight_map_time)


lat_point_list = [51.76563889,51.835,51.79361111,51.80944444,51.73024444,51.66416667,51.705,51.68888889]
lon_point_list = [-1.867183333,-1.490277778,-1.426944444,-1.332777778,-1.2981,-1.675277778,-1.740833333,-1.833611111]

polygon_geom = Polygon(zip(lon_point_list, lat_point_list)) 
c= folium.GeoJson(polygon_geom)
folium.Popup('BRIZE NORTON CTR').add_to(c)
c.add_to(flight_map_time)

lat_point_list = [51.27527778,51.33709442,51.29463889,51.25546533,51.33694444]
lon_point_list = [-0.7775,-0.517813639,-0.490938889,-0.610742972,-0.633333333]

polygon_geom = Polygon(zip(lon_point_list, lat_point_list))

c= folium.GeoJson(polygon_geom)
folium.Popup('FARNBOROUGH ATZ').add_to(c)
c.add_to(flight_map_time)

def addpolygontomap(latlist,longlist,name):
    polygon_geom = Polygon(zip(longlist, latlist))
    c = folium.GeoJson(polygon_geom,style_function=style_function,highlight_function=highlight_function)
    folium.Popup(str(name)).add_to(c)
    c.add_to(flight_map_time)

### Farnborough ###
lat_point_list = [51.28478889,51.17636658,51.18359642,51.25968333]
lon_point_list = [-0.918847222,-0.848226861,-0.898699694,-0.963383333]
addpolygontomap(lat_point_list,lon_point_list,'FARNBOROUGH CTA 2')

lat_point_list = [51.25968333,51.18359642,51.19528333]
lon_point_list = [-0.963383333,-0.898699694,-0.980758333]
addpolygontomap(lat_point_list,lon_point_list,'FARNBOROUGH CTA 3')

lat_point_list = [51.25546533,51.17055556,51.14222222,51.10887778,51.08028581,51.11444444,51.17636658]
lon_point_list = [-0.610742972,-0.556944444,-0.681944444,-0.660372222,-0.785885889,-0.808055556,-0.848226861]
addpolygontomap(lat_point_list,lon_point_list,'FARNBOROUGH CTA 4')

lat_point_list = [51.11444444,51.08028581,51.10055556]
lon_point_list = [-0.808055556,-0.785885889,-0.910833333]
addpolygontomap(lat_point_list,lon_point_list,'FARNBOROUGH CTA 5')

lat_point_list = [51.19528333,51.17636658,51.11444444,51.10055556]
lon_point_list = [-0.980758333,-0.848226861,-0.808055556,-0.910833333]
addpolygontomap(lat_point_list,lon_point_list,'FARNBOROUGH CTA 6')

lat_point_list = [51.09252389,51.08028581,51.01312222,51.01312222]
lon_point_list = [-0.861212611,-0.785885889,-0.742398694,-0.880942944]
addpolygontomap(lat_point_list,lon_point_list,'FARNBOROUGH CTA 7')

lat_point_list = [51.16575556,51.10055556,51.01312222,50.90972222,51.07222222,51.11]
lon_point_list = [-0.958905556,-0.910833333,-0.880942944,-1.059722222,-1.115833333,-1.138055556]
addpolygontomap(lat_point_list,lon_point_list,'FARNBOROUGH CTA 8')

lat_point_list = [50.96083333,50.85521667,50.85521667,50.92]
lon_point_list = [-0.684444444,-0.571839111,-0.915695889,-0.985555556]
addpolygontomap(lat_point_list,lon_point_list,'FARNBOROUGH CTA 9')

lat_point_list = [51.35339367,51.35079608,51.34292928,51.25546533,51.17636658,51.28478889]
lon_point_list = [-0.712965722,-0.709921056,-0.66638475,-0.610742972,-0.848226861,-0.918847222]
addpolygontomap(lat_point_list,lon_point_list,'FARNBOROUGH CTR 1')

lat_point_list = [51.34292928,51.33694444,51.25546533]
lon_point_list = [-0.66638475,-0.633333333,-0.610742972]
addpolygontomap(lat_point_list,lon_point_list,'FARNBOROUGH CTR 2')
### Farnborough ###

### Stanstead ###
lat_point_list = [51.90444444,52.01777778,52.08805556,51.97444444]
lon_point_list = [0.448055556,0.250833333,0.356666667,0.553888889]
addpolygontomap(lat_point_list,lon_point_list,'Stanstead CTA 1')

lat_point_list = [51.75222222,51.68194444,51.76388889,51.86277778,51.86527778]
lon_point_list = [0.219166667,0.114444444,-0.054444444,-0.001666667,0.022222222]
addpolygontomap(lat_point_list,lon_point_list,'Stanstead CTA 2')

lat_point_list = [51.97444444,51.89694444,51.76555556,51.75222222]
lon_point_list = [0.553888889,0.584166667,0.385833333,0.219166667]
addpolygontomap(lat_point_list,lon_point_list,'Stanstead CTA 3')

lat_point_list = [52.05,52.08805556,51.86527778,51.86277778,52.02416667]
lon_point_list = [0.151944444,0.356666667,0.022222222,-0.001666667,0]
addpolygontomap(lat_point_list,lon_point_list,'Stanstead CTA 4')

lat_point_list = [51.90444444,51.75222222,51.86527778,52.01777778]
lon_point_list = [0.448055556,0.219166667,0.022222222,0.250833333]
addpolygontomap(lat_point_list,lon_point_list,'Stanstead CTR')

lat_point_list = [51.90444444,52.01777778,52.08805556,51.97444444]
lon_point_list = [0.448055556,0.250833333,0.356666667,0.553888889]
#addpolygontomap(lat_point_list,lon_point_list,'Stanstead TMZ 1')

lat_point_list = [51.75222222,51.68194444,51.76388889,51.86277778,51.86527778]
lon_point_list = [0.219166667,0.114444444,-0.054444444,-0.001666667,0.022222222]
#addpolygontomap(lat_point_list,lon_point_list,'Stanstead TMZ 2')
### Stanstead ###

### Luton ###
lat_point_list = [51.9825,52.02416667,51.86277778,51.85053889,51.80833333,51.845]
lon_point_list = [-0.242777778,0,-0.001666667,-0.008213889,-0.251666667,-0.158611111]
addpolygontomap(lat_point_list,lon_point_list,'Luton CTA 1')

lat_point_list = [51.80277778,51.81805556,51.75083333,51.73583333]
lon_point_list = [-0.698611111,-0.613055556,-0.5825,-0.668055556]
addpolygontomap(lat_point_list,lon_point_list,'Luton CTA 2')

lat_point_list = [51.80277778,51.86388889,51.87888889,51.81805556]
lon_point_list = [-0.698611111,-0.726666667,-0.641111111,-0.613055556]
addpolygontomap(lat_point_list,lon_point_list,'Luton CTA 3')

lat_point_list = [51.86388889,51.80277778,51.78305556,51.84666667]
lon_point_list = [-0.726666667,-0.698611111,-0.810555556,-0.823888889]
addpolygontomap(lat_point_list,lon_point_list,'Luton CTA 4')

lat_point_list = [52.01055556,51.96194444,51.83916667,51.81805556,51.87888889,51.88277778]
lon_point_list = [-0.475555556,-0.3625,-0.491944444,-0.613055556,-0.641111111,-0.619166667]
addpolygontomap(lat_point_list,lon_point_list,'Luton CTA 5')

lat_point_list = [52.05444444,52.01055556,51.88277778,51.87888889,51.9175]
lon_point_list = [-0.578055556,-0.475555556,-0.619166667,-0.641111111,-0.731388889]
addpolygontomap(lat_point_list,lon_point_list,'Luton CTA 6')

lat_point_list = [52.10166667,51.99305556,51.96194444,52.01055556]
lon_point_list = [-0.286666667,-0.182222222,-0.3625,-0.475555556]
addpolygontomap(lat_point_list,lon_point_list,'Luton CTA 7')

lat_point_list = [51.86388889,51.87888889,51.9175]
lon_point_list = [-0.726666667,-0.641111111,-0.731388889]
addpolygontomap(lat_point_list,lon_point_list,'Luton CTA 8')

lat_point_list = [51.86388889,51.9175,51.96361111,51.89888889,51.84666667]
lon_point_list = [-0.726666667,-0.731388889,-0.679888889,-0.834863889,-0.823888889]
addpolygontomap(lat_point_list,lon_point_list,'Luton CTA 9')

lat_point_list = [51.87888889,51.91972222,51.96194444,51.9825,51.845,51.80833333,51.75083333]
lon_point_list = [-0.641111111,-0.407222222,-0.3625,-0.242777778,-0.158611111,-0.251666667,-0.5825]
addpolygontomap(lat_point_list,lon_point_list,'Luton CTR')
### Luton ###

### Heathrow ###
lat_point_list = [51.60305556,51.60305556,51.59794957925,51.58408346583,51.56935672833,51.5538825548,51.53777916537,51.52116883868,51.50417734216,51.4869325135,51.46956409567,51.45220218407,51.43497677062,51.41801694406,51.40144973378,51.38539955445,51.36998701875,51.35532855722,51.34153520329,51.33694444,51.33694444,51.34153519652,51.35532855076,51.36998703984,51.38539954919,51.40144972936,51.41801694062,51.43497677901,51.45220218285,51.46956409564,51.48693251466,51.50417734447,51.52116884208,51.53777916975,51.55388256002,51.56935673425,51.58408347226,51.59794958599]
lon_point_list = [-0.6925,-0.214722222, -0.20764, -0.19072535432, -0.17582937181, -0.1630611555, -0.15251299233, -0.1442600754, -0.13836037382, -0.13485421308, -0.13376440339, -0.13509606093, -0.13883677821, -0.14495668357, -0.15340873668, -0.16412893307, -0.17703689319, -0.19203600162, -0.20901422138,-0.214722222,-0.633333333, -0.69820799152, -0.71518621312, -0.73018534838, -0.74309328498, -0.75381348272, -0.76226553694, -0.76838544621, -0.77212616089, -0.77345781861, -0.77236800876, -0.76886184754, -0.76296214517, -0.75470922715, -0.74416106264, -0.73139284476, -0.71649686053, -0.69958207328]
addpolygontomap(lat_point_list,lon_point_list,'Heathrow CTR')
### Heathrow ###

#Now add the heatmap data
HeatMapWithTime(date_hour_data,index =  date_hour_index,radius=8).add_to(flight_map_time)

#save it as a html
flight_map_time.save('/Users/Gareth.Ahern/Desktop/mapwithtimemapall9991.html')
