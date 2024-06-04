import gspread, pandas as pd, streamlit as st, toml

st.markdown("<h1 style='text-align: center;'>Roamify</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center;'>Adding User Ratings</h3>", unsafe_allow_html=True)


spreadsheet_id = "1gCvF2PfMQpp1cVsbSpfzTG8ShN5GAktQ2kY8iLUb7mI"
scopes = ["https://spreadsheets.google.com/feeds",
         "https://www.googleapis.com/auth/drive"]

service_account_info = st.secrets["gcp_service_account"]

gc = gspread.service_account_from_dict(service_account_info, scopes=scopes)
sh = gc.open_by_key(spreadsheet_id)
worksheet = sh.worksheet("Attractions")
data = worksheet.get_all_values()
attractions_data = pd.DataFrame(data[1:], columns = data[0])

state_ = st.selectbox('Select State', attractions_data['State'].unique())
new_user = st.text_input('Enter your name')

if new_user != "":
    if new_user not in attractions_data.columns:
        attractions_data[new_user] = 0

    available_attractions = attractions_data[attractions_data['State'] == state_]['Name'].tolist()
    with st.form(key='ratings_form'):
        st.write('Rate the attractions you have visited:')
        for attraction in available_attractions:
            existing_rating = attractions_data.loc[attractions_data['Name'] == attraction, new_user].values[0]

            rating = st.slider(f'{attraction}', min_value=0, max_value=5, value=int(existing_rating), step=1, key=f'rating_{attraction}')
            if rating != existing_rating:
                 attractions_data.loc[attractions_data['Name'] == attraction, new_user] = rating
        
        submit_button = st.form_submit_button('Submit Ratings')
    if submit_button:
        st.success('Ratings submitted successfully!')
        worksheet.clear()
        worksheet.update([attractions_data.columns.values.tolist()] + attractions_data.values.tolist())
        st.write("Data updated successfully!")
