import streamlit as st
import pandas as pd
import os

# Function to save words to a local file
def save_words(file_path, df):
    df.to_csv(file_path, index=False)

# Function to load words from the file if it exists and has data
def load_words(file_path):
    if os.path.exists(file_path) and os.path.getsize(file_path) > 0:
        return pd.read_csv(file_path)
    else:
        return pd.DataFrame(columns=['Class', 'Word', 'Meaning'])

# Main App
def main():
    st.title("Word Saver App")

    # File to save words
    file_path = "words.csv"

    # Load existing words from the CSV file
    if "word_data" not in st.session_state:
        st.session_state.word_data = load_words(file_path)

    # Get unique classes
    unique_classes = st.session_state.word_data['Class'].unique().tolist()

    # Tabs at the top: "View Words" and "Add Word"
    tab1, tab2 = st.tabs(["View Words", "Add Word"])

    with tab1:
        #st.subheader("View Words by Class")

        # Dropdown to select a class without a label
        if unique_classes:
            selected_class = st.selectbox("", unique_classes)  # No label for the selectbox

            st.subheader(f"Words in Class: {selected_class}")
            class_data = st.session_state.word_data[st.session_state.word_data['Class'] == selected_class]

            if not class_data.empty:
                st.table(class_data[['Word', 'Meaning']])
            else:
                st.write(f"No words saved in class '{selected_class}' yet.")
        else:
            st.write("No classes available yet. Please add words in the 'Add Word' tab.")

    with tab2:
        st.subheader("Add New Word")

        # Input fields
        word = st.text_input("Enter the new word:")
        meaning = st.text_area("Enter the meaning of the word:")
        word_class = st.text_input("Enter the class of the word:")

        if st.button("Add Word"):
            if word and meaning and word_class:
                new_word = pd.DataFrame([[word_class, word, meaning]], columns=['Class', 'Word', 'Meaning'])
                st.session_state.word_data = pd.concat([st.session_state.word_data, new_word], ignore_index=True)
                st.success(f"Word '{word}' added successfully!")
            else:
                st.warning("Please enter the word, its meaning, and class.")

        st.subheader("Save Words to CSV")
        if st.button("Save Words"):
            save_words(file_path, st.session_state.word_data)
            st.success(f"Words saved to {file_path} successfully!")

if __name__ == "__main__":
    main()
