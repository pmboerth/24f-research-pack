import logging
logger = logging.getLogger(__name__)
import pandas as pd
import streamlit as st
import requests
from modules.nav import SideBarLinks

# Call the SideBarLinks from the nav module in the modules directory
SideBarLinks()

# Set the header of the page
st.header('Students')

# You can access the session state to make a more customized/personalized app experience
st.write(f"### Hi, {st.session_state['first_name']}.")

# Add a button to fetch all students
if st.button('See All Students', type='primary'):
    response = requests.get('http://api:4000/students')
    
    if response.status_code == 200:
        students = response.json()
        
        if students:
            for student in students:
                student_id = student.get('StudentId', 'No ID')
                student_firstname = student.get('FirstName', 'No First Name')
                student_lastname = student.get('LastName', 'No Last Name')
                student_email = student.get('Email', 'No Email')
                student_skillid = student.get('SkillId', 'No Skill ID')
                student_departmentid = student.get('DepartmentId', 'No Department ID')
                student_interest = student.get('ResearchInterest', 'No Research Interest')
                student_year = student.get('Year', 'No Year')
                student_major = student.get('Major', 'No Major')
                student_type = student.get('StudentType', 'No Student Type')

                # Get skill and department information
                skill_response = requests.get(f'http://api:4000/d/departments/d{student_skillid}')
                department_response = requests.get(f'http://api:4000/pr/professors/p{student_departmentid}')
                
                if skill_response.status_code == 200:
                    skill_name = skill_response.json()[0].get('Name', 'No Name')
                else:
                    skill_name = 'No Name'
                
                if department_response.status_code == 200:
                    department_name = department_response.json()[0].get('Name', 'No Name')
                else:
                    department_name = 'No Name'

                # Display student info
                st.markdown(f"""
                    <div style="border: 1px solid #ddd; padding: 15px; margin-bottom: 10px; border-radius: 5px; box-shadow: 2px 2px 5px rgba(0,0,0,0.1);">
                        <h3 style="margin-bottom: 5px; color: #4CAF50;">{student_firstname + ' ' + student_lastname}</h3>
                        <p style="margin-bottom: 5px; color: #555;"><strong>Email:</strong> {student_email}</p>
                        <p style="margin-bottom: 5px; color: #555;"><strong>Skill:</strong> {skill_name}</p>
                        <p style="margin-bottom: 5px; color: #555;"><strong>Department:</strong> {department_name}</p>
                        <p style="margin-bottom: 5px; color: #555;"><strong>Interest:</strong> {student_interest}</p>
                        <p style="margin-bottom: 5px; color: #555;"><strong>Year:</strong> {student_year}</p>
                        <p style="margin-bottom: 5px; color: #555;"><strong>Major:</strong> {student_major}</p>
                        <p style="margin-bottom: 5px; color: #555;"><strong>Type:</strong> {student_type}</p>
                """, unsafe_allow_html=True)

                # Add a delete button for each student
                if st.button(f"Delete {student_firstname} {student_lastname}", key=f"delete_{student_id}"):
                    delete_response = requests.delete(f'http://api:4000/students/s{student_id}')
                    
                    if delete_response.status_code == 200:
                        st.success(f"Successfully deleted {student_firstname} {student_lastname}.")
                    else:
                        st.error(f"Failed to delete {student_firstname} {student_lastname}. Please try again.")

                st.markdown("</div>", unsafe_allow_html=True)  # Close the student info div
        else:
            st.warning("No students available.")
    else:
        st.error("Failed to fetch student data.")

# Back button to return to admin home page
if st.button("Back"):
    st.switch_page('pages/00_Admin_Home.py')