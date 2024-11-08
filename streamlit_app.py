# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col

# Write directly to the app
st.title("🥤 Customize Your Smoothie! 🥤")
st.write("Choose the fruits you want in your custom Smoothie!")

# Create Snowflake session and get data
session = get_active_session()
my_dataframe = session.table("smoothies.public.fruit_options")

# Check the available columns
columns = my_dataframe.columns
st.write(f"Available columns: {columns}")

cnx = st.connection("snowflake")
session = snx.session()

# Correct the column name based on the available columns
fruit_options = my_dataframe.to_pandas()['fruit'].tolist()  # Adjusted column name

# Ingredients selection with multiselect
ingredients_list = st.multiselect(
    'Choose up to 5 ingredients:',
    fruit_options,  # Use the list of fruits as options
    max_selections=5  # Restrict to 5 selections
)

# Create the ingredients string
if ingredients_list:
    ingredients_string = ", ".join(ingredients_list)  # Join the selected fruits into a string

    # Insert into the orders table
    my_insert_stmt = f"""
        INSERT INTO smoothies.public.orders (ingredients)
        VALUES ('{ingredients_string}')
    """

    # Execute the insert statement
    session.sql(my_insert_stmt).collect()

    st.success('Your Smoothie is ordered!', icon="✅")
else:
    st.warning("Please select at least one ingredient before submitting your order.")
