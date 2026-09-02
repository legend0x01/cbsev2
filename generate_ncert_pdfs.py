"""
NCERT Notes PDF Generator
Fetches notes from multiple websites and generates PDF files for all chapters
across Classes 9, 10, 11, 12 for all subjects.
"""

import os
import json
import time
import requests
from bs4 import BeautifulSoup
from fpdf import FPDF
from urllib.parse import quote_plus, urljoin
import re

# =============================================================================
# NCERT CURRICULUM DEFINITION - All Classes 9-12, All Subjects, All Chapters
# =============================================================================

NCERT_CURRICULUM = {
    "9": {
        "Science": {
            "chapters": [
                "Chapter 1: Matter in Our Surroundings",
                "Chapter 2: Is Matter Around Us Pure?",
                "Chapter 3: Atoms and Molecules",
                "Chapter 4: Structure of the Atom",
                "Chapter 5: The Fundamental Unit of Life",
                "Chapter 6: Tissues",
                "Chapter 7: Diversity in Living Organisms",
                "Chapter 8: Motion",
                "Chapter 9: Force and Laws of Motion",
                "Chapter 10: Gravitation",
                "Chapter 11: Work and Energy",
                "Chapter 12: Sound",
                "Chapter 13: Why Do We Fall Ill",
                "Chapter 14: Natural Resources",
                "Chapter 15: Improvement in Food Resources"
            ],
            "search_terms": [
                "Matter in Our Surroundings", "Is Matter Around Us Pure", "Atoms and Molecules",
                "Structure of the Atom", "Fundamental Unit of Life", "Tissues",
                "Diversity in Living Organisms", "Motion", "Force and Laws of Motion",
                "Gravitation", "Work and Energy", "Sound", "Why Do We Fall Ill",
                "Natural Resources", "Improvement in Food Resources"
            ]
        },
        "Mathematics": {
            "chapters": [
                "Chapter 1: Number Systems",
                "Chapter 2: Polynomials",
                "Chapter 3: Coordinate Geometry",
                "Chapter 4: Linear Equations in Two Variables",
                "Chapter 5: Introduction to Euclid's Geometry",
                "Chapter 6: Lines and Angles",
                "Chapter 7: Triangles",
                "Chapter 8: Quadrilaterals",
                "Chapter 9: Areas of Parallelograms and Triangles",
                "Chapter 10: Circles",
                "Chapter 11: Constructions",
                "Chapter 12: Heron's Formula",
                "Chapter 13: Surface Areas and Volumes",
                "Chapter 14: Statistics",
                "Chapter 15: Probability"
            ],
            "search_terms": [
                "Number Systems", "Polynomials", "Coordinate Geometry",
                "Linear Equations in Two Variables", "Introduction to Euclid's Geometry",
                "Lines and Angles", "Triangles", "Quadrilaterals",
                "Areas of Parallelograms and Triangles", "Circles", "Constructions",
                "Heron's Formula", "Surface Areas and Volumes", "Statistics", "Probability"
            ]
        },
        "Social Science": {
            "chapters": [
                "History Chapter 1: The French Revolution",
                "History Chapter 2: Socialism in Europe and the Russian Revolution",
                "History Chapter 3: Nazism and the Rise of Hitler",
                "History Chapter 4: Forest Society and Colonialism",
                "History Chapter 5: Pastoralists in the Modern World",
                "Geography Chapter 1: India - Size and Location",
                "Geography Chapter 2: Physical Features of India",
                "Geography Chapter 3: Drainage",
                "Geography Chapter 4: Climate",
                "Geography Chapter 5: Natural Vegetation and Wildlife",
                "Geography Chapter 6: Population",
                "Political Science Chapter 1: What is Democracy? Why Democracy?",
                "Political Science Chapter 2: Constitutional Design",
                "Political Science Chapter 3: Electoral Politics",
                "Political Science Chapter 4: Working of Institutions",
                "Political Science Chapter 5: Democratic Rights",
                "Economics Chapter 1: The Story of Village Palampur",
                "Economics Chapter 2: People as Resource",
                "Economics Chapter 3: Poverty as a Challenge",
                "Economics Chapter 4: Food Security in India"
            ],
            "search_terms": [
                "French Revolution", "Socialism in Europe Russian Revolution",
                "Nazism Rise of Hitler", "Forest Society Colonialism", "Pastoralists Modern World",
                "India Size Location", "Physical Features India", "Drainage", "Climate",
                "Natural Vegetation Wildlife", "Population", "What is Democracy Why Democracy",
                "Constitutional Design", "Electoral Politics", "Working of Institutions",
                "Democratic Rights", "Story of Village Palampur", "People as Resource",
                "Poverty Challenge", "Food Security India"
            ]
        },
        "English": {
            "chapters": [
                "Beehive Chapter 1: The Fun They Had",
                "Beehive Chapter 2: The Sound of Music",
                "Beehive Chapter 3: The Little Girl",
                "Beehive Chapter 4: A Truly Beautiful Mind",
                "Beehive Chapter 5: The Snake and the Mirror",
                "Beehive Chapter 6: My Childhood",
                "Beehive Chapter 7: Packing",
                "Beehive Chapter 8: Reach for the Top",
                "Beehive Chapter 9: The Bond of Love",
                "Beehive Chapter 10: Kathmandu",
                "Beehive Chapter 11: If I Were You",
                "Beehive Poem 1: The Road Not Taken",
                "Beehive Poem 2: Wind",
                "Beehive Poem 3: Rain on the Roof",
                "Beehive Poem 4: The Lake Isle of Innisfree",
                "Beehive Poem 5: A Legend of the Northland",
                "Beehive Poem 6: No Men Are Foreign",
                "Beehive Poem 7: The Duck and the Kangaroo",
                "Beehive Poem 8: On Killing a Tree",
                "Beehive Poem 9: The Snake Trying",
                "Beehive Poem 10: A Slumber Did My Spirit Seal",
                "Moments Chapter 1: The Lost Child",
                "Moments Chapter 2: The Adventures of Toto",
                "Moments Chapter 3: Iswaran the Storyteller",
                "Moments Chapter 4: In the Kingdom of Fools",
                "Moments Chapter 5: The Happy Prince",
                "Moments Chapter 6: Weathering the Storm in Ersama",
                "Moments Chapter 7: The Last Leaf",
                "Moments Chapter 8: A House Is Not a Home",
                "Moments Chapter 9: The Beggar"
            ],
            "search_terms": [
                "The Fun They Had", "Sound of Music", "Little Girl", "Truly Beautiful Mind",
                "Snake and Mirror", "My Childhood", "Packing", "Reach for the Top",
                "Bond of Love", "Kathmandu", "If I Were You", "Road Not Taken",
                "Wind poem", "Rain on the Roof", "Lake Isle of Innisfree", "Legend of Northland",
                "No Men Are Foreign", "Duck and Kangaroo", "On Killing a Tree", "Snake Trying",
                "Slumber Did My Spirit Seal", "Lost Child", "Adventures of Toto",
                "Iswaran Storyteller", "Kingdom of Fools", "Happy Prince",
                "Weathering Storm Ersama", "Last Leaf", "House Not Home", "Beggar"
            ]
        },
        "Hindi": {
            "chapters": [
                "Kshitij Chapter 1: Do Bailon Ki Katha",
                "Kshitij Chapter 2: Lhasa Ki Aur",
                "Kshitij Chapter 3: Upbhoktawad Ki Sanskriti",
                "Kshitij Chapter 4: Saavan Ki Phuhar",
                "Kshitij Chapter 5: Premchand Ke Phate Joothe",
                "Kshitij Chapter 6: Mere Bachpan Ke Din",
                "Kshitij Chapter 7: Sakhi",
                "Kshitij Chapter 8: Kar Chale Hum Fida",
                "Kshitij Chapter 9: Agnipath",
                "Kshitij Chapter 10: Naye Ilake Mein",
                "Kshitij Chapter 11: Khoob Ladi Mardaani",
                "Kritika Chapter 1: Is Jal Pralay Mein",
                "Kritika Chapter 2: Mere Sang Ki Auratein",
                "Kritika Chapter 3: Reedh Ki Haddi",
                "Sparsh Chapter 1: Dukh Ka Adhikar",
                "Sparsh Chapter 2: Everest Meri Shikhar Yatra",
                "Sparsh Chapter 3: Tum Kab Jaoge Atithi",
                "Sparsh Chapter 4: Vaigyanik Chetna Ke Vahak",
                "Sparsh Chapter 5: Dhool",
                "Sparsh Chapter 6: Gili Mitti",
                "Sparsh Chapter 7: Pehchan",
                "Sanchayan Chapter 1: Gillu",
                "Sanchayan Chapter 2: Smriti",
                "Sanchayan Chapter 3: Kallu Kumhar Ki Unakoti"
            ],
            "search_terms": [
                "Do Bailon Ki Katha", "Lhasa Ki Aur", "Upbhoktawad Ki Sanskriti",
                "Saavan Ki Phuhar", "Premchand Ke Phate Joothe", "Mere Bachpan Ke Din",
                "Sakhi", "Kar Chale Hum Fida", "Agnipath", "Naye Ilake Mein",
                "Khoob Ladi Mardaani", "Is Jal Pralay Mein", "Mere Sang Ki Auratein",
                "Reedh Ki Haddi", "Dukh Ka Adhikar", "Everest Meri Shikhar Yatra",
                "Tum Kab Jaoge Atithi", "Vaigyanik Chetna Ke Vahak", "Dhool",
                "Gili Mitti", "Pehchan", "Gillu", "Smriti", "Kallu Kumhar Ki Unakoti"
            ]
        }
    },
    "10": {
        "Science": {
            "chapters": [
                "Chapter 1: Chemical Reactions and Equations",
                "Chapter 2: Acids, Bases and Salts",
                "Chapter 3: Metals and Non-metals",
                "Chapter 4: Carbon and its Compounds",
                "Chapter 5: Periodic Classification of Elements",
                "Chapter 6: Life Processes",
                "Chapter 7: Control and Coordination",
                "Chapter 8: How do Organisms Reproduce?",
                "Chapter 9: Heredity and Evolution",
                "Chapter 10: Light: Reflection and Refraction",
                "Chapter 11: Human Eye and Colourful World",
                "Chapter 12: Electricity",
                "Chapter 13: Magnetic Effects of Electric Current",
                "Chapter 14: Sources of Energy",
                "Chapter 15: Our Environment",
                "Chapter 16: Sustainable Management of Natural Resources"
            ],
            "search_terms": [
                "Chemical Reactions Equations", "Acids Bases Salts", "Metals Non-metals",
                "Carbon Compounds", "Periodic Classification Elements", "Life Processes",
                "Control Coordination", "How do Organisms Reproduce", "Heredity Evolution",
                "Light Reflection Refraction", "Human Eye Colourful World", "Electricity",
                "Magnetic Effects Electric Current", "Sources of Energy", "Our Environment",
                "Sustainable Management Natural Resources"
            ]
        },
        "Mathematics": {
            "chapters": [
                "Chapter 1: Real Numbers",
                "Chapter 2: Polynomials",
                "Chapter 3: Pair of Linear Equations in Two Variables",
                "Chapter 4: Quadratic Equations",
                "Chapter 5: Arithmetic Progressions",
                "Chapter 6: Triangles",
                "Chapter 7: Coordinate Geometry",
                "Chapter 8: Introduction to Trigonometry",
                "Chapter 9: Some Applications of Trigonometry",
                "Chapter 10: Circles",
                "Chapter 11: Constructions",
                "Chapter 12: Areas Related to Circles",
                "Chapter 13: Surface Areas and Volumes",
                "Chapter 14: Statistics",
                "Chapter 15: Probability"
            ],
            "search_terms": [
                "Real Numbers", "Polynomials", "Pair of Linear Equations Two Variables",
                "Quadratic Equations", "Arithmetic Progressions", "Triangles",
                "Coordinate Geometry", "Introduction to Trigonometry",
                "Applications of Trigonometry", "Circles", "Constructions",
                "Areas Related to Circles", "Surface Areas Volumes", "Statistics", "Probability"
            ]
        },
        "Social Science": {
            "chapters": [
                "History Chapter 1: The Rise of Nationalism in Europe",
                "History Chapter 2: Nationalism in India",
                "History Chapter 3: The Making of a Global World",
                "History Chapter 4: The Age of Industrialisation",
                "History Chapter 5: Print Culture and the Modern World",
                "Geography Chapter 1: Resources and Development",
                "Geography Chapter 2: Forest and Wildlife Resources",
                "Geography Chapter 3: Water Resources",
                "Geography Chapter 4: Agriculture",
                "Geography Chapter 5: Minerals and Energy Resources",
                "Geography Chapter 6: Manufacturing Industries",
                "Geography Chapter 7: Lifelines of National Economy",
                "Political Science Chapter 1: Power Sharing",
                "Political Science Chapter 2: Federalism",
                "Political Science Chapter 3: Gender, Religion and Caste",
                "Political Science Chapter 4: Political Parties",
                "Political Science Chapter 5: Outcomes of Democracy",
                "Economics Chapter 1: Development",
                "Economics Chapter 2: Sectors of the Indian Economy",
                "Economics Chapter 3: Money and Credit",
                "Economics Chapter 4: Globalisation and the Indian Economy",
                "Economics Chapter 5: Consumer Rights"
            ],
            "search_terms": [
                "Rise of Nationalism Europe", "Nationalism India", "Making Global World",
                "Age Industrialisation", "Print Culture Modern World", "Resources Development",
                "Forest Wildlife Resources", "Water Resources", "Agriculture",
                "Minerals Energy Resources", "Manufacturing Industries", "Lifelines National Economy",
                "Power Sharing", "Federalism", "Gender Religion Caste", "Political Parties",
                "Outcomes Democracy", "Development", "Sectors Indian Economy",
                "Money Credit", "Globalisation Indian Economy", "Consumer Rights"
            ]
        },
        "English": {
            "chapters": [
                "First Flight Chapter 1: A Letter to God",
                "First Flight Chapter 2: Nelson Mandela: Long Walk to Freedom",
                "First Flight Chapter 3: Two Stories About Flying",
                "First Flight Chapter 4: From the Diary of Anne Frank",
                "First Flight Chapter 5: The Hundred Dresses - I",
                "First Flight Chapter 6: The Hundred Dresses - II",
                "First Flight Chapter 7: Glimpses of India",
                "First Flight Chapter 8: Mijbil the Otter",
                "First Flight Chapter 9: Madam Rides the Bus",
                "First Flight Chapter 10: The Sermon at Benares",
                "First Flight Chapter 11: The Proposal",
                "First Flight Poem 1: Dust of Snow",
                "First Flight Poem 2: Fire and Ice",
                "First Flight Poem 3: A Tiger in the Zoo",
                "First Flight Poem 4: How to Tell Wild Animals",
                "First Flight Poem 5: The Ball Poem",
                "First Flight Poem 6: Amanda!",
                "First Flight Poem 7: Animals",
                "First Flight Poem 8: The Trees",
                "First Flight Poem 9: Fog",
                "First Flight Poem 10: The Tale of Custard the Dragon",
                "First Flight Poem 11: For Anne Gregory",
                "Footprints Chapter 1: A Triumph of Surgery",
                "Footprints Chapter 2: The Thief's Story",
                "Footprints Chapter 3: The Midnight Visitor",
                "Footprints Chapter 4: A Question of Trust",
                "Footprints Chapter 5: Footprints Without Feet",
                "Footprints Chapter 6: The Making of a Scientist",
                "Footprints Chapter 7: The Necklace",
                "Footprints Chapter 8: The Hack Driver",
                "Footprints Chapter 9: Bholi",
                "Footprints Chapter 10: The Book That Saved the Earth"
            ],
            "search_terms": [
                "Letter to God", "Nelson Mandela Long Walk Freedom", "Two Stories Flying",
                "Diary Anne Frank", "Hundred Dresses", "Glimpses India", "Mijbil Otter",
                "Madam Rides Bus", "Sermon Benares", "Proposal", "Dust Snow", "Fire Ice",
                "Tiger Zoo", "Tell Wild Animals", "Ball Poem", "Amanda", "Animals poem",
                "Trees poem", "Fog poem", "Custard Dragon", "Anne Gregory",
                "Triumph Surgery", "Thief Story", "Midnight Visitor", "Question Trust",
                "Footprints Without Feet", "Making Scientist", "Necklace", "Hack Driver",
                "Bholi", "Book Saved Earth"
            ]
        },
        "Hindi": {
            "chapters": [
                "Kshitij Chapter 1: Surdas Ke Pad",
                "Kshitij Chapter 2: Tulsidas Ke Pad",
                "Kshitij Chapter 3: Jayashankar Prasad Ke Pad",
                "Kshitij Chapter 4: Suryakant Tripathi Nirala Ke Pad",
                "Kshitij Chapter 5: Nagarjun Ke Pad",
                "Kshitij Chapter 6: Girija Kumar Mathur Ke Pad",
                "Kshitij Chapter 7: Rituraj Ke Pad",
                "Kshitij Chapter 8: Manglesh Dabral Ke Pad",
                "Kshitij Chapter 9: Sarveshwar Dayal Saxena Ke Pad",
                "Kshitij Chapter 10: Ramvilas Sharma Ke Pad",
                "Kshitij Chapter 11: Harishankar Parsai Ke Pad",
                "Kritika Chapter 1: Mata Ka Anchal",
                "Kritika Chapter 2: George Pancham Ki Naak",
                "Kritika Chapter 3: Sana Sana Hath Jodi",
                "Kritika Chapter 4: Ahi Thaiya Jhulani Herani Ho Rama",
                "Sparsh Chapter 1: Kabir Ke Dohe",
                "Sparsh Chapter 2: Meera Ke Pad",
                "Sparsh Chapter 3: Bihari Ke Dohe",
                "Sparsh Chapter 4: Maithili Sharan Gupt Ke Pad",
                "Sparsh Chapter 5: Sumitranandan Pant Ke Pad",
                "Sparsh Chapter 6: Mahadevi Verma Ke Pad",
                "Sparsh Chapter 7: Viren Dangwal Ke Pad",
                "Sparsh Chapter 8: Kaifi Azmi Ke Pad",
                "Sparsh Chapter 9: Ravinder Ke Pad",
                "Sanchayan Chapter 1: Harihar Kaka",
                "Sanchayan Chapter 2: Sapno Ke Se Din",
                "Sanchayan Chapter 3: Topi Shukla"
            ],
            "search_terms": [
                "Surdas Pad", "Tulsidas Pad", "Jayashankar Prasad Pad", "Suryakant Tripathi Nirala Pad",
                "Nagarjun Pad", "Girija Kumar Mathur Pad", "Rituraj Pad", "Manglesh Dabral Pad",
                "Sarveshwar Dayal Saxena Pad", "Ramvilas Sharma Pad", "Harishankar Parsai Pad",
                "Mata Ka Anchal", "George Pancham Ki Naak", "Sana Sana Hath Jodi",
                "Ahi Thaiya Jhulani Herani Ho Rama", "Kabir Dohe", "Meera Pad", "Bihari Dohe",
                "Maithili Sharan Gupt Pad", "Sumitranandan Pant Pad", "Mahadevi Verma Pad",
                "Viren Dangwal Pad", "Kaifi Azmi Pad", "Ravinder Pad", "Harihar Kaka",
                "Sapno Ke Se Din", "Topi Shukla"
            ]
        }
    },
    "11": {
        "Physics": {
            "chapters": [
                "Chapter 1: Physical World",
                "Chapter 2: Units and Measurements",
                "Chapter 3: Motion in a Straight Line",
                "Chapter 4: Motion in a Plane",
                "Chapter 5: Laws of Motion",
                "Chapter 6: Work, Energy and Power",
                "Chapter 7: System of Particles and Rotational Motion",
                "Chapter 8: Gravitation",
                "Chapter 9: Mechanical Properties of Solids",
                "Chapter 10: Mechanical Properties of Fluids",
                "Chapter 11: Thermal Properties of Matter",
                "Chapter 12: Thermodynamics",
                "Chapter 13: Kinetic Theory",
                "Chapter 14: Oscillations",
                "Chapter 15: Waves"
            ],
            "search_terms": [
                "Physical World", "Units Measurements", "Motion Straight Line",
                "Motion Plane", "Laws of Motion", "Work Energy Power",
                "System Particles Rotational Motion", "Gravitation",
                "Mechanical Properties Solids", "Mechanical Properties Fluids",
                "Thermal Properties Matter", "Thermodynamics", "Kinetic Theory",
                "Oscillations", "Waves"
            ]
        },
        "Chemistry": {
            "chapters": [
                "Chapter 1: Some Basic Concepts of Chemistry",
                "Chapter 2: Structure of Atom",
                "Chapter 3: Classification of Elements and Periodicity in Properties",
                "Chapter 4: Chemical Bonding and Molecular Structure",
                "Chapter 5: States of Matter",
                "Chapter 6: Thermodynamics",
                "Chapter 7: Equilibrium",
                "Chapter 8: Redox Reactions",
                "Chapter 9: Hydrogen",
                "Chapter 10: The s-Block Elements",
                "Chapter 11: The p-Block Elements",
                "Chapter 12: Organic Chemistry - Some Basic Principles and Techniques",
                "Chapter 13: Hydrocarbons",
                "Chapter 14: Environmental Chemistry"
            ],
            "search_terms": [
                "Basic Concepts Chemistry", "Structure of Atom", "Classification Elements Periodicity",
                "Chemical Bonding Molecular Structure", "States of Matter", "Thermodynamics",
                "Equilibrium", "Redox Reactions", "Hydrogen", "s-Block Elements",
                "p-Block Elements", "Organic Chemistry Basic Principles", "Hydrocarbons",
                "Environmental Chemistry"
            ]
        },
        "Mathematics": {
            "chapters": [
                "Chapter 1: Sets",
                "Chapter 2: Relations and Functions",
                "Chapter 3: Trigonometric Functions",
                "Chapter 4: Principle of Mathematical Induction",
                "Chapter 5: Complex Numbers and Quadratic Equations",
                "Chapter 6: Linear Inequalities",
                "Chapter 7: Permutations and Combinations",
                "Chapter 8: Binomial Theorem",
                "Chapter 9: Sequences and Series",
                "Chapter 10: Straight Lines",
                "Chapter 11: Conic Sections",
                "Chapter 12: Introduction to Three Dimensional Geometry",
                "Chapter 13: Limits and Derivatives",
                "Chapter 14: Mathematical Reasoning",
                "Chapter 15: Statistics",
                "Chapter 16: Probability"
            ],
            "search_terms": [
                "Sets", "Relations Functions", "Trigonometric Functions",
                "Mathematical Induction", "Complex Numbers Quadratic Equations",
                "Linear Inequalities", "Permutations Combinations", "Binomial Theorem",
                "Sequences Series", "Straight Lines", "Conic Sections",
                "Three Dimensional Geometry", "Limits Derivatives", "Mathematical Reasoning",
                "Statistics", "Probability"
            ]
        },
        "Biology": {
            "chapters": [
                "Chapter 1: The Living World",
                "Chapter 2: Biological Classification",
                "Chapter 3: Plant Kingdom",
                "Chapter 4: Animal Kingdom",
                "Chapter 5: Morphology of Flowering Plants",
                "Chapter 6: Anatomy of Flowering Plants",
                "Chapter 7: Structural Organisation in Animals",
                "Chapter 8: Cell: The Unit of Life",
                "Chapter 9: Biomolecules",
                "Chapter 10: Cell Cycle and Cell Division",
                "Chapter 11: Transport in Plants",
                "Chapter 12: Mineral Nutrition",
                "Chapter 13: Photosynthesis in Higher Plants",
                "Chapter 14: Respiration in Plants",
                "Chapter 15: Plant Growth and Development",
                "Chapter 16: Digestion and Absorption",
                "Chapter 17: Breathing and Exchange of Gases",
                "Chapter 18: Body Fluids and Circulation",
                "Chapter 19: Excretory Products and their Elimination",
                "Chapter 20: Locomotion and Movement",
                "Chapter 21: Neural Control and Coordination",
                "Chapter 22: Chemical Coordination and Integration"
            ],
            "search_terms": [
                "Living World", "Biological Classification", "Plant Kingdom", "Animal Kingdom",
                "Morphology Flowering Plants", "Anatomy Flowering Plants", "Structural Organisation Animals",
                "Cell Unit Life", "Biomolecules", "Cell Cycle Cell Division",
                "Transport Plants", "Mineral Nutrition", "Photosynthesis Higher Plants",
                "Respiration Plants", "Plant Growth Development", "Digestion Absorption",
                "Breathing Exchange Gases", "Body Fluids Circulation", "Excretory Products Elimination",
                "Locomotion Movement", "Neural Control Coordination", "Chemical Coordination Integration"
            ]
        },
        "English": {
            "chapters": [
                "Hornbill Chapter 1: The Portrait of a Lady",
                "Hornbill Chapter 2: We're Not Afraid to Die...",
                "Hornbill Chapter 3: Discovering Tut: The Saga Continues",
                "Hornbill Chapter 4: Landscape of the Soul",
                "Hornbill Chapter 5: The Ailing Planet: The Green Movement's Role",
                "Hornbill Chapter 6: The Browning Version",
                "Hornbill Chapter 7: The Adventure",
                "Hornbill Chapter 8: Silk Road",
                "Hornbill Poem 1: A Photograph",
                "Hornbill Poem 2: The Laburnum Top",
                "Hornbill Poem 3: The Voice of the Rain",
                "Hornbill Poem 4: Childhood",
                "Hornbill Poem 5: Father to Son",
                "Snapshots Chapter 1: The Summer of the Beautiful White Horse",
                "Snapshots Chapter 2: The Address",
                "Snapshots Chapter 3: Ranga's Marriage",
                "Snapshots Chapter 4: Albert Einstein at School",
                "Snapshots Chapter 5: Mother's Day",
                "Snapshots Chapter 6: The Ghat of the Only World",
                "Snapshots Chapter 7: Birth",
                "Snapshots Chapter 8: The Tale of Melon City"
            ],
            "search_terms": [
                "Portrait of a Lady", "We're Not Afraid to Die", "Discovering Tut",
                "Landscape of the Soul", "Ailing Planet Green Movement", "Browning Version",
                "Adventure", "Silk Road", "Photograph poem", "Laburnum Top", "Voice of Rain",
                "Childhood poem", "Father to Son", "Summer Beautiful White Horse",
                "Address", "Ranga Marriage", "Albert Einstein School", "Mother's Day",
                "Ghat Only World", "Birth", "Tale Melon City"
            ]
        }
    },
    "12": {
        "Physics": {
            "chapters": [
                "Chapter 1: Electric Charges and Fields",
                "Chapter 2: Electrostatic Potential and Capacitance",
                "Chapter 3: Current Electricity",
                "Chapter 4: Moving Charges and Magnetism",
                "Chapter 5: Magnetism and Matter",
                "Chapter 6: Electromagnetic Induction",
                "Chapter 7: Alternating Current",
                "Chapter 8: Electromagnetic Waves",
                "Chapter 9: Ray Optics and Optical Instruments",
                "Chapter 10: Wave Optics",
                "Chapter 11: Dual Nature of Radiation and Matter",
                "Chapter 12: Atoms",
                "Chapter 13: Nuclei",
                "Chapter 14: Semiconductor Electronics",
                "Chapter 15: Communication Systems"
            ],
            "search_terms": [
                "Electric Charges Fields", "Electrostatic Potential Capacitance", "Current Electricity",
                "Moving Charges Magnetism", "Magnetism Matter", "Electromagnetic Induction",
                "Alternating Current", "Electromagnetic Waves", "Ray Optics Optical Instruments",
                "Wave Optics", "Dual Nature Radiation Matter", "Atoms", "Nuclei",
                "Semiconductor Electronics", "Communication Systems"
            ]
        },
        "Chemistry": {
            "chapters": [
                "Chapter 1: Solutions",
                "Chapter 2: Electrochemistry",
                "Chapter 3: Chemical Kinetics",
                "Chapter 4: The d and f Block Elements",
                "Chapter 5: Coordination Compounds",
                "Chapter 6: Haloalkanes and Haloarenes",
                "Chapter 7: Alcohols, Phenols and Ethers",
                "Chapter 8: Aldehydes, Ketones and Carboxylic Acids",
                "Chapter 9: Amines",
                "Chapter 10: Biomolecules",
                "Chapter 11: Polymers",
                "Chapter 12: Chemistry in Everyday Life"
            ],
            "search_terms": [
                "Solutions", "Electrochemistry", "Chemical Kinetics", "d f Block Elements",
                "Coordination Compounds", "Haloalkanes Haloarenes", "Alcohols Phenols Ethers",
                "Aldehydes Ketones Carboxylic Acids", "Amines", "Biomolecules",
                "Polymers", "Chemistry Everyday Life"
            ]
        },
        "Mathematics": {
            "chapters": [
                "Chapter 1: Relations and Functions",
                "Chapter 2: Inverse Trigonometric Functions",
                "Chapter 3: Matrices",
                "Chapter 4: Determinants",
                "Chapter 5: Continuity and Differentiability",
                "Chapter 6: Application of Derivatives",
                "Chapter 7: Integrals",
                "Chapter 8: Application of Integrals",
                "Chapter 9: Differential Equations",
                "Chapter 10: Vector Algebra",
                "Chapter 11: Three Dimensional Geometry",
                "Chapter 12: Linear Programming",
                "Chapter 13: Probability"
            ],
            "search_terms": [
                "Relations Functions", "Inverse Trigonometric Functions", "Matrices",
                "Determinants", "Continuity Differentiability", "Application Derivatives",
                "Integrals", "Application Integrals", "Differential Equations",
                "Vector Algebra", "Three Dimensional Geometry", "Linear Programming", "Probability"
            ]
        },
        "Biology": {
            "chapters": [
                "Chapter 1: Sexual Reproduction in Flowering Plants",
                "Chapter 2: Human Reproduction",
                "Chapter 3: Reproductive Health",
                "Chapter 4: Principles of Inheritance and Variation",
                "Chapter 5: Molecular Basis of Inheritance",
                "Chapter 6: Evolution",
                "Chapter 7: Human Health and Disease",
                "Chapter 8: Microbes in Human Welfare",
                "Chapter 9: Biotechnology: Principles and Processes",
                "Chapter 10: Biotechnology and its Applications",
                "Chapter 11: Organisms and Populations",
                "Chapter 12: Ecosystem",
                "Chapter 13: Biodiversity and Conservation",
                "Chapter 14: Environmental Issues"
            ],
            "search_terms": [
                "Sexual Reproduction Flowering Plants", "Human Reproduction", "Reproductive Health",
                "Principles Inheritance Variation", "Molecular Basis Inheritance", "Evolution",
                "Human Health Disease", "Microbes Human Welfare", "Biotechnology Principles Processes",
                "Biotechnology Applications", "Organisms Populations", "Ecosystem",
                "Biodiversity Conservation", "Environmental Issues"
            ]
        },
        "English": {
            "chapters": [
                "Flamingo Chapter 1: The Last Lesson",
                "Flamingo Chapter 2: Lost Spring",
                "Flamingo Chapter 3: Deep Water",
                "Flamingo Chapter 4: The Rattrap",
                "Flamingo Chapter 5: Indigo",
                "Flamingo Chapter 6: Poets and Pancakes",
                "Flamingo Chapter 7: The Interview",
                "Flamingo Chapter 8: Going Places",
                "Flamingo Poem 1: My Mother at Sixty-six",
                "Flamingo Poem 2: An Elementary School Classroom in a Slum",
                "Flamingo Poem 3: Keeping Quiet",
                "Flamingo Poem 4: A Thing of Beauty",
                "Flamingo Poem 5: A Roadside Stand",
                "Flamingo Poem 6: Aunt Jennifer's Tigers",
                "Vistas Chapter 1: The Third Level",
                "Vistas Chapter 2: The Tiger King",
                "Vistas Chapter 3: Journey to the End of the Earth",
                "Vistas Chapter 4: The Enemy",
                "Vistas Chapter 5: Should Wizard Hit Mommy?",
                "Vistas Chapter 6: On the Face of It",
                "Vistas Chapter 7: Evans Tries an O-Level",
                "Vistas Chapter 8: Memories of Childhood"
            ],
            "search_terms": [
                "Last Lesson", "Lost Spring", "Deep Water", "Rattrap", "Indigo",
                "Poets Pancakes", "Interview", "Going Places", "Mother at Sixty-six",
                "Elementary School Slum", "Keeping Quiet", "Thing of Beauty",
                "Roadside Stand", "Aunt Jennifer Tigers", "Third Level", "Tiger King",
                "Journey End Earth", "Enemy", "Wizard Hit Mommy", "Face of It",
                "Evans Tries O-Level", "Memories Childhood"
            ]
        }
    }
}

