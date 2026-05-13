from chatbot_psikologi import CurhatBot, ThemeManager


def choose_theme() -> str:
    themes = list(ThemeManager.themes.keys())
    print('Pilih tema bot:')
    for idx, name in enumerate(themes, start=1):
        print(f'{idx}. {ThemeManager.themes[name]["name"]} ({name})')
    choice = input('Masukkan nomor tema (default 1): ').strip()
    if choice.isdigit():
        index = int(choice) - 1
        if 0 <= index < len(themes):
            return themes[index]
    return themes[0]


if __name__ == '__main__':
    print('=== Chatbot Psikologi: Teman Curhat ===')
    theme_name = choose_theme()
    bot = CurhatBot(theme_name=theme_name)
    print('\nBot: ' + bot.get_greeting())

    while True:
        user_input = input('Kamu: ').strip()
        if user_input.lower() in ('exit', 'keluar', 'bye', 'quit'):
            print('Bot: Makasih ya udah cerita. Semoga harimu lebih enteng.')
            break
        response = bot.process_message(user_input)
        print('Bot: ' + response)
