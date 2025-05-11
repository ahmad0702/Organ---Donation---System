from flask import Flask, render_template, request, redirect, url_for
from flask_mysqldb import MySQL
from datetime import datetime
app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '******' # Put your SQL server password here
app.config['MYSQL_DB'] = 'organ_donation_network_db'
app.config['MYSQL_PORT'] = 3306
db = MySQL(app)

doctors = []
organs = []
organisations = []
loc = []
organisation_id = ""
org_login = False

@app.route('/')
def index(msg=""):
    global organisations, loc

    load_loc()

    cur = db.connection.cursor()

    cur.execute("select organisation_id, organisation_name, city \
                    from organisation")
    organisations = cur.fetchall()

    cur.close()

    return render_template('index.html', 
            locations=loc, organisations=organisations, msg=msg)


#########################ORGANISATION UTILITY FUNCTIONS#########################

@app.route('/login/<string:user>', methods=['GET', 'POST'])
def login(user , msg = ""):
    form = request.form
    global doctors, organs, organisation_id, org_login
    
    if(user == "org"):
        org_login = True
        cur = db.connection.cursor()
        hit = cur.execute("select * from organisation \
                          where organisation_id = %s and pass = %s", 
                          (form['organisation_id'], form['Pass']))

        if(hit == 0):
            cur.close()
            return index(msg = "Wrong Credentials")

        row = list(cur.fetchone())

        organisation_id = form['organisation_id']

        cur.execute("select count(donor_id) \
                    from donated natural join donor \
                    where organisation_id = %s", (organisation_id))
        donors = cur.fetchone()
    
        cur.execute("select doctor_id, doctor_name, organ_name \
                    from doctor natural join organ \
                    where organisation_id = %s", (organisation_id))
        doctors = cur.fetchall()
    
        cur.execute("select * from organ natural join doctor \
                    where organisation_id = %s group by organ_id", 
                    (organisation_id))
        organs = cur.fetchall()

        
        cur.execute("select contact_number \
                    from organisation_contact where \
                    organisation_id = %s",(organisation_id))
        contact = cur.fetchall()

        cur.close()

        row.append((int)(donors[0]))
        row.append(len(doctors))
        row.append(contact)

        return render_template('home.html', organisation_data=row, msg = "")

    else:
        org_login = False
        cur = db.connection.cursor()
        hit = cur.execute("select * from patient \
                          where patient_id = %s and pass = %s \
                          and organisation_id = %s", (form['patient_id'], 
                          form['Pass'], form['organisation_id']))
        
        if(hit == 0):
            cur.close()
            return index(msg = "Wrong Credentials")

        organisation_id = form['organisation_id']

        return patient_details(form['patient_id'])

@app.route('/add_new_organisation', methods=['GET', 'POST'])
def add_new_organisation():
    global organisation_id
    form = request.form
    cur = db.connection.cursor()

    cur.execute("insert into organisation \
                (pass, organisation_name, head_name, office_no, street_no, city, state) \
                values (%s, %s, %s, %s, %s, %s, %s)", 
                [form['Pass'], form['organisation_name'], form['head_name'], 
                form['office_no'], form['street_no'], 
                form['location'][:form['location'].find(',')], 
                form['location'][form['location'].find(',') + 1:]])
    db.connection.commit()
    
    cur.execute("select organisation_id \
                from organisation order by \
                organisation_id desc limit 1")
    organisation_id = cur.fetchone()[0]
    
    contacts = form['contact'].split()

    for contact in contacts:
        cur.execute("insert into organisation_contact \
                    (organisation_id, contact_number) \
                    values (%s, %s)", (organisation_id, contact))
    db.connection.commit()

    cur.close()

    return index(msg="Your ID is {}. Login using your password".format(organisation_id))

@app.route('/review_transplants', methods=['GET', 'POST'])
def review_transplants():
    global organisation_id

    cur = db.connection.cursor()

    cur.execute("select donor_id, donor_name, patient_id, \
                patient_name, organ_name, transplantation_date \
                from \
                    (select * from donated \
                    where patient_id is not null) transplants\
                natural join donor \
                natural join organ \
                join patient using (patient_id) \
                where patient.organisation_id = %s", [organisation_id])
    transplants = cur.fetchall()
    
    cur.close()

    msg = ""
    if(len(transplants) == 0):
        msg = "No transplants approved till date"

    return render_template("review_transplantations.html", 
                            transplants=transplants, msg=msg)