# =============================================================================
# WEBSITE SOURCES FOR NOTES (3-4 sources per chapter)
# =============================================================================

NOTE_SOURCES = {
    "learncbse": {
        "base": "https://www.learncbse.in",
        "search": "https://www.learncbse.in/search?q={query}",
        "selectors": [".post-content", ".entry-content", "article", ".content", "main"]
    },
    "tiwariacademy": {
        "base": "https://www.tiwariacademy.com",
        "search": "https://www.tiwariacademy.com/search?q={query}",
        "selectors": [".content", ".post-content", ".entry-content", "article", "main"]
    },
    "vedantu": {
        "base": "https://www.vedantu.com",
        "search": "https://www.vedantu.com/search?q={query}",
        "selectors": [".content", ".notes-content", ".chapter-content", "main"]
    },
    "topperlearning": {
        "base": "https://www.topperlearning.com",
        "search": "https://www.topperlearning.com/search?q={query}",
        "selectors": [".content", ".study-material", ".notes", "main"]
    },
    "byjus": {
        "base": "https://byjus.com",
        "search": "https://byjus.com/search?q={query}",
        "selectors": [".content", ".notes", ".chapter-notes", "main"]
    },
    "ncertbooks": {
        "base": "https://ncertbooks.net",
        "search": "https://ncertbooks.net/search?q={query}",
        "selectors": [".content", ".post-content", "article", "main"]
    },
    "ncertsolutions": {
        "base": "https://ncertsolutions.guru",
        "search": "https://ncertsolutions.guru/search?q={query}",
        "selectors": [".content", ".post-content", ".entry-content", "main"]
    }
}

