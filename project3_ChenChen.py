#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import plotly
import plotly.plotly as py
import plotly.graph_objs as go
import warnings
#!pip install plotly_express
import plotly_express as px


# In[2]:


#sign in plotly
py.sign_in("name", "APIkey")
# set all the data to 2 decimal
pd.set_option("display.float.format", lambda x: "%.2f" % x)
#ignore warning message 
warnings.filterwarnings("ignore")


# # World inbound toursits from other country 

# In[3]:


#import inbound tourist data set
inbound_tourists = pd.read_excel("travel_data.xls", sheet_name="number_of_arrival", header=3, index_col=0)
inbound_tourists.head()


# In[4]:


#import world country list data
country_list = pd.read_excel("travel_data.xls", sheet_name="country code")
country_list.head()


# In[5]:


#define a function to select rows and columns
def data_selection(df):
    #merge the data frame with country list data frame by county Code, so we can drop irrelevant rows
    df = pd.merge(country_list, df, left_on = "Country Code", right_on = "Country Code", how="left")
    df = df.set_index("Country Name")
    #select columns from year 2007 to 2017
    df_new = pd.concat([df["Country Code"],df.loc[:,"2007":"2017"]], axis=1)
    #replace missing value by 0
    df_new = df_new.fillna(0)
    return df_new


# In[6]:


#use "data_selection" function to select inbound tourists data
inbound_tourists_clean = data_selection(inbound_tourists)
inbound_tourists_clean.head()


# In[7]:


#define function to reshape the data frame
def reshape_data(df):
    df_new = df[:] 
    df_new.set_index(["Country Code"], inplace = True, append = True)
    #use stack to change the data frame shape
    df_new = df_new.stack()
    df_new = pd.DataFrame(df_new)
    df_new = df_new.reset_index()
    #rename column names
    df_new = df_new.rename(columns = {"level_2":"Year",0:"Amount"})
    return df_new


# In[8]:


#use "reshape_data" function to reshape the inbound_touists_clean data frame
inbound_tourists_stack = reshape_data(inbound_tourists_clean)
inbound_tourists_stack.head()


# In[9]:


#make the map plot of the inbound tourists use plotly_express package
inbound_map = px.choropleth(inbound_tourists_stack, 
                            locations="Country Code", 
                            color="Amount", 
                            hover_name="Country Name",
                            #set the animation slide bar
                            animation_frame="Year",
                            color_continuous_scale=px.colors.sequential.BuGn,
                            #set the map type
                            projection="natural earth")
inbound_map
#plotly.offline.plot(inbound_map, filename="inbound_map")


# # Top countries that attract tourists

# In[10]:


#find the top countries that attract tourists
top_country_inbound = inbound_tourists_clean.sort_values("2017", ascending=False).head(10)
top_inbound_country_list = list(top_country_inbound.index)
top_inbound_country_list


# In[11]:


#select the top countries' data 
top_inbound_data = inbound_tourists_stack.loc[inbound_tourists_stack["Country Name"].isin(top_inbound_country_list)]
top_inbound_data.head()


# In[12]:


#make the line plot for top countries
inbound_top = px.line(top_inbound_data, 
                      x="Year", 
                      y="Amount", 
                      color="Country Name", 
                      line_group="Country Name",  
                      line_shape="linear", 
                      title="Top countries that attract tourists")
inbound_top
#plotly.offline.plot(inbound_top, filename="inbound_top")


# In[13]:


top_country_inbound


# In[14]:


# define fucntion to calculate the yearly military spending growth 
def growth_inbound(df):
    for year in range(2007, 2017,1):
        # add growth columns 
        df["growth"+ str(year+1)] = (df[str(year+1)] - df[str(year)])/df[str(year)]*100
        df_new = df.iloc[:, -10:]
    return df_new


# In[15]:


growth_inbound_data = growth_inbound(top_country_inbound)
growth_inbound_data = growth_inbound_data.stack()
growth_inbound_data = growth_inbound_data.reset_index()
growth_inbound_data = growth_inbound_data.rename(columns = {"level_1":"Year",0:"Amount"})
growth_inbound_data.head()


# In[16]:


#make the bar plot of the country's inbound tourists growth
growth_bar = px.bar(growth_inbound_data, 
                         x="Year", 
                         y="Amount", 
                         color="Country Name", 
                         hover_name="Country Name",
                         #make grouped bar code
                         barmode="group",
                         title="Top attractive countries inbound tourists yearly growth rate")
growth_bar
#plotly.offline.plot(growth_bar, filename="growth_bar")


# # Top countries with the highest receipts from tourists 

# In[17]:


#import tourists receipts data set
receipts = pd.read_excel("travel_data.xls", sheet_name="receipts for travel items", header=3, index_col=0)
receipts.head()


# In[18]:


#use "data_selection" function to select inbound tourists data
receipts_clean = data_selection(receipts)
receipts_clean.head()


# In[19]:


#find the top countries with the attract tourists most
top_country_receipts = receipts_clean.sort_values("2017", ascending=False).head(10)
top_receipts_country_list = list(top_country_receipts.index)
top_receipts_country_list


# In[20]:


#select the top countries' data 
top_receipts_data = receipts_clean.loc[receipts_clean.index.isin(top_receipts_country_list)]
top_receipts_data.head()


# In[21]:


#use "reshape_data" function to reshape the inbound_touists_clean data frame
receipts_clean_stack = reshape_data(top_receipts_data)
receipts_clean_stack.head()


# In[22]:


#make the bar plot of the top countries with highest receipts from trouism
receipts_bar = px.bar(receipts_clean_stack, 
                      x="Year", 
                      y="Amount", 
                      color="Country Name", 
                      hover_name="Country Name",
                      title="Top countries with highest receipts")
receipts_bar
#plotly.offline.plot(receipts_bar, filename="receipts_bar")


# # Top countries with the highest tourism share of exports (i.e. tourism-oriented export)

# In[23]:


#import receipts count percentage of export data set
percent_export = pd.read_excel("travel_data.xls", sheet_name="receipts (% of total exports)", header=3, index_col=0)
percent_export.head()


# In[24]:


#use "data_selection" function to select receipts export data
percent_export_clean = data_selection(percent_export)
percent_export_clean.head()


# In[25]:


#find the top countries with the attract tourists most
top_country_export = percent_export_clean.sort_values("2017", ascending=False).head(10)
top_export_country_list = list(top_country_export.index)
top_export_country_list


# In[26]:


#use "reshape_data" function to reshape the percent_export_clean data frame
percent_export_stack = reshape_data(percent_export_clean)
percent_export_stack.head()


# In[27]:


#select the top countries' data 
top_country_export = percent_export_stack.loc[percent_export_stack['Country Name'].isin(top_export_country_list)]
top_country_export.head()


# In[28]:


#make the polar bar plot for the top countries tourism are export oriented
export_polar = px.bar_polar(top_country_export,
                            #radius column
                            r="Amount",
                            #angle column
                            theta="Country Name",
                            color="Country Name", 
                            #slider animation column
                            animation_frame="Year", 
                            title="Top countries ranked by tourism share of exports")
export_polar
#plotly.offline.plot(export_polar, filename="export_polar")


# # GDP and tourists number correlation

# In[29]:


#import countries GDP data set
gdp = pd.read_excel("travel_data.xls", sheet_name="GDP", header=3, index_col=0)
gdp.head()


# In[30]:


#select relevant years data
gdp = gdp.loc[:,"2007":"2017"]
#reshape the data frame
gdp_data = pd.DataFrame(gdp.stack()).reset_index()
#rename the column name
gdp_data = gdp_data.rename(columns = {"level_1":"Year", 0:"GDP"})
gdp_data.head()


# In[31]:


#merge the inbound tourists data and gdp data by Country name and year
gdp_inbound = inbound_tourists_stack.merge(gdp_data, left_on=("Country Name","Year"), right_on=("Country Name","Year"))
gdp_inbound.head()


# In[32]:


#make the scatter plot check the relation between GDP and inbound tourists number
gdp_inbound_plot = px.scatter(gdp_inbound, 
                              x="Amount", 
                              y="GDP",
                              #set the color of the plot
                              color_discrete_sequence = px.colors.qualitative.Vivid,
                              hover_name="Country Name",
                              #use log data to plot
                              log_x=True, 
                              log_y=True, 
                              labels="Amount(number of people)",
                              title="Correlation between GDP and number of inbound tourists")
gdp_inbound_plot
#plotly.offline.plot(gdp_inbound_plot, filename="gdp_inbound_plot")


# # world tourists travel outbound 

# In[33]:


#import tourists outbound data set
outbound_tourists = pd.read_excel("travel_data.xls", sheet_name="number_of_departure", header=3, index_col=0)
outbound_tourists.head()


# In[34]:


#use "data_selection" function to select inbound tourists data
outbound_tourists_clean = data_selection(outbound_tourists)
outbound_tourists_clean.head()


# In[35]:


#use "reshape_data" function to reshape the outbound_tourists_clean data frame
outbound_tourists_stack = reshape_data(outbound_tourists_clean)
outbound_tourists_stack.head()


# In[36]:


#make the map plot of world outbound tourist
outbound_map = px.scatter_geo(outbound_tourists_stack, 
                              locations="Country Code", 
                              color="Amount", 
                              hover_name="Country Name", 
                              size="Amount",
                              #set animation column
                              animation_frame="Year",
                              color_continuous_scale=px.colors.sequential.Aggrnyl,
                              projection="natural earth")
outbound_map
#plotly.offline.plot(outbound_map, filename="outbound_map")


# In[37]:


#find the top countries with the attract tourists most
top_country_outbound = outbound_tourists_clean.sort_values("2017", ascending=False).head(10)
top_outbound_country_list = list(top_country_outbound.index)
top_outbound_country_list 


# In[38]:


top_outbound_data = outbound_tourists_stack.loc[outbound_tourists_stack['Country Name'].isin(top_outbound_country_list)]
top_outbound_data.head()


# In[39]:


#make the line plot for top outbound countries
outbound_top = px.line(top_outbound_data,
                       #x axis column
                       x="Year",
                       #y axis column
                       y="Amount", 
                       color="Country Name", 
                       line_group="Country Name", 
                       hover_name="Country Name",
                       #line type
                       line_shape="linear",
                       title="Top countries where people like to travel")
outbound_top
#plotly.offline.plot(outbound_top, filename="outbound_top")


# # Relationship between population and the number of outbound tourists

# In[40]:


#import the population data set
population = pd.read_excel("travel_data.xls", sheet_name="population", header=3, index_col=0)
population.head()


# In[41]:


#use "data_selection" function to select population data set
population_clean = data_selection(population)
population_clean.head()


# In[42]:


#def a function concate the population data with outbound tourists data
def population_outbound(year):
    df1 = population_clean.loc[population_clean.index.isin(top_outbound_country_list)].loc[:,year]
    df2 = outbound_tourists_clean.loc[outbound_tourists_clean.index.isin(top_outbound_country_list)].loc[:,year]
    df = pd.concat([df1, df2], axis=1)
    return df


# In[43]:


population_outbound("2017")


# In[44]:


#make the line-bar plot
#make the scatter plot
trace1=go.Scatter(
    x=population_outbound("2017").index,
    y=population_outbound("2017").iloc[:,0],
    name="population")
#make the bar plot
trace2=go.Bar(
    x=population_outbound("2017").index,
    y=population_outbound("2017").iloc[:,1],
    name="tourists",
    yaxis="y2",
    #transparent level
    opacity=0.6,
    #bar wide
    width=[0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5])
data=[trace1,trace2]
layout=go.Layout(
    title="Outbound tourists number vs country's population",
    yaxis=dict(title="population"),
    yaxis2=dict(title="number of people", 
                titlefont=dict(color="rgb(148, 103, 189)"),
                tickfont=dict(color="rgb(148, 103, 189)"),
                overlaying="y",
                side="right"))
outbound_population_compare=go.Figure(data=data, layout=layout)
py.iplot(outbound_population_compare)
#plotly.offline.plot(outbound_population_compare, filename="outbound_population_compare")


# In[45]:


#merge the outbound tourists data and gdp data
gdp_outbound = outbound_tourists_stack.merge(gdp_data, left_on=("Country Name","Year"), right_on=("Country Name","Year"))
gdp_outbound.head()


# In[46]:


#make the scatter plot to check the relationship between tourists number and GDP
gdp_outbound_plot = px.scatter(gdp_outbound, 
                               x="Amount", 
                               y="GDP",  
                               hover_name="Country Name",
                               #use log data to make the plot
                               log_x=True, 
                               log_y=True,
                               title="Correlation between GDP and outbound tourists")
gdp_outbound_plot
#plotly.offline.plot(gdp_outbound_plot, filename="gdp_outbound_plot")


# In[47]:


#import expenditure data set
expenditure = pd.read_excel("travel_data.xls", sheet_name="expenditure for travel item", header=3, index_col=0)
expenditure_clean = data_selection(expenditure)
expenditure_clean.head()


# In[48]:


#calculate the per capita data 
expenditure_p = expenditure_clean.iloc[:,1:12]/outbound_tourists_clean.iloc[:,1:12]
#drop nan, inf rows
expenditure_p = expenditure_p[~expenditure_p.isin([np.nan, np.inf, -np.inf]).any(1)]
expenditure_p.head()


# In[49]:


#select the top countries' data 
top_expenditure_p_data = expenditure_p.loc[expenditure_p.index.isin(top_outbound_country_list)].sort_values("2017", ascending=False)
top_expenditure_p_data.head()


# In[50]:


#reshape the top_expenditure_p_data data frame
top_expenditure_p_stack = top_expenditure_p_data.stack().reset_index()
top_expenditure_p_stack = top_expenditure_p_stack.rename(columns = {"level_1":"Year",0:"Per capita expenditure"})
top_expenditure_p_stack.head()


# In[51]:


#make the bar plot of the top countries' people with highest spending in the travel
expenditure_bar = px.bar(top_expenditure_p_stack, 
                         x="Year", 
                         y="Per capita expenditure", 
                         color="Country Name", 
                         hover_name="Country Name",
                         title="Top countries per capita expenditure in travel(exclude international transportation)")
expenditure_bar
#plotly.offline.plot(expenditure_bar, filename="expenditure_bar")


# In[ ]:




