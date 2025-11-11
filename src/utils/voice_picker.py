import random

GOOGLE_TTS_VOICES = {
    "female": [
        "Achernar", "Aoede", "Autonoe", "Callirrhoe", "Despina",
        "Erinome", "Gacrux", "Kore", "Laomedeia", "Leda",
        "Pulcherrima", "Sulafat", "Vindemiatrix", "Zephyr"
    ],
    "male": [
        "Achird", "Algenib", "Algieba", "Alnilam", "Charon",
        "Enceladus", "Fenrir", "Iapetus", "Orus", "Puck",
        "Rasalgethi", "Sadachbia", "Sadaltager", "Schedar",
        "Umbriel", "Zubenelgenubi"
    ]
}

VOICE_STYLES = {
    "educational": {
        "female": ["Achernar", "Erinome", "Sulafat", "Aoede"],
        "male": ["Charon", "Rasalgethi", "Sadaltager", "Iapetus"]
    },
    "casual": {
        "female": ["Callirrhoe", "Vindemiatrix", "Laomedeia", "Zephyr"],
        "male": ["Zubenelgenubi", "Achird", "Umbriel", "Orus"]
    },
    "motivational": {
        "female": ["Gacrux", "Despina", "Pulcherrima", "Laomedeia"],
        "male": ["Puck", "Fenrir", "Sadachbia", "Schedar"]
    },
    "emotional": {
        "female": ["Sulafat", "Despina", "Gacrux", "Aoede", "Achernar"],
        "male": ["Algieba", "Enceladus", "Charon"]
    },
    "storytelling": {
        "female": ["Autonoe", "Pulcherrima", "Erinome", "Kore", "Aoede"],
        "male": ["Enceladus", "Schedar", "Algenib", "Iapetus"]
    },
    "youthful": {
        "female": ["Leda", "Kore", "Zephyr", "Callirrhoe"],
        "male": ["Orus", "Alnilam", "Algenib", "Achird"]
    }
}


def pick_voice(post_type):
    """
    Pick a Google Cloud TTS voice based on style-gender combo, gender only, or specific name.
    
    Args:
        post_type: Can be one of:
            - "style-gender": "educational-female", "motivational-male", etc.
            - "gender": "female", "male"
            - "voice_name": "Charon", "Erinome", etc.
    
    Returns:
        Voice name (e.g., "Charon", "Erinome")
    
    Examples:
        pick_voice("educational-female")  → Random female educational voice
        pick_voice("motivational-male")   → Random male motivational voice
        pick_voice("female")              → Random female voice
        pick_voice("Charon")              → Returns "Charon"
    """
    
    # Case 1: Specific voice name (if it exists in our voice lists)
    all_voices = GOOGLE_TTS_VOICES["female"] + GOOGLE_TTS_VOICES["male"]
    if post_type in all_voices:
        return post_type
    
    # Case 2: Gender only ("female" or "male")
    if post_type.lower() in ["female", "male"]:
        return random.choice(GOOGLE_TTS_VOICES[post_type.lower()])
    
    # Case 3: Style-Gender combination (e.g., "educational-female")
    if "-" in post_type:
        parts = post_type.lower().split("-")
        if len(parts) == 2:
            style, gender = parts
            
            if style in VOICE_STYLES and gender in ["female", "male"]:
                return random.choice(VOICE_STYLES[style][gender])
    
    # Fallback: return random voice
    print(f"Warning: '{post_type}' not recognized. Returning random voice.")
    gender = random.choice(["female", "male"])
    return random.choice(GOOGLE_TTS_VOICES[gender])


if __name__ == "__main__":
    print("="*60)
    print("VOICE PICKER - USAGE EXAMPLES")
    print("="*60)
    
    # Example 1: Style-Gender combo
    print("\n1. Educational Female:")
    for _ in range(3):
        print(f"   {pick_voice('educational-female')}")
    
    # Example 2: Style-Gender combo (male)
    print("\n2. Motivational Male:")
    for _ in range(3):
        print(f"   {pick_voice('motivational-male')}")
    
    # Example 3: Gender only
    print("\n3. Random Female voice:")
    for _ in range(3):
        print(f"   {pick_voice('female')}")
    
    # Example 4: Specific voice name
    print("\n4. Specific voice:")
    print(f"   {pick_voice('Charon')}")
    print(f"   {pick_voice('Erinome')}")
    
    print("\n" + "="*60)
    print("VALID INPUT FORMATS:")
    print("="*60)
    print("""
  Style-Gender Combos:
    - educational-female / educational-male
    - casual-female / casual-male
    - motivational-female / motivational-male
    - emotional-female / emotional-male
    - storytelling-female / storytelling-male
    - youthful-female / youthful-male
  
  Gender Only:
    - female
    - male
  
  Specific Voice Names:
    - Charon, Erinome, Puck, Leda, etc.
    """)
    print("="*60)