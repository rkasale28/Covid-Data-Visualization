import streamlit as st
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
import matplotlib.pyplot as plt
import random
import numpy as np

def purple_color_func(word=None, font_size=None, position=None, orientation=None, random_state=None,
                    **kwargs):
    return "hsl(285, 100%%, %d%%)" % random.randint(20, 90)

def blue_color_func(word, font_size, position, orientation, random_state=None,
                    **kwargs):
    return "hsl(240, 100%%, %d%%)" % random.randint(20, 90)

def pink_color_func(word, font_size, position, orientation, random_state=None,
                    **kwargs):
    return "hsl(30, 100%%, %d%%)" % random.randint(20, 90)

def generateWordCloud(text,color_function):
    # Create and generate a word cloud image:
    wordcloud = WordCloud(
        stopwords=STOPWORDS,
        max_words=35,
        background_color='black',
        width=1000,
        height=600,
        margin=10
    ).generate(text)

    plt.imshow(wordcloud.recolor(color_func=color_function, random_state=3),
               interpolation="bilinear")
    plt.axis("off")
    plt.show()
    st.pyplot()

# Create some sample text
text = 'Mumbai Metropolitan Region Development Authority (MMRDA), which is constructing Metro projects, has begun to receive offers from private parties for foot over bridges between stations and their properties for exclusive access to their patrons, residents and employees. So far, MMRDA has received four offers from various developers. Two of the proposals that have received its approval are for Metro-VII line along the Western Express Highway from Andheri to Dahisar. The line is expected to open in May 2021. Additional metropolitan commissioner Sonia Sethi said, “The two parties which have received approval are Oberoi Realty (for connectivity from Oberoi Mall to Aarey station) and S D Corporation (for link between Poisar station and some residential as well as commercial properties).” Work will commence after MMRDA approves the designs. Sethi said, “The cost of constructing a bridge will be borne by the private establishment.” MMRDA said it is a win-win situation for the establishments as well as the Metro network. An MMRDA official said, “It will help decongest the road network outside such crowded establishments. Due to the pandemic, currently more developers are not showing an interest but we are sure of a response once the situation normalizes.” Commuters have welcomed the initiative as roads outside major malls have become bottleneck points. Evershine Nagar resident Mahesh Shah said. “There is huge traffic outside InOrbit Mall on Link Road. Access to the Metro corridor directly from the mall will help reduce congestion. There will be less public on the road and autorickshaws and private cars will not clutter it.” Ghatkopar resident K G Gaikwad said, “There is a lot jaywalking on the road outside R-City Mall. The Metro will be a boon for residents using L B S Road.”'
generateWordCloud(text, purple_color_func)

text = 'The CBSE axed chapters on secularism, democractic rights, federalism, gender, religion and caste from the syllabus. The chapter on demonetisation was removed from class 12 business studies books. The decision drew flak from various stakeholders. The government was criticised for removing these chapters and opposition parties denounced the move as being part of a “bigger conspiracy”. Sitaram Yechury, of the CPIM, termed the decision atrocious. “Using the pandemic, the Modi government is deleting sections dealing with India\'s diversity, plurality, democracy etc that uphold our Constitutional values,” he tweeted. Responding to the criticism, the CBSE claimed the dropped topics would be covered in the rationalised syllabus or in the alternative academic calendar-- a calendar designed specifically to aid learning in the pandemic. In a circular released on July 8, it said, “Schools have been directed to follow the Alternative Academic Calendar prepared by NCERT for transacting the curriculum. Therefore, each of the topics that has been wrongly mentioned in the media as deleted has been covered under Alternative Academic Calendar of NCERT, which is already on force for all the affiliated schools of Board.” However, in his same tweet thread on July 7, Pokhriyal mentioned that he had sought suggestions from academics on reducing the syllabus and received over 1,500 of them. The transfer of the RTI application and the response to it beg the question: were educationists actually consulted about the deletion of chapters from the CBSE syllabus? If they were, why does the NCERT not have information about this? The only other possible explanation is that the ministry and the NCERT have deliberately withheld information, in violation of the RTI Act.'
generateWordCloud(text, blue_color_func)

text = 'Mumbai and its suburbs received moderate showers with intense spells recorded in isolated areas between Saturday night and Sunday morning. Overnight showers made it the strongest spell of rainfall in September. The India Meteorological Department (IMD) had predicted a revival of active monsoon conditions over Mumbai over the weekend. Between 8.30 am on Saturday and 8.30 am on Sunday, the Santacruz weather observatory, representative of Mumbai and its suburbs, recorded 25.7 millimetres (mm) of rain and 16.4 mm was recorded at Colaba, which covers south Mumbai. Intense rainfall was recorded between 12.30 am and 5.30 am Sunday. Neighbouring Thane district recorded 22.8 mm of rain. Over 24 hours, a location-wise distribution showed many areas in the Mumbai Metropolitan Region (MMR) recorded between 20 mm and 40 mm of rainfall. The highest rainfall was recorded in parts of the western and eastern suburbs. The area around the Chhatrapati Shivaji Maharaj International Airport recorded 55 mm of rainfall, while Chembur and Navi Mumbai received 47.2 mm and 41.2 mm, respectively. The IMD said light to moderate rain with the possibility of occasional intense spells would continue on Sunday. “Factors such as the formation of a low-pressure weather system of west-central Bay of Bengal off the coast of Andhra Pradesh, an upper air cyclonic circulation over Maharashtra coast and associated systems such as an offshore trough from north Maharashtra to Kerala have allowed the revival of active monsoon conditions for Konkan and interior Maharashtra. Moderate to heavy rain is likely to continue for the next 24 hours,” said KS Hosalikar, deputy director-general, western region, IMD. Over the past 24 hours, the highest rain was recorded in Ratnagiri at 40 mm, followed by Vengurla in Sindhudurg (30.4 mm), Matheran (28.4 mm), and Mahabaleshwar (26.2 mm). Maharashtra has recorded 13% excess rainfall between June 1 and September 13. South Mumbai and suburban Mumbai received 59% and 57% of excess rainfall, respectively. The rainfall received by suburban Mumbai is the highest for any district along the Konkan coast during this monsoon season.'
generateWordCloud(text, pink_color_func)

# mask=imread('C:\\Users\\Rohit\\Documents\\Interview\\Selected_Students\\img\\maharastra_map.png'),