#########################PATIENT UTILITY FUNCTIONS#########################

@app.route('/view_patient', methods=['GET', 'POST'])
def view_patient(msg=""):
    global doctors, loc, organisation_id
    return render_template ('view_patients.html', 
                            doctors=doctors, locations=loc, 
                            msg=msg, organisation_id=organisation_id)

@app.route('/search_patient/<string:type>', methods=['GET', 'POST'])
def search_patient(type):
    global organisation_id, doctors, loc
    
    form = request.form

    cur = db.connection.cursor()
    if(type == "id"):
        cur.execute("select distinct(patient_id), patient_name \
                    from attended_by natural join patient \
                    where organisation_id = %s and patient_id = %s", 
                    (organisation_id, form['patient_id']))   

    elif(type == "name"):
        cur.execute("select distinct(patient_id), patient_name \
                    from attended_by natural join patient \
                    where organisation_id = %s and patient_name = %s", 
                    (organisation_id, form['patient_name']))  

    elif(type == "city"):
        cur.execute("select distinct(patient_id), patient_name \
                    from attended_by natural join patient \
                    where organisation_id = %s and city = %s", 
                    (organisation_id, form['city']))  
    
    elif(type == "state"):
        cur.execute("select distinct(patient_id), patient_name \
                    from attended_by natural join patient \
                    where organisation_id = %s and state = %s", 
                    (organisation_id, form['state']))

    elif(type == "all"):
        cur.execute("select distinct(patient_id), patient_name \
                    from attended_by natural join patient \
                    where organisation_id = %s", [organisation_id])
    
    patients = cur.fetchall()
    cur.close()

    msg = ""
    if(len(patients) == 0):
        msg = "No matching records"

    return render_template ('view_patients.html', 
                            patients=patients, doctors=doctors, msg = msg,  
                            locations=loc, organisation_id=organisation_id)

@app.route('/add_new_patient/<string:signup>', methods=['GET', 'POST'])
def add_new_patient(signup = "false"):
    global organisation_id
    
    form = request.form   

    cur = db.connection.cursor()
    
    cur.execute("insert into patient (patient_name, date_of_birth, \
                insurance_no, house_no, street_no, city, state, pass, organisation_id) \
                values (%s, %s, %s, %s, %s, %s, %s, %s, %s)", 
                [form['patient_name'], str_to_date(form['date_of_birth']), 
                form['insurance_no'], form['house_no'], form['street_no'], 
                form['location'][:form['location'].find(',')], 
                form['location'][form['location'].find(',') + 1:],
                form['Pass'], form['organisation_id']])

    organisation_id = form['organisation_id']

    cur.execute("select patient_id from patient order by patient_id desc limit 1")
    patient_id = cur.fetchone()[0]
    
    db.connection.commit()

    contacts = form['contact'].split()

    for contact in contacts:
        cur.execute("insert into patient_contact \
                    (patient_id, contact_number) \
                    values (%s, %s)", (patient_id, contact))
    db.connection.commit()

    if(signup == "false"):
        cur.execute("insert into attended_by (patient_id, doctor_id, date_of_demand) \
                    values (%s, %s, %s)", (patient_id, form['doctor_id'], 
                    datetime.strptime(form['date_of_demand'], "%Y-%m-%d").strftime('%Y-%m-%d')))
        db.connection.commit()

    else:
        return index(msg="Your ID is {}. Login using your password and registered organisation".format(patient_id))
    cur.close()
    
    return patient_details(patient_id)

@app.route('/patient_details/<string:patient_id>', methods=['GET', 'POST'])
def patient_details(patient_id, donorlist = [], msg = "", organ_id = 0):
    
    global organisation_id
    cur = db.connection.cursor()
    
    cur.execute("select * from patient where patient_id = %s", [patient_id])
    details = cur.fetchone()

    cur.execute("select doctor_id, date_of_demand, doctor_name, organ_name, organ_id  \
                from attended_by natural join doctor natural join organ \
                where patient_id = %s and organisation_id = %s",  
                (patient_id, organisation_id))
    doctorlist = cur.fetchall()

    cur.execute("select doctor_id, doctor_name, organ_name\
                from doctor natural join organ \
                where organisation_id = %s and doctor_id not in \
                (select doctor_id from attended_by where patient_id = %s)", 
                (organisation_id, patient_id))
    doctors = cur.fetchall()

    cur.execute("select donor_id, donor_name, organ_name, \
                transplantation_date from patient \
                natural join donated \
                join donor using (donor_id) \
                natural join organ \
                where patient_id = %s and \
                donor.organisation_id = %s",
                (patient_id, organisation_id))
    transplants = cur.fetchall()

    cur.execute("select contact_number \
                from patient_contact where \
                patient_id = %s", [patient_id])
    contact = cur.fetchall()

    cur.close()

    details = list(details)
    details.append(contact)

    return render_template('patient_details.html', transplants=transplants,
            details=details, doctors=doctors, msg=msg, org_login=org_login,
            doctorlist=doctorlist, donorlist=donorlist, organ_id=organ_id)

