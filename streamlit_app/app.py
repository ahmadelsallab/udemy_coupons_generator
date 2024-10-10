import os
import csv
import uuid
import pandas as pd
import streamlit as st
from io import StringIO, BytesIO
from datetime import datetime

# Function to generate a unique 20-character uppercase coupon code
def generate_unique_coupon_code():
    return uuid.uuid4().hex[:20].upper()

# Function to handle coupon generation logic
def generate_coupons(eligible_courses_df, previous_coupons_df=None, output_date=None):
    coupons_data = []
    
    if previous_coupons_df is not None:
        previous_coupons = dict(zip(previous_coupons_df['course_id'], previous_coupons_df['coupon_type']))
    else:
        previous_coupons = {}

    # Process the courses to generate coupons
    for index, course in eligible_courses_df.iterrows():
        if int(course['coupons_remaining']) > 0:
            course_id = course['course_id']
            coupon_type = previous_coupons.get(course_id, 'best_price')
            coupon_code = generate_unique_coupon_code()
            start_date = output_date
            start_time = "00:00"
            custom_price = '' if coupon_type != 'custom_price' else course['min_custom_price']

            coupons_data.append({
                'course_id': course_id,
                'coupon_type': coupon_type,
                'coupon_code': coupon_code,
                'start_date': start_date,
                'start_time': start_time,
                'custom_price': custom_price
            })
    
    # Convert to DataFrame for easy editing
    coupons_df = pd.DataFrame(coupons_data)
    return coupons_df

# Streamlit App

st.title("Udemy Bulk Coupons Generator")

# Step 1: Upload eligible courses CSV
st.subheader("Step 1: Upload Eligible Courses CSV")
eligible_courses_file = st.file_uploader("Upload eligible_courses.csv", type="csv")

# Step 2: Upload previous coupons CSV (optional)
st.subheader("Step 2: Upload Previous Coupons CSV (Optional)")
previous_coupons_file = st.file_uploader("Upload previous_coupons.csv", type="csv", key="previous")

# Step 3: Enter Coupon Start Date
st.subheader("Step 3: Enter Coupon Start Date")
output_date = st.date_input("Coupon Start Date", datetime.now())

if eligible_courses_file:
    # Step 4: Generate Coupons CSV
    st.subheader("Step 4: Generate and Edit Coupons CSV")

    eligible_courses_df = pd.read_csv(eligible_courses_file)
    
    if previous_coupons_file:
        previous_coupons_df = pd.read_csv(previous_coupons_file)
    else:
        previous_coupons_df = None
    
    # Generate initial coupons CSV
    coupons_df = generate_coupons(eligible_courses_df, previous_coupons_df, output_date)

    # Display editable coupons table
    edited_coupons_df = st.dataframe(coupons_df)

    # Step 5: Save Coupons CSV
    st.subheader("Step 5: Download Edited Coupons CSV")

    def convert_df_to_csv(df):
        return df.to_csv(index=False).encode('utf-8')

    csv = convert_df_to_csv(coupons_df)
    st.download_button(label="Download Coupons CSV", data=csv, file_name=f"coupons_{output_date}.csv", mime="text/csv")

# LinkedIn Post Generation
st.subheader("Generate LinkedIn Post")

# Step 1: Upload Active Coupons CSV
active_coupons_file = st.file_uploader("Upload active_coupons.csv", type="csv", key="active")

# Step 2: Upload Post Template
post_template_file = st.file_uploader("Upload post_template.txt", type="txt")

if active_coupons_file and post_template_file:
    active_coupons_df = pd.read_csv(active_coupons_file)
    post_template = post_template_file.read().decode("utf-8")

    course_details = []
    for index, row in active_coupons_df.iterrows():
        course_name = row['course_name']
        coupon_url = row['course_coupon_url']
        course_details.append(f"{course_name}:\n{coupon_url}\n")

    post_content = post_template.format(courses='\n'.join(course_details))

    # Step 3: Generate and Download LinkedIn Post
    st.text_area("Generated LinkedIn Post", post_content, height=300)
    
    st.download_button(label="Download LinkedIn Post", data=post_content.encode('utf-8'), file_name=f"linkedin_post_{datetime.now().strftime('%Y-%m-%d')}.txt", mime="text/plain")
