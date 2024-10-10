import csv
from datetime import datetime
import argparse
import uuid

# Function to generate a random 20-character uppercase coupon code
def generate_unique_coupon_code():
    return uuid.uuid4().hex[:20].upper()  # Generates 20-character unique string and converts it to uppercase

def generate_coupon_csv(eligible_courses_path, output_date, previous_coupons_path=None):
    # Prepare output file
    output_file = f"coupons_{output_date}.csv"
    with open(eligible_courses_path, newline='') as f:
        reader = csv.DictReader(f)
        courses = [row for row in reader]

    # Load previous coupons if provided
    previous_coupons = {}
    if previous_coupons_path:
        with open(previous_coupons_path, newline='') as f:
            reader = csv.DictReader(f)
            previous_coupons = {row['course_id']: row['coupon_type'] for row in reader}

    # Prepare the output CSV
    with open(output_file, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['course_id', 'coupon_type', 'coupon_code', 'start_date', 'start_time', 'custom_price'])
        
        for course in courses:
            # Only generate a coupon if coupons_remaining > 0
            if int(course['coupons_remaining']) > 0:
                course_id = course['course_id']
                coupon_type = previous_coupons.get(course_id, 'best_price')  # Default to 'best_price'
                
                # Generate a unique 20-character coupon code
                coupon_code = generate_unique_coupon_code()
                
                start_date = output_date
                start_time = "00:00"
                custom_price = '' if coupon_type != 'custom_price' else course['min_custom_price']

                writer.writerow([course_id, coupon_type, coupon_code, start_date, start_time, custom_price])

    print(f"Coupons CSV created: {output_file}")

'''
python coupons.py --eligible_courses eligible_courses.csv --output_date 2024-10-11 --previous_coupons previous_coupons.csv
'''
if __name__ == "__main__":
    # Setting up argument parsing
    parser = argparse.ArgumentParser(description="Generate Udemy coupon CSV")
    parser.add_argument('--eligible_courses', required=True, help="Path to the eligible courses CSV")
    parser.add_argument('--output_date', required=True, default=datetime.now().strftime("%Y-%m-%d"), help="Date for coupon generation (format: YYYY-MM-DD)")
    parser.add_argument('--previous_coupons', help="Path to previous coupons CSV (optional)", required=False)
    
    args = parser.parse_args()
    
    generate_coupon_csv(args.eligible_courses, args.output_date, args.previous_coupons)
