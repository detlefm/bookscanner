# bookscanner
OCR tools to convert a typewritten manuscript or a printed book into plain text and create a PDF file with all scanned manuscript or book pages and a Word file with the extracted text.\
Current state: \
Two interfaces: commandline and scriptit

## Usage
Install the nessesary moduls (see requirements.txt).\
Edit the prompt inside of contants.py to your needs. \
Provide an API key from OpenAI within an .env file or via environments variable

Commandline calls
#### scriptit web_app.py 
For testing the openai api. Provide a prompt and optional an image and ask gpt-4o-mini

#### python terminal_app.py normalize foldername  
This normalize the filenames from Microsoft Lens into something like 'Book_Page_XX.jpeg'
#### python terminal_app.py ocr_folder foldername
Starts the OCR process and generates a json file with the ocr result for every image in the 'folder'. 
A second call will only ocr images where no imagefilename.json exists.\
#### python terminal_app.py make_word foldername destinationfilename 
Produces a word file with all OCR results
#### python terminal_app.py make_pdf foldername destinationfilename 
This produce a pdf file with all image files within this folder.\
The image files will be sorted by name and then stored inside the pdf file.

## Reason
My wife had inherited a book manuscript (650 A4 pages) written on a typewriter from her father. As a memory of her father and as a legacy for the whole family, the plan was to scan the book. Then it would be converted into a Word document for future processing using OCR. And the family members would receive the original manuscript as a PDF file.

I was given the task of selecting and testing the appropriate software and hardware on a tight budget.

## Scanner
A commercial scanner was too expensive and would no longer be needed after this project. A flatbed scanner was out of the question. I would have had to divide the book into individual pages. So I decided on Microsoft Lens and a tripod. I chose one that I could attach to a table and was stable ($20)
A few Python scripts and the generated jpg files were given names like Page_001, Page_002, etc.

## OCR
I chose gpt-4o as the OCR software. The costs are manageable (approx. US$1.50 per 100 pages)
Additional benefit: No training in special software such as Tesseract and Keras-OCR, but I was able to learn the ChatGPT API.
As of mid july 24: OpenAI has provided a new model: gpt-4o-mini with much less costs.

## Output
The output should be a Word file on the one hand and a PDF document with the scanned original pages on the other. In Python, this is not rocket science with python-docx and reportlab.

## Time required
Scanning took me around 45 minutes for 150 pages. Then I looked through the scans, replaced the bad ones and fixed one or two things. That would not have been necessary for the OCR process, but for the PDF document the scan should look as good as possible. The OCR process with ChatGPT 4o was around 17 seconds per image.


## Alternative
Instead of going the Microsoft Lens -> Cleanup File Names -> OCR route, it is also possible to simply let Microsoft Lens do the work.\
There is an option to transcribe the image and save the image together with the plain text as a Word document. Microsoft Lens does a good job of this and manages to largely retain the original formatting.


## Miscellaneous
I got help from DeepSeek Coder-V2. Of course you can get everything directly on the Internet, but a chatbot is (at least for me) a significant help.