# =============================================================================
# PDF GENERATOR CLASS
# =============================================================================

class NCERTNotesPDF(FPDF):
    def __init__(self, class_num, subject, chapter_title):
        super().__init__()
        self.class_num = class_num
        self.subject = subject
        self.chapter_title = chapter_title
        self.set_auto_page_break(auto=True, margin=20)
        
    def header(self):
        self.set_font('Helvetica', 'B', 14)
        self.set_text_color(30, 60, 120)
        self.cell(0, 10, f'NCERT Class {self.class_num} - {self.subject}', 0, 1, 'C')
        self.set_font('Helvetica', 'B', 11)
        self.set_text_color(60, 60, 60)
        self.cell(0, 8, self.chapter_title, 0, 1, 'C')
        self.line(10, self.get_y(), 200, self.get_y())
        self.ln(5)
        
    def footer(self):
        self.set_y(-15)
        self.set_font('Helvetica', 'I', 8)
        self.set_text_color(128, 128, 128)
        self.cell(0, 10, f'Page {self.page_no()}/{{nb}} | NCERT Notes | Class {self.class_num} {self.subject}', 0, 0, 'C')
    
    def add_section(self, title, content):
        self.set_font('Helvetica', 'B', 12)
        self.set_text_color(30, 60, 120)
        self.cell(0, 8, title, 0, 1, 'L')
        self.set_font('Helvetica', '', 10)
        self.set_text_color(40, 40, 40)
        self.multi_cell(0, 5, content)
        self.ln(3)
    
    def add_bullet_points(self, items):
        self.set_font('Helvetica', '', 10)
        self.set_text_color(40, 40, 40)
        for item in items:
            self.cell(5, 5, '')
            self.cell(4, 5, chr(8226))
            self.multi_cell(0, 5, f' {item}')
        self.ln(2)

