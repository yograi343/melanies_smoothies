# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col
import requests
import pandas as pd

# Write directly to the app
st.title("My Parents New Healthy Diner")
st.subheader('Breakfast Menu')
st.write('Omega 3 & Blueberry Oatmeal')
st.write('Kale, Spinach & Rocket Smoothie')
st.write('Hard-Boiled Free-Range Engg')
st.write(
    """Choose the fruits you want in your custom Smoothie!
    """
)

name_on_order = st.text_input('Name on Smoothie')
st.write('The name on your Smoothie will be', name_on_order)
# creating a snowpark session
cnx = st.connection('snowflake')
session = cnx.session()
#loading the Data frame
my_dataframe =session.table("SMOOTHIES.PUBLIC.FRUIT_OPTIONS").select(col('FRUIT_NAME'),col('search_on'))
#st.dataframe(data=my_dataframe,use_container_width=True)
pd_df = my_dataframe.to_pandas()

ingredientlist = st.multiselect(
    'Choose up to 5 ingredients: ',
    my_dataframe
    ,max_selections=5
)
if ingredientlist:
    ingredients_string =''
    for fruit_chosen in ingredientlist:
        ingredients_string +=fruit_chosen+' '

        search_on = pd_df.loc[pd_df['FRUIT_NAME']==fruit_chosen,'search_on'].iloc[0]
        st.write('The search value for',fruit_chosen,' is ', search_on,'.')
        
        st.subheader(fruit_chosen + ' Nutrition Information')
        fruityvice_response = requests.get("https://fruityvice.com/api/fruit/"+fruit_chosen)
        fv_df = st.dataframe(data= fruityvice_response.json(),use_container_width=True)

    my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order) 
        values ('""" + ingredients_string + """','""" + name_on_order + """')"""
    #st.write(my_insert_stmt)
    time_to_insert = st.button('Submit Order')

    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered!', icon="✅")




    
