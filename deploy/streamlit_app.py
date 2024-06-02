import streamlit as st
from recommendations_streamlit import get_recommendations, load_data, load_user_data, add_user_ratings, search_user_ratings, load_predicted_data

def main_page():
    st.markdown("<h1 style='text-align: center;'>Roamify</h1>", unsafe_allow_html=True)
    st.sidebar.title('Navigation')
    page = st.sidebar.radio('Go to', ['Home','Add User Ratings'])
    if page == 'Add User Ratings':
        add_user_streamlit_page()
    elif page == 'Home':
        recommendation_page()

def recommendation_page():
    attractions_data, user_ratings_data = load_predicted_data()
    st.markdown("<h3 style='text-align: center;'>Tourist Attraction Recommendation System</h3>", unsafe_allow_html=True)

    state = st.selectbox('Select State', attractions_data['State'].unique())

    number_of_attractions = st.number_input('Number of Attractions', min_value=1, max_value=20, value=5, step=1)

    user = st.text_input('Enter your name')

    if st.button('Get Recommendations'):
        recommendations, message = get_recommendations(state, number_of_attractions, user)
        if recommendations == []:
            st.write(message)
        else:
            st.write(f"Top {number_of_attractions} attractions in {state} for {user}:")
            for rec in recommendations:
                st.write(f"**Attraction name:** {rec['Name']}")
                st.write(f"**City:** {rec['City']}")
                st.write(f"**Opening Hours:** {rec['Opening Hours']}")
                st.write(f"**Description:** {rec['Description']}")
                st.write("***************************************************")

    if st.checkbox('Show Raw Data'):
        if user in user_ratings_data.columns:
            st.write('Attractions and User Ratings Data')
            user_ratings_data = load_user_data(user)
            st.dataframe(user_ratings_data)
        else:
            st.warning(f"User {user} not found in the database. Please add user first.")

def add_user_streamlit_page():
    attractions_data, user_ratings_data = load_data()
    st.markdown("<h3 style='text-align: center;'>Adding User Ratings</h3>", unsafe_allow_html=True)
    state_ = st.selectbox('Select State', attractions_data['State'].unique())
    new_user = st.text_input('Enter your name')

    new_user_ratings = {}
    available_attractions = attractions_data[attractions_data['State'] == state_]['Name'].tolist()
    with st.form(key='ratings_form'):
        st.write('Rate the attractions you have visited:')
        for attraction in available_attractions:
            existing_rating = float(search_user_ratings(new_user, attraction))
            rating = st.slider(f'{attraction}', min_value=0.0, max_value=5.0, value=existing_rating, step=0.1, key=f'rating_{attraction}')

            if rating > 0:
                new_user_ratings[attraction] = rating
    
        if st.form_submit_button('Submit Ratings'):
            add_user_ratings(new_user_ratings, new_user)
            st.success('Ratings submitted successfully!')

if __name__ == "__main__":
    main_page()