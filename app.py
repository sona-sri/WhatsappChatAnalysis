import streamlit as st
from matplotlib import pyplot as plt
import preprocessor
import helper

st.sidebar.title("Whatsapp Chat Analysis")

uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")  # converting byte to string

    df = preprocessor.preprocess(data)  # preprocessing the input data
    st.dataframe(df)

    # Fetch unique users
    user_list = df['user'].unique().tolist()
    user_list.remove('group_notification')
    user_list.sort()
    user_list.insert(0, 'All Users')

    selected_user = st.sidebar.selectbox("Show analysis wrt, ", user_list)

    if st.sidebar.button("Analyze"):
        # Statistics
        num_messages, words, num_media, links = helper.show_stats(selected_user, df)

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.header("Total Messages")
            st.title(num_messages)

        with col2:
            st.header("Total Words")
            st.title(words)

        with col3:
            st.header("Total Media")
            st.title(num_media)

        with col4:
            st.header("Total Links")
            st.title(links)

        # Busiest User
        if selected_user == 'All Users':
            st.title("Most Busiest Users ")

            x, new_df = helper.busy_users(df)
            fig, ax = plt.subplots()

            col1, col2 = st.columns(2)

            with col1:
                ax.bar(x.index, x.values)
                st.pyplot(fig)

            with col2:
                st.dataframe(new_df)

        # WordCloud
        st.title("Word Cloud")
        df_wc = helper.create_word_cloud(selected_user, df)
        fig, ax = plt.subplots()
        plt.imshow(df_wc)
        st.pyplot(fig)

        # Most common words
        most_common_df = helper.most_common_words(selected_user, df)
        fig, ax = plt.subplots()
        ax.bar(most_common_df[0], most_common_df[1])
        plt.xticks(rotation='vertical')
        st.title("Most Common Words")
        st.pyplot(fig)




