from production import IF, AND, THEN, FAIL, OR

## ZOOKEEPER RULES
ZOOKEEPER_RULES = (
    
    IF( AND( '(?x) has hair' ),         # Z1
        THEN( '(?x) is a mammal' )),
   
    IF( AND( '(?x) gives milk' ),       # Z2
        THEN( '(?x) is a mammal' )),
    
    IF( AND( '(?x) has feathers' ),     # Z3
        THEN( '(?x) is a bird' )),
   
    IF( AND( '(?x) flies',              # Z4
             '(?x) lays eggs' ),
        THEN( '(?x) is a bird' )),
   
    IF( AND( '(?x) is a mammal',        # Z5
             '(?x) eats meat' ),
        THEN( '(?x) is a carnivore' )),
   
    IF( AND( '(?x) is a mammal',        # Z6
             '(?x) has pointed teeth',
             '(?x) has claws',
             '(?x) has forward-pointing eyes' ),
        THEN( '(?x) is a carnivore' )),
    
    IF( AND( '(?x) is a mammal',        # Z7
             '(?x) has hoofs' ),
        THEN( '(?x) is an ungulate' )),
    
    IF( AND( '(?x) is a mammal',        # Z8
             '(?x) chews cud' ),
        THEN( '(?x) is an ungulate' )),
    
    IF( AND( '(?x) is a carnivore',     # Z9
             '(?x) has tawny color',
             '(?x) has dark spots' ),
        THEN( '(?x) is a cheetah' )),
    
    IF( AND( '(?x) is a carnivore',     # Z10
             '(?x) has tawny color',
             '(?x) has black stripes' ),
        THEN( '(?x) is a tiger' )),
    
    IF( AND( '(?x) is an ungulate',     # Z11
             '(?x) has long legs',
             '(?x) has long neck',
             '(?x) has tawny color',
             '(?x) has dark spots' ),
        THEN( '(?x) is a giraffe' )),
    
    IF( AND( '(?x) is an ungulate',     # Z12
             '(?x) has white color',
             '(?x) has black stripes' ),
        THEN( '(?x) is a zebra' )),
    
    IF( AND( '(?x) is a bird',          # Z13
             '(?x) does not fly',
             '(?x) has long legs',
             '(?x) has long neck',
             '(?x) has black and white color' ),
        THEN( '(?x) is an ostrich' )),
    
    IF( AND( '(?x) is a bird',          # Z14
             '(?x) does not fly',
             '(?x) swims',
             '(?x) has black and white color' ),
        THEN( '(?x) is a penguin' )),
    
    IF( AND( '(?x) is a bird',        # Z15
             '(?x) is a good flyer' ),
        THEN( '(?x) is an albatross' )),
    
    )


TOURIST_RULES = (

    # General facts that could apply to both
    IF( AND( '(?x) wears clothing that stands out' ),  # F1
        THEN( '(?x) is noticeable' )),
    
    IF( AND( '(?x) walks slowly' ),  # F2
        THEN( '(?x) moves cautiously' )),

    IF( AND( '(?x) frequently checks a device' ),  # F3
        THEN( '(?x) is dependent on technology' )),
    
    IF( AND( '(?x) takes frequent photos' ),  # F4
        THEN( '(?x) likes to document experiences' )),

    IF( AND( '(?x) asks about Luna-City history' ),  # F5
        THEN( '(?x) is interested in lunar knowledge' )),

    IF( AND( '(?x) shows excitement when visiting landmarks' ),  # F6
        THEN( '(?x) is enthusiastic about Luna-City' )),

    # Differentiation based on context
    IF( AND( '(?x) is noticeable',
             '(?x) wears bright flashy clothing' ),  # T1
        THEN( '(?x) is a tourist' )),

    IF( AND( '(?x) is noticeable',
             '(?x) wears muted, utilitarian clothing' ),  # L1
        THEN( '(?x) is a Loonie' )),
    
    IF( AND( '(?x) moves cautiously',
             '(?x) takes photos while walking' ),  # T2
        THEN( '(?x) is a tourist' )),
    
    IF( AND( '(?x) moves cautiously',
             '(?x) avoids hazards in lunar gravity' ),  # L2
        THEN( '(?x) is a Loonie' )),
    
    IF( AND( '(?x) is dependent on technology',
             '(?x) frequently checks for directions' ),  # T3
        THEN( '(?x) is a tourist' )),
    
    IF( AND( '(?x) is dependent on technology',
             '(?x) uses tech to navigate efficiently' ),  # L3
        THEN( '(?x) is a Loonie' )),
    
    IF( AND( '(?x) likes to document experiences',
             '(?x) takes selfies at landmarks' ),  # T4
        THEN( '(?x) is a tourist' )),
    
    IF( AND( '(?x) likes to document experiences',
             '(?x) takes notes for academic purposes' ),  # T5
        THEN( '(?x) is an academic tourist' )),
    
    IF( AND( '(?x) is interested in lunar knowledge',
             '(?x) asks basic questions about lunar history' ),  # T6
        THEN( '(?x) is a tourist' )),

    IF( AND( '(?x) is interested in lunar knowledge',
             '(?x) asks in-depth technical questions' ),  # L4
        THEN( '(?x) is a Loonie' )),
    
    IF( AND( '(?x) is enthusiastic about Luna-City',
             '(?x) expresses nostalgia for Earth' ),  # T7
        THEN( '(?x) is an Earth retiree tourist' )),

    IF( AND( '(?x) is enthusiastic about Luna-City',
             '(?x) discusses Luna-City innovations' ),  # L5
        THEN( '(?x) is a Loonie' )),

    # More complex classifications based on combinations
    IF( AND( '(?x) is a tourist',
             '(?x) wears business attire',
             '(?x) asks about corporate policies' ),  # T8
        THEN( '(?x) is an Earth business traveler' )),

    IF( AND( '(?x) is a tourist',
             '(?x) wears adventure-themed clothing',
             '(?x) asks about lunar landmarks' ),  # T9
        THEN( '(?x) is an Earth explorer' )),

    IF( AND( '(?x) is a tourist',
             '(?x) talks about lunar research',
             '(?x) takes notes for academic purposes' ),  # T10
        THEN( '(?x) is an Earth academic' )),

    IF( AND( '(?x) is a tourist',
             '(?x) wears stylish outfits',
             '(?x) records videos constantly' ),  # T11
        THEN( '(?x) is an Earth influencer' )),

    IF( AND( '(?x) is a tourist',
             '(?x) moves slowly in lunar gravity',
             '(?x) talks nostalgically about Earth' ),  # T12
        THEN( '(?x) is an Earth retiree' ))
)