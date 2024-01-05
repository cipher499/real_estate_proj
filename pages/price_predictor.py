import streamlit as st
import pickle

st.set_page_config(page_title="Viz Demo")
st.title('Page 2')

with open('df.pkl', 'rb') as file:
    df = pickle.load(file)


# ['property_type', 'sector', 'bedrooms', 'bathrooms', 'balconies',
#        'age_possession', 'built_up_area', 'study room', 'servant room',
#        'store room', 'furnishing_type', 'luxury_category', 'floor_category']

st.dataframe(df)

st.header('Enter your inputs')


property_type = st.selectbox('Property Type', ['flat', 'house'])
sector = st.selectbox('Sector', sorted(df.sector.unique().tolist()))
bedrooms = float(st.selectbox('Bedrooms', sorted(df.bedrooms.unique().tolist())))
bathrooms = float(st.selectbox('Bathrooms', sorted(df.bathrooms.unique().tolist())))
balconies = st.selectbox('Balconies', sorted(df.balconies.unique().tolist()))
property_age = st.selectbox('Property Age', sorted(df.age_possession.unique().tolist()))
built_up_area = float(st.number_input('Built-up Area'))
study_room = float(st.selectbox('Study Room', ['0.0', '1.0']))
servant_room = float(st.selectbox('Servant Room', ['0.0', '1.0']))
store_room = float(st.selectbox('Store Room', ['0.0', '1.0']))
furnishing_type = st.selectbox('Furnishing Type', sorted(df.furnishing_type.unique().tolist()))
luxury_type = st.selectbox('Luxury Type', sorted(df.luxury_category.unique().tolist()))
floor = st.selectbox('Floor', sorted(df.floor_category.unique().tolist()))

