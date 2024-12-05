import logging
logger = logging.getLogger(__name__)
import pandas as pd
import streamlit as st
import requests
from modules.nav import SideBarLinks

# Call the SideBarLinks from the nav module in the modules directory
SideBarLinks()

# set the header of the page
st.header('Students')


response = requests.get('http://api:4000/s/students')

if response.status_code == 200:
    results = response.json()
    
    if results:
        for student in results:
            student_id = student.get('StudentId')
            student_firstname = student.get('FirstName', 'No First Name')
            student_lastname = student.get('LastName', 'No Last Name')
            student_email = student.get('Email', 'No Email')
            student_skillid = student.get('SkillId', 'No Skill ID')
            student_departmentid = student.get('DepartmentId', 'No Department ID')
            student_interest = student.get('ResearchInterest', 'No Research Interest')
            student_year = student.get('Year', 'No Year')
            student_major = student.get('Major', 'No Major')
            student_type = student.get('StudentType', 'No Student Type')
            
            response1 = requests.get(f'http://api:4000/sk/skills/s{student_skillid}')
            skill_name = ''
            if response1.status_code == 200:
                skill_data = response1.json()
                skill_name = skill_data[0].get('Name', 'No Name')
        
            response2 = requests.get(f'http://api:4000/d/departments/d{student_departmentid}')
            department_name = ''
            if response2.status_code == 200:
                department_data = response1.json()
                department_name = department_data[0].get('Name', 'No Name')

            st.markdown(f"""
                <div style="border: 1px solid #2C3E50; padding: 18px; margin-bottom: 15px; border-radius: 10px; box-shadow: 0px 3px 6px rgba(0, 0, 0, 0.15); background-color: #2C3E50;">
                <h3 style="margin-bottom: 10px; color: #76C7C0;">{student_firstname + ' ' + student_lastname}</h3>
                <p style="margin-bottom: 6px; color: #ECF0F1;"><strong>Email:</strong> {student_email}</p>
                <p style="margin-bottom: 6px; color: #ECF0F1;"><strong>Skill:</strong> {skill_name}</p>
                <p style="margin-bottom: 6px; color: #ECF0F1;"><strong>Department:</strong> {department_name}</p>
                <p style="margin-bottom: 6px; color: #ECF0F1;"><strong>Interest:</strong> {student_interest}</p>
                <p style="margin-bottom: 6px; color: #ECF0F1;"><strong>Year:</strong> {student_year}</p>
                <p style="margin-bottom: 6px; color: #ECF0F1;"><strong>Major:</strong> {student_major}</p>
                <p style="margin-bottom: 6px; color: #ECF0F1;"><strong>Type:</strong> {student_type}</p>
            </div>
            """, unsafe_allow_html=True)

            if st.button(f"Delete {student_firstname} {student_lastname}", key=f"delete_{student_id}"):
                delete_response = requests.delete(f'http://api:4000/s/students/s{student_id}')
                
                if delete_response.status_code == 200:
                    st.success(f"Successfully deleted {student_firstname} {student_lastname}.")
                    st.session_state['show_students'] = True  # Keep the list visible
                else:
                    st.error(f"Failed to delete {student_firstname} {student_lastname}. Please try again.")
    else:
        st.warning("No Students available.")
else:
    st.error("Failed to fetch students.")

# Back button
if st.button("Back"):
    st.session_state['show_students'] = False
    st.switch_page('pages/30_Admin_Home.py')