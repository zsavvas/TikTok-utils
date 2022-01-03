# TikTok-utils

This repository includes scripts to work with TikTok data that is generated when users requests their personal data from the TikTok platform.


### Anonymizing TikTok data
```
python user_data_depersonalizer.py
```

This script is used to anonymize the TikTok file by removing personal identifiers and providing a set of options where users can select which parts of the data will be included in the anonymized file (e.g., remove the comments). The script takes as input the following options:

| Option           | Default Value             | Description                                                                                                                                                   |
|------------------|---------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------|
| --file           | user_data.json            | The file that you downloaded from TikTok                                                                                                                      |
| --output         | user_data_anonymized.json | The output file where the anonymized file with be written                                                                                                     |
| --like-history   | True                      | Whether the output should include the like history (change to False if you want to exclude)                                                                   |
| --share-history  | True                      | Whether the output should include the share history (change to False if you want to exclude)                                                                  |
| --search-history | True                      | Whether the output should include the search history (change to False if you want to exclude)                                                                 |
| --favorites      | True                      | Whether the output should include the favorite videos, hashtags, sounds etc. (change to False if you want to exclude)                                         |
| --followers      | True                      | Whether the output should include the list of followers (change to False if you want to exclude)                                                              |
| --following      | True                      | Whether the output should include the list of followings (change to False if you want to exclude)                                                             |
| --comments       | True                      | Whether the output should include information about the comments you made on TikTok (change to False to completely remove comments)                           |
| --comments-text  | True                      | Whether the comments' text should be included or no (if True we store the timestamp and the comment text, if False the text is substituted with "[redacted]") |
| --ads            | True                      | Whether the output should include information about advertisers that targeted you on TikTok (change to False to remove ad information)                        |
| --settings       | True                      | Whether the output should include information about the settings you use in the TikTok app (change to False if you want to exclude)                           |
| --session-times  | True                      | Whether the output should include the session times (i.e., when you started using the TikTok app)                                                             |
#### Information that is exluded by default
| Type of data        | Description                                                                                                                                       |
|---------------------|---------------------------------------------------------------------------------------------------------------------------------------------------|
| Profile Information | The output does not include profile information, which include sensitive and personal identifiers like username, telephone number, email address. |
| Account status      | The output does not include the status of the application on the user's phone (e.g., app version, screen resolution, etc.)                        |
| Messages            | The output does not include any information related to private messages sent between the user and other TikTok users.                             |
| Uploads             | The output does not include any information about the videos that the participant uploaded on TikTok.                                             |
| Purchase History    | The output does not include any information about purchases made within the TikTok app.                                                           |


#### Example (keep only video viewing history)
```
python user_data_depersonaliser.py --like-history=False --share-history=False --search-history=False --favorites=False --followers=False --following=False --comments=False --ads=False --settings=False --session-times=False 
```



