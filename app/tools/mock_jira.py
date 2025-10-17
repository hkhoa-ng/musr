JIRA_TICKETS = [
    {
        "epic": {
            "key": "ALF-100",
            "title": "User-Driven Interaction Assistant",
            "description": "Develop a voice-controlled virtual butler to assist older adults with daily tasks at home and on the go, ensuring accessibility and ease of use.",
        },
        "tickets": [
            {
                "key": "ALF-101",
                "title": "Implement Voice Interaction for Commands",
                "description": (
                    "Enable ALFRED to accept voice commands for daily tasks.\n\n"
                    "Acceptance Criteria:\n"
                    "- Users can issue voice commands (e.g., 'set reminder', 'call friend') in natural language.\n"
                    "- System recognizes commands with 95% accuracy in quiet environments.\n"
                    "- ALFRED responds with clear, loud speech.\n"
                    "- Supports multiple languages (English, French, German, Dutch).\n"
                    "- Handles misrecognized commands with polite prompts to repeat."
                ),
            },
            {
                "key": "ALF-102",
                "title": "Develop Agenda and Reminder System",
                "description": (
                    "Create a system for managing agendas and reminders.\n\n"
                    "Acceptance Criteria:\n"
                    "- Users can set appointments and reminders via voice (e.g., 'remind me to take pills at 8 PM').\n"
                    "- System syncs agenda with user’s smartphone or tablet.\n"
                    "- Reminders are delivered via voice and visual notifications.\n"
                    "- Users can review and edit agenda entries vocally.\n"
                    "- System confirms reminder settings with verbal feedback."
                ),
            },
            {
                "key": "ALF-103",
                "title": "Integrate Home Domotics Control",
                "description": (
                    "Enable ALFRED to control home appliances.\n\n"
                    "Acceptance Criteria:\n"
                    "- Users can control lights, heating, and shades via voice commands (e.g., 'turn off living room light').\n"
                    "- System integrates with common smart home protocols (e.g., Zigbee, Z-Wave).\n"
                    "- Commands execute within 2 seconds.\n"
                    "- Provides feedback on action status (e.g., 'Light turned off').\n"
                    "- Supports fallback manual controls for power outages."
                ),
            },
            {
                "key": "ALF-104",
                "title": "Provide Navigation Support",
                "description": (
                    "Implement navigation assistance for users on the go.\n\n"
                    "Acceptance Criteria:\n"
                    "- Users can request directions via voice (e.g., 'guide me to the nearest pharmacy').\n"
                    "- System provides step-by-step voice-guided navigation.\n"
                    "- Routes prioritize accessibility (e.g., avoiding stairs).\n"
                    "- Visual map displayed on companion app for users with smartphones.\n"
                    "- Updates directions in real-time if user deviates from route."
                ),
            },
        ],
    },
    {
        "epic": {
            "key": "ALF-200",
            "title": "Personalized Social Inclusion",
            "description": "Develop features to connect older adults with social events and contacts to prevent isolation, tailored to their interests.",
        },
        "tickets": [
            {
                "key": "ALF-201",
                "title": "Suggest Personalized Social Events",
                "description": (
                    "Enable ALFRED to suggest social events based on user interests.\n\n"
                    "Acceptance Criteria:\n"
                    "- System suggests events (e.g., cultural events, local meetups) based on user preferences.\n"
                    "- Suggestions delivered via voice (e.g., 'There’s a concert tomorrow, would you like to attend?').\n"
                    "- Users can accept or decline suggestions vocally.\n"
                    "- Events are sourced from local APIs or community calendars.\n"
                    "- Tracks user participation to refine future suggestions."
                ),
            },
            {
                "key": "ALF-202",
                "title": "Facilitate Communication with Contacts",
                "description": (
                    "Allow users to connect with friends and family via ALFRED.\n\n"
                    "Acceptance Criteria:\n"
                    "- Users can initiate calls or messages via voice (e.g., 'call my daughter').\n"
                    "- System accesses user’s contact list securely.\n"
                    "- Supports video calls for devices with cameras.\n"
                    "- Provides tactile or auditory feedback for call initiation.\n"
                    "- Handles failed connections with clear error messages."
                ),
            },
            {
                "key": "ALF-203",
                "title": "Organize Social Group Activities",
                "description": (
                    "Enable users to join or organize social group activities.\n\n"
                    "Acceptance Criteria:\n"
                    "- Users can join local social groups via voice commands (e.g., 'find a book club near me').\n"
                    "- System allows users to create events and invite contacts.\n"
                    "- Event details are shared via voice and app notifications.\n"
                    "- Tracks RSVPs and reminds users of upcoming events.\n"
                    "- Integrates with social platforms for broader reach."
                ),
            },
            {
                "key": "ALF-204",
                "title": "Enable Online Multiplayer Games",
                "description": (
                    "Provide online games to connect users with others.\n\n"
                    "Acceptance Criteria:\n"
                    "- Users can join multiplayer games (e.g., card games, trivia) via voice commands.\n"
                    "- Games support interaction with friends or other ALFRED users.\n"
                    "- System ensures low latency for smooth gameplay.\n"
                    "- Games are accessible with simple voice or button controls.\n"
                    "- Tracks game participation for social engagement metrics."
                ),
            },
        ],
    },
    {
        "epic": {
            "key": "ALF-300",
            "title": "Effective & Personalized Care",
            "description": "Implement health monitoring and care coordination features using wearable sensors to support caregivers and medical staff.",
        },
        "tickets": [
            {
                "key": "ALF-301",
                "title": "Monitor Vital Signs via Wearables",
                "description": (
                    "Enable ALFRED to collect and share vital signs from wearable sensors.\n\n"
                    "Acceptance Criteria:\n"
                    "- System collects heart rate, blood pressure, body temperature, and breathing frequency.\n"
                    "- Data is transmitted securely to caregivers via a dedicated interface.\n"
                    "- Alerts caregivers if vitals exceed safe thresholds.\n"
                    "- Wearables are unobtrusive and comfortable (e.g., T-shirt sensors).\n"
                    "- Data updates every 5 minutes or on-demand."
                ),
            },
            {
                "key": "ALF-302",
                "title": "Implement Fall Detection and Alerts",
                "description": (
                    "Develop fall detection and emergency response features.\n\n"
                    "Acceptance Criteria:\n"
                    "- System detects falls using wearable sensors with 90% accuracy.\n"
                    "- Automatically alerts emergency contacts or services upon fall detection.\n"
                    "- Users can trigger manual emergency alerts via voice or button.\n"
                    "- Alerts include user’s location.\n"
                    "- False positives are minimized through confirmation prompts."
                ),
            },
            {
                "key": "ALF-303",
                "title": "Medication Reminder and Validation",
                "description": (
                    "Create a system for medication reminders and tracking.\n\n"
                    "Acceptance Criteria:\n"
                    "- Users receive voice reminders for medication schedules (e.g., 'Take your pill now').\n"
                    "- System confirms medication intake via voice or button press.\n"
                    "- Logs medication adherence for caregiver review.\n"
                    "- Supports multiple medications with distinct schedules.\n"
                    "- Alerts caregivers if doses are missed."
                ),
            },
            {
                "key": "ALF-304",
                "title": "Enable Caregiver Data Access",
                "description": (
                    "Provide caregivers with access to user health data.\n\n"
                    "Acceptance Criteria:\n"
                    "- Caregivers can view real-time vital signs and activity levels via a secure portal.\n"
                    "- Portal supports role-based access (formal vs. informal caregivers).\n"
                    "- Users can grant or revoke data access via voice commands.\n"
                    "- Data is encrypted end-to-end.\n"
                    "- Portal is accessible on web and mobile devices."
                ),
            },
        ],
    },
    {
        "epic": {
            "key": "ALF-400",
            "title": "Physical & Cognitive Impairments Prevention",
            "description": "Develop serious games and exercises to improve physical and cognitive health, tailored to older adults’ needs.",
        },
        "tickets": [
            {
                "key": "ALF-401",
                "title": "Implement Cognitive Stimulation Games",
                "description": (
                    "Create games to enhance cognitive abilities.\n\n"
                    "Acceptance Criteria:\n"
                    "- Games include memory exercises and puzzles tailored to user interests (e.g., architecture, arts).\n"
                    "- Accessible via voice or simple button controls.\n"
                    "- Games adapt difficulty based on user performance.\n"
                    "- Tracks progress and provides motivational feedback.\n"
                    "- Limits session duration to prevent fatigue."
                ),
            },
            {
                "key": "ALF-402",
                "title": "Develop Physical Exercise Games",
                "description": (
                    "Create games to promote physical activity.\n\n"
                    "Acceptance Criteria:\n"
                    "- Games include exercises for muscle groups and coordination (e.g., arm-leg opposition).\n"
                    "- Supports virtual sports (e.g., skiing, diving) for engagement.\n"
                    "- Provides real-time feedback on posture and movement.\n"
                    "- Exercises are checked by virtual trainer and periodically reviewed.\n"
                    "- Tracks exercise results and suggests variations."
                ),
            },
            {
                "key": "ALF-403",
                "title": "Motivate Regular Exercise",
                "description": (
                    "Implement motivational features for exercise adherence.\n\n"
                    "Acceptance Criteria:\n"
                    "- System sends voice reminders for daily exercise (e.g., 'Time for your workout').\n"
                    "- Offers rewards (e.g., virtual badges) for consistent participation.\n"
                    "- Suggests new activities based on user progress (e.g., 'Try yoga this week').\n"
                    "- Tracks adherence and shares summaries with users.\n"
                    "- Integrates with health data to tailor recommendations."
                ),
            },
            {
                "key": "ALF-404",
                "title": "Provide Healthy Lifestyle Tips",
                "description": (
                    "Offer tips and recipes for a healthy lifestyle.\n\n"
                    "Acceptance Criteria:\n"
                    "- System delivers voice-based healthy recipes tailored to dietary needs.\n"
                    "- Provides daily tips (e.g., 'Drink water to stay hydrated').\n"
                    "- Tips are sourced from credible health databases.\n"
                    "- Users can request tips on-demand (e.g., 'Give me a healthy snack idea').\n"
                    "- Tracks user engagement with tips for personalization."
                ),
            },
        ],
    },
    {
        "epic": {
            "key": "ALF-500",
            "title": "Core System Requirements",
            "description": "Implement general system functionalities, including accessibility, privacy, and developer support.",
        },
        "tickets": [
            {
                "key": "ALF-501",
                "title": "Ensure Accessibility for Vision and Hearing",
                "description": (
                    "Adapt ALFRED for users with vision or hearing impairments.\n\n"
                    "Acceptance Criteria:\n"
                    "- System supports adjustable font sizes and zoom.\n"
                    "- Offers high-contrast visuals for low vision.\n"
                    "- Provides loud, slow speech with repeat options.\n"
                    "- Includes tactile feedback for touch inputs.\n"
                    "- Tested with users having mild vision/hearing impairments."
                ),
            },
            {
                "key": "ALF-502",
                "title": "Implement Data Privacy and Security",
                "description": (
                    "Ensure user data is protected. User has complete control over their personal data.\n\n"
                    "Acceptance Criteria:\n"
                    "- All data is encrypted in transit and at rest (EU Directive 95/46/EC).\n"
                    "- Users can control data sharing permissions via voice.\n"
                    "- Health data is accessible only to authorized caregivers.\n"
                    "- System logs access attempts for auditing.\n"
                    "- Passes third-party security audit."
                ),
            },
            {
                "key": "ALF-503",
                "title": "Develop ALFREDO Marketplace for Apps",
                "description": (
                    "Create a marketplace for third-party ALFRED apps.\n\n"
                    "Acceptance Criteria:\n"
                    "- Developers can submit apps via a high-level API.\n"
                    "- Marketplace displays apps with clear descriptions.\n"
                    "- Users can install apps via voice commands.\n"
                    "- System tracks app performance and crashes.\n"
                    "- Provides API documentation and support."
                ),
            },
            {
                "key": "ALF-504",
                "title": "Ensure Battery and Wearable Reliability",
                "description": (
                    "Optimize battery life and wearable functionality.\n\n"
                    "Acceptance Criteria:\n"
                    "- Wearables last at least 24 hours on a single charge.\n"
                    "- System alerts users of low battery via voice and visual cues.\n"
                    "- Wearables are lightweight and inconspicuous.\n"
                    "- Supports reminders to wear devices daily.\n"
                    "- Tested for reliability in daily use scenarios."
                ),
            },
        ],
    },
]


def get_jira_tickets():
    """This function mocks the JIRA tickets."""
    return JIRA_TICKETS
