# Immersion Club csv to Anki conversion script guide

## Download script from Github
1. Click the green "Code" button in the upper right corner
2. Select "Download ZIP"
3. Extract the zip file
## File setup from Drive
1. In Google Drive, open the Google Sheets file you want to use, click File -> Download -> Comma-separated values(csv, current sheet)
2. Add any csv file that you want to use to the directory "/anki-csv-main", you can use multiple csv files at once
3. Place any associated audio files in the directory "/anki-csv-main/audio_files", these must be placed directly in the directory itself and cannot be nested in folders

## Run Script
1. Open up the command line or terminal - if you do not know how, consult [this article](https://www.ionos.com/help/email/troubleshooting-mail-basicmail-business/access-the-command-prompt-or-terminal/#:~:text=With%20the%20command%20prompt%20in,command%20line%20for%20your%20computer.)
2. Type: "cd " followed by the path of anki-csv-main. For example: "cd /Users/keenan/Downloads/anki-csv-main"
3. enter the command "python anki-csv.py" to run the script, decks should appear in a folder called vocab-decks in /anki-csv-main