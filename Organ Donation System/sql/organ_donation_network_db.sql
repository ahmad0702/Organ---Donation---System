use organ_donation_network_db;

drop table if exists patient_contact;
drop table if exists donor_contact;
drop table if exists doctor_contact;
drop table if exists organisation_contact;
drop table if exists donated;
drop table if exists attended_by;
drop table if exists doctor;
drop table if exists donor;
drop table if exists organ;
drop table if exists organisation;
drop table if exists patient;

#table 1
create table if not exists patient (
	patient_id int primary key auto_increment,
    patient_name varchar(20),
    pass varchar(20) not null,
    date_of_birth date not null,
    insurance_no varchar(20),
    house_no varchar(20),
    street_no varchar(20),
    city varchar(20) not null,
    state varchar(20) not null,
    organisation_id int not null
);

#table 2
create table if not exists organ (
	organ_id int primary key auto_increment,
    organ_name varchar(20) not null
);

#table 3
create table if not exists organisation (
	organisation_id int primary key auto_increment,
    pass varchar(20) not null,
    organisation_name varchar(20),
    head_name varchar(20),
    office_no varchar(20),
    street_no varchar(20),
    city varchar(20),
    state varchar(20)
);

#table 4
create table if not exists donor (
	donor_id int primary key auto_increment,
    donor_name varchar(20),
    date_of_birth date not null,
    house_no varchar(20),
    street_no varchar(20),
    city varchar(20) not null,
    state varchar(20) not null,
    organisation_id int,
    foreign key (organisation_id) references organisation(organisation_id)
);

#table 5
create table if not exists doctor (
	doctor_id int primary key auto_increment,
    doctor_name varchar(20),
    date_of_birth date,
    date_of_joining date,
    highest_degree varchar(20),
    organ_id int,
    organisation_id int,
    pass varchar(20),
    foreign key (organ_id) references organ(organ_id),
    foreign key (organisation_id) references organisation(organisation_id)
);

#table 6
create table if not exists attended_by (
	patient_id int,
    doctor_id int,
    date_of_demand date not null,
    primary key (patient_id, doctor_id),
    foreign key (patient_id) references patient(patient_id),
    foreign key (doctor_id) references doctor(doctor_id)
);

#table 7
create table if not exists donated (
	donor_id int,
    organ_id int,
    date_of_donation date not null,
    date_of_expiry date,
    transplantation_date date,
    patient_id int, 
    primary key (donor_id, organ_id),
    foreign key (donor_id) references donor(donor_id),
    foreign key (organ_id) references organ(organ_id),
    check (date_of_expiry >= date_of_donation),
    check (date_of_expiry >= transplantation_date),
    check (transplantation_date >= date_of_donation)
);

#table 8
create table if not exists patient_contact (
	patient_id int,
    contact_number varchar(20),
    primary key (patient_id, contact_number)
);

#table 9
create table if not exists donor_contact (
	donor_id int,
    contact_number varchar(20),
    primary key (donor_id, contact_number)
);

#table 10
create table if not exists doctor_contact (
	doctor_id int,
    contact_number varchar(20),
    primary key (doctor_id, contact_number),
    foreign key (doctor_id) references doctor(doctor_id)
);

#table 11
create table if not exists organisation_contact (
	organisation_id int,
    contact_number varchar(20),
    primary key (organisation_id, contact_number),
    foreign key (organisation_id) references organisation(organisation_id)
);


#insert organisation
insert into organisation (pass, organisation_name, head_name, office_no, street_no, city, state)
values ("password", "AIIMS", "Dr. Randeep Guleria", 123, 456, "New Delhi", "Delhi");
insert into organisation (pass, organisation_name, head_name, office_no, street_no, city, state)
values ("password", "AIIMS", "Dr. Strange", 123, 456, "Chandigarh", "Punjab");

#insert organ
insert into organ (organ_name) 
values ("Heart");
insert into organ (organ_name) 
values ("Kidney");
insert into organ (organ_name) 
values ("Lung");
insert into organ (organ_name) 
values ("Liver");
insert into organ (organ_name) 
values ("Pancreas");
insert into organ (organ_name) 
values ("Eye Tissue");
insert into organ (organ_name) 
values ("Bone");
insert into organ (organ_name) 
values ("Tendon");
insert into organ (organ_name) 
values ("Skin Tissue");
insert into organ (organ_name) 
values ("Heart Tissue");
insert into organ (organ_name) 
values ("Small Intestine");
insert into organ (organ_name) 
values ("Cornea");

