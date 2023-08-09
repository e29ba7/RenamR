<p align="center">
  <img src="https://raw.githubusercontent.com/f09f9095/RenamR/main/renamr/ui/resources/icons/VHS.png" alt="RenamR VHS" width="245"/>
</p>

<h1 align="center">
  RenamR
</h1>

<p align="center">
  RenamR provides a convenient solution for easily renaming your media collection, including movies and TV shows. With a user-friendly interface and customizable naming options, you can quickly organize and manage your media library in just a few clicks. Say goodbye to confusing and generic file names and hello to a more organized and user-friendly media collection with RenamR.
</p>

## Features

<ul>
  <li>Media Lookup: Quickly search for info such as the title, year, and id of a movie or TV show from your choice of sources</li>
  <li>Custom filenames: Create your own template for files to be renamed to</li>
  <li>Batch renaming: Rename an entire TV series or multiple movies at once</li>
  <li>Practical user interface for effortless usage</li>
</ul>

## To-Do

- [ ] Drag and drop files into application
- [ ] Multithreading
- [ ] Table context menu
- [ ] Support other media databases
- [ ] Renaming history and undoing
- [ ] Remux video files to your favorite container
- [ ] Search, download, and attach subtitles to media

## Usage

1. Add files by using Open Files button or dragging files to the window.
2. Click the Search button and select which provider you'd like to search for information.
3. Make any necessary adjustments to new media titles.
4. Click Rename!

## Screens

<details>
  <summary>Main</summary>

  ![Main](https://raw.githubusercontent.com/f09f9095/RenamR/main/renamr/ui/resources/usage.png)
  
</details>

<details>
  <summary>Template</summary>
  
  ![Template](https://raw.githubusercontent.com/f09f9095/RenamR/main/renamr/ui/resources/template.png)

</details>

## Running from source

1. Ensure at least [Python](https://www.python.org/downloads/) 3.8 is installed (also make sure Python is added to PATH).
2. Open your preferred terminal or command prompt in a folder where you want to download RenamR.
3. Run `git clone https://github.com/f09f9095/RenamR`.
4. Navigate to the downloaded folder, RenamR
5. Run `pip install -r requirements.txt` to install necessary dependencies
6. Finally run `python main.py`.

## Building from source for Windows

1. Follow steps 1 - 5 above
2. Install [Nuitka](https://nuitka.net/doc/download.html) with `pip install Nuitka`
3. In the cloned RenamR folder, run `python -m nuitka --follow-imports --disable-console --standalone --onefile --include-data-files="renamr/ui/resources/icons/*.*"="renamr/ui/resources/icons/" --include-data-files="renamr/ui/resources/themes/*.qss"="renamr/ui/resources/themes/" --plugin-enable=pyqt6 --windows-icon-from-ico="renamr/ui/resources/icons/VHS.ico" main.py`
4. Follow instructions in terminal to install necessary dependencies
5. Results in main.exe

## Contributions

Contributions are always welcome! If you have any ideas, suggestions, or bug reports, please open an issue or submit a pull request.

## License

RenamR is licensed under the [AGPL License](https://github.com/f09f9095/RenamR/blob/master/LICENSE)