@app.route('/add_new_doctor/<string:patient_id>', methods=['GET', 'POST'])
def add_new_doctor(patient_id): 
    form = request.form

    cur = db.connection.cursor()
    
    cur.execute("insert into attended_by (patient_id, doctor_id, date_of_demand) \
                values (%s, %s, %s)", (patient_id , form['doctor_id'], 
                datetime.strptime(form['date_of_demand'], "%Y-%m-%d").strftime('%Y-%m-%d')))

    db.connection.commit()
    cur.close()

    return patient_details(patient_id)

@app.route('/delete_patient/<string:patient_id>', methods=['GET', 'POST'])
def delete_patient(patient_id):

    global organisation_id
    cur = db.connection.cursor()

    cur.execute("delete from attended_by where patient_id = %s and \
                doctor_id in (select doctor_id from doctor where organisation_id = %s)", 
                (patient_id, organisation_id))
    
    db.connection.commit()
    cur.close()

    cur = db.connection.cursor()
    cur.execute("delete from patient_contact \
        where patient_id = %s", [patient_id])
        
    cur.execute("delete from patient where patient_id = %s \
                and not exists \
                    (select * from attended_by \
                     where patient_id = %s)",
                (patient_id, patient_id))
    
    db.connection.commit()
    cur.close()

    if(org_login):
        return view_patient("Patient deleted")
    else:
        return index(msg="You removed yourself from the Organisation/Hospital")

@app.route('/search_for_donor/<string:patient_id>', methods=['GET', 'POST'])
def search_for_donor(patient_id):
    form = request.form
    donorlist = []
    cur = db.connection.cursor()

    if(form['type'] == "Search by Age"):
        cur.execute("select date_of_birth from patient where patient_id = %s",
                    [patient_id])
        patient_dob = cur.fetchone()[0]

        cur.execute("select donor_id, donor_name, date_of_birth, \
                    city, state, organ_name, organ_id  \
                    from donor natural join donated natural join organ \
                    where patient_id is null and \
                    organ_id = %s and \
                    (abs(datediff(date_of_birth, %s)) / 365) <= 5", 
                    (form['organ_id'], patient_dob))
    
    elif(form['type'] == "Search by City"):
        cur.execute("select city from patient where patient_id = %s",
                    [patient_id])
        patient_city = cur.fetchone()[0]

        cur.execute("select donor_id, donor_name, date_of_birth, \
                    city, state, organ_name, organ_id \
                    from donor natural join donated natural join organ \
                    where patient_id is null and \
                    organ_id = %s and city = %s", 
                    (form['organ_id'], patient_city))

    elif(form['type'] == "Search by State"):
        cur.execute("select state from patient where patient_id = %s",
                    [patient_id])
        patient_state = cur.fetchone()[0]

        cur.execute("select donor_id, donor_name, date_of_birth, \
                    city, state, organ_name, organ_id  \
                    from donor natural join donated natural join organ \
                    where patient_id is null and \
                    organ_id = %s and state = %s", 
                    (form['organ_id'], patient_state))

    elif(form['type'] == "Search without Constraints"):

        cur.execute("select donor_id, donor_name, date_of_birth, \
                    city, state, organ_name, organ_id  \
                    from donor natural join donated natural join organ \
                    where patient_id is null and organ_id = %s", 
                    (form['organ_id']))

    donorlist = cur.fetchall()
    cur.close()
    
    msg = ""

    if(len(donorlist) == 0):
        msg = "No matching donors"

    return patient_details(patient_id, donorlist, msg, form['organ_id'])

