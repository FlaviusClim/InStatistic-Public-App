import streamlit as st
import instaloader
import json
import re
import pandas as pd
import altair as alt
from collections import Counter
# from datetime import datetime


def authenticate_instagram(login_username, password):
    """This function check if the authentication process on instagram was successful or not"""

    L = instaloader.Instaloader()
    try:
        L.load_session_from_file(login_username)
        print("Session loaded succesfully")
    except FileNotFoundError:
        try:
            L.context.log_in(login_username, password)
            L.save_session_to_file()
            return True
        except Exception as e:
            print(f"Failed to log in: {e}")
            return False
    return True


def get_profile_info(username):
    """Here, the app will get all details and information about the username specified"""

    L = instaloader.Instaloader()
    profile = instaloader.Profile.from_username(L.context, username)

    profile_info = {
        'username': profile.username,
        'full_name': profile.full_name,
        'biography': profile.biography,
        's': profile.biography_hashtags,
        'followers': profile.followers,
        'following': profile.followees,
        'posts': profile.mediacount,
        'external_url': profile.external_url,
        'verified': profile.is_verified,
        'profile_pic_url': profile.profile_pic_url
    }

    return profile_info


def get_hashtags_from_posts(profile):
    """This function obtain all hashtags used by profile[username]"""

    L = instaloader.Instaloader()
    hashtags = []
    for post in profile.get_posts():
        caption = post.caption
        if caption:
            hashtags.extend(re.findall(r'#(\w+)', caption))
    return hashtags


def get_top_10_hashtags(username):
    """Get top 10 hashtags function will sort first 10 # used considering number of uses"""

    L = instaloader.Instaloader()
    profile = instaloader.Profile.from_username(L.context, username)
    hashtags = get_hashtags_from_posts(profile)
    top_10_hashtags = Counter(hashtags).items()
    top_10_hashtags = sorted(top_10_hashtags, key=lambda x: x[1], reverse=True)[:10]
    return top_10_hashtags


def get_posts_per_month(username):
    """Here we will calculate the amount of posts per month"""

    L = instaloader.Instaloader()
    profile = instaloader.Profile.from_username(L.context, username)
    posts_per_month = {}

    for post in profile.get_posts():
        month_year = post.date.strftime('%Y-%m')
        if month_year in posts_per_month:
            posts_per_month[month_year] += 1
        else:
            posts_per_month[month_year] = 1

    return posts_per_month


def get_engagement_rate(username):
    """Get engagement rate will calculate important metrics about instagram profile engagement"""

    engagement_rate = 0
    total_likes = 0
    total_comments = 0
    highest_eng_hour = ''
    highest_engagement = 0

    L = instaloader.Instaloader()
    profile = instaloader.Profile.from_username(L.context, username)

    for post in profile.get_posts():
        total_likes += post.likes
        total_comments += post.comments

    post_engagement = total_comments + total_likes
    engagement_rate = post_engagement / profile.followers * 0.1

    if post_engagement > highest_engagement:
        highest_engagement = post_engagement
        highest_eng_hour = post.date.strftime('%H:%M')

    return engagement_rate, total_likes, total_comments, highest_eng_hour


if __name__ == "__main__":
    st.set_page_config(
        page_title="InStatistic",
        page_icon= ":chart_with_upwards_trend:"
    )

    st.title('InStatistic')
    st.caption('InStatistic will help you to find useful information from your instagram competitors')
    st.subheader('How to use?')
    st.caption('Login to your Instagram account with username and password')
    st.caption('Enter the instagram username of the profile you want to scrape in "Search Section"')
    st.caption('Press "Get Profile Info" button')
    st.caption('Let the App do the magic')

    st.sidebar.header('Instagram Login')
    with st.sidebar.form(key='login_form'):
        login_username = st.text_input('Enter your Instagram Username')
        login_password = st.text_input('Enter your Instagram Password', type='password')
        login_button = st.form_submit_button('Login')

    if login_button:
        if authenticate_instagram(login_username, login_password):
            st.sidebar.success("Successfully logged in")
        else:
            st.sidebar.error("Failed to log in. Check your credentials and try again.")

    st.sidebar.caption('Search Section')

    with st.sidebar.form(key='profile_form'):
        username = st.text_input(label='Enter Instagram Username you want to scrape')
        submit_button = st.form_submit_button(label='Get Profile Info')

    st.sidebar.caption('Result Summary Section')

    if submit_button:
        try:
            profile_info = get_profile_info(username)
            st.sidebar.image(profile_info['profile_pic_url'], use_column_width=True)

            st.sidebar.write(f"Username: {profile_info['username']}")
            st.sidebar.write(f"Full Name: {profile_info['full_name']}")
            st.sidebar.write(f"Biography: {profile_info['biography']}")
            st.sidebar.write(f"Followers: {profile_info['followers']}")
            st.sidebar.write(f"Following: {profile_info['following']}")
            st.sidebar.write(f"Posts: {profile_info['posts']}")

            with open(f'{username}_profile_info.json', 'w') as json_file:
                json.dump(profile_info, json_file)

            top_10_hashtags = get_top_10_hashtags(username)
            hashtags_df = pd.DataFrame(top_10_hashtags, columns=['Hashtag', 'Count'])

            st.subheader(f'Top 10 Hashtags used by {username}')
            # st.dataframe(hashtags_df.T)

            chart = alt.Chart(hashtags_df).mark_bar().encode(
                x='Count:Q',
                y=alt.Y('Hashtag:N', sort='-x'),
                tooltip=['Hashtag', 'Count']
            ).properties(
                width=600,
                height=300
            )
            st.altair_chart(chart)

            posts_per_month = get_posts_per_month(username)
            posts_per_month_df = pd.DataFrame(posts_per_month.items(), columns=['Month', 'Posts'])

            st.subheader(f'Number of posts per month')
            chart = alt.Chart(posts_per_month_df).mark_bar().encode(
                x='Posts:Q',
                y=alt.Y('Month:N', sort='-x'),
                tooltip=['Month', 'Posts']
            ).properties(
                width=600,
                height=300
            )
            st.altair_chart(chart)


            engagement_rate, total_likes, total_comments, highest_eng_hour = get_engagement_rate(username)
            st.subheader('Engagement Rate')

            col1, col2, col3, col4 = st.columns(4)
            col1.metric(label='Total Engagement Rate', value=f'{engagement_rate:.2f}')
            col2.metric(label='Highest Engagement Hour', value=highest_eng_hour)
            col3.metric(label='Total Likes', value=total_likes)
            col4.metric(label='Total Comments', value=total_comments)

        except Exception as e:
            st.error(f"Failed to get profile info: {e}")