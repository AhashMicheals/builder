import streamlit as st
from datetime import datetime
from fpdf import FPDF
import google.generativeai as genai

# Configure API key for Gemini model
api_key = "AIzaSyCBQl3mTVovqddKKzk7NBJxEHx3ZaZV99I"
genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-1.5-flash")

# Set up Streamlit app
st.title("AI-Powered Advanced Resume and Cover Letter Builder")

# Step 1: Collect user information
st.header("Enter Your Details")

# Upload photo
photo = st.file_uploader("Upload Your Photo", type=["jpg", "jpeg", "png"])
name = st.text_input("Full Name")
phone = st.text_input("Phone Number")
email = st.text_input("Gmail")
linkedin = st.text_input("LinkedIn Profile URL")

field_of_interest = st.selectbox(
    "Interested Field of Work",
    [
        "Data Science", "Software Development", "Digital Marketing", "Product Management",
        "Cybersecurity", "Cloud Computing", "DevOps", "UI/UX Design", "Business Analysis",
        "Quality Assurance", "IT Support", "Sales Engineering", "Technical Writing",
        "Finance and Accounting", "HR Management", "Project Management", "AI and Machine Learning",
        "Robotics Engineering", "Network Administration", "Blockchain Development", "Game Development",
        "Other"
    ]
)

# Add predefined company options
company_list = [
    "Google", "Microsoft", "Amazon", "Apple", "Facebook (Meta)", "Netflix", "Tesla", "IBM",
    "Salesforce", "Oracle", "Adobe", "Intel", "Cisco", "Spotify", "Shopify", "Twitter (X)",
    "SpaceX", "NVIDIA", "LinkedIn", "Airbnb", "Uber", "Lyft", "Zoom", "Slack", "Samsung",
    "TikTok", "Reddit", "Snap Inc.", "Dell", "HP", "Siemens", "Capgemini", "Accenture",
    "Deloitte", "PwC", "KPMG", "EY", "Spotify", "Alibaba", "Tencent", "Other"
]

company_interest = st.selectbox("Interested Company", company_list)

# Allow user to input a custom company name if "Other" is selected
if company_interest == "Other":
    company_interest = st.text_input("Enter the Name of Your Desired Company")

# Step 2: Collect educational background
st.header("Education Background")
ug_college = st.text_input("Undergraduate College Name")
ug_course = st.text_input("Undergraduate Course")
ug_year = st.text_input("Undergraduate Graduation Year")

has_pg = st.radio("Do you have a Postgraduate Degree?", ["No", "Yes"])
pg_college, pg_course, pg_year = "", "", ""
if has_pg == "Yes":
    pg_college = st.text_input("Postgraduate College Name")
    pg_course = st.text_input("Postgraduate Course")
    pg_year = st.text_input("Postgraduate Graduation Year")

has_phd = st.radio("Do you have a PhD?", ["No", "Yes"])
phd_college, phd_course, phd_year = "", "", ""
if has_phd == "Yes":
    phd_college = st.text_input("PhD College Name")
    phd_course = st.text_input("PhD Field of Study")
    phd_year = st.text_input("PhD Graduation Year")

# Step 3: Collect hobbies
st.header("Hobbies")
hobbies = st.text_area("List Your Hobbies (separate with commas)")

# Step 4: Collect previous job experience details
st.header("Previous Job Experience")
has_experience = st.radio("Do you have previous job experience?", ["Yes", "No"])

job_experience = []
if has_experience == "Yes":
    num_jobs = st.number_input("Number of Previous Jobs", min_value=1, max_value=10, step=1, value=1)
    
    for i in range(num_jobs):
        st.subheader(f"Job {i + 1}")
        company_name = st.text_input(f"Company Name (Job {i + 1})")
        job_title = st.text_input(f"Job Title (Job {i + 1})")
        years_of_experience = st.text_input(f"Years of Experience (Job {i + 1})")
        project_name = st.text_input(f"Project Name (Job {i + 1})")
        project_description = st.text_area(f"Project Short Description (Job {i + 1})")
        
        job_experience.append({
            "company_name": company_name,
            "job_title": job_title,
            "years_of_experience": years_of_experience,
            "project_name": project_name,
            "project_description": project_description
        })

# Step 5: Define AI-assisted job objective, skills, and cover letter recommendations
def generate_objective(field):
    objectives = {
        "Data Science": f"As a data scientist passionate about extracting meaningful insights from data, I aim to drive strategic decisions at {company_interest}.",
        "Software Development": f"Ambitious software developer seeking to join {company_interest} to create robust and innovative applications.",
        "Digital Marketing": f"Creative digital marketer aiming to craft engaging campaigns to enhance brand reach at {company_interest}.",
        "Product Management": f"Results-driven product manager ready to spearhead product innovation and growth at {company_interest}.",
        "Cybersecurity": f"Dedicated cybersecurity analyst, seeking to strengthen data integrity and protect sensitive information at {company_interest}.",
        "UI/UX Design": f"Innovative UI/UX designer committed to crafting intuitive user experiences for {company_interest}.",
        "Machine Learning": f"Machine learning engineer with a passion for developing predictive models, aiming to innovate at {company_interest}.",
        "Project Management": f"Efficient project manager dedicated to delivering projects on time and within scope, aspiring to contribute to {company_interest}.",
        "Other": f"Professional committed to making a meaningful contribution to {company_interest}."
    }
    return objectives.get(field, "An enthusiastic professional seeking new opportunities.")