@app.route('/approve_donation/<string:patient_id>', methods=['GET', 'POST'])
def approve_donation(patient_id):

    global organisation_id
    form = request.form

    cur = db.connection.cursor()

    cur.execute("update donated \
                set patient_id=%s, \
                transplantation_date=%s \
                where donor_id=%s and organ_id=%s",
                (patient_id, str_to_date(form['transplantation_date']), 
                form['donor_id'], form['organ_id']))
    
    cur.execute("delete from attended_by where patient_id = %s and \
                doctor_id in \
                    (select doctor_id from doctor \
                    where organisation_id = %s and \
                    organ_id = %s)", 
                (patient_id, organisation_id, form['organ_id']))
    
    db.connection.commit()
    cur.close()

    return patient_details(patient_id = patient_id, msg = "Transplantation Approved")

#########################DONOR UTILITY FUNCTIONS#########################

@app.route('/view_donor', methods=['GET', 'POST'])
def view_donor():
    global organisation_id, organs, loc
    return render_template ('view_donors.html', 
                            organs=organs, locations=loc, 
                            organisation_id=organisation_id)

@app.route('/add_new_donor', methods=['GET', 'POST'])
def add_new_donor():
    global organisation_id
    form = request.form    
    cur = db.connection.cursor()

    organisation_id = form['organisation_id']
    
    cur.execute("insert into donor (donor_name, date_of_birth, house_no,\
                street_no, city, state, organisation_id) \
                values (%s, %s, %s, %s, %s, %s, %s)", 
                [form['donor_name'], str_to_date(form['date_of_birth']), 
                form['house_no'], form['street_no'], 
                form['location'][:form['location'].find(',')],
                form['location'][form['location'].find(',') + 1:], organisation_id])
    db.connection.commit()
    
    cur.execute("select donor_id from donor order by donor_id desc limit 1")
    donor_id = cur.fetchone()[0]

    contacts = form['contact'].split()

    for contact in contacts:
        cur.execute("insert into donor_contact \
                    (donor_id, contact_number) \
                    values (%s, %s)", (donor_id, contact))
    db.connection.commit()
    
    cur.execute("insert into donated (donor_id, organ_id, date_of_donation, date_of_expiry) \
                values (%s, %s, %s, %s)", 
                [donor_id, form['organ_id'], 
                str_to_date(form['date_of_donation']), 
                str_to_date(form['date_of_expiry'])])
    
    db.connection.commit()
    cur.close()
    
    return donor_details(donor_id)

@app.route('/search_donor/<string:type>', methods=['GET', 'POST'])
def search_donor(type):

    global organisation_id, doctors, loc, organs
    form = request.form
    cur = db.connection.cursor()

    if(type == "id"):
        cur.execute("select distinct(donor_id), donor_name \
                    from donor \
                    where organisation_id = %s and donor_id = %s", 
            (organisation_id, form['donor_id']))

    elif(type == "name"):
        cur.execute("select distinct(donor_id), donor_name \
                    from donor \
                    where organisation_id = %s and \
                    donor_name = %s", 
                    (organisation_id, form['donor_name']))

    elif(type == "city"):
        cur.execute("select distinct(donor_id), donor_name \
                    from donor \
                    where organisation_id = %s and city = %s", 
                    (organisation_id, form['city']))

    elif(type == "state"):
        cur.execute("select distinct(donor_id), donor_name \
                    from donor \
                    where organisation_id = %s and state = %s", 
                    (organisation_id, form['state']))

    elif(type == "all"):
        cur.execute("select distinct(donor_id), donor_name \
                    from donor \
                    where organisation_id = %s", [organisation_id])

    donors = cur.fetchall()
    cur.close()
    
    msg = ""

    if(len(donors) == 0):
        msg = "No matching records"

    return render_template ('view_donors.html', 
                            organs=organs, donors=donors, doctors=doctors, 
                            locations=loc, msg = msg, organisation_id=organisation_id)

@app.route('/donor_details/<string:donor_id>', methods=['GET', 'POST'])
def donor_details(donor_id):
    global organs

    cur = db.connection.cursor()
    
    cur.execute("select * from donor where donor_id = %s", [donor_id])
    details = cur.fetchone()

    cur.execute("select organ_name, date_of_donation \
                from donor natural join donated \
                natural join organ where donor_id = %s", [donor_id])
    organlist = cur.fetchall()
    
    cur.execute("select contact_number \
                from donor_contact where \
                donor_id = %s", [donor_id])
    contact = cur.fetchall()

    cur.close()

    details = list(details)
    details.append(contact)

    return render_template('donor_details.html', 
                            details=details, organs=organs, 
                            organlist=organlist)

