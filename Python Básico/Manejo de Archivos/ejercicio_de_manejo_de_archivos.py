def main():
    try:
        print("---File before sorting---\n")
        show_file_content("songs.txt")

        songs = create_songs_list()
        sorted_songs = sort_list(songs)
        create_new_file(sorted_songs)

        print("---File after sorting---\n")
        show_file_content("sorted songs.txt")

    except FileNotFoundError:
        print("Error: The file was not found.")

    except PermissionError:
        print("Error: You do not have permission to read or write the file.")

    except UnicodeDecodeError:
        print("Error: The file could not be read using UTF-8 encoding.")

    except OSError as error:
        print(f"File system error: {error}")



def show_file_content(file_name):
    with open(file_name, 'r', encoding='utf-8') as file:
        print(file.read())
        print("")


def create_songs_list():
    with open("songs.txt", "r", encoding="utf-8") as file:
        songs_list = file.readlines()

    if songs_list and not songs_list[-1].endswith("\n"):
        songs_list[-1] += "\n"

    return songs_list


def sort_list(songs_list):
    songs_list.sort(key=str.lower)

    return songs_list


def create_new_file(songs_list):
    with open("sorted songs.txt", "w", encoding="utf-8") as file:
        file.writelines(songs_list)


main()