#insert doctor
insert into doctor (doctor_name, date_of_birth, date_of_joining, highest_degree, organ_id, organisation_id, pass)
values ('Hardeep Singh', '2021-03-18', '2021-03-18', 'DPhil', 1, 1, "password");
insert into doctor (doctor_name, date_of_birth, date_of_joining, highest_degree, organ_id, organisation_id, pass)
values ('Ramesh Singh', '1965-04-02', '2007-02-19', 'MBBS', 2, 1, "password");
insert into doctor (doctor_name, date_of_birth, date_of_joining, highest_degree, organ_id, organisation_id, pass)
values ('Jai Sharma', '1997-06-22', '2010-04-01', 'BTech', 3, 1, "password");
insert into doctor (doctor_name, date_of_birth, date_of_joining, highest_degree, organ_id, organisation_id, pass)
values ('Akhilesh Yadav', '1972-03-18', '2015-03-18', 'DPhil', 4, 1, "password");
insert into doctor (doctor_name, date_of_birth, date_of_joining, highest_degree, organ_id, organisation_id, pass)
values ('Javed Akhtra', '1961-03-18', '2018-03-18', 'DPhil', 5, 1, "password");
insert into doctor (doctor_name, date_of_birth, date_of_joining, highest_degree, organ_id, organisation_id, pass)
values ('Rohan Gundu', '1977-03-18', '2103-03-18', 'DPhil', 6, 1, "password");
insert into doctor (doctor_name, date_of_birth, date_of_joining, highest_degree, organ_id, organisation_id, pass)
values ('Anuj Shankar', '1987-03-18', '2010-03-18', 'DPhil', 7, 1, "password");

#insert donor
insert into donor (donor_name, date_of_birth, house_no, street_no, city, state, organisation_id)
values ("Thanos", "2000-04-13", 123, 12321, "Lucknow", "Uttar Pradesh", 1); 
insert into donor (donor_name, date_of_birth, house_no, street_no, city, state, organisation_id)
values ("Ashish Gupta", "2000-05-13", 123, 12321, "Mumbai", "Maharashtra", 1); 
insert into donor (donor_name, date_of_birth, house_no, street_no, city, state, organisation_id)
values ("Jai Shankar", "2000-06-13", 123, 12321, "New Delhi", "Delhi", 1);
insert into donor (donor_name, date_of_birth, house_no, street_no, city, state, organisation_id)
values ("Ambar Das", "2000-08-13", 123, 12321, "Kolkata", "West Bengal", 1);  
insert into donor (donor_name, date_of_birth, house_no, street_no, city, state, organisation_id)
values ("Ambuja Cement", "1989-04-13", 123, 12321, "Bhopal", "Madhya Pradesh", 1); 
insert into donor (donor_name, date_of_birth, house_no, street_no, city, state, organisation_id)
values ("Bangur Cement", "1989-05-13", 123, 12321, "Shimla", "Himachal Pradesh", 1); 
insert into donor (donor_name, date_of_birth, house_no, street_no, city, state, organisation_id)
values ("MDH Masale", "1989-07-13", 123, 12321, "Jaipur", "Rajasthan", 1); 
insert into donor (donor_name, date_of_birth, house_no, street_no, city, state, organisation_id)
values ("Ankit Oraon", "1989-04-13", 123, 12321, "Ranchi", "Jharkhand", 1); 

#insert donated
insert into donated (donor_id, organ_id, date_of_donation, date_of_expiry)
values (1, 8, '2012-08-31', '2025-10-31');
insert into donated (donor_id, organ_id, date_of_donation, date_of_expiry)
values (2, 1, '2012-08-31', '2025-10-31');
insert into donated (donor_id, organ_id, date_of_donation, date_of_expiry)
values (3, 1, '2012-08-31', '2025-10-31');
insert into donated (donor_id, organ_id, date_of_donation, date_of_expiry)
values (4, 3, '2012-08-31', '2025-10-31');
insert into donated (donor_id, organ_id, date_of_donation, date_of_expiry)
values (5, 4, '2012-08-31', '2025-10-31');
insert into donated (donor_id, organ_id, date_of_donation, date_of_expiry)
values (6, 6, '2012-08-31', '2025-10-31');
insert into donated (donor_id, organ_id, date_of_donation, date_of_expiry)
values (7, 8, '2012-08-31', '2025-10-31');
insert into donated (donor_id, organ_id, date_of_donation, date_of_expiry)
values (8, 5, '2012-08-31', '2025-10-31');
insert into donated (donor_id, organ_id, date_of_donation, date_of_expiry)
values (1, 12, '2012-08-31', '2025-10-31');
insert into donated (donor_id, organ_id, date_of_donation, date_of_expiry)
values (2, 6, '2012-08-31', '2025-10-31');
insert into donated (donor_id, organ_id, date_of_donation, date_of_expiry)
values (3, 2, '2012-08-31', '2025-10-31');
insert into donated (donor_id, organ_id, date_of_donation, date_of_expiry)
values (4, 1, '2012-08-31', '2025-10-31');
insert into donated (donor_id, organ_id, date_of_donation, date_of_expiry)
values (5, 3, '2012-08-31', '2025-10-31');
insert into donated (donor_id, organ_id, date_of_donation, date_of_expiry)
values (6, 4, '2012-08-31', '2025-10-31');
insert into donated (donor_id, organ_id, date_of_donation, date_of_expiry)
values (7, 3, '2012-08-31', '2025-10-31');
insert into donated (donor_id, organ_id, date_of_donation, date_of_expiry)
values (8, 4, '2012-08-31', '2025-10-31');
insert into donated (donor_id, organ_id, date_of_donation, date_of_expiry)
values (8, 2, '2012-08-31', '2025-10-31');
insert into donated (donor_id, organ_id, date_of_donation, date_of_expiry)
values (1, 10, '2012-08-31', '2025-10-31');
insert into donated (donor_id, organ_id, date_of_donation, date_of_expiry)
values (2, 2, '2012-08-31', '2025-10-31');
insert into donated (donor_id, organ_id, date_of_donation, date_of_expiry)
values (3, 4, '2012-08-31', '2025-10-31');
insert into donated (donor_id, organ_id, date_of_donation, date_of_expiry)
values (4, 5, '2012-08-31', '2025-10-31');

