"""
questions.py — Question bank for the OrientAI questionnaire.

Houses the full set of 25 Likert-scale items for Questionnaire 1 and 
Questionnaire 2. Ordered exactly as they appear in the original PDFs.
"""

def getQuestions() -> list[dict]:
    """Return the complete list of 25 questionnaire items for Q1."""
    return [
        {"id": "q1_1", "text": "Design illustrations or visual content for magazines."},
        {"id": "q1_2", "text": "Study the structure of the human body."},
        {"id": "q1_3", "text": "Write scripts, novels, or creative texts for publication."},
        {"id": "q1_4", "text": "Maintain and manage computer networks or data servers."},
        {"id": "q1_5", "text": "Analyze philosophical texts to debate ethics and thought."},
        {"id": "q1_6", "text": "Perform maintenance or repair tasks on common objects or electronics."},
        {"id": "q1_7", "text": "Teach new skills or knowledge to children or young people to aid their development."},
        {"id": "q1_8", "text": "Test the quality of industrial machinery or manufacturing processes."},
        {"id": "q1_9", "text": "Conduct research on the behavior of plants or animals."},
        {"id": "q1_10", "text": "Debate laws, regulations, or policies to resolve conflicts."},
        {"id": "q1_11", "text": "Design sets or environments for theatrical plays."},
        {"id": "q1_12", "text": "Organize databases and accounting systems."},
        {"id": "q1_13", "text": "Study historical events or analyze philosophical texts to understand society."},
        {"id": "q1_14", "text": "Perform complex mathematical calculations to solve physical problems."},
        {"id": "q1_15", "text": "Provide support and guidance to people in crisis situations or with personal problems."},
        {"id": "q1_16", "text": "Compose, perform, or produce musical pieces."},
        {"id": "q1_17", "text": "Assemble and maintain products on an industrial production line."},
        {"id": "q1_18", "text": "Develop a new medical treatment or procedure."},
        {"id": "q1_19", "text": "Investigate and preserve cultural heritage or archaeological remains."},
        {"id": "q1_20", "text": "Lead a team or persuade others to achieve a common goal."},
        {"id": "q1_21", "text": "Translate or analyze the structure of different languages and literatures."},
        {"id": "q1_22", "text": "Handle and process chemical or biological samples using specialized laboratory equipment."},
        {"id": "q1_23", "text": "Create a mobile application."},
        {"id": "q1_24", "text": "Provide follow-up and care for patients to improve their well-being."},
        {"id": "q1_25", "text": "Study mathematical proofs or theorems."}
    ]


def getQuestionsQ2() -> list[dict]:
    """Return the complete list of 25 questionnaire items for Q2."""
    return [
        {"id": "q2_1", "text": "I prefer getting my hands dirty testing and breaking physical machinery prototypes rather than just simulating everything on a screen."},
        {"id": "q2_2", "text": "I'm intrigued by the challenge of designing physical devices or artificial tissues that interact directly with the human body without being rejected."},
        {"id": "q2_3", "text": "I would enjoy programming the \"brain\" (microcontroller) that decides how and when an automated system should react to an obstacle."},
        {"id": "q2_4", "text": "I'd like the challenge of taking a reaction that works in a test tube and designing a way to reproduce it on an industrial scale, in quantities of tons."},
        {"id": "q2_5", "text": "I'm drawn to the idea of planning supply networks (water, sanitation) that connect and sustain an urban center."},
        {"id": "q2_6", "text": "I find great satisfaction in balancing the technical strength of a flexible material with its aesthetics, drape, and comfort against the human body."},
        {"id": "q2_7", "text": "When imagining a new space, I prioritize how natural light, acoustics, and the flow of people interact with the geometry of the place."},
        {"id": "q2_8", "text": "I would enjoy researching how different compounds react to create coatings that completely repel liquids or prevent corrosion."},
        {"id": "q2_9", "text": "I find it stimulating to calculate heat transfer, friction, and aerodynamics within a vehicle's engine to make it more efficient."},
        {"id": "q2_10", "text": "When I see an automated machine, I'm more fascinated by the complexity of its moving physical components than by the code that controls it."},
        {"id": "q2_11", "text": "I would enjoy analyzing how to process organic raw materials to extend their shelf life in a supermarket without altering their nutritional value."},
        {"id": "q2_12", "text": "I'm more drawn to creating virtual environments, databases, or digital interfaces than to designing tangible infrastructure."},
        {"id": "q2_13", "text": "I'm passionate about the challenge of calculating how to distribute the weight and forces of a massive structure so that it can withstand earthquakes or hurricane-force winds."},
        {"id": "q2_14", "text": "I find the challenge of compressing and sending encrypted information through electromagnetic waves with the lowest possible latency fascinating."},
        {"id": "q2_15", "text": "I'm fascinated by the idea of altering the atomic structure of an element to make it lighter but a hundred times stronger."},
        {"id": "q2_16", "text": "I'm more inclined toward the idea of optimizing a system's efficiency by rewriting its software rather than redesigning its mechanical or physical components."},
        {"id": "q2_17", "text": "It's important to me that the projects I work on leave a physical and visible legacy in the city's landscape."},
        {"id": "q2_18", "text": "I would prefer to use microorganism cultures (like bacteria or yeast) to decontaminate water or synthesize medicines rather than purely chemical methods."},
        {"id": "q2_19", "text": "I'm interested in designing complex networks for the generation, storage, and uninterrupted distribution of energy at a regional level."},
        {"id": "q2_20", "text": "I would enjoy designing large-scale strategies to reverse the degradation of an ecosystem or manage the waste of an entire city."},
        {"id": "q2_21", "text": "I'm more interested in understanding what an object is made of at a microscopic level than understanding how its large parts are assembled."},
        {"id": "q2_22", "text": "I would enjoy designing the gears, joints, and physical structure of a robotic arm so that it can precisely support heavy loads."},
        {"id": "q2_23", "text": "I'm motivated to explore how to weave together \"smart fibers\" that can measure the temperature or heart rate of the wearer."},
        {"id": "q2_24", "text": "I value working on problems where the variables are living, dynamic systems rather than inanimate components."},
        {"id": "q2_25", "text": "I am motivated by writing the abstract logic and algorithms necessary for software to process millions of data points instantly."}
    ]
