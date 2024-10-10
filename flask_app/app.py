import os
import csv
import uuid
from flask import Flask, request, render_template, redirect, url_for, send_file, flash
from datetime import datetime

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = './static/uploads'
app.secret_key = 'secret'

# Ensure upload folder exists
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

# Function to generate a unique 20-character uppercase coupon code
def generate_unique_coupon_code():
    return uuid.uuid4().hex[:20].upper()

# Route for the home page
@app.route('/')
def index():
    return render_template('index.html')

# Route to upload and generate coupons CSV
@app.route('/generate-coupons', methods=['POST'])
def generate_coupons():
    if 'eligible_courses' not in request.files:
        flash('No eligible courses file uploaded')
        return redirect(request.url)

    eligible_courses_file = request.files['eligible_courses']
    previous_coupons_file = request.files.get('previous_coupons')

    # Save uploaded files
    eligible_courses_path = os.path.join(app.config['UPLOAD_FOLDER'], eligible_courses_file.filename)
    eligible_courses_file.save(eligible_courses_path)

    if previous_coupons_file:
        previous_coupons_path = os.path.join(app.config['UPLOAD_FOLDER'], previous_coupons_file.filename)
        previous_coupons_file.save(previous_coupons_path)
    else:
        previous_coupons_path = None

    output_date = request.form.get('output_date', datetime.now().strftime("%Y-%m-%d"))

    # Generate coupons CSV
    coupons_data = []
    with open(eligible_courses_path, newline='') as f:
        reader = csv.DictReader(f)
        courses = [row for row in reader]

    previous_coupons = {}
    if previous_coupons_path:
        with open(previous_coupons_path, newline='') as f:
            reader = csv.DictReader(f)
            previous_coupons = {row['course_id']: row['coupon_type'] for row in reader}

    for course in courses:
        if int(course['coupons_remaining']) > 0:
            course_id = course['course_id']
            coupon_type = previous_coupons.get(course_id, 'best_price')
            coupon_code = generate_unique_coupon_code()
            start_date = output_date
            start_time = "00:00"
            custom_price = '' if coupon_type != 'custom_price' else course['min_custom_price']

            coupons_data.append([course_id, coupon_type, coupon_code, start_date, start_time, custom_price])

    # Render the CSV as an editable table instead of downloading
    return render_template('edit_coupons.html', coupons_data=coupons_data)

# Route to handle editing and saving the coupons CSV
@app.route('/save-coupons', methods=['POST'])
def save_coupons():
    updated_rows = []

    # Get the form data
    course_ids = request.form.getlist('course_id')
    coupon_types = request.form.getlist('coupon_type')
    coupon_codes = request.form.getlist('coupon_code')
    start_dates = request.form.getlist('start_date')
    start_times = request.form.getlist('start_time')
    custom_prices = request.form.getlist('custom_price')

    # Loop through the form data and handle custom_price properly
    for i in range(len(course_ids)):
        custom_price = custom_prices[i] if i < len(custom_prices) and coupon_types[i] == 'custom_price' else ''
        
        updated_rows.append([
            course_ids[i],
            coupon_types[i],
            coupon_codes[i],
            start_dates[i],
            start_times[i],
            custom_price
        ])

    # Save the updated CSV file
    output_file = os.path.join(app.config['UPLOAD_FOLDER'], f"edited_coupons_{datetime.now().strftime('%Y-%m-%d')}.csv")
    with open(output_file, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['course_id', 'coupon_type', 'coupon_code', 'start_date', 'start_time', 'custom_price'])
        writer.writerows(updated_rows)

    return send_file(output_file, as_attachment=True)


# Route to upload and generate the LinkedIn post using a custom post template
@app.route('/generate-post', methods=['POST'])
def generate_post():
    if 'active_coupons' not in request.files or 'post_template' not in request.files:
        flash('Active coupons file or post template file is missing')
        return redirect(request.url)

    active_coupons_file = request.files['active_coupons']
    eligible_courses_file = request.files.get('eligible_courses')
    post_template_file = request.files['post_template']

    # Save uploaded files
    active_coupons_path = os.path.join(app.config['UPLOAD_FOLDER'], active_coupons_file.filename)
    active_coupons_file.save(active_coupons_path)

    if eligible_courses_file:
        eligible_courses_path = os.path.join(app.config['UPLOAD_FOLDER'], eligible_courses_file.filename)
        eligible_courses_file.save(eligible_courses_path)
    else:
        eligible_courses_path = None

    post_template_path = os.path.join(app.config['UPLOAD_FOLDER'], post_template_file.filename)
    post_template_file.save(post_template_path)

    # Generate post
    post_file = f"post_{datetime.now().strftime('%Y-%m-%d')}.txt"
    post_path = os.path.join(app.config['UPLOAD_FOLDER'], post_file)

    with open(active_coupons_path, newline='') as f:
        reader = csv.DictReader(f)
        active_coupons = {row['course_id']: row['course_coupon_url'] for row in reader}

    with open(eligible_courses_path, newline='') as f:
        reader = csv.DictReader(f)
        eligible_courses = {row['course_id']: row for row in reader}

    # Load post template
    with open(post_template_path, 'r') as f:
        post_template = f.read()

    course_details = []
    for course_id, course in eligible_courses.items():
        if course_id in active_coupons:
            coupon_url = active_coupons[course_id]
        else:
            coupon_url = course['referral_url']

        course_details.append(f"{course['course_name']}:\n{coupon_url}\n")

    post_content = post_template.format(courses='\n'.join(course_details))

    with open(post_path, 'w') as f:
        f.write(post_content)

    return send_file(post_path, as_attachment=True)

# Run the Flask app
if __name__ == "__main__":
    app.run(debug=True)
