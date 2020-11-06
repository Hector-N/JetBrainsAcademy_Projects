import requests
import pickle
import sys

from bs4 import BeautifulSoup

# ---------------- structure info ------------------
# top_results = response.find(id='translations-content')
# id='top-results'
# id='translations-content'
# class='translation ltr dict n'
# a_class1 = "translation ltr dict adv"
# a_class2 = "translation ltr dict first n"
# a_class3 = "translation ltr dict no-pos"

my_headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) '
                            'AppleWebKit/537.36 (KHTML, like Gecko) '
                            'Chrome/84.0.4147.135 '
                            'YaBrowser/20.8.3.132 (beta) '
                            'Yowser/2.5 Safari/537.36'}

# lang_str = "\n".join('Arabic German English Spanish French Hebrew Japanese ' \
#            'Dutch Polish Portuguese Romanian Russian Turkish'.split())
# languages = dict(enumerate(lang_str.split('\n'), start=1))

# using pickling for the first time)
# with open('languages.pickle', 'wb') as fh:
#     pickle.dump(languages, fh)
with open('languages.pickle', 'rb') as fh:
    languages = pickle.load(fh)


def main():

    argv = sys.argv

    if len(argv) == 4:  # use command line arguments
        source, target = (a.capitalize() for a in argv[1:3])
        req_word = argv[3].lower()

        trg_lang = None
        for k in languages:
            if languages[k] == source:
                src_lang = k
            if languages[k] == target:
                trg_lang = k

        if not trg_lang:  # target is all languages
            if target == 'All':
                trg_lang = 0

    else:  # use user input
        print("Hello, you're welcome to the translator. Translator supports:")
        for n, lng in languages.items():
            print(f"{n}. {lng}")

        # user input
        src_lang = int(input('Type the number of your language:'))
        trg_lang = int(input("Type the number of a language you want to translate to "
                             "or '0' to translate to all languages:"))
        req_word = input('Type the word you want to translate:').strip().lower()

    # trying to catch unsupported language, variables src_lang and trg_lang must != None
    try:
        if trg_lang != 0:
            translate(src_lang, trg_lang, req_word)

        else:
            target_langs = languages.copy()
            del target_langs[src_lang]
            result = []
            for lang in target_langs:
                res = translate(src_lang, lang, req_word, save=True)
                if res is None:
                    break
                result.append(res)

            if result:
                with open(req_word + '.txt', 'w') as fh:
                    fh.writelines(result)
    except KeyError:
        if src_lang not in languages.keys():
            print(f"Sorry, the program doesn't support {source.lower()}")
        elif trg_lang not in languages.keys():
            print(f"Sorry, the program doesn't support {target.lower()}")



def translate(src_lng_num:int, trg_lng_num:int, word:str, save:bool=False):
    try:
        direction = f"{languages[src_lng_num].lower()}-{languages[trg_lng_num].lower()}/"
        reverso = 'https://context.reverso.net/translation/'
        search_url = reverso + direction + word
        response = requests.get(search_url, headers=my_headers)
        soup = BeautifulSoup(response.content, 'html.parser')

        translations_info_1 = f"{languages[trg_lng_num]} Translations:"
        print(translations_info_1)

        # Arabic Translations:
        #AttributeError: 'NoneType' object has no attribute 'find_all'
        top_results = soup.find(id='translations-content')

        top_words = top_results.find_all('a')
        words = [w.text.strip() for w in top_words]
        first_word = words[0]
        print(f"{first_word}\n")

        # EXAMPLES
        translations_info_2 = f"{languages[trg_lng_num]} Examples:"
        print(translations_info_2)

        main_results = soup.find(id='examples-content')
        examples = main_results.find_all('div', class_='example')
        context = []
        for e in examples:
            src_res, trg_res = (el.text.strip() for el in e.find_all('span', class_='text'))
            context.append((src_res, trg_res))
        first_sentence_origin, first_sentence_foreign = context[0]

        context_example = f"{first_sentence_origin}:\n{first_sentence_foreign}\n"
        print(context_example)

        if save is True:
            return '\n'.join((translations_info_1,
                              first_word + '\n',
                              translations_info_2,
                              context_example + '\n'))
    except AttributeError:
        print(f'Sorry, unable to find {languages[trg_lng_num].lower()}')

# main()

while True:
    main()
