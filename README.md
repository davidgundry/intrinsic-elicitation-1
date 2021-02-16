# Intrinsic Elicitation, Experiment 1

Intrinsic Elicitation Experiment: Enjoyment and data quality in a game for human-subject data collection

This is a repository of materials and data for the Enjoyment and Data Collection in an Applied Game study.

## Directory Structure

* `data/` - processed/anonymised data
* `out/` - output of analysis scripts including data and graphs. Logs of script console output is saved here too
* `python/` - python scripts
* `r/` - r scripts
* `design/` - ethics, preregistration documents, etc.
* `final/` - versions of documents that have been officially submitted somewhere
* `materials/` - contains materials that were used in the experiment
* `img/` - screenshots of the game //TODO: video figure to show gameplay as well.
* `design/` - preregistration and ethics documents
* `raw/` - raw data stored here before processing and anonymisation

## Pre-Registration

Pre-registration documents are found in `design/`. Dated uploads to OSF (which should match the records on OSF) are in `final/`. The power analysis script used in the pre-registration can be found in `r/`, which generated `out/power-anaysis.Rout`. You can generate this using the following command:

    R CMD BATCH --quiet r/power-analysis.r out/power-analysis.Rout

## Data Collection

Data collection began at 11:28 on 15 Jun 2020 and ended at 13:32.

110 submissions recorded on Prolific. In addition:
* 1 rejected due to wrong code
* 11 returned their submissions without completing (inc. 1 manually completed)
* 3 timed out (inc. 1 manually completed)

* 108 records downloaded from database
* 2 pid excluded
* 6 excluded to bring down to first 50 in each condition (before analysis) to match with preregistration. As we were only supposed to collect 50 in each condition, and this was before exclusions took place, this happens before exclusions.
* 2 excluded to language: other. 2 to negative ages (<18)
* 96 records processed

Raw data has been deleted in line with the anonymisation procedure specified in the ethics application.

## Data Source

Data downloaded from [Restdb.io](https://restdb.io) using the script [get-restdb-data](https://github.com/davidgundry/get-restdb-data).

### Pre-anonymised Data Format

Data was collected using the non-relational database service [restdb.io](https://restdb.io). All data was downloaded as a json file.

This is an example of the JSON file format with a single data record, showing the type of data collected as it was downloaded from the database. The data here does not refer to a real participant.

    [
        {"_id":"5f118222b0e1d1670001ce11","data":{"gameVersion":"Normal","loadTime":1594982440874,"uploadTime":1594982944816,"duration":485.424,"answers":["27","female","english","every-day","1","2","3","4","5","4","3"],"moves":[["blue","circle","small"],["red","circle","empty"],["blue","circle","empty"],["blue","circle","filled"],["red","circle","empty"],["red","circle","filled"],["blue","circle","empty"],["red","triangle","filled"],["blue","circle","triangle"],["blue","filled","circle"],["blue","circle","empty"],["red","triangle","filled"],["circle","empty","red"],["red","circle","filled"],["red","triangle","empty"],["blue","triangle","empty"],["blue","triangle","filled"],["blue","circle","filled"],["red","circle","filled"],["red","circle","empty"]]},"version":"1.0.0.IEX-enj-dataq-1.0.0.Normal","studyID":"daa2e38ef9864764b95f4e545","prolificPID":"6440a9870c404843a195ba4a","sessionID":"501617b49a904139b1608183","uid":123}
    ]

* **_id**: Database record ID
* **data**: Participant data recorded from game (a JSON object)
    * **gameVersion**: `Normal` or `Tool`
    * **loadTime**: a timestamp at the point the game loads (uses JavaScript `Date.now()`)
    * **uploadTime**: a timestamp at the point the game begins uploading data to the server, which is immediately upon the final questionnaire being submitted (uses JavaScript `Date.now()`)
    * **duration**: seconds between submission of pre-test questionnaire and play start, and play-end interrupt before post-test questionnaire
* **version**: Game version and condition data was collected from
* **studyID, prolificPID, sessionID**: Values from the Prolific service for particiant payment purposes.
* **uid**: Auto-incrementing datanbase record UID.

For other variables, see the 'Data Format' section below.

### Anonymising Data

To prepare (i.e. anonymise) the raw data run the following command from the project directory. 

    python python/prepare-data.py

Edit that file to set the source data filename to match the one as downloaded.

The script will write files to disk in the folder "data". It will also write many files to disk in the same directory as the source (raw) data file. Many of these are for sanity checking purposes and should be deleted as they are not fully anonymised. The important files are:

* `data.json` (containing the main data)
* `duration.csv` (associating duration and condition)
* `age-gender.csv` (associating age and gender)

**Note:** The script shuffles the lines of the data file and it doesn't do any JSON parsing, so it is almost certain that the end-of-line commas will be incorrect. This will lead cause errors in later analysis scripts. To fix this, ensure there is a comma at the end of each line of data, except for the last one.

## Data Format

### Data.json

After processing, the data looks like this:

    [
        {"data":{"gameVersion":"Tool","answers":["english","every-day","2","1","5","3","2","2","1"],"moves":[["square","green","empty"],["triangle","blue","small"],["triangle","red","small"],["square","blue","big"],["triangle","green","small"],["triangle","green","small"],["triangle","green","small"],["square","red","small"],["square","blue","small"],["square","red","big"],["circle","blue","small"],["circle","big","empty"],["triangle","small","empty"],["square","small","blue"],["circle","big","empty"],["square","empty","red"],["square","blue","big"],["triangle","red","small"],["triangle","blue","small"],["circle","blue","small"]]},"version":"1.0.0.IEX-enj-dataq-1.0.0.Tool"}
    ]

* **gameVersion**: Either "Tool" (for the non-game version) or "Normal" (for the game version).
* **answers**: Answers to the questions (in order):
    1. What is your first language (`english`/`other`)
    2. How often do you play digital games? (`every-day`/`several-times-a-week`/`about-once-a-week`/`about-once-a-month`/`almost-never`)
    * Seven (7) Likert scale (`1-5`) answers to the Intrinsic Motivation Inventory: Enjoyment Subscale, in default question order
* **moves**: Array of moves attempted by the player (sets of three words inputted, whether or not they trigger an action in the game). These are in order they were selected. Moves are in order attempted.
* **version**: Game version and condition data was collected from

### Age and Gender

The file `data/age-gender.csv` has records in the format: `age (number entry), gender (female/male/other/prefer-not-to-say)`

    36,female
    19,female
    58,male

### Duration

The file `data/duration.csv` has records in the format: `condition (Normal/Tool), duration in seconds`

    Normal,229.97
    Tool,208.909
    Normal,439.921

## Analysis

In the project directory (for this experiment) run the following commands (on Linux). These create (or overwrite) files in `out/`).

    python python/create_data_csv.py
    
    python python/hypothesis_test.py > out/hypothesis_test.txt

    python python/duration_analysis.py > out/duration_analysis.txt

    python python/age_gender_analysis.py  > out/age_gender_analysis.txt

    python python/exploratory_analysis.py  > out/exploratory_analysis.txt
