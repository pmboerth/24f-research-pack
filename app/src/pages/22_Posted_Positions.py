import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks
import requests

st.set_page_config(layout = 'wide')

SideBarLinks()

st.title('My Posted Research Positions')

ownerID = st.session_state['professor_id']

response = requests.get(f"http://api:4000/o/opportunities/o{ownerID}")

if response.status_code == 200:
    results = response.json()
    
    if results:
        for position in results:
            research_title = position.get('Name', 'No Title')
            research_area = position.get('ResearchArea', 'No Area')
            research_description = position.get('Description', 'No Description')
            department_id = position.get('DepartmentId', 'No Department')
            skill_id = position.get('SkillId', 'No Skill')
            position_id = position.get('PositionId', 'No Position')
            
            # Fetch department name based on department ID
            result1 = requests.get(f'http://api:4000/d/departments/d{department_id}').json()
            department_name = result1[0].get('Name', 'No Name')
    
            # Fetch skill name based on skill ID
            result2 = requests.get(f'http://api:4000/sk/skills/s{skill_id}').json()
            skill_name = result2[0].get('Name', 'No Name')


            # Display each post using styled HTML
            st.markdown(f"""
                <div style="border: 1px solid #3D4A59; padding: 20px; margin-bottom: 20px; border-radius: 8px; box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.2); background-color: #3D4A59;">
                    <h3 style="margin-bottom: 10px; color: #90AEAD;">{research_title}</h3>
                    <p style="margin-bottom: 8px; color: #D1D7DC;"><strong>Faculty: </strong>Professor Emily Chen</p>
                    <p style="margin-bottom: 8px; color: #D1D7DC;"><strong>Research Area: </strong> {research_area}</p>
                    <p style="margin-bottom: 8px; color: #D1D7DC;"><strong>Department: </strong> {department_name}</p>
                    <p style="margin-bottom: 8px; color: #D1D7DC;"><strong>Required Skill:</strong> {skill_name}</p>
                    <p style="margin-bottom: 12px; color: #D1D7DC;"><strong>Description:</strong> {research_description}</p>
                </div>
            """, unsafe_allow_html=True)

            col1, col2 = st.columns([1, 15])

            with col1:

                if st.button(f"Update", type="primary", key=f"apply_p{position_id}"):
                    
                    st.session_state['update_position'] = {
                        'position_id': position_id,
                        'research_title': research_title,
                        'research_area': research_area,
                        'research_description': research_description,
                        'department_id': department_id,
                        'skill_id': skill_id
                    }
                    st.switch_page('pages/24_Update_Position.py')
            with col2:
                if st.button(f"Delete",  type="primary", key=f"delete_p{position_id}"):
                    response = requests.delete(f'http://api:4000/o/opportunities/p{position_id}')

                    if response.status_code == 200:
                        st.success(f"Successfully deleted: {research_title}.")
                    else:
                        st.error(f"Failed to delete: {response.text}")



            
    else:
        st.warning("No posts found for the selected group.")
else:
    st.error(f"Error: {response.status_code}, {response.text}")



if st.button("Back"):
    st.switch_page('pages/20_Professor_Home.py')

        



