import os
from typing import Callable


# https://stackoverflow.com/a/234329
def walklevel(root_dir: str, level=1) -> tuple[str, list[str], list[str]]:
    """Walk through directories until a certain depth.
    Similiar to os.walk()

    Args:
        root_dir (str): Path to target directory
        level (int, optional): Depth. Defaults to 1.

    Yields:
        Iterator[tuple[str, list[str], list[str]]]: Root, directories, files
    """
    root_dir = root_dir.rstrip(os.path.sep)
    assert os.path.isdir(root_dir)
    num_sep = root_dir.count(os.path.sep)
    for root, dirs, files in os.walk(root_dir):
        yield root, dirs, files
        num_sep_this = root.count(os.path.sep)
        if num_sep + level <= num_sep_this:
            del dirs[:]


def letter_to_number(letter: str, start=0) -> int:
    return ord(letter.lower()) - (97 - start)


def number_to_letter(number: int, start=0) -> str:
    return chr(number + 97 - start)


def print_list(items: list[str], heading: str, n=9999, use_letters=False) -> None:
    print(heading + '\n')

    def print_item(i: int, item: str):
        print('{}. {}'.format(i, item))

    if use_letters:
        def print_item(i: int, item: str):
            print('{}. {}'.format(number_to_letter(i, 1), item))

    for i, item in enumerate(items, 1):
        if i > n:
            print('\n')
            return
        print_item(i, item)


def print_latest_downloads(downloads: list[str], depth=1, n=9) -> None:
    print_list(map(lambda filepath: os.sep.join(filepath.split(os.sep)
               [-depth:]), downloads), 'Latest:', 9)


def prompt_selection(items: list[str], heading: str, use_letters=False) -> int:
    print_list(items, heading, len(items), use_letters)

    while True:
        user_input = input('\n > ')
        try:
            selected_index = 0
            if use_letters:
                selected_index = letter_to_number(user_input[0])
            else:
                selected_index = int(user_input) - 1

            if selected_index + 1 > len(items) or selected_index + 1 <= 0:
                print('\nOut of range')
                continue
            return selected_index

        except Exception as e:
            print('')
            print(e)
            print('')


def expand_variables(content: str,
                     variables: dict[str, str | Callable[[], str]]) -> str:
    output = content

    def get_key_len(key_value_pair: tuple[str, any]) -> int:
        return len(key_value_pair[0])

    # Sorts the variables so the ones with longer key names
    # are checked first than the shorter ones.
    #
    # Useful when there are variables such as $e and $edc simultaneously
    key_value_pairs = list(variables.items())
    key_value_pairs.sort(key=get_key_len, reverse=True)

    for key, value in key_value_pairs:
        if callable(value):
            output = output.replace('$' + key, value())
            continue
        output = output.replace('$' + key, value)
    return output
