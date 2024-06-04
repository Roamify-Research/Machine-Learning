import streamlit as st
import pandas as pd
import pymysql

hostname = 'sql12.freesqldatabase.com'
user = 'sql12711667'
password = 'vmrGDRbZvm'

db = pymysql.connections.Connection(
    host = hostname,
    user = user,
    password = password,
)

cursor = db.cursor()
cursor.execute('use sql12711667;')
db.commit()

def main_page():
    st.markdown("<h1 style='text-align: center;'>Roamify</h1>", unsafe_allow_html=True)
    st.sidebar.title('Navigation')
    page = st.sidebar.radio('Go to', ['Home','Add User Ratings'])
    if page == 'Add User Ratings':
        add_user_streamlit_page()
    elif page == 'Home':
        recommendation_page()

def recommendation_page():
    st.write('Disabled for now!')
    # attractions_data, user_ratings_data = load_predicted_data()
    # st.markdown("<h3 style='text-align: center;'>Tourist Attraction Recommendation System</h3>", unsafe_allow_html=True)

    # state = st.selectbox('Select State', attractions_data['State'].unique())

    # number_of_attractions = st.number_input('Number of Attractions', min_value=1, max_value=20, value=5, step=1)

    # user = st.text_input('Enter your name')

    # if st.button('Get Recommendations'):
    #     recommendations, message = get_recommendations(state, number_of_attractions, user)
    #     if recommendations == []:
    #         st.write(message)
    #     else:
    #         st.write(f"Top {number_of_attractions} attractions in {state} for {user}:")
    #         for rec in recommendations:
    #             st.write(f"**Attraction name:** {rec['Name']}")
    #             st.write(f"**City:** {rec['City']}")
    #             st.write(f"**Opening Hours:** {rec['Opening Hours']}")
    #             st.write(f"**Description:** {rec['Description']}")
    #             st.write("***************************************************")

    # if st.checkbox('Show Raw Data'):
    #     if user in user_ratings_data.columns:
    #         st.write('Attractions and User Ratings Data')
    #         user_ratings_data = load_user_data(user)
    #         st.dataframe(user_ratings_data)
    #     else:
    #         st.warning(f"User {user} not found in the database. Please add user first.")

def add_user_streamlit_page():
    cursor.execute(f"SELECT Attractions, State, Country FROM user_ratings;")
    attractions_data = cursor.fetchall()
    attractions_data = pd.DataFrame(attractions_data, columns=['Name', 'State', 'Country'])

    st.markdown("<h3 style='text-align: center;'>Adding User Ratings</h3>", unsafe_allow_html=True)
    state_ = st.selectbox('Select State', attractions_data['State'].unique())
    new_user = st.text_input('Enter your name')
    if new_user != "":
        cursor.execute(f"SHOW COLUMNS FROM user_ratings LIKE '{new_user}';")
        if cursor.fetchone() is None:
            cursor.execute(f"ALTER TABLE user_ratings ADD COLUMN {new_user} int default 0;")
            db.commit()

        available_attractions = attractions_data[attractions_data['State'] == state_]['Name'].tolist()
        with st.form(key='ratings_form'):
            st.write('Rate the attractions you have visited:')
            for attraction in available_attractions:
                cursor.execute(f"select {new_user} from user_ratings where Attractions = '{attraction}';")
                existing_rating = cursor.fetchone()[0]
                rating = st.slider(f'{attraction}', min_value=0, max_value=5, value=existing_rating, step=1, key=f'rating_{attraction}')

                if rating > 0:
                    cursor.execute(f"update user_ratings set {new_user} = {rating} where Attractions = '{attraction}';")
                    db.commit()
        if st.form_submit_button('Submit Ratings'):
            st.success('Ratings submitted successfully!')
if __name__ == "__main__":
    main_page()