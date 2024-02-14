import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import seaborn as sns
import folium

df = pd.read_csv('historical_automobile_sales.csv')
df_Recession_Years = df[df['Recession'] == 1]

#ASK 1.1: Develop a Line chart using the functionality of pandas to show how automobile sales fluctuate from year to year
df_avg_sales = df.groupby(df['Year'])['Automobile_Sales'].mean()
plt.figure(figsize=(10,6))
df_avg_sales.plot(kind = 'line')
plt.xticks(list(range(1980,2024)), rotation = 75)
plt.xlabel('Year')
plt.ylabel('Sales')
plt.title('Automobile Sales during Recession')
plt.text(1991, 650, '1991 Recession')
plt.text(2009, 600, '2007-mid 2009 Recession')
plt.legend()
plt.show()

#TASK 1.2: Plot different lines for categories of vehicle type and analyse the trend to answer the question Is there a noticeable difference in sales trends between different vehicle types during recession periods?
df_Recession_Years = df[df['Recession'] == 1]
df_Multi_Line = df_Recession_Years.groupby(['Year','Vehicle_Type'], as_index=False)['Automobile_Sales'].sum()
df_Multi_Line.set_index('Year', inplace=True)
df_Multi_Line = df_Multi_Line.groupby(['Vehicle_Type'])['Automobile_Sales']
df_Multi_Line.plot(kind='line', figsize=(12, 6))
#plt.xticks(list(range(1980,2024)), rotation = 75)
plt.xlabel('Year')
plt.ylabel('Sales')
plt.title('Vehicle-wise sales trend during Recession')
plt.legend()
plt.show()

#TASK 1.3: Use the functionality of Seaborn Library to create a visualization to compare the sales trend per vehicle type for a recession period with a non-recession period
df_trend = df.groupby('Recession')['Automobile_Sales'].mean().reset_index()
plt.figure(figsize=(10,6))
sns.barplot(x='Recession', y='Automobile_Sales', hue='Recession',  data=df_trend)
plt.xlabel('Years')
plt.ylabel('Sales')
plt.title('Average Automobile Sales during Recession and Non-Recession')
plt.xticks(ticks=[0, 1], labels=['Non-Recession', 'Recession'])
plt.show()

df_sales_recession = df[df['Recession'] == 1]
df_sales_by_type = df_sales_recession.groupby(['Vehicle_Type'])['Automobile_Sales'].mean().reset_index()
plt.figure(figsize=(10, 6))
sns.barplot(x='Vehicle_Type', y='Automobile_Sales', hue='Vehicle_Type', data=df_sales_by_type)
plt.xlabel('Vehicle Types')
plt.ylabel('Sales')
plt.title('Vehicle-Wise Sales during Recession and Non-Recession Period')
plt.show()


#TASK 1.4: Use sub plotting to compare the variations in GDP during recession and non-recession period by developing line plots for each period.
df_sales_recession = df[df['Recession'] == 1]
df_sales_non_recession = df[df['Recession'] == 0]

plt.figure(figsize=(12,6))

plt.subplot(1, 2, 1)
sns.lineplot(x='Year', y='GDP', data=df_sales_recession, label='GDP Variation during Recession Period')
plt.xlabel('Year')
plt.ylabel('GDP')
plt.legend()


plt.subplot(1, 2, 2)
sns.lineplot(x='Year', y='GDP', data=df_sales_non_recession, label='GDP Variation during Non-Recession Period')
plt.xlabel('Year')
plt.ylabel('GDP')
plt.legend()

plt.tight_layout()
plt.show()

#TASK 1.5: Develop a Bubble plot for displaying the impact of seasonality on Automobile Sales.
df_sales_non_recession = df[df['Recession'] == 0]
size=df_sales_non_recession['Seasonality_Weight']
sns.scatterplot(x='Month',y='Automobile_Sales',data=df_sales_non_recession,size=size)
plt.xlabel('Month')
plt.ylabel('Automobile_Sales')
plt.title('Seasonality impact on Automobile Sales')
plt.show()


#TASK 1.6: Use the functionality of Matplotlib to develop a scatter plot to identify the correlation between average vehicle price relate to the sales volume during recessions
df_sales_recession = df[df['Recession'] == 1]
plt.scatter(df_sales_recession['Consumer_Confidence'], df_sales_recession['Automobile_Sales'])
plt.xlabel('Consumer Confidence')
plt.ylabel('Sales')
plt.title('Consumer Confidence and Automobile Sales during Recessions')
plt.show()

df_sales_recession = df[df['Recession'] == 1]
plt.scatter(df_sales_recession['Price'], df_sales_recession['Automobile_Sales'])
plt.xlabel('Price')
plt.ylabel('Sales')
plt.title('Relationship between Average Vehicle Price and Sales during Recessions')
plt.show()


#TASK 1.7: Create a pie chart to display the portion of advertising expenditure of XYZAutomotives during recession and non-recession periods
df_sales_recession = df[df['Recession'] == 1]
df_sales_non_recession = df[df['Recession'] == 0]
Ad_Exp_Recession = df_sales_recession['Advertising_Expenditure'].sum()
Ad_Exp_Non_Recession = df_sales_non_recession['Advertising_Expenditure'].sum()

plt.figure(figsize=(8, 6))
labels = ['Recession', 'Non-Recession']
sizes = [Ad_Exp_Recession, Ad_Exp_Non_Recession]
plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
plt.title('Advertising Expenditure during Recession and Non-Recession Periods')
plt.show()


#TASK 1.8: Develop a pie chart to display the total Advertisement expenditure for each vehicle type during recession period.
df_sales_recession = df[df['Recession'] == 1]
Ad_By_VT = df_sales_recession.groupby('Vehicle_Type')['Advertising_Expenditure'].sum()
plt.figure(figsize=(8, 6))
labels = Ad_By_VT.index
sizes = Ad_By_VT.values
plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
plt.title('Share of Each Vehicle Type in Total Sales during Recessions')
plt.show()


#TASK 1.9: Develop a lineplot to analyse the effect of the unemployment rate on vehicle type and sales during the Recession Period.¶
df_sales_recession = df[df['Recession'] == 1]
sns.lineplot(data=df_sales_recession,x='unemployment_rate',y='Automobile_Sales',hue='Vehicle_Type',style='Vehicle_Type', markers='o',err_style=None)
plt.ylim(0,850)
plt.legend(loc=(0.05,.3))
plt.show()


#OPTIONAL : TASK 1.10 Create a map on the hightest sales region/offices of the company during recession period
# Filter the data for the recession period and specific cities
recession_data = df[df['Recession'] == 1]

# Calculate the total sales by city
sales_by_city = recession_data.groupby('City')['Automobile_Sales'].sum().reset_index()

# Create a base map centered on the United States
map1 = folium.Map(location=[37.0902, -95.7129], zoom_start=4)

# Create a choropleth layer using Folium
choropleth = folium.Choropleth(
    geo_data= 'us-states.json',  # GeoJSON file with state boundaries
    data=sales_by_city,
    columns=['City', 'Automobile_Sales'],
    key_on='feature.properties.name',
    fill_color='YlOrRd',
    fill_opacity=0.7,
    line_opacity=0.2,
    legend_name='Automobile Sales during Recession'
).add_to(map1)


# Add tooltips to the choropleth layer
choropleth.geojson.add_child(
    folium.features.GeoJsonTooltip(['name'], labels=True)
)

map1.save('Sales_By_City.html')