# =============================================================================
# WEB SCRAPER FOR NOTES
# =============================================================================

class NotesScraper:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        })
    
    def search_google(self, query, num_results=5):
        """Search using DuckDuckGo HTML (no API key needed)"""
        url = f"https://html.duckduckgo.com/html/?q={quote_plus(query)}"
        try:
            resp = self.session.get(url, timeout=15)
            soup = BeautifulSoup(resp.text, 'html.parser')
            results = []
            for link in soup.select('.result__snippet a, .result__url a, a.result__snippet'):
                href = link.get('href')
                if href and href.startswith('http'):
                    results.append(href)
            return list(set(results))[:num_results]
        except Exception as e:
            print(f"  Search error: {e}")
            return []
    
    def extract_content(self, url):
        """Extract main content from a webpage"""
        try:
            resp = self.session.get(url, timeout=15)
            soup = BeautifulSoup(resp.text, 'html.parser')
            
            # Remove unwanted elements
            for tag in soup(['script', 'style', 'nav', 'header', 'footer', 'aside', 
                            'form', 'button', 'iframe', 'noscript', 'img', 'svg']):
                tag.decompose()
            
            # Try multiple selectors for content
            content = ""
            for selector in ['main', 'article', '.content', '.post-content', '.entry-content',
                           '.notes-content', '.chapter-content', '.study-material', '#content',
                           '.main-content', '.post-body', '.entry-body']:
                elem = soup.select_one(selector)
                if elem:
                    content = elem.get_text(separator='\n', strip=True)
                    if len(content) > 500:
                        break
            
            if not content or len(content) < 500:
                content = soup.get_text(separator='\n', strip=True)
            
            # Clean up
            lines = [line.strip() for line in content.split('\n') if line.strip()]
            content = '\n'.join(lines)
            
            return content[:15000]  # Limit size
        except Exception as e:
            print(f"  Extract error for {url}: {e}")
            return ""
    
    def get_notes_for_chapter(self, class_num, subject, chapter_search_term):
        """Get notes from 3-4 sources for a chapter"""
        query = f"NCERT Class {class_num} {subject} {chapter_search_term} notes"
        urls = self.search_google(query, num_results=8)
        
        all_content = []
        sources_used = []
        
        for url in urls:
            # Skip unwanted domains
            skip_domains = ['youtube.com', 'facebook.com', 'twitter.com', 'instagram.com',
                          'linkedin.com', 'pinterest.com', 'amazon.com', 'flipkart.com',
                          'quora.com', 'reddit.com', 'stackoverflow.com']
            if any(d in url for d in skip_domains):
                continue
            
            # Prefer known educational sites
            preferred = any(d in url for d in ['learncbse', 'tiwariacademy', 'vedantu', 
                                               'topperlearning', 'byjus', 'ncertbooks', 
                                               'ncertsolutions', 'aglasem', 'evidyarthi',
                                               'school.careers360', 'ncert.nic.in'])
            
            if not preferred and len(sources_used) >= 2:
                continue
                
            content = self.extract_content(url)
            if content and len(content) > 300:
                all_content.append({
                    'source': url,
                    'content': content
                })
                sources_used.append(url)
                print(f"    Got content from: {url[:60]}...")
            
            if len(all_content) >= 4:
                break
        
        return all_content

