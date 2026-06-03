"""
CurhatBuddy - Chatbot Teman Curhat
New Architecture v2: Advanced Reasoning & Response System
"""

from integrated_chatbot import IntegratedChatbot
import sys


def print_banner():
    """Print welcome banner"""
    print("\n" + "="*60)
    print("CurhatBuddy - Teman Curhat Kamu")
    print("Advanced Reasoning & Response System v2")
    print("="*60 + "\n")


def print_help():
    """Print help message"""
    print("\nKomentar khusus:")
    print("  /help    - Tampilkan bantuan")
    print("  /status  - Lihat profil emosi & progress")
    print("  /reset   - Reset percakapan")
    print("  /exit    - Keluar dari chatbot\n")


def display_status(bot: IntegratedChatbot):
    """Display current emotional profile and progress"""
    profile = bot.get_emotional_profile()
    progress = bot.get_understanding_progress()
    
    print("\n" + "-"*60)
    print("📊 EMOTIONAL PROFILE & PROGRESS")
    print("-"*60)
    
    print(f"\nMessage Count: {bot.get_message_count()}")
    print(f"Understanding Depth: {progress['understanding_depth']}/5")
    print(f"Context Coherence: {progress['context_coherence']:.1%}")
    
    if profile['primary_emotions']:
        print(f"\nPrimary Emotions:")
        for emotion, count in list(profile['primary_emotions'].items())[:3]:
            print(f"  • {emotion}: {count}x")
    
    if progress['main_topic']:
        print(f"\nMain Topic: {progress['main_topic']}")
    
    print(f"\nReady for Interpretation: {progress['is_ready_for_interpretation']}")
    print(f"Already Interpreted: {progress['has_interpreted']}")
    
    print("-"*60 + "\n")


def main():
    """Main chatbot loop"""
    print_banner()
    
    # Initialize bot
    bot = IntegratedChatbot()
    
    # Show greeting
    print(f"Bot: {bot.get_greeting()}\n")
    
    # Conversation loop
    while True:
        try:
            user_input = input("Kamu: ").strip()
            
            # Handle special commands
            if user_input.lower() in ('/exit', 'exit', 'keluar', 'bye', 'quit'):
                print(f"\nBot: {bot.closing}")
                break
            
            elif user_input.lower() == '/help':
                print_help()
                continue
            
            elif user_input.lower() == '/status':
                display_status(bot)
                continue
            
            elif user_input.lower() == '/reset':
                bot.reset_conversation()
                print("Bot: Percakapan direset. Mari mulai dari awal. Cerita apa yang mengganggu pikiran kamu?\n")
                continue
            
            # Empty message
            elif not user_input:
                print("Bot: Kamu bisa langsung ketik apa yang mau kamu sampaikan.\n")
                continue
            
            # Process normal message
            response = bot.process_user_message(user_input)
            print(f"Bot: {response}\n")
        
        except KeyboardInterrupt:
            print(f"\n\nBot: {bot.closing}")
            break
        
        except Exception as e:
            print(f"Error: {str(e)}")
            print("Bot: Maaf, ada error. Bisa coba lagi?\n")


if __name__ == '__main__':
    main()