#insert patient
insert into patient (patient_name, date_of_birth, insurance_no, house_no, street_no, city, state, pass, organisation_id)
values ("Josephine Culpepper", "2000-02-20", "asdfasdfx", 123, 213, "Lucknow", "Uttar Pradesh", "password", 1);
insert into patient (patient_name, date_of_birth, insurance_no, house_no, street_no, city, state, pass, organisation_id)
values ("Shana Voth", "2000-03-20", "asdffh", 123, 213, "Mumbai", "Maharashtra", "password", 1);
insert into patient (patient_name, date_of_birth, insurance_no, house_no, street_no, city, state, pass, organisation_id)
values ("Ramesh Kumar", "2000-10-20", "asdfasdg", 123, 213, "Kolkata", "West Bengal", "password", 1);
insert into patient (patient_name, date_of_birth, insurance_no, house_no, street_no, city, state, pass, organisation_id)
values ("Suresh Kumar", "2000-01-20", "asdfgagh", 123, 213, "New Delhi", "Delhi", "password", 1);
insert into patient (patient_name, date_of_birth, insurance_no, house_no, street_no, city, state, pass, organisation_id)
values ("Mahesh Kumar", "2000-06-20", "asdfgahgafd", 123, 213, "Mumbai", "Maharashtra", "password", 1);

#insert attended_by
insert into attended_by (patient_id, doctor_id, date_of_demand)
values (1, 1, '2010-05-12');
insert into attended_by (patient_id, doctor_id, date_of_demand)
values (1, 2, '2010-05-12');
insert into attended_by (patient_id, doctor_id, date_of_demand)
values (1, 3, '2010-05-12');
insert into attended_by (patient_id, doctor_id, date_of_demand)
values (2, 2, '2011-05-12');
insert into attended_by (patient_id, doctor_id, date_of_demand)
values (2, 3, '2011-05-12');
insert into attended_by (patient_id, doctor_id, date_of_demand)
values (2, 4, '2011-05-12');
insert into attended_by (patient_id, doctor_id, date_of_demand)
values (3, 4, '2016-05-12');
insert into attended_by (patient_id, doctor_id, date_of_demand)
values (3, 5, '2016-05-12');
insert into attended_by (patient_id, doctor_id, date_of_demand)
values (4, 6, '2020-05-12');
insert into attended_by (patient_id, doctor_id, date_of_demand)
values (4, 7, '2019-05-12');
insert into attended_by (patient_id, doctor_id, date_of_demand)
values (4, 4, '2011-05-12');
insert into attended_by (patient_id, doctor_id, date_of_demand)
values (5, 3, '2015-05-12');
insert into attended_by (patient_id, doctor_id, date_of_demand)
values (5, 6, '2015-05-12');

insert into organisation_contact(organisation_id, contact_number)
values(1, '+011-123124');
insert into organisation_contact(organisation_id, contact_number)
values(1, '+011-123125');

