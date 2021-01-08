from sqlalchemy import create_engine
from sqlalchemy.ext.compiler import compiles
from sqlalchemy.orm import Session
from sqlalchemy.schema import DropTable

from models import *

engine = create_engine('postgresql://postgres:pword@localhost:5433/complex_systems_sqlalchemy', echo=True)


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
    karolinska = University(name='Karolinska Institutet', url='https://ki.se/en', location='Stockholm, Sweden')
    oxford = University(name='Oxford', url="https://www.ox.ac.uk/", location='Oxford, England')
    cambridge = University(name='Cambridge', url='https://www.cam.ac.uk/', location='Cambridge, England')

    # Degrees
    phd = Degree(name="PhD")
    mphil = Degree(name="M.Phil")
    mres = Degree(name="M.Res")
    mphil_res = Degree(name="M.Phil/Res")
    bs = Degree(name="BSc")

    # Topics
    comp_mech = Topic(name='Computational Mechanics')
    synchronization = Topic(name='Synchronization')
    alg_comp = Topic(name='Algorithmic Complexity')
    log_phil_epi = Topic(name='Logic, Philosophy and Epistemology')
    cs_theory = Topic(name='Theoretical Computer Science')

    # Centers
    csc = Center(name='Complexity Sciences Center', url='http://csc.ucdavis.edu/Welcome.html', university=uc_davis)
    santa_fe = Center(name='Santa Fe Institute', url='https://www.santafe.edu/')
    nrl = Center(name='United States Naval Research Laboratory')
    quanta = Center(name="Quanta Magazine", url="https://www.quantamagazine.org/")
    adl = Center(name='Algorithmic Dynamics Lab', url='https://www.algorithmicdynamics.net/', university=karolinska)

    # Researchers
    jim_crutchfield = Researcher(name='Jim Crutchfield', university=uc_davis)
    jim_crutchfield.affiliations.append(Affiliation(institute=csc))
    jim_crutchfield.affiliations.append(Affiliation(institute=santa_fe))

    raissa_dsouza = Researcher(name="Raissa D'Souza", university=uc_davis, url='http://mae.engr.ucdavis.edu/dsouza/')
    raissa_dsouza.affiliations.append(Affiliation(institute=csc))
    raissa_dsouza.affiliations.append(Affiliation(institute=santa_fe))
    raissa_dsouza.affiliations.append(Affiliation(institute=quanta, type="Member of magazine's advisory board"))

    steven_strogatz = Researcher(name="Steven Strogatz", university=cornell,
                                 url='https://math.cornell.edu/steven-strogatz')
    steven_strogatz.affiliations.append(Affiliation(institute=quanta, type="Member of magazine's advisory board"))

    michael_roukes = Researcher(name="Michael Roukes", university=caltech,
                                url='http://nano.caltech.edu/people/roukes-m.html')
    matt_matheny = Researcher(name="Matt Matheny", university=caltech,
                              url='http://pma.divisions.caltech.edu/people/matt-matheny')

    louis_pecora = Researcher(name="Louis Pecora")
    louis_pecora.affiliations.append(Affiliation(institute=nrl))

    yohiki_kuramoto = Researcher(name="Yoshiki Kuramoto")

    solomonoff = Researcher(name="Ray Solomonoff")

    zenil = Researcher(name="Hector Zenil", url="https://www.hectorzenil.net/home.html", university=karolinska)
    zenil.affiliations.append(Affiliation(institute=adl, type='Lab Leader'))
    zenil.affiliations.append(Affiliation(institute=oxford, type="Director, Oxford Immune Algorithmics"))
    zenil.affiliations.append(Affiliation(institute=oxford, type="Senior Researcher, Department of Computer Science"))
    zenil.affiliations.append(Affiliation(institute=cambridge, type="Associated Senior Researcher, Synthetic Biology Strategic Research Initiative"))

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
    sync_patterns.institutes.append(csc)
    sync_patterns.institutes.append(quanta)
    sync_patterns.researchers.append(raissa_dsouza)
    sync_patterns.researchers.append(steven_strogatz)
    sync_patterns.researchers.append(michael_roukes)
    sync_patterns.researchers.append(matt_matheny)
    sync_patterns.researchers.append(louis_pecora)
    sync_patterns.researchers.append(yohiki_kuramoto)
    sync_patterns.topics.append(synchronization)

    cs_bio_alg_evo = Reading(name="Mathematical Simplicity May Drive Evolution’s Speed",
                             url="https://www.quantamagazine.org/computer-science-and-biology-explore-algorithmic-evolution-20181129/")
    cs_bio_alg_evo.topics.append(alg_comp)
    cs_bio_alg_evo.institutes.append(quanta)

    aid = Reading(name="Algorithmic Information Dynamics",
                  url="http://www.scholarpedia.org/article/Algorithmic_Information_Dynamics")
    aid.topics.append(alg_comp)

    alg_prob = Reading(name="Algorithmic Probability",
                       url="http://www.scholarpedia.org/article/Algorithmic_probability")
    alg_prob.researchers.append(solomonoff)
    alg_prob.researchers.append(zenil)
    alg_prob.topics.append(alg_comp)

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
    genetic_memory = Note(
        name=""""genetic memory, in turn, yielded greater structure more quickly — implying, the researchers propose, that algorithmically probable mutations can lead to diversity explosions and extinctions, too." """,
        reading=cs_bio_alg_evo)

    Model.metadata.drop_all(engine)
    Model.metadata.create_all(engine)

    with Session(engine) as session:
        session.add_all(x for x in locals().values() if isinstance(x, Model))
        session.commit()
