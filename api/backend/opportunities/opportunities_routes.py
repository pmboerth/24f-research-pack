from flask import Blueprint
from flask import request
from flask import jsonify
from flask import make_response
from flask import current_app
from backend.db_connection import db

# Blueprint object for all opportunities routes
opportunities = Blueprint('opportunities', __name__)


#------------------------------------------------------------
# Get all opportunities from the system
@opportunities.route('/opportunities', methods=['GET'])
def get_all_opportunities():
    cursor = db.get_db().cursor()
    cursor.execute('SELECT * FROM ResearchOpportunities')
    
    theData = cursor.fetchall()
    cursor.close()
    
    the_response = make_response(jsonify(theData))
    the_response.status_code = 200
    return the_response


#------------------------------------------------------------
# Get all name of opportunity based on the PositionId
@opportunities.route('/opportunities/p<positionid>', methods=['GET'])
def get_opportunity_name(positionid):
    cursor = db.get_db().cursor()
    cursor.execute('SELECT Name FROM ResearchOpportunities WHERE PositionId = {0}'.format(positionid))
    
    theData = cursor.fetchall()
    cursor.close()
    
    the_response = make_response(jsonify(theData))
    the_response.status_code = 200
    return the_response


#------------------------------------------------------------
# Enter a new opportunity into the system
@opportunities.route('/opportunities', methods=['POST'])
def add_new_opportunities():
    the_data = request.json
    current_app.logger.info(the_data)
    
    query = '''
            INSERT INTO ResearchOpportunities (
                Name,
                OwnerId,
                ResearchArea,
                Description,
                DepartmentId,
                SkillId
            ) VALUES (%s, %s, %s, %s, %s, %s)
        '''
        
    params = (
        the_data['name'],
        the_data['owner_id'],
        the_data['research_area'],
        the_data['description'],
        the_data['department_id'],
        the_data['skill_id']
    )

    cursor = db.get_db().cursor()
    cursor.execute(query, params)
    db.get_db().commit()
    cursor.close()
    
    return make_response({"message": "Successfully added opportunity"}, 200)


#------------------------------------------------------------
# Get all opportunities in a specific department based on the given DepartmentId
@opportunities.route('/opportunities/d<departmentID>', methods=['GET'])
def get_opportunities(departmentID):
    current_app.logger.info('GET /opportunities/d<departmentID> route')
    cursor = db.get_db().cursor()
    cursor.execute('SELECT * FROM ResearchOpportunities WHERE DepartmentId = {0}'.format(departmentID))
    
    theData = cursor.fetchall()
    cursor.close()
    
    the_response = make_response(jsonify(theData))
    the_response.status_code = 200
    return the_response


#------------------------------------------------------------
# Get all opportunities posted by a particular owner based on the given OwnerId
@opportunities.route('/opportunities/o<ownerID>', methods=['GET'])
def get_opportunities_by_owner(ownerID):
    current_app.logger.info('GET /opportunities/o<ownerID> route')
    cursor = db.get_db().cursor()
    cursor.execute('SELECT * FROM ResearchOpportunities WHERE OwnerId = {0}'.format(ownerID))
    
    theData = cursor.fetchall()
    cursor.close()
    
    the_response = make_response(jsonify(theData))
    the_response.status_code = 200
    return the_response


#------------------------------------------------------------
# Update a specific opportunity based on the PositionId
@opportunities.route('/opportunities/p<positionID>', methods=['PUT'])
def update_opportunity(positionID):
    
    the_data = request.get_json()
    
    valid_fields = {
            'name': 'Name',
            'research_area': 'ResearchArea',
            'description': 'Description',
            'department_id': 'DepartmentId',
            'skill_id': 'SkillId'
        }

    # build the set dynamically based on which fields were provided
    update_fields = []
    params = []
        
    for json_key, db_column in valid_fields.items():
        if json_key in the_data:
            update_fields.append(f"{db_column} = %s")
            params.append(the_data[json_key])

    if not update_fields:
        return make_response({"error": "No valid fields to update"}, 400)

    query = f'''
        UPDATE ResearchOpportunities 
        SET {', '.join(update_fields)}
        WHERE PositionId = %s
    '''
        
    params.append(positionID)

    cursor = db.get_db().cursor()
    cursor.execute(query, params)            
    db.get_db().commit()
    cursor.close()

    return make_response({"message": f"Successfully updated opportunity {positionID}"}, 200)


#------------------------------------------------------------
# Delete a specific opportunity based on the PositionId
@opportunities.route('/opportunities/p<positionID>', methods=['DELETE'])
def del_opportunity(positionID):
    cursor = db.get_db().cursor()    
    query = 'DELETE FROM ResearchOpportunities WHERE PositionId = %s'
    cursor.execute(query, (positionID))
        
    db.get_db().commit()
    cursor.close()
        
    return make_response({"message": f"Successfully deleted opportunity {positionID}"}, 200)
    
