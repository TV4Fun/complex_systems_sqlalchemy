from sqlalchemy import create_engine
from sqlalchemy.ext.compiler import compiles
from sqlalchemy.orm import Session
from sqlalchemy.schema import DropTable

from models import *

engine = create_engine('postgresql://postgres:pword@localhost:5432/complex_systems_sqlalchemy', echo=True)


@compiles(DropTable, "postgresql")
def _compile_drop_table(element, compiler, **kwargs):
    return compiler.visit_drop_table(element) + " CASCADE"


def rebuild():
    # Universities
    uc_davis = University(name='UC Davis', location='Outside Sacramento')
    cornell = University(name='Cornell', location='Ithaca, NY')
    caltech = University(name='CalTech', location='Pasadena')
    indiana = University(name='Indiana University', url='https://www.indiana.edu/academics/schools.html',
                         location='Indiana')

    # Topics
    comp_mech = Topic(name='Computational Mechanics')
    synchronization = Topic(name='Synchronization')

    # Centers
    csc = Center(name='Complexity Sciences Center', url='http://csc.ucdavis.edu/Welcome.html', university=uc_davis)
    santa_fe = Center(name='Santa Fe Institute', url='https://www.santafe.edu/')
    nrl = Center(name='United States Naval Research Laboratory')
    quanta = Center(name="Quanta Magazine", url="https://www.quantamagazine.org/")

    # Researchers
    jim_crutchfield = Researcher(name='Jim Crutchfield', university=uc_davis)
    jim_crutchfield.affiliations.append(Affiliation(center=csc))
    jim_crutchfield.affiliations.append(Affiliation(center=santa_fe))

    raissa_dsouza = Researcher(name="Raissa D'Souza", university=uc_davis, url='http://mae.engr.ucdavis.edu/dsouza/')
    raissa_dsouza.affiliations.append(Affiliation(center=csc))
    raissa_dsouza.affiliations.append(Affiliation(center=santa_fe))
    raissa_dsouza.affiliations.append(Affiliation(center=quanta, type="Member of magazine's advisory board"))

    steven_strogatz = Researcher(name="Steven Strogatz", university=cornell,
                                 url='https://math.cornell.edu/steven-strogatz')
    steven_strogatz.affiliations.append(Affiliation(center=quanta, type="Member of magazine's advisory board"))

    michael_roukes = Researcher(name="Michael Roukes", university=caltech,
                                url='http://nano.caltech.edu/people/roukes-m.html')
    matt_matheny = Researcher(name="Matt Matheny", university=caltech,
                              url='http://pma.divisions.caltech.edu/people/matt-matheny')

    louis_pecora = Researcher(name="Louis Pecora")
    louis_pecora.affiliations.append(Affiliation(center=nrl))

    yohiki_kuramoto = Researcher(name="Yoshiki Kuramoto")

    # Readings
    comp_mech_origins = Reading(name='Dynamics, Information, and Organization: The Origins of Computational Mechanics',
                                url="https://sinews.siam.org/Details-Page/dynamics-information-and-organization-the-origins-of-computational-mechanics",
                                researchers=[jim_crutchfield])
    comp_mech_origins.topics.append(comp_mech)

    sync = Reading(name='Sync: How Order Emerges from Chaos in the Universe, Nature, and Daily Life',
                   url='https://www.powells.com/book/sync-how-order-emerges-from-chaos-in-the-universe-nature-daily-life-9780786887217',
                   researchers=[steven_strogatz])
    sync.topics.append(synchronization)

    sync_patterns = Reading(name='Scientists Discover Exotic New Patterns of Synchronization',
                            url='https://www.quantamagazine.org/physicists-discover-exotic-patterns-of-synchronization-20190404/')
    sync_patterns.centers.append(csc)
    sync_patterns.researchers.append(raissa_dsouza)
    sync_patterns.researchers.append(steven_strogatz)
    sync_patterns.researchers.append(michael_roukes)
    sync_patterns.researchers.append(matt_matheny)
    sync_patterns.researchers.append(louis_pecora)
    sync_patterns.researchers.append(yohiki_kuramoto)
    sync_patterns.topics.append(synchronization)

    # Notes
    sync_quantum = Note(name="Long range synchronization like this almost sounds like quantum entanglement",
                        reading=sync_patterns, topic=synchronization)
    sync_asymmetries = Note(name="""Asymmetries can actually help systems stay synchronized, where as too much similarity or symmetry between oscillators can cause unstable islands to form more easily
    Argument for diversity?
    Monte Carlo simulation?
    Redundancy can help keep the integrity of the system, but it can work better when the redundant components are not exact duplicates
    Require two people to work in tandem on especially sensitive equipment—it is unlikely that both of them will be traitors.
    “A variety of tasks can be achieved by a suitable combination of synchrony and asynchrony,” Kuramoto observed in an email. “Without a doubt, the processes of biological evolution must have developed this highly useful mechanism. I expect man-made systems will also become much more functionally flexible by introducing similar mechanisms.”
    """, reading=sync_patterns, topic=synchronization, researcher=yohiki_kuramoto)

    Model.metadata.drop_all(engine)
    Model.metadata.create_all(engine)

    with Session(engine) as session:
        session.add_all(x for x in locals().values() if isinstance(x, Model))
        session.commit()
