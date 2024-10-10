# Udemy Bulk Coupons Generator

## Overview

This repository provides an automated solution for generating, editing, and managing Udemy bulk coupons, along with creating LinkedIn posts to promote courses. Instead of going through the manual process of downloading, generating, and uploading coupon files, this project automates the process using a **Command-Line Interface (CLI)** or a **Flask web app**. 

### Manual Process:
Instructors typically follow these steps to generate bulk coupons on Udemy:
1. **Download Eligible Courses**: Instructors must download the eligible courses information by navigating to [Udemy's Multiple Coupons Creation API](https://www.udemy.com/api-2.0/discounts/multiple-coupons-creation/export-instructor-courses/) or through their instructor dashboard. This `.csv` file contains the course information necessary to generate coupons.
2. **Generate Coupons**: Instructors manually create a `.csv` file containing coupon codes, types, and other details, which can be uploaded via Udemy’s [Bulk Coupons Creation](https://www.udemy.com/instructor/multiple-coupons-creation/) page.
3. **Upload Coupons**: The `.csv` file is uploaded to Udemy to activate the coupons. This step requires navigating to the [Bulk Coupons Creation](https://www.udemy.com/instructor/multiple-coupons-creation/) page and submitting the generated `.csv`.
4. **Download Active Coupons**: Once the coupons are generated, instructors can download the active coupons using the [Export Instructor Coupons API](https://www.udemy.com/api-2.0/discounts/multiple-coupons-creation/export-instructor-coupons/) to get a `.csv` of the active coupons.

### Automated Process:
This project streamlines the process by automating coupon generation, modification, and LinkedIn post creation. Instead of manually handling multiple CSV files, the system can:
1. **CLI Version**:
   - Automatically process eligible courses, generate coupon codes, and save the details to a `.csv` file.
   - Allow users to modify the coupons before uploading them to Udemy.
   - Generate LinkedIn posts with coupon links for easy promotion.
   
2. **Flask App Version**:
   - A user-friendly web interface allows for the upload of eligible course data, automatic generation of coupon codes, and easy modification of coupon details.
   - Generate LinkedIn posts from active coupons, streamlining the entire promotional workflow.

## Usage

### 1. Command-Line Interface (CLI)

#### Prerequisites:
- Install the required dependencies (e.g., `csv`, `argparse`, `uuid`).

```bash
pip install -r requirements.txt
```
# Steps to Generate Bulk Coupons via CLI:
1. Get Eligible Courses from Udemy:

    - Log in to your Udemy Instructor account.
    - Navigate to Udemy's [Multiple Coupons Creation API](https://www.udemy.com/api-2.0/discounts/multiple-coupons-creation/export-instructor-courses/) to download the `eligible_courses.csv`. This file contains details about the eligible courses, including course ID, name, pricing, and other metadata.

2. Generate the Coupons CSV:

    - Run the `coupons.py` script to generate the initial coupons CSV. You can optionally provide a `previous_coupons.csv` file if you have previous coupon data to reuse the same types.
    ``` bash
    python coupons.py --eligible_courses eligible_courses.csv --date 2024-10-11 --previous_coupons previous_coupons.csv
    ```

    - This will generate a `coupons_<date>.csv` file based on the eligible courses and any previous coupon data.

3. Modify the Coupons:

    - You can open the generated coupons.csv to manually modify any details, such as coupon types, custom pricing, etc.

4. Upload the Coupons to Udemy:

    - Go to [Udemy's Bulk Coupons Creation page](https://www.udemy.com/instructor/multiple-coupons-creation/) and upload the `coupons.csv` file.
    - Udemy will process the file and generate the coupons.

5. Download Active Coupons from Udemy:

    - After the bulk coupons have been created, download the active coupons using the [Export Instructor Coupons API](https://www.udemy.com/api-2.0/discounts/multiple-coupons-creation/export-instructor-coupons/). Save this file as `active_coupons.csv`.

6. Generate LinkedIn Post:

    - Use the post.py script to generate a LinkedIn post that contains the course names and active coupon links.
        ``` bash 
        python post.py --active_coupons active_coupons.csv --post_template post_template.txt --eligible_courses eligible_courses.csv --date 2024-10-11 
        ```

    - The LinkedIn post will be saved in a .txt file (`post_<date>.txt`), ready for you to copy and paste into your LinkedIn account.

# Flask Web Application

## Prerequisites:        
- Install the required dependencies for Flask.
    ```bash
    pip install -r requirements.txt
    ```
## Steps to Generate Bulk Coupons via the App:

1. Start the Flask App:
    - Run the Flask app using the following command:
        ```bash
        python app.py
        ```
    - Open your browser and go to http://127.0.0.1:5000/.

2. Generate Coupons:

    - On the homepage, upload the eligible_courses.csv (downloaded from [Udemy's API](https://www.udemy.com/api-2.0/discounts/multiple-coupons-creation/export-instructor-courses/)) and optionally, the `previous_coupons.csv`.
    - Click Generate Coupons CSV to generate the initial coupons based on the uploaded data.
    - The app will then display the generated coupons in a table where you can review and modify the details.

3. Edit Coupons:

    - Modify coupon types, start dates, and custom prices directly in the web interface.
    - The fields for Course ID and Coupon Code will be non-editable.
    - Custom Price will only be editable if the coupon type is set to custom_price.
    - Click Save and Download Updated Coupons CSV to download the modified coupons.

4. Upload Coupons to Udemy:

    - After downloading the updated coupons.csv, navigate to [Udemy's Bulk Coupons Creation page)](https://www.udemy.com/instructor/multiple-coupons-creation/) to upload your updated CSV and generate the active coupons.

5. Download Active Coupons from Udemy:

    - After the coupons are generated, download the active coupons using [Udemy's Export Instructor Coupons API](https://www.udemy.com/api-2.0/discounts/multiple-coupons-creation/export-instructor-coupons/) and save the file as active_coupons.csv.

6. Generate LinkedIn Post:

    - In the Generate LinkedIn Post section of the app, upload the `active_coupons.csv`, `eligible_courses.csv`, and the `post_template.txt`.
    - Click Generate LinkedIn Post to download a .txt file with the formatted post, which includes course names and coupon links.

# Streamlit App

## Step 1: Install Streamlit and Dependencies

Ensure you have installed Streamlit and the necessary libraries. Run the following command to install the required dependencies:

```bash
pip install streamlit pandas uuid
```

## Step 2: Run the Streamlit App

To run the Streamlit app, use the following command in your terminal:

streamlit run app.py

This will start the app, and you can open it in your browser using the URL provided (usually `http://localhost:8501/`).

## Step 3: Use the App

### Generate Coupons CSV

1. **Upload Eligible Courses CSV**: 
   - Download the `eligible_courses.csv` from [Udemy's API](https://www.udemy.com/api-2.0/discounts/multiple-coupons-creation/export-instructor-courses/) and upload it using the file uploader.

2. **(Optional) Upload Previous Coupons CSV**: 
   - Upload the `previous_coupons.csv` if available (optional).

3. **Select the Coupon Start Date**: 
   - Choose the start date for the coupon generation.

4. **Generate Coupons CSV**: 
   - The app will display a table with the generated coupons. You can review and modify the coupon types, custom prices, and other details directly in the app.

5. **Download Coupons CSV**: 
   - After making any changes, click the **Download Coupons CSV** button to download the updated coupons file.

### Generate LinkedIn Post

1. **Upload Active Coupons CSV**: 
   - Download the `active_coupons.csv` from [Udemy's API](https://www.udemy.com/api-2.0/discounts/multiple-coupons-creation/export-instructor-coupons/) and upload it.

2. **Upload Post Template**: 
   - Upload a `post_template.txt` file that will be used to generate the LinkedIn post. This text file should include a placeholder for the course and coupon details.

3. **Generate LinkedIn Post**: 
   - The app will generate the LinkedIn post content by inserting the coupon URLs and course names into the template.
   
4. **Download LinkedIn Post**: 
   - After reviewing the generated LinkedIn post, click the **Download LinkedIn Post** button to download the post as a `.txt` file.

---

By following these steps, you can use the Streamlit app to easily generate and manage Udemy coupons and create LinkedIn posts to promote your courses.

# CSV Files Overview:
- `eligible_courses.csv`: This file is downloaded from Udemy's [Multiple Coupons Creation API](https://www.udemy.com/api-2.0/discounts/multiple-coupons-creation/export-instructor-courses/). It contains details about your eligible courses, such as course ID, course name, currency, price, etc.
- `coupons.csv`: This is the file generated by the script or app, containing the coupons that can be uploaded to Udemy.
- `previous_coupons.csv`: Optionally used to track and reuse the same coupon types for consistency.
- `active_coupons.csv`: This file is downloaded from [Udemy's Export Instructor Coupons API](https://www.udemy.com/api-2.0/discounts/multiple-coupons-creation/export-instructor-coupons/) after your coupons have been created by Udemy. It contains the active coupon codes for each course.
- `post_template.txt`: A text file template for generating LinkedIn posts. It can include placeholders for course names and coupon URLs.

# Conclusion
This project provides an automated workflow for managing Udemy bulk coupon creation and LinkedIn promotion. By using the CLI version or the Flask web application, instructors can save time and effort in generating, editing, and promoting their Udemy course coupons.

