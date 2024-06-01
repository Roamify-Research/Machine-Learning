import streamlit as st
from recommendations_streamlit import get_recommendations, load_data, load_user_data

attractions_data, user_ratings_data = load_data()

st.markdown("<h1 style='text-align: center;'>Roamify</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center;'>Tourist Attraction Recommendation System</h3>", unsafe_allow_html=True)

state = st.selectbox('Select State', attractions_data['State'].unique())

number_of_attractions = st.number_input('Number of Attractions', min_value=1, max_value=20, value=5, step=1)

user = st.text_input('Enter your name')

available_attractions = attractions_data[attractions_data['State'] == state]['Name'].tolist()
user_ratings = {}
st.write('Rate the attractions you have visited:')
for attraction in available_attractions:
    rating = st.slider(f'{attraction}', min_value=0, max_value=5, step=1)
    if rating > 0:
        user_ratings[attraction] = rating

if st.button('Get Recommendations'):
    recommendations, message = get_recommendations(state, number_of_attractions, user, user_ratings)
    
    if message:
        st.warning(message)

    st.write(f"Top {number_of_attractions} attractions in {state} for {user}:")
    for rec in recommendations:
        st.write(f"**Attraction name:** {rec['Name']}")
        st.write(f"**City:** {rec['City']}")
        st.write(f"**Opening Hours:** {rec['Opening Hours']}")
        st.write(f"**Description:** {rec['Description']}")
        st.write("***************************************************")

if st.checkbox('Show Raw Data'):
    st.write('Attractions Data')
    st.dataframe(attractions_data)
    # st.write('User Ratings Data')
    # st.dataframe(user_ratings_data)