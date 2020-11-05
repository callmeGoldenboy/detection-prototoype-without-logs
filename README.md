## Prototype for the dection of web scraping 
A prototype for detection of web scraping that uses some attributes found in the header of a request. 
Done in collaboration with [@amarhod](https://github.com/amarhod) for bachelor's thesis project

## The aim of the thesis 
The aim of the thesis was to explorer the landscape of webscraping and see whether it was possible
to detect web scraping. For that we also developed a small prototype that used the information stored in a HTTP request to derive a conclusion on the entity that sent the request. 

## The different modules 
- **Analyzer** - Takes in a list of unique IPs (from the batch of logs) and gives a score between 1-4 for each IP. This is the main method.
- **Log reader** - Used to read the logs from a text file
- **Detection** - Used for testing the prototype. It calls the log reader to process the batch. Then it calls the analyzer with the list of unique IPs. Finally, it prints the results for each IP.
- **Database handler** - Handles all the communication with the SQLite local DB.
- **Client info** - Returns useful info for a given IP if there are any prior requests done by it. It returns info such as request rate, number of different user agents etc.

For privacy reasons, the logs that were used for testing the prototype will not be available in this repository. 
