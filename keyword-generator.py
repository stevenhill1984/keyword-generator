import pandas as pd
import streamlit as st

phrase_list = ['salaries {0}', 'how much does a {0} make']
phrase_list_2 = ['{0} {1} salaries', 'how much does a {1} make at {0}']
initial_data = {'Company': ['Amazon', 'Facebook', 'Indeed', 'Tesla', 'Rolyes Royce'], 
                'Job_Title': ['Engineer', 'Data Scientist', 'Accountant', 'SEO Analyst', 'HR Coordinator']}

st.markdown('# Keyword Generator')
st.markdown("""
    This application aids with the creation of large sets of keyword lists based on a set of Keyword _Seeds_ and Keyword _Phrases_.

""")

st.markdown('### Upload Keyword List File (CSV)')
seed_words = st.file_uploader('Upload Keyword List')

def convert_df(df):
    return df.to_csv(index=False).encode('utf-8')

if seed_words is not None:
    seed_df = pd.read_csv(seed_words, header=None)

    st.markdown('### Upload Phrase List File (CSV)')
    phrase_words = st.file_uploader('Upload Phrase List')
    
    if phrase_words is not None:
        phrase_df = pd.read_csv(phrase_words, header=None)


        if phrase_df is not None:
            with st.spinner('Computing...'):
                if len(seed_df.columns) == 1:
                    output = [(row, phrase, phrase.replace('{0}',row)) for phrase in phrase_df.iloc[:, 0] for row in seed_df.iloc[:, 0]]
                elif len(seed_df.columns) == 2:
                    output = [(cell_1, cell_2, phrase, phrase.replace('{0}',cell_1).replace('{1}',cell_2)) for phrase in phrase_df.iloc[:, 0] for cell_1 in seed_df.iloc[:, 0] for cell_2 in seed_df.iloc[:, 1]]
                elif len(seed_df.columns) == 3:
                    output = [(cell_1, cell_2, cell_3, phrase, phrase.replace('{0}',cell_1).replace('{1}',cell_2)) for phrase in phrase_df.iloc[:, 0] for cell_1 in seed_df.iloc[:, 0] for cell_2 in seed_df.iloc[:, 1] for cell_3 in seed_df.iloc[:, 2]]

                result = pd.DataFrame(output)
                
                st.markdown('### Keywords Generated')
                st.markdown('Showing the top 5 rows generated')

                st.write(result.head(5))
            
                csv = convert_df(result)

                st.download_button(label="Download data as CSV", data=csv, file_name='output.csv', mime='text/csv')
