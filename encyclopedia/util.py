import re

from django.core.files.base import ContentFile
from django.core.files.storage import default_storage


def list_entries():
    """
    Returns a list of all names of encyclopedia entries.
    """
    _, filenames = default_storage.listdir("entries")
    return list(sorted(re.sub(r"\.md$", "", filename)
                for filename in filenames if filename.endswith(".md")))


def save_entry(title, content):
    """
    Saves an encyclopedia entry, given its title and Markdown
    content. If an existing entry with the same title already exists,
    it is replaced.
    """
    filename = f"entries/{title}.md"
    if default_storage.exists(filename):
        default_storage.delete(filename)
    default_storage.save(filename, ContentFile(content))


def get_entry(title):
    """
    Retrieves an encyclopedia entry by its title. If no such
    entry exists, the function returns None.
    """
    try:
        f = default_storage.open(f"entries/{title}.md")
        return f.read().decode("utf-8")
    except FileNotFoundError:
        return None


def checkSave(title, content):
    """
    check for create entry and save if it doesn't extis and return true.
    """
    exist = get_entry(title)
    if exist == None:
        # myfile = open(f"entries/{title.capitalize()}.md", "w")
        # myfile.write(f'{content}')
        # myfile.close
        save_entry(title.capitalize(),content)
        isSaved = True
    else:
        isSaved = False
    return isSaved


def checkEdit(title, content):
    """
    check for edit entry and save if it exist and return true.
    """
    exist = get_entry(title)
    if exist == None:
        isEdited = False
    else:
        save_entry(title,content)
        isEdited = True
    return isEdited

