import pandas as pd
import geopandas as gpd
import folium as folium

#Starting really basic - creating a map
#flight_map = folium.Map(location =[53, -1],zoom_start=12)
#flight_map.save('/Users/Gareth.Ahern/Desktop/basicmap.html')

#Load some of my flight data into a datafram
flights_df = pd.read_csv(r"C:\Users\Gareth.Ahern\Desktop\NonCommercialOver1000\NonCommercialOver1000_20200713.csv")

#The Position_DateTime is being treated as an object - i need it to be a datetime
#Otherwise it is tricky to truncate the time part off
#print(flights_df['Position_DateTime'].dtypes)
flights_df['Position_DateTime']= pd.to_datetime(flights_df['Position_DateTime'])
#print(flights_df['Position_DateTime'].dtypes)


#Pick first 5 lat/longs
#lat = flights_df["Latitude"].values[:5]
#lon = flights_df["Longitude"].values[:5]

#Stick them in a map
#for i in range(len(lat)):
#    folium.Marker((lat[i],lon[i]),popup ="Flight {}".format(i+1)).add_to(flight_map)
    
#save that map
#flight_map.save('/Users/Gareth.Ahern/Desktop/mapwith15Flights.html')

from folium.plugins import HeatMap

#Stick 1000 GPS points into another dataframe
#lat_lon = flights_df[["Latitude","Longitude"]].values[:1000]
#HeatMap(lat_lon,radius=13).add_to(flight_map)
#flight_map.save('/Users/Gareth.Ahern/Desktop/heatmapbasic.html')

#weighted_flight_map = folium.Map(location =[53, -1],zoom_start=12)

#flights_df["Weight"]  = 0.1
#lat_long = flights_df[["Latitude","Longitude","Weight"]].values[:1000]
#HeatMap(lat_lon,radius=13).add_to(weighted_flight_map)
#weighted_flight_map.save('/Users/Gareth.Ahern/Desktop/weightedheatmapbasic.html')
        
#There is probably a nicer way to do this
#What i am doing is loading the diffferent data to flights_df and then geopandering it into another datafram                                       
flights13 = gpd.GeoDataFrame(flights_df, geometry=gpd.points_from_xy(flights_df.Longitude, flights_df.Latitude))
              
flights_df = pd.read_csv(r"C:\Users\Gareth.Ahern\Desktop\NonCommercialOver1000\NonCommercialOver1000_20200714.csv")
flights14 = gpd.GeoDataFrame(flights_df, geometry=gpd.points_from_xy(flights_df.Longitude, flights_df.Latitude))
              
flights_df = pd.read_csv(r"C:\Users\Gareth.Ahern\Desktop\NonCommercialOver1000\NonCommercialOver1000_20200715.csv")
flights15 = gpd.GeoDataFrame(flights_df, geometry=gpd.points_from_xy(flights_df.Longitude, flights_df.Latitude))
                                    
flights_df = pd.read_csv(r"C:\Users\Gareth.Ahern\Desktop\NonCommercialOver1000\NonCommercialOver1000_20200716.csv")
flights16 = gpd.GeoDataFrame(flights_df, geometry=gpd.points_from_xy(flights_df.Longitude, flights_df.Latitude))

flights_df = pd.read_csv(r"C:\Users\Gareth.Ahern\Desktop\NonCommercialOver1000\NonCommercialOver1000_20200717.csv")
flights17 = gpd.GeoDataFrame(flights_df, geometry=gpd.points_from_xy(flights_df.Longitude, flights_df.Latitude))

flights_df = pd.read_csv(r"C:\Users\Gareth.Ahern\Desktop\NonCommercialOver1000\NonCommercialOver1000_20200718.csv")
flights18 = gpd.GeoDataFrame(flights_df, geometry=gpd.points_from_xy(flights_df.Longitude, flights_df.Latitude))

flights_df = pd.read_csv(r"C:\Users\Gareth.Ahern\Desktop\NonCommercialOver1000\NonCommercialOver1000_20200719.csv")
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
map_data = map_data.groupby("Date").apply(lambda x: x[["Latitude","Longitude","Weight"]].sample(int(len(x)/300)).values.tolist())

#Not really sure what this bit does
#seems important as these are the only two variables used to create the heatmap!
date_hour_index = [x.strftime("%m/%d/%Y, %H:%M:%S") for x in map_data.index]
date_hour_data = map_data.tolist()

from folium.plugins import HeatMapWithTime

#Create a datafram with some lat/lons for some airports
airports_df = pd.DataFrame({'Latitude': [51.88926,51.87999, 51.470020,51.157925,51.278755,51.75], 
              'Longitude': [0.262703,-0.37627178,-0.454295,-0.163917,-0.770607,-1.58361],
              'Airport': ['Stansted', 'Luton', 'London', 'Gatwick','Farnborough','Brize Norton']})

#Stick the datafram data into a set of series
lat = airports_df["Latitude"]
lon = airports_df["Longitude"]
air = airports_df["Airport"]

#Create our map
flight_map_time = folium.Map(location =[53, -1],zoom_start=10)

#Add our airport series into the map
for i in range(len(lat)):
    folium.Marker((lat[i],lon[i]),popup =air[i]).add_to(flight_map_time)

#Now add the heatmap data
HeatMapWithTime(date_hour_data,index =  date_hour_index,radius=2,).add_to(flight_map_time)

#save it as a html
flight_map_time.save('/Users/Gareth.Ahern/Desktop/mapwithtimemapall22.html')