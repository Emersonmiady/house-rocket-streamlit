# Importing the libraries
import pandas as pd
import streamlit as st
import folium
import geopandas
import plotly.express as px
from streamlit_folium import folium_static
from folium.plugins import MarkerCluster
from datetime import datetime

# Setting page layout for figures
st.set_page_config(layout='wide')

@st.cache(allow_output_mutation=True)
def get_data(path):
    '''
    Reads main data (.csv) and returns the pandas dataframe.
    '''
    data = pd.read_csv(path)
    data['date'] = pd.to_datetime(data['date'])
    return data

@st.cache(allow_output_mutation=True)
def get_geofile(url):
    '''
    Reads .json from a specific url and returns the pandas geofile.
    '''
    geofile = geopandas.read_file(url)
    return geofile

def set_features(data):
    '''
    Changes the dataframe adding some features, then returns that.
    '''
    # Price by square meters
    data['price_m2'] = round(data['price'] / (data['sqft_lot'] / 10.764), 2)
    # Living room in square meters
    data['living_m2'] = round(data['sqft_living'] / 10.764, 2)
    return data

def descriptive_statistics(data):
    '''
    Returns numeric variables dataframe statistics, including min, max, 
    mean, median and std.
    '''
    df_statistics = data.describe().T.reset_index().rename({'index':'attributes', 
                                                            '50%':'median'}, axis=1)
    df_statistics = df_statistics[['attributes', 'min', 'max', 
                                   'mean', 'median', 'std']]
    return df_statistics

def overview_data(data):
    '''
    Creates all overview stuffs on the app, including:
    - Data table;
    - Descriptive statistics;
    - Zipcode informations;
    - Overview layout;
    - Overview sidebar part.
    '''
    f_attributes = st.sidebar.multiselect('Enter columns', data.columns)
    f_zipcode = st.sidebar.multiselect('Enter zipcode', data['zipcode'].unique())

    st.title('Data Overview')

    if (f_zipcode != []) & (f_attributes != []):
        data = data.loc[data['zipcode'].isin(f_zipcode), f_attributes]
    elif (f_zipcode != []) & (f_attributes == []):
        data = data.loc[data['zipcode'].isin(f_zipcode), :]
    elif (f_zipcode == []) & (f_attributes != []):
        data = data.loc[:, f_attributes]
    else:
        data = data.copy()

    st.dataframe(data.head())

    # New dataframes
    c1, c2 = st.beta_columns((1, 1))

    # Descriptive statistics
    stat_df = descriptive_statistics(data)

    c1.header('Descriptive Statistics')
    c1.dataframe(stat_df, height=600)

    # Average metrics
    df1 = data[['id', 'zipcode']].groupby('zipcode').count().reset_index()
    df2 = data[['price', 'zipcode']].groupby('zipcode').mean().reset_index()
    df3 = data[['living_m2', 'zipcode']].groupby('zipcode').mean().reset_index()
    df4 = data[['price_m2', 'zipcode']].groupby('zipcode').mean().reset_index()

    # Merge
    m1 = pd.merge(df1, df2, on='zipcode', how='inner')
    m2 = pd.merge(m1, df3, on='zipcode', how='inner')
    avg_df = pd.merge(m2, df4, on='zipcode', how='inner')

    avg_df.columns = ['ZIPCODE', 'TOTAL HOUSES', 'PRICE', 'LIVING ROOM M2', 'PRICE/LOT M2']

    c2.header('Average Values by Zipcode')
    c2.dataframe(avg_df, height=575)

    return None

def business_maps(data, geofile):
    '''
    Creates all map stuffs on the app, including:
    - Map section layout;
    - Portfolio density;
    - Region price map.
    '''
    st.title('Region Overview')

    c1, c2 = st.beta_columns((1, 1))
    c1.header('Portfolio Density')

    ## base map - folium
    density_map = folium.Map(location=[data['lat'].mean(), data['long'].mean()],
                            default_zoom_start=15)

    marker_cluster = MarkerCluster().add_to(density_map)
    for name, row in data.iterrows():
        folium.Marker([row['lat'], row['long']],
                      popup='Sold ${0} on: {1}. Features: {2} m2, '+\
                            '{3} bedrooms, {4} bathrooms, '+\
                            'year built: {5}.'.format(row['price'],
                                                      row['date'],
                                                      row['living_m2'],
                                                      row['bedrooms'],
                                                      row['bathrooms'],
                                                      row['yr_built'])).add_to(marker_cluster)

    with c1:
        folium_static(density_map)

    # Region price map
    c2.header('Price Density')

    df_aux = data[['price', 'zipcode']].groupby('zipcode').mean().reset_index()
    df_aux.columns = ['ZIP', 'PRICE']

    geofile = geofile[geofile['ZIP'].isin(df_aux['ZIP'].tolist())]

    region_price_map = folium.Map(location=[data['lat'].mean(), data['long'].mean()],
                                  default_zoom_start=15)

    folium.Choropleth(data=df_aux, geo_data=geofile, 
                    columns=['ZIP', 'PRICE'], 
                    key_on='feature.properties.ZIP',
                    fill_color='YlOrRd',
                    fill_opacity=0.7,
                    line_opacity=0.2,
                    legend_name='AVG PRICE').add_to(region_price_map)

    with c2:
        folium_static(region_price_map)

    return None

def commercial_distribution(data):
    '''
    Creates all commercial stuffs on the app, including:
    - Average price distribution per year;
    - Average price distribution per day;
    - Price histogram;
    - Commercial layout;
    - Commercial filters.
    '''
    # House distribution per commercial attributes
    st.sidebar.title('Commercial Options')
    st.title('Commercial Attributes')

    #------------------------------------------------------------------------------------------
    # Average price per year
    #------------------------------------------------------------------------------------------
    st.header('Average Price per Year Built')
    st.sidebar.subheader('Select Max Year')

    # Filters
    min_year_built = data['yr_built'].min()
    max_year_built = data['yr_built'].max()

    f_yr_built = st.sidebar.slider('Year Built', min_year_built, max_year_built, max_year_built)

    # Data selection
    yr_df = data.loc[data['yr_built'] <= f_yr_built] 
    avg_price_yr_df = yr_df[['yr_built', 'price']].groupby('yr_built').mean().reset_index()

    # Plot
    fig = px.line(avg_price_yr_df, x='yr_built', y='price')
    st.plotly_chart(fig, use_container_width=True)

    #------------------------------------------------------------------------------------------
    ## Average price per day
    #------------------------------------------------------------------------------------------
    st.header('Average Price per Day')
    st.sidebar.subheader('Select Max Date')

    # Filters
    min_date = datetime.strptime(data['date'].min().strftime('%Y-%m-%d'), '%Y-%m-%d')
    max_date = datetime.strptime(data['date'].max().strftime('%Y-%m-%d'), '%Y-%m-%d')

    f_date = st.sidebar.slider('Date', min_date, max_date, max_date)

    # Data selection
    date_df = data.loc[data['date'] <= f_date]
    avg_price_day_df = date_df[['date', 'price']].groupby('date').mean().reset_index()

    # Plot
    fig = px.line(avg_price_day_df, x='date', y='price')
    st.plotly_chart(fig, use_container_width=True)

    #------------------------------------------------------------------------------------------
    # Price histogram
    #------------------------------------------------------------------------------------------
    st.header('Price Distribution')
    st.sidebar.subheader('Select Max Price')

    ## Filters
    min_price = int(data['price'].min())
    max_price = int(data['price'].max())
    avg_price = int(data['price'].mean())

    f_price = st.sidebar.slider('Price', min_price, max_price, avg_price)

    ## Data selection
    price_df = data.loc[data['price'] <= f_price]

    ## Plot
    fig = px.histogram(price_df, x='price', nbins=50)
    st.plotly_chart(fig, use_container_width=True)

    return None

def attributes_distribution(data):
    '''
    Creates all attributes distribution stuffs on the app, including:
    - Bedrooms distribution;
    - Bathrooms distribution;
    - Floors distribution;
    - Is waterfront houses count;
    - Attributes layout;
    - Attributes filters.
    '''
    # Other house categories
    st.sidebar.title('Attributes Options')
    st.title('House Attributes')

    #------------------------------------------------------------------------------------------
    # Filters to bedrooms and bathrooms
    #------------------------------------------------------------------------------------------
    f_bedrooms = st.sidebar.selectbox('Max number of bedrooms', 
                                      sorted(data['bedrooms'].unique()))
    f_bathrooms = st.sidebar.selectbox('Max number of bathrooms', 
                                       sorted(data['bathrooms'].unique()))

    c1, c2 = st.beta_columns(2)
    # Data selection
    bedrooms_df = data.loc[data['bedrooms'] <= f_bedrooms]
    bathrooms_df = data.loc[data['bathrooms'] <= f_bathrooms]

    # House per bedrooms
    c1.header('Houses per bedrooms')
    fig = px.histogram(bedrooms_df, x='bedrooms', nbins=19)
    c1.plotly_chart(fig, use_container_width=True)

    # House per bathrooms
    c2.header('Houses per bathrooms')
    fig = px.histogram(bathrooms_df, x='bathrooms', nbins=19)
    c2.plotly_chart(fig, use_container_width=True)

    #------------------------------------------------------------------------------------------
    # Filters to floors and waterview
    #------------------------------------------------------------------------------------------
    f_floors = st.sidebar.selectbox('Max number of floors', sorted(data['floors'].unique()))
    f_waterview = st.sidebar.checkbox('Only Houses with Water View')

    c1, c2 = st.beta_columns(2)
    # Data selection
    df_floors = data.loc[data['floors'] <= f_floors]
    if f_waterview:
        df_waterview = data[data['waterfront'] == 1]
    else:
        df_waterview = data

    # House per floors
    c1.header('Houses per floors')
    fig = px.histogram(df_floors, x='floors', nbins=10)
    c1.plotly_chart(fig, use_container_width=True)

    # House per water view
    c2.header('Houses with waterfront')
    fig = px.histogram(df_waterview, x='waterfront', nbins=2)
    c2.plotly_chart(fig, use_container_width=True)

    return None

if __name__ == '__main__':
    # Data extraction
    path = 'kc_house_data.csv'

    url = 'https://opendata.arcgis.com/datasets/83fc2e72903343aabff6de8cb445b81c_2.geojson'

    df = get_data(path)

    geofile = get_geofile(url)

    # Data transformation
    df = set_features(df)

    overview_data(df)

    business_maps(df, geofile)

    commercial_distribution(df)

    attributes_distribution(df)