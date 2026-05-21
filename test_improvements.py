"""
Test script to demonstrate the improved chatbot
Compares old vs new response system
"""

from chatbot_psikologi import CurhatBot


def test_relationship_scenario():
    """Test the example from the requirements"""
    
    bot = CurhatBot()
    
    print("=" * 70)
    print("TEST SCENARIO: Relationship Issues")
    print("=" * 70)
    
    print(f"\nBot: {bot.get_greeting()}\n")
    
    # User message from requirements
    user_message = (
        "aku capek sama hubunganku. dulu dia perhatian banget tapi sekarang berubah. "
        "chatnya dingin, sering ilang, dan aku jadi takut dia udah nggak sayang lagi."
    )
    
    print(f"User: {user_message}\n")
    
    response = bot.process_message(user_message)
    
    print(f"Bot: {response}\n")
    
    # Get emotional profile
    profile = bot.emotional_memory.get_emotional_profile()
    print("\n" + "=" * 70)
    print("EMOTIONAL ANALYSIS")
    print("=" * 70)
    print(f"Primary Emotions: {profile['primary_emotions']}")
    print(f"Implied Emotions: {profile['implied_emotions']}")
    print(f"Repeated Themes: {profile['repeated_themes']}")
    print(f"Attachment Style: {profile['attachment_style']}")
    print(f"Conversation Stage: {profile['conversation_stage']}/4")
    
    # Continue conversation
    print("\n" + "=" * 70)
    print("CONTINUATION")
    print("=" * 70)
    
    user_message_2 = "iya... sepertinya sudah hampir 2 bulan dia kayak gitu. aku jadi overthinking terus."
    print(f"\nUser: {user_message_2}\n")
    
    response_2 = bot.process_message(user_message_2)
    print(f"Bot: {response_2}\n")


def test_anxiety_scenario():
    """Test anxiety/overthinking scenario"""
    
    bot = CurhatBot()
    bot.reset()
    
    print("\n\n" + "=" * 70)
    print("TEST SCENARIO 2: Anxiety & Overthinking")
    print("=" * 70)
    
    print(f"\nBot: {bot.get_greeting()}\n")
    
    user_message = "aku lagi overthinking banget. teman itu nggak bales chat aku 3 hari. aku takut dia marah sama aku atau udah bosan."
    
    print(f"User: {user_message}\n")
    
    response = bot.process_message(user_message)
    
    print(f"Bot: {response}\n")
    
    profile = bot.emotional_memory.get_emotional_profile()
    print("\n" + "=" * 70)
    print("EMOTIONAL ANALYSIS")
    print("=" * 70)
    print(f"Primary Emotions: {profile['primary_emotions']}")
    print(f"Implied Emotions: {profile['implied_emotions']}")


def test_loneliness_scenario():
    """Test loneliness scenario"""
    
    bot = CurhatBot()
    bot.reset()
    
    print("\n\n" + "=" * 70)
    print("TEST SCENARIO 3: Loneliness & Emotional Exhaustion")
    print("=" * 70)
    
    print(f"\nBot: {bot.get_greeting()}\n")
    
    user_message = "aku capek pura-pura kuat terus. nggak ada yang ngerti apa yang aku rasain. sendirian banget rasanya."
    
    print(f"User: {user_message}\n")
    
    response = bot.process_message(user_message)
    
    print(f"Bot: {response}\n")
    
    profile = bot.emotional_memory.get_emotional_profile()
    print("\n" + "=" * 70)
    print("EMOTIONAL ANALYSIS")
    print("=" * 70)
    print(f"Primary Emotions: {profile['primary_emotions']}")
    print(f"Implied Emotions: {profile['implied_emotions']}")
    print(f"Repeated Themes: {profile['repeated_themes']}")


def test_progression():
    """Test conversation progression through stages"""
    
    bot = CurhatBot()
    
    print("\n\n" + "=" * 70)
    print("TEST: Conversation Stage Progression")
    print("=" * 70)
    
    messages = [
        "aku sedih banget akhir-akhir ini",
        "nggak tahu mengapa, semuanya terasa hampa dan nggak bermakna",
        "sudah hampir sebulan aku kayak gini, capek terus",
        "iya, bahkan tidur dan makan jadi nggak teratur",
        "aku pikir ini dimulai sejak hubunganku putus 2 bulan lalu",
    ]
    
    print(f"\nBot: {bot.get_greeting()}\n")
    
    for i, message in enumerate(messages, 1):
        print(f"User ({i}): {message}")
        
        response = bot.process_message(message)
        
        print(f"Bot: {response}")
        print(f"[Stage: {bot.emotional_memory.conversation_stage}/4]\n")


if __name__ == '__main__':
    print("\n\n")
    print("╔" + "=" * 68 + "╗")
    print("║" + " " * 68 + "║")
    print("║" + "  IMPROVED CURHAT BUDDY CHATBOT - TEST SUITE".center(68) + "║")
    print("║" + " " * 68 + "║")
    print("╚" + "=" * 68 + "╝")
    
    try:
        test_relationship_scenario()
        test_anxiety_scenario()
        test_loneliness_scenario()
        test_progression()
        
        print("\n\n" + "=" * 70)
        print("✓ ALL TESTS COMPLETED SUCCESSFULLY")
        print("=" * 70 + "\n")
        
    except Exception as e:
        print(f"\n✗ ERROR: {e}")
        import traceback
        traceback.print_exc()
