import streamlit as st
from recommendations_streamlit import get_recommendations, load_data, load_user_data

attractions_data, user_ratings_data = load_data()

st.markdown("<h1 style='text-align: center;'>Roamify</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center;'>Tourist Attraction Recommendation System</h3>", unsafe_allow_html=True)

state = st.selectbox('Select State', attractions_data['State'].unique())

number_of_attractions = st.number_input('Number of Attractions', min_value=1, max_value=20, value=5, step=1)

user = st.selectbox('Select User', user_ratings_data.columns[1:]) 

if st.button('Get Recommendations'):
    recommendations, message = get_recommendations(state, number_of_attractions, user)
    
    if message:
        st.warning(message)

    st.write(f"<h3>Top {number_of_attractions} attractions in {state} for {user}:</h2>", unsafe_allow_html=True)
    st.write("***************************************************")
    for rec in recommendations:
        st.write(f"**Attraction name:** {rec['Name']}")
        st.write(f"**City:** {rec['City']}")
        st.write(f"**Opening Hours:** {rec['Opening Hours']}")
        st.write(f"**Description:** {rec['Description']}")
        st.write("***************************************************")

if st.checkbox('Show Raw Data'):
    st.write('Attractions and User Ratings Data')
    user_ratings_data = load_user_data(user)
    st.dataframe(user_ratings_data)