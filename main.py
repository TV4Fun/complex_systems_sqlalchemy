from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from models import *

engine = create_engine('postgresql://postgres:pword@localhost:5432/complex_systems_sqlalchemy', echo=True)
Model.metadata.drop_all(engine)
Model.metadata.create_all(engine)

session = Session(engine)

# Universities
uc_davis = University(name='UC Davis', location='Outside Sacramento')
cornell = University(name='Cornell', location='Ithaca, NY')
caltech = University(name='CalTech', location='Pasadena')
indiana = University(name='Indiana University', url='https://www.indiana.edu/academics/schools.html', location='Indiana')

# Topics
comp_mech = Topic(name='Computational Mechanics')
synchronization = Topic(name='Synchronization')

# Researchers
jim_crutchfield = Researcher(name='Jim Crutchfield', university=uc_davis)
raissa_dsouza = Researcher(name="Raissa D'Souza", university=uc_davis, url='http://mae.engr.ucdavis.edu/dsouza/')
steven_strogatz = Researcher(name="Steven Strogatz", university=cornell, url='https://math.cornell.edu/steven-strogatz')
michael_roukes = Researcher(name="Michael Roukes", university=caltech, url='http://nano.caltech.edu/people/roukes-m.html')
matt_matheny = Researcher(name="Matt Matheny", university=caltech, url='http://pma.divisions.caltech.edu/people/matt-matheny')
louis_pecora = Researcher(name="Louis Pecora")
yohiki_kuramoto = Researcher(name="Yoshiki Kuramoto")

# Centers
csc = Center(name='Complexity Sciences Center', url='http://csc.ucdavis.edu/Welcome.html', university=uc_davis)
santa_fe = Center(name='Santa Fe Institute', url='https://www.santafe.edu/')
nrl = Center(name='United States Naval Research Laboratory')
quanta = Center(name="Quanta Magazine", url="https://www.quantamagazine.org/")