insert into patient_contact(patient_id, contact_number)
values(1, '+011-123124');
insert into patient_contact(patient_id, contact_number)
values(1, '+011-123125');
insert into patient_contact(patient_id, contact_number)
values(2, '+011-123124');
insert into patient_contact(patient_id, contact_number)
values(2, '+011-123125');
insert into patient_contact(patient_id, contact_number)
values(3, '+011-123124');
insert into patient_contact(patient_id, contact_number)
values(3, '+011-123125');
insert into patient_contact(patient_id, contact_number)
values(4, '+011-123124');
insert into patient_contact(patient_id, contact_number)
values(4, '+011-123125');
insert into patient_contact(patient_id, contact_number)
values(5, '+011-123124');
insert into patient_contact(patient_id, contact_number)
values(5, '+011-123125');

insert into doctor_contact(doctor_id, contact_number)
values(1, '+011-123124');
insert into doctor_contact(doctor_id, contact_number)
values(1, '+011-123125');
insert into doctor_contact(doctor_id, contact_number)
values(2, '+011-123124');
insert into doctor_contact(doctor_id, contact_number)
values(2, '+011-123125');
insert into doctor_contact(doctor_id, contact_number)
values(3, '+011-123124');
insert into doctor_contact(doctor_id, contact_number)
values(3, '+011-123125');
insert into doctor_contact(doctor_id, contact_number)
values(4, '+011-123124');
insert into doctor_contact(doctor_id, contact_number)
values(4, '+011-123125');
insert into doctor_contact(doctor_id, contact_number)
values(5, '+011-123124');
insert into doctor_contact(doctor_id, contact_number)
values(5, '+011-123125');
insert into doctor_contact(doctor_id, contact_number)
values(6, '+011-123124');
insert into doctor_contact(doctor_id, contact_number)
values(6, '+011-123125');
insert into doctor_contact(doctor_id, contact_number)
values(7, '+011-123124');
insert into doctor_contact(doctor_id, contact_number)
values(7, '+011-123125');


insert into donor_contact(donor_id, contact_number)
values(1, '+011-123124');
insert into donor_contact(donor_id, contact_number)
values(1, '+011-123125');
insert into donor_contact(donor_id, contact_number)
values(2, '+011-123124');
insert into donor_contact(donor_id, contact_number)
values(2, '+011-123125');
insert into donor_contact(donor_id, contact_number)
values(3, '+011-123124');
insert into donor_contact(donor_id, contact_number)
values(3, '+011-123125');
insert into donor_contact(donor_id, contact_number)
values(4, '+011-123124');
insert into donor_contact(donor_id, contact_number)
values(4, '+011-123125');
insert into donor_contact(donor_id, contact_number)
values(5, '+011-123124');
insert into donor_contact(donor_id, contact_number)
values(5, '+011-123125');
insert into donor_contact(donor_id, contact_number)
values(6, '+011-123124');
insert into donor_contact(donor_id, contact_number)
values(6, '+011-123125');
insert into donor_contact(donor_id, contact_number)
values(7, '+011-123124');
insert into donor_contact(donor_id, contact_number)
values(7, '+011-123125');
insert into donor_contact(donor_id, contact_number)
values(8, '+011-123124');
insert into donor_contact(donor_id, contact_number)
values(8, '+011-123125');

drop table if exists locations;

create table if not exists locations (
	city varchar(20),
    state varchar(20),
    primary key(city, state)
);

insert into locations(city, state)
values ('Mumbai', 'Maharashtra');
insert into locations(city, state)
values ('New Delhi', 'Delhi');
insert into locations(city, state)
values ('Bengaluru', 'Karanataka');
insert into locations(city, state)
values ('Hyderabad', 'Andhra Pradesh');
insert into locations(city, state)
values ('Ahmedabad', 'Gujarat');
insert into locations(city, state)
values ('Chennai', 'Tamil Nadu');
insert into locations(city, state)
values ('Kolkata', 'West Bengal');
insert into locations(city, state)
values ('Surat', 'Gujarat');
insert into locations(city, state)
values ('Pune', 'Maharashtra');
insert into locations(city, state)
values ('Jaipur', 'Rajasthan');
insert into locations(city, state)
values ('Lucknow', 'Uttar Pradesh');
insert into locations(city, state)
values ('Kanpur', 'Uttar Pradesh');
insert into locations(city, state)
values ('Nagpur', 'Maharashtra');
insert into locations(city, state)
values ('Indore', 'Madhya Pradesh');
insert into locations(city, state)
values ('Bhopal', 'Madhya Pradesh');
insert into locations(city, state)
values ('Vishakhapatnam', 'Andhra Pradesh');
insert into locations(city, state)
values ('Patna', 'Bihar');
insert into locations(city, state)
values ('Agra', 'Uttar Pradesh');
insert into locations(city, state)
values ('Ranchi', 'Jharkhand');
insert into locations(city, state)
values ('Shimla', 'Himachal Pradesh');
select * from donor where organisation_id = 1;
