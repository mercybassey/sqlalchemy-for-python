from sqlalchemy import create_engine, ForeignKey, Column, String, Integer, CHAR, CheckConstraint, join
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    ssn = Column("ssn", Integer, primary_key=True)
    firstname =  Column("FirstName", String)
    lastname = Column("LastName", String)
    country = Column("Country", String)
    gender = Column("Gender", CHAR(1), CheckConstraint('gender = upper(gender)'))
    expertise = Column("Expertise", String)
    age = Column("Age", Integer)

    pets = relationship('Pet', back_populates='owner')

    def __init__(self, ssn, firstname, lastname, country, gender, expertise, age):
        self.ssn = ssn
        self.firstname = firstname
        self.lastname = lastname
        self.country = country
        self.gender = gender
        self.expertise = expertise
        self.age = age

    def __repr__(self):
        return f"({self.ssn}) {self.firstname} {self.lastname} ({self.gender},{self.age})"
    
class Pet(Base):
    __tablename__ = 'pets'

    id = Column("ID", Integer, primary_key=True)
    name = Column("NAME", String)
    owner_id = Column("OWNER", Integer, ForeignKey('users.ssn'))

    def __init__(self, id, name, owner_id):
        self.id = id
        self.name = name
        self.owner_id = owner_id

    def __repr__(self):
        return f"({self.id}) ({self.name}) ({self.owner_id})"

    owner = relationship('User', back_populates='pets')
    
engine = create_engine("sqlite:///mydb.db", echo=True)
Base.metadata.create_all(bind=engine)

Session = sessionmaker(bind=engine)
session = Session()

user1 = User(1000, "John", "Doe", "San Fransisco", "F", "Software Engineer", 35)
user2 = User(1001, "Jane", "Doe", "Mexico", "M", "Data Analyst", 25)
user3 = User(1002, "Bob", "Smith", "Los Angeles", "M", "Python Developer", 30)
user4 = User(1003, "Brandy", "Smith", "Califonia", "F", "Technical Writer", 23)
user5 = User(1004, "Blue", "Ivy", "Texas", "F", "Singer", 21)
# session.add(user1)
# session.add(user2)
# session.add(user3)
# session.add(user4)
# session.add(user5)
# session.commit()

pet1 = Pet(1, "Dog", user1.ssn)
pet2 = Pet(2, "Cat", user1.ssn)
pet3 = Pet(3, "Rabbit", user4.ssn)
pet4 = Pet(4, "Rabbit", user3.ssn)
# session.add(pet1)
# session.add(pet2)
# session.add(pet3)
# session.add(pet4)
# session.commit()

# Output all entries from the users table
output = session.query(User).all()
print(output)

# Output all entries from the pets table
output = session.query(Pet).all()
print(output)

# Output all entries from the users table with lastname "Doe"
output = session.query(Pet).filter(User.lastname == "Doe")
for i in output:
    print(i)

# Output all entries with pet name "Rabbit"
output = session.query(Pet).filter(Pet.name == "Rabbit")
for i in output:
    print(i)

# Output all users whose contry starts with the letter "M"
output = session.query(User).filter(User.country.like("M%"))
for i in output:
    print(i)

# Sorting the User object by age in decending order
output = session.query(User).order_by(User.age.desc()).all()
for i in output:
    print(i)

# Sorting the User object by age in decending order, then by firstname in asending order
output = session.query(User).order_by(User.age.desc(), User.firstname.asc()).all()
for i in output:
    print(i)

# Joining and Selecing from the users and pet tables 

joined_tables = join(User, Pet, User.ssn == Pet.owner_id)
result = session.query(User.firstname, Pet.name).select_from(joined_tables).all()

for row in result:
    print(row)
