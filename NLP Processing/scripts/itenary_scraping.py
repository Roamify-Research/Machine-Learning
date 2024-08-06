itenary  = """

*Day 1: India Gate, Lotus Temple*

•⁠  ⁠Morning: Start your day at India Gate (9:00 am - 10:30 am), which is located in the heart of New Delhi. Take some time to admire the monument and the eternal flame that burns nearby.
•⁠  ⁠Afternoon: Head over to the Lotus Temple (11:00 am - 1:00 pm), a beautiful Bahá'í House of Worship. This temple is known for its stunning architecture and serene surroundings.
•⁠  ⁠Evening: Take some time to relax at your hotel or explore the local market near the temple.

*Day 2: Akshardham Temple, Hauz Khas*

•⁠  ⁠Morning: Visit the Akshardham Temple (9:00 am - 11:30 am), a magnificent Hindu temple that is dedicated to Lord Swaminarayan. Be sure to catch the evening light and sound show, which is absolutely breathtaking.
•⁠  ⁠Afternoon: Head over to Hauz Khas (2:00 pm - 4:30 pm), a historic village that is known for its beautiful Mughal-era architecture and tranquil surroundings. Take some time to explore the complex and visit the mosque and reservoir.

*Day 3: Chandni Chowk, Lodhi Gardens*

•⁠  ⁠Morning: Start your day at Chandni Chowk (9:00 am - 11:30 am), a bustling market that is known for its street food, local shops, and historic significance.
•⁠  ⁠Afternoon: Visit the Lodhi Gardens (2:00 pm - 4:30 pm), a beautiful Mughal-era garden that is known for its intricate architecture and peaceful surroundings. Take some time to relax and enjoy the serene atmosphere.

*Day 4: Humayun's Tomb, Jama Masjid*

•⁠  ⁠Morning: Visit Humayun's Tomb (9:00 am - 11:30 am), a beautiful Mughal-era mausoleum that is known for its stunning architecture.
•⁠  ⁠Afternoon: Head over to the Jama Masjid (2:00 pm - 4:30 pm), the largest mosque in India, which is known for its peaceful and tranquil surroundings. Take some time to admire the intricate architecture of this historic monument.

*Day 5: Leisure day*

•⁠  ⁠Take some time to relax at your hotel or explore the local market.
•⁠  ⁠If you have any last-minute sightseeing plans, now is a good time to fit them in.

This itinerary should give you a good balance of history, culture, and relaxation. Enjoy your trip!"""


import nltk
import re
from nltk.tokenize import sent_tokenize, word_tokenize

nltk.download('punkt')

days_dict = {}

# Use regular expression to find all day headings and their respective content
matches = re.findall(r'\*([^*]+)\*\n(.*?)(?=\n\*|$)', itenary, re.DOTALL)

# Iterate over matches and store them in the dictionary
for match in matches:
    day, content = match
    days_dict[day.strip()] = content.strip()

itenary_dict = {}
# Display the dictionary
for i in days_dict:
    itenary_dict[i] = []
    for j in days_dict[i].split("\n"):
        itenary_dict[i].append(j.replace("•⁠  ⁠", "").strip())

print(itenary_dict)