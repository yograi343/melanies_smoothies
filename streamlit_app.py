# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col

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
my_dataframe =session.table("SMOOTHIES.PUBLIC.FRUIT_OPTIONS").select(col('FRUIT_NAME'))
#st.dataframe(data=my_dataframe,use_container_width=True)

ingredientlist = st.multiselect(
    'Choose up to 5 ingredients: ',
    my_dataframe
    ,max_selections=5
)
if ingredientlist:
    ingredients_string =''
    for fruit_chosen in ingredientlist:
        ingredients_string +=fruit_chosen+' '
    st.write(ingredients_string)

    my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order) 
        values ('""" + ingredients_string + """','""" + name_on_order + """')"""
    #st.write(my_insert_stmt)
    time_to_insert = st.button('Submit Order')

    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered!', icon="✅")

    # new section to display fruityvise nutrition information
import requests
fruityvice_response = requests.get('https://fruityvise.com/api/fruit/watermelon')
st.text(fruityvice_response)
    
