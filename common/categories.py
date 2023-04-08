food_and_treats = [
    "Dry food (kibble)",
    "Wet food (canned)",
    "Freeze-dried or dehydrated food",
    "Raw food (BARF diet)",
    "Treats and chews",
    "Food supplements and vitamins",
]

toys = [
    "Chew toys",
    "Fetch toys (balls, frisbees, etc.)",
    "Puzzle toys and treat dispensers",
    "Interactive toys (like laser pointers)",
    "Plush toys",
    "Catnip toys (for cats)",
    "Tug toys (for dogs)",
]

grooming_supplies = [
    "Brushes and combs",
    "Shampoos and conditioners",
    "Nail clippers and files",
    "Toothbrushes and toothpaste",
    "Ear and eye cleaning supplies",
    "Grooming gloves",
    "Hair clippers and scissors",
]

health_and_wellness = [
    "Flea and tick prevention",
    "Heartworm prevention",
    "Dewormers",
    "Joint supplements",
    "Skin and coat supplements",
    "Calming aids and anxiety relief products",
    "First aid supplies",
]

bedding_and_furniture = [
    "Beds and mats",
    "Blankets",
    "Crates and carriers",
    "Cat trees and scratching posts",
    "Dog houses",
    "Hammocks and window perches (for cats)",
    "Heating pads and cooling mats",
]

feeding_and_watering_supplies = [
    "Bowls and dishes",
    "Automatic feeders",
    "Food storage containers",
    "Water fountains and dispensers",
    "Slow feeder bowls",
    "Travel bowls and bottles",
]

collars_leashes_and_harnesses = [
    "Collars (standard, training, and breakaway)",
    "Leashes (standard, retractable, and adjustable)",
    "Harnesses (vest, step-in, and no-pull)",
    "ID tags and personalized collars",
    "Training collars (shock, vibration, and spray)",
]

training_and_behavior_aids = [
    "Clickers and whistles",
    "Training treats and pouches",
    "Puppy pads and potty training aids",
    "Bark control devices",
    "Pet gates and barriers",
    "Agility equipment",
]

clothing_and_accessories = [
    "Sweaters and coats",
    "Boots and shoes",
    "Costumes and outfits",
    "Life jackets and safety vests",
    "Collar charms and bandanas",
]

cleaning_and_odor_control = [
    "Litter boxes and litter (for cats)",
    "Poop bags and scoopers",
    "Stain and odor removers",
    "Disinfectants and sanitizers",
    "Air fresheners and odor eliminators",
]


categories = [
	"Food and treats",
	"Toys",
	"Grooming supplies",
	"Health and wellness",
	"Bedding and furniture",
	"Feeding and watering supplies",
	"Collars, leashes, and harnesses",
	"Training and behavior aids",
	"Clothing and accessories",
	"Cleaning and odor control"
]

category_dict = {
	"Food and treats": food_and_treats,
	"Toys": toys,
	"Grooming supplies": grooming_supplies,
	"Health and wellness": health_and_wellness,
	"Bedding and furniture": bedding_and_furniture,
	"Feeding and watering supplies": feeding_and_watering_supplies,
	"Collars, leashes, and harnesses": collars_leashes_and_harnesses,
	"Training and behavior aids": training_and_behavior_aids,
	"Clothing and accessories": clothing_and_accessories,
	"Cleaning and odor control": cleaning_and_odor_control,
    "General-purpose shampoos": [
        "Mild shampoos",
        "Deodorizing shampoos",
        "Moisturizing shampoos"
    ],
    "Medicated shampoos": [
        "Anti-fungal shampoos",
        "Anti-bacterial shampoos",
        "Anti-itch shampoos",
        "Anti-dandruff shampoos",
        "Hypoallergenic shampoos",
        "Shampoos for sensitive skin"
    ],
    "Flea and tick shampoos": [
        "Flea-repelling shampoos",
        "Tick-repelling shampoos",
        "Flea and tick treatment shampoos"
    ],
    "Coat-specific shampoos": [
        "Shampoos for long-haired dogs",
        "Shampoos for short-haired dogs",
        "Shampoos for curly-haired dogs",
        "Shampoos for wire-haired dogs",
        "Shampoos for double-coated dogs"
    ],
    "Color-enhancing shampoos": [
        "Shampoos for white coats",
        "Shampoos for black coats",
        "Shampoos for brown/red coats",
        "Shampoos for multi-colored coats"
    ],
    "Puppy shampoos": [
        "Gentle shampoos for puppies",
        "Tear-free shampoos for puppies"
    ],
    "Natural and organic shampoos": [
        "Vegan shampoos",
        "Eco-friendly shampoos",
        "Shampoos with essential oils",
        "Herbal shampoos"
    ],
    "Specialty shampoos": [
        "Whitening shampoos",
        "De-shedding shampoos",
        "De-matting shampoos",
        "Waterless shampoos",
        "Dry shampoos"
    ]
}



all_sub_categories: list[str] = food_and_treats + toys + grooming_supplies + health_and_wellness + bedding_and_furniture + feeding_and_watering_supplies + collars_leashes_and_harnesses + training_and_behavior_aids + clothing_and_accessories + cleaning_and_odor_control