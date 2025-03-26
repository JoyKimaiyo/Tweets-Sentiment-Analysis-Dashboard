import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from wordcloud import WordCloud

# Streamlit Title
st.title("Sentiment Analysis Dashboard")

st.markdown("A sentiment analysis job about the problems of each major U.S. airline. Twitter data was scraped from February of 2015 and contributors were asked to first classify positive, negative, and neutral tweets, followed by categorizing negative reasons such as late flight or rude service")

# Sidebar Header
st.sidebar.title("Twitter US Airline Sentiment Analysis")

# File Path
csv_path = "/home/joy/Documents/app/tweets.csv"

# Load Data
@st.cache_data
def load_data():
    df = pd.read_csv(csv_path, encoding="utf-8")
    df["tweet_coord"] = df["tweet_coord"].astype(str)
    df["latitude"] = df["tweet_coord"].apply(lambda x: eval(x)[0] if x != "nan" and x != "None" else None)
    df["longitude"] = df["tweet_coord"].apply(lambda x: eval(x)[1] if x != "nan" and x != "None" else None)
    return df

df = load_data()
df = df.dropna(subset=["latitude", "longitude"])

# Sidebar - Random Tweet by Sentiment
st.sidebar.subheader("Show Random Tweet")
selected_sentiment = st.sidebar.radio("Sentiment", ("positive", "negative", "neutral"))
if selected_sentiment:
    filtered_df = df[df["airline_sentiment"] == selected_sentiment]
    if not filtered_df.empty:
        random_tweet = filtered_df.sample(n=1)["text"].values[0]
        st.sidebar.success(random_tweet)
    else:
        st.sidebar.warning("No tweets found for this sentiment.")

# Sidebar - Number of Tweets per Sentiment
st.sidebar.subheader("Select Visualization Type")
viz_type = st.sidebar.selectbox("Choose Visualization", ('Histogram', 'Pie Chart'))

# Tweet Count by Sentiment
sentiment_count = df["airline_sentiment"].value_counts().reset_index()
sentiment_count.columns = ["Sentiment", "Count"]

# Sentiment Distribution
st.subheader("Sentiment Distribution")
if viz_type == "Histogram":
    fig = px.bar(sentiment_count, x="Sentiment", y="Count", color="Sentiment", title="Sentiment Distribution",
                 color_discrete_sequence=px.colors.qualitative.Plotly)
    st.plotly_chart(fig)
elif viz_type == "Pie Chart":
    fig = px.pie(sentiment_count, names="Sentiment", values="Count", title="Sentiment Distribution",
                 color_discrete_sequence=px.colors.qualitative.Plotly, hole=0.3)
    st.plotly_chart(fig)

# Tweet Locations
if not df.empty:
    st.subheader("Tweet Locations")
    st.map(df)
else:
    st.warning("No location data available for mapping.")

# Sidebar - Hour of the Day Filter
st.sidebar.subheader("Filter by Hour")
hour = st.sidebar.slider("Select Hour", min_value=0, max_value=23, value=12)

# Tweets by Airline - Plotly version
st.subheader("Total Tweets per Airline")
airline_counts = df['airline'].value_counts().reset_index()
airline_counts.columns = ['Airline', 'Count']
fig = px.bar(airline_counts, x='Airline', y='Count', color='Airline',
             title="Total No. of Tweets per Airline",
             color_discrete_sequence=px.colors.qualitative.Plotly)
fig.update_layout(xaxis_title="Airline", yaxis_title="Number of Tweets")
st.plotly_chart(fig)

# Negative Tweet Reasons - Plotly version
st.subheader("Reasons for Negative Tweets")
neg_reasons = df['negativereason'].value_counts().reset_index()
neg_reasons.columns = ['Reason', 'Count']
fig = px.bar(neg_reasons, y='Reason', x='Count', orientation='h',
             title="Reasons for Negative Tweets About Airlines",
             color='Reason', color_discrete_sequence=px.colors.qualitative.Plotly)
fig.update_layout(yaxis={'categoryorder':'total ascending'})
st.plotly_chart(fig)

# Word Clouds for Sentiments with larger size
st.subheader("Word Clouds for Sentiments")
sentiments = ["positive", "neutral", "negative"]

# Create tabs for each sentiment word cloud
tab1, tab2, tab3 = st.tabs([s.capitalize() for s in sentiments])

for idx, sentiment in enumerate(sentiments):
    text_data = " ".join(df[df["airline_sentiment"] == sentiment]["text"])
    wordcloud = WordCloud(width=1200, height=800, max_words=200, background_color='white').generate(text_data)
    
    if idx == 0:
        with tab1:
            st.image(wordcloud.to_array(), caption=f"{sentiment.capitalize()} Tweets", use_container_width=True)
    elif idx == 1:
        with tab2:
            st.image(wordcloud.to_array(), caption=f"{sentiment.capitalize()} Tweets", use_container_width=True)
    else:
        with tab3:
            st.image(wordcloud.to_array(), caption=f"{sentiment.capitalize()} Tweets", use_container_width=True)