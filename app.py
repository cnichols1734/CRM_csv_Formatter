import pandas as pd
import streamlit as st


def transform_contacts(input_file, reference_file):
    # Load input and reference files
    input_df = pd.read_csv(input_file)
    reference_df = pd.read_csv(reference_file)

    # Define the column mapping based on the reference file
    column_mapping = {
        'First Name': 'first_name',
        'Last Name': 'last_name',
        'Email 1': 'email',
        'Phone Number 1': 'phone',
        'Mailing Address': 'street_address',
        'Mailing City': 'city',
        'Mailing State/Province': 'state',
        'Mailing Postal Code': 'zip_code',
        'Groups': 'groups'
    }

    # Map and rename columns to match the reference format
    transformed_df = input_df[list(column_mapping.keys())].rename(columns=column_mapping)

    # Combine additional columns into the notes field
    additional_columns = set(input_df.columns) - set(column_mapping.keys())
    input_df['additional_notes'] = input_df[additional_columns].apply(
        lambda row: ', '.join(f"{col}: {row[col]}" for col in additional_columns if pd.notnull(row[col])), axis=1
    )

    # Merge notes into the transformed dataframe
    if 'notes' in transformed_df.columns:
        transformed_df['notes'] = transformed_df['notes'].fillna('') + ", " + input_df['additional_notes']
    else:
        transformed_df['notes'] = input_df['additional_notes']

    # Ensure the groups column uses ';' as a delimiter
    if 'groups' in transformed_df.columns:
        transformed_df['groups'] = transformed_df['groups'].str.replace(',', ';')

    # Fill missing columns with empty strings
    for col in reference_df.columns:
        if col not in transformed_df.columns:
            transformed_df[col] = ''

    # Reorder columns to match the reference file
    transformed_df = transformed_df[reference_df.columns]

    return transformed_df


# Streamlit UI
st.title("Contact Formatter")

# File upload
uploaded_input_file = st.file_uploader("Upload the contacts file to be transformed (CSV format):", type="csv")
reference_file = 'Christopher_Nichols_contacts (1).csv'

if uploaded_input_file is not None:
    # Process the file
    transformed_df = transform_contacts(uploaded_input_file, reference_file)

    # Convert the dataframe to CSV for download
    csv_data = transformed_df.to_csv(index=False).encode('utf-8')

    st.success("File transformed successfully. You can download it below.")
    st.download_button(label="Download the formatted file", data=csv_data, file_name="formatted_contacts.csv",
                       mime="text/csv")
