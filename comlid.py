import requests
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich import print as rprint
from deep_translator import GoogleTranslator

console = Console()

# ── Dictionary ─────────────────────────────────────────────
def get_definition(word):
    try:
        url = "https://api.dictionaryapi.dev/api/v2/entries/en/" + word
        response = requests.get(url)

        if response.status_code != 200:
            console.print("[red]Word not found![/red]")
            return

        data = response.json()
        word_data = data[0]

        console.print(Panel(
            "[bold cyan]" + word_data["word"].upper() + "[/bold cyan]",
            title="COMLID Dictionary",
            border_style="cyan"
        ))

        # Phonetic
        if "phonetic" in word_data:
            console.print("[yellow]Phonetic:[/yellow] " + word_data["phonetic"])

        # Meanings
        for meaning in word_data["meanings"]:
            console.print("\n[bold green]" + meaning["partOfSpeech"].upper() + "[/bold green]")

            for i, definition in enumerate(meaning["definitions"][:3]):
                console.print("  " + str(i+1) + ". " + definition["definition"])
                if "example" in definition:
                    console.print("     [italic]Example: " + definition["example"] + "[/italic]")

            # Synonyms
            if meaning["synonyms"]:
                console.print("  [magenta]Synonyms:[/magenta] " + ", ".join(meaning["synonyms"][:5]))

            # Antonyms
            if meaning["antonyms"]:
                console.print("  [red]Antonyms:[/red] " + ", ".join(meaning["antonyms"][:5]))

    except Exception as e:
        console.print("[red]Error: " + str(e) + "[/red]")

# ── Translator ─────────────────────────────────────────────
def translate_word(word):
    try:
        console.print("\n[bold cyan]Available Languages:[/bold cyan]")
        console.print("  hi = Hindi        fr = French")
        console.print("  es = Spanish      de = German")
        console.print("  ja = Japanese     ar = Arabic")
        console.print("  zh-CN = Chinese   ru = Russian")
        console.print("  pt = Portuguese   ko = Korean")

        lang = input("\nEnter language code: ").strip()

        result = GoogleTranslator(source="auto", target=lang).translate(word)

        console.print(Panel(
            "[bold white]" + word + "[/bold white]" +
            " → [bold green]" + result + "[/bold green]" +
            "\n[yellow]Language:[/yellow] " + lang,
            title="Translation",
            border_style="green"
        ))

    except Exception as e:
        console.print("[red]Translation failed: " + str(e) + "[/red]")
# ── Main Menu ──────────────────────────────────────────────
def main():
    console.print(Panel(
        "[bold cyan]COMLID[/bold cyan]\n[white]Console Dictionary & Translator[/white]",
        border_style="cyan"
    ))

    while True:
        console.print("\n[bold]MENU:[/bold]")
        console.print("  [cyan]1.[/cyan] Search word definition")
        console.print("  [cyan]2.[/cyan] Translate a word")
        console.print("  [cyan]3.[/cyan] Search and translate")
        console.print("  [cyan]4.[/cyan] Exit")

        choice = input("\nChoose (1-4): ").strip()

        if choice == "1":
            word = input("Enter word: ").strip().lower()
            if word:
                get_definition(word)
            else:
                console.print("[red]Please enter a word![/red]")

        elif choice == "2":
            word = input("Enter word to translate: ").strip()
            if word:
                translate_word(word)
            else:
                console.print("[red]Please enter a word![/red]")

        elif choice == "3":
            word = input("Enter word: ").strip().lower()
            if word:
                get_definition(word)
                translate_word(word)
            else:
                console.print("[red]Please enter a word![/red]")

        elif choice == "4":
            console.print("[cyan]Goodbye![/cyan]")
            break

        else:
            console.print("[red]Invalid choice! Enter 1-4[/red]")

if __name__ == "__main__":
    main()