@app.route('/add_new_organ/<string:donor_id>', methods=['GET', 'POST'])
def add_new_organ(donor_id): 
    form = request.form

    cur = db.connection.cursor()
    
    cur.execute("insert into donated \
                (donor_id, organ_id, date_of_donation, \
                date_of_expiry) values (%s, %s, %s, %s)", 
                (donor_id, form['organ_id'], 
                str_to_date(form['date_of_donation']), 
                str_to_date(form['date_of_expiry'])))
    
    db.connection.commit()
    cur.close()

    return donor_details(donor_id)

#########################DOCTOR UTILITY FUNCTIONS#########################

@app.route('/doctor_login', methods=['GET', 'POST'])
def doctor_login():
    form = request.form

    cur = db.connection.cursor()
    
    hit = cur.execute('select doctor_id, pass \
                from doctor where \
                doctor_id = %s and pass = %s', 
                (form['doctor_id'], form['Pass']))
    cur.close()
    
    if(hit == 0):
        return index(msg="Wrong credentials")

    cur = db.connection.cursor()

    cur.execute('select patient_id, patient_name, \
                date_of_demand, date_of_birth, city, state\
                from attended_by \
                natural join patient \
                where doctor_id = %s',
                (form['doctor_id']))
    patients = cur.fetchall()

    cur.execute('select doctor_name, highest_degree, \
                date_of_birth, date_of_joining, organisation_name, city \
                from doctor natural join organisation \
                where doctor_id = %s', 
                (form['doctor_id']))
    doctor = cur.fetchone()

    cur.execute('select contact_number \
                from doctor_contact \
                where doctor_id = %s', (form['doctor_id']))
    contact = cur.fetchall()

    cur.close()

    doctor = list(doctor)
    doctor.append(contact)
    
    msg = ""
    if(len(patients) == 0):
        msg = "Currently there are no patients under you"

    return render_template('doctor_patients.html', doctor=doctor, patients=patients, msg=msg)

@app.route('/view_doctor', methods=['GET', 'POST'])
def view_doctor():

    global doctors, organs, organisation_id

    cur = db.connection.cursor()
    
    cur.execute("select doctor_id, doctor_name, organ_name \
                from doctor natural join organ \
                where organisation_id = %s", (organisation_id))
    doctors = cur.fetchall()

    cur.execute("select * from organ natural join doctor \
                where organisation_id = %s \
                group by organ_id", (organisation_id))
    organs = cur.fetchall()

    cur.execute("select organ_id, organ_name from organ")
    all_organs = cur.fetchall()

    cur.close()

    doctors = list(doctors)

    return render_template ('view_doctors.html', 
                            doctor_data = doctors, organs = all_organs)

@app.route('/add_doctor', methods=['GET', 'POST'])
def add_doctor():
    global organisation_id
    
    form = request.form   
    cur = db.connection.cursor()
    
    cur.execute("insert into doctor (doctor_name, date_of_birth, date_of_joining, \
                highest_degree, organ_id, organisation_id, pass) \
                values (%s, %s, %s, %s, %s, %s, %s)", 
                (form['doctor_name'], str_to_date(form['date_of_birth']), 
                str_to_date(form['date_of_joining']), form['highest_degree'], 
                form['organ_id'], organisation_id, form['pass']))
    
    db.connection.commit()
    
    cur.execute("select doctor_id from doctor \
                order by doctor_id desc limit 1")
    doctor_id = cur.fetchone()[0]
    
    contacts = form['contact'].split()

    for contact in contacts:
        cur.execute("insert into doctor_contact \
                    (doctor_id, contact_number) \
                    values (%s, %s)", (doctor_id, contact))
    db.connection.commit()

    cur.close()

    return view_doctor()

#########################GENERAL UTILITY FUNCTIONS#########################

def load_loc():
    global loc

    cur = db.connection.cursor()

    cur.execute('select * from locations')
    
    for location in cur.fetchall():
        loc.append(location[0] + ', ' + location[1])

    cur.close()

def str_to_date(date):
    return datetime.strptime(date, "%Y-%m-%d").strftime('%Y-%m-%d')
    
if __name__ == '__main__':
    app.run(debug = True)