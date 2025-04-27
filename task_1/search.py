from task_1.models import Author, Quote

def search_by_author(name):
    author = Author.objects(fullname=name).first()
    if not author:
        return []
    quotes = Quote.objects(author=author)
    return [quote.quote for quote in quotes]

def search_by_tag(tag):
    quotes = Quote.objects(tags=tag)
    return [quote.quote for quote in quotes]

def search_by_tags(tags):
    tags_list = tags.split(',')
    quotes = Quote.objects(tags__in=tags_list)
    return [quote.quote for quote in quotes]

def print_results(results):
    if results:
        print(f"\nЗнайдено {len(results)} цитат(и):\n")
        for idx, quote in enumerate(results, 1):
            print(f"{idx}. {quote}\n")
    else:
        print("\nНічого не знайдено.\n")

def main():
    print("Ласкаво просимо до пошуку цитат!")
    print("Команди:")
    print("name:<ім'я автора>")
    print("tag:<тег>")
    print("tags:<тег1,тег2,...>")
    print("exit - вихід із програми\n")

    while True:
        user_input = input("Введіть запит: ").strip()

        if user_input.lower() == 'exit':
            print("\nВихід з програми.")
            break

        if ':' not in user_input:
            print("\nНевірний формат. Використовуйте формат команда:значення\n")
            continue

        command, value = user_input.split(':', 1)
        command = command.strip().lower()
        value = value.strip()

        if command == 'name':
            results = search_by_author(value)
            print_results(results)
        elif command == 'tag':
            results = search_by_tag(value)
            print_results(results)
        elif command == 'tags':
            results = search_by_tags(value)
            print_results(results)
        else:
            print("\nНевідома команда. Спробуйте ще раз.\n")

if __name__ == '__main__':
    main()
