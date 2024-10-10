import csv
import argparse
from datetime import datetime

def generate_post(active_coupons_path, post_template_path, eligible_courses_path, post_date):
    # Load active coupons
    with open(active_coupons_path, newline='') as f:
        reader = csv.DictReader(f)
        active_coupons = {row['course_id']: row['course_coupon_url'] for row in reader}

    # Load eligible courses
    with open(eligible_courses_path, newline='') as f:
        reader = csv.DictReader(f)
        eligible_courses = {row['course_id']: row for row in reader}

    # Load post template
    with open(post_template_path, 'r') as f:
        post_template = f.read()

    # Prepare course list with coupon links
    course_details = []
    for course_id, course in eligible_courses.items():
        if course_id in active_coupons:
            coupon_url = active_coupons[course_id]
        else:
            coupon_url = course['referral_url']  # Use referral URL if no active coupon

        course_details.append(f"{course['course_name']}:\n{coupon_url}\n")

    # Format the post using the template
    post_content = post_template.format(courses='\n'.join(course_details))

    # Prepare output filename with the date
    output_file = f"post_{post_date}.txt"

    # Write the post to the file
    with open(output_file, "w") as f:
        f.write(post_content)

    print(f"Post content saved to {output_file}")

'''
python post.py --active_coupons active_coupons.csv --post_template post_template.txt --eligible_courses eligible_courses.csv --post_date 2024-10-11

'''
if __name__ == "__main__":
    # Setting up argument parsing
    parser = argparse.ArgumentParser(description="Generate LinkedIn post content")
    parser.add_argument('--active_coupons', required=True, help="Path to active coupons CSV")
    parser.add_argument('--post_template', required=True, help="Path to the post template text file")
    parser.add_argument('--eligible_courses', required=True, help="Path to eligible courses CSV")
    parser.add_argument('--post_date', required=True, default=datetime.now().strftime("%Y-%m-%d"), help="Date for the post (format: YYYY-MM-DD)")

    args = parser.parse_args()
    
    generate_post(args.active_coupons, args.post_template, args.eligible_courses, args.post_date)