# =============================================================================
# MAIN GENERATION FUNCTION
# =============================================================================

def generate_pdf_for_chapter(class_num, subject, chapter_title, chapter_search_term, scraper, output_dir):
    """Generate a comprehensive PDF for a single chapter"""
    
    print(f"\n  Generating PDF: Class {class_num} {subject} - {chapter_title}")
    
    # Fetch notes from multiple sources
    sources_content = scraper.get_notes_for_chapter(class_num, subject, chapter_search_term)
    
    if not sources_content:
        print(f"    WARNING: No content found for {chapter_title}")
        return False
    
    # Create PDF
    pdf = NCERTNotesPDF(class_num, subject, chapter_title)
    pdf.alias_nb_pages()
    pdf.add_page()
    
    # Add chapter overview
    pdf.add_section("Chapter Overview", 
        f"This chapter covers key concepts from the NCERT Class {class_num} {subject} textbook. "
        f"Notes compiled from {len(sources_content)} educational sources for comprehensive coverage.")
    
    # Add content from each source
    for i, src in enumerate(sources_content, 1):
        source_name = src['source'].split('/')[2].replace('www.', '')
        pdf.add_section(f"Notes from Source {i}: {source_name}", src['content'][:3000])
    
    # Add key points summary section
    pdf.add_section("Key Points for Revision", 
        "1. Review all definitions and key terms from the chapter\n"
        "2. Practice numerical problems and derivations\n"
        "3. Memorize important formulas and their applications\n"
        "4. Understand diagrams and their labels\n"
        "5. Solve NCERT exemplar and previous year questions\n"
        "6. Create mind maps for quick revision before exams")
    
    # Save PDF
    safe_subject = subject.replace(' ', '_').replace('/', '_')
    safe_chapter = chapter_title.replace(':', '').replace('/', '_').replace(' ', '_')
    filename = f"{safe_chapter}.pdf"
    filepath = os.path.join(output_dir, filename)
    
    pdf.output(filepath)
    print(f"    Saved: {filename}")
    return True

def main():
    base_dir = r"C:\legend0x01!\cbsev2\assets\pdf"
    scraper = NotesScraper()
    
    total_chapters = 0
    successful = 0
    
    for class_num, subjects in NCERT_CURRICULUM.items():
        print(f"\n{'='*60}")
        print(f"PROCESSING CLASS {class_num}")
        print(f"{'='*60}")
        
        for subject, data in subjects.items():
            chapters = data['chapters']
            search_terms = data['search_terms']
            
            output_dir = os.path.join(base_dir, class_num, subject.replace(' ', '_'))
            os.makedirs(output_dir, exist_ok=True)
            
            print(f"\n  Subject: {subject} ({len(chapters)} chapters)")
            
            for idx, (chapter, search_term) in enumerate(zip(chapters, search_terms)):
                total_chapters += 1
                try:
                    if generate_pdf_for_chapter(class_num, subject, chapter, search_term, scraper, output_dir):
                        successful += 1
                    time.sleep(1)  # Be polite to servers
                except Exception as e:
                    print(f"    ERROR: {e}")
                    continue
    
    print(f"\n{'='*60}")
    print(f"COMPLETE: {successful}/{total_chapters} PDFs generated successfully")
    print(f"{'='*60}")

if __name__ == "__main__":
    main()