def recommend_skills(field):
    skills = {
        "Data Science": ["Python", "Machine Learning", "Data Visualization", "SQL", "Statistical Analysis"],
        "Software Development": ["JavaScript", "React", "Node.js", "Python", "C++"],
        "Digital Marketing": ["SEO", "Content Creation", "Social Media Marketing", "Google Analytics", "Brand Management"],
        "Product Management": ["Project Management", "Market Research", "Product Roadmapping", "Agile Methodologies", "Stakeholder Management"],
        "Cybersecurity": ["Network Security", "Threat Analysis", "Penetration Testing", "Firewalls", "Encryption"],
        "UI/UX Design": ["Wireframing", "Prototyping", "User Research", "Adobe XD", "Figma"],
        "Machine Learning": ["Python", "TensorFlow", "Data Preprocessing", "Model Evaluation", "Deep Learning"],
        "Project Management": ["Resource Allocation", "Risk Management", "Scrum", "Time Management", "Communication"],
        "Other": ["Communication", "Teamwork", "Adaptability", "Problem Solving"]
    }
    return skills.get(field, ["Communication", "Adaptability"])

def generate_cover_letter(name, field, company_interest):
    cover_letter_templates = {
        "Data Science": f"Dear Hiring Manager at {company_interest},\n\nI am {name}, a dedicated data science professional with a passion for leveraging data-driven insights to fuel impactful decision-making. With a strong background in statistical analysis, machine learning, and data visualization, I am eager to contribute my expertise to {company_interest}.\n\nYour company's innovative approach to technology and commitment to excellence align perfectly with my career aspirations. I am confident that my skills will be a valuable addition to your data-driven initiatives.\n\nThank you for considering my application. I look forward to the opportunity to discuss how I can contribute to {company_interest}.\n\nBest regards,\n{name}",
        
        "Software Development": f"Dear {company_interest} Recruitment Team,\n\nMy name is {name}, and I am a motivated software developer passionate about building scalable and efficient solutions. I am excited by the opportunity to join {company_interest} and contribute to your dynamic development team.\n\nWith a solid foundation in various programming languages and frameworks, I have a track record of creating robust applications and collaborating effectively within cross-functional teams. I am drawn to {company_interest}'s dedication to pushing technological boundaries and would be honored to be part of such an environment.\n\nThank you for your time and consideration.\n\nBest,\n{name}",
        
        "Other": f"Dear {company_interest} Hiring Manager,\n\nI am {name}, a professional keen on bringing my diverse skill set and passion for excellence to {company_interest}. Your company's values and innovative projects resonate with my career objectives, and I am eager to contribute meaningfully to your team.\n\nI am looking forward to the chance to further discuss how my experience and enthusiasm can benefit {company_interest}.\n\nSincerely,\n{name}"
    }
    return cover_letter_templates.get(field, cover_letter_templates["Other"])

# Step 6: PDF Generation Function
def create_pdf():
    pdf = FPDF()
    pdf.add_page()

    # Title
    pdf.set_font("Arial", "B", 16)
    pdf.cell(200, 10, txt="Resume", ln=True, align="C")

    # Personal Details
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt=f"Name: {name}", ln=True)
    pdf.cell(200, 10, txt=f"Phone: {phone}", ln=True)
    pdf.cell(200, 10, txt=f"Email: {email}", ln=True)
    pdf.cell(200, 10, txt=f"LinkedIn: {linkedin}", ln=True)
    pdf.cell(200, 10, txt=f"Field of Interest: {field_of_interest}", ln=True)
    pdf.cell(200, 10, txt=f"Desired Company: {company_interest}", ln=True)

    # Add education and job details
    pdf.cell(200, 10, txt="Education:", ln=True)
    pdf.cell(200, 10, txt=f"{ug_college} - {ug_course} ({ug_year})", ln=True)
    if has_pg == "Yes":
        pdf.cell(200, 10, txt=f"{pg_college} - {pg_course} ({pg_year})", ln=True)
    if has_phd == "Yes":
        pdf.cell(200, 10, txt=f"{phd_college} - {phd_course} ({phd_year})", ln=True)

    # Add job experience
    pdf.cell(200, 10, txt="Job Experience:", ln=True)
    for job in job_experience:
        pdf.cell(200, 10, txt=f"Company: {job['company_name']}", ln=True)
        pdf.cell(200, 10, txt=f"Job Title: {job['job_title']}", ln=True)
        pdf.cell(200, 10, txt=f"Years of Experience: {job['years_of_experience']}", ln=True)
        pdf.cell(200, 10, txt=f"Project: {job['project_name']}", ln=True)
        pdf.multi_cell(0, 10, txt=f"Project Description: {job['project_description']}", ln=True)

    # Save PDF to file
    filename = f"{name}_Resume_{datetime.now().strftime('%Y-%m-%d')}.pdf"
    pdf.output(filename)

    st.success("Resume generated successfully!")
    st.download_button("Download Resume", filename=filename)

# Step 7: Generating and displaying the cover letter and objective
if st.button("Generate Resume and Cover Letter"):
    objective = generate_objective(field_of_interest)
    cover_letter = generate_cover_letter(name, field_of_interest, company_interest)

    st.header("Objective")
    st.write(objective)

    st.header("Cover Letter")
    st.write(cover_letter)

    # Optionally create and download PDF
    create_pdf()
