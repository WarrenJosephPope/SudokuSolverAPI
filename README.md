# Sudoku Solver API
## 1. API endpoint
[API Endpoint](https://warren-sudoku.herokuapp.com/)
## 2. Method Types
### i. GET
Displays "Hello World".
### ii. POST
Contains actual logic for the program. Send data using POST method
## 3. Input
### i. 9x9 array of array of characters
A 9x9 array of array of characters where a blank space is represented by '-'.  
Example:  
[['-', '-', '4', '-', '5', '-', '-', '-', '-'],
['9', '-', '-', '7', '3', '4', '6', '-', '-'],
['-', '-', '3', '-', '2', '1', '-', '4', '9'],
['-', '3', '5', '-', '9', '-', '4', '8', '-'],
['-', '9', '-', '-', '-', '-', '-', '3', '-'],
['-', '7', '6', '-', '1', '-', '9', '2', '-'],
['3', '1', '-', '9', '7', '-', '2', '-', '-'],
['-', '-', '9', '1', '8', '2', '-', '-', '-'],
['-', '-', '-', '-', '6', '-', '1', '-', '-']]

### ii. An image
An image of a puzzle can be provided to be scanned and the digits will be extracted and identified using Tesseract's OCR.  
**WARNING:** This method is not 100% accurate and may return incorrect results. Please double check after receiving the result.
## 4. Output
### i. 9x9 array of array of characters/ INVALID BOARD

The input board will be scanned and checked to see if the inputs are valid. If so, the board will be solved and a JSON output will be sent back of the form  
{  
    "result": [['2', '6', '4', '8', '5', '9', '3', '1', '7'],  
              ['9', '8', '1', '7', '3', '4', '6', '5', '2'],  
              ['7', '5', '3', '6', '2', '1', '8', '4', '9'],  
              ['1', '3', '5', '2', '9', '7', '4', '8', '6'],  
              ['8', '9', '2', '5', '4', '6', '7', '3', '1'],  
              ['4', '7', '6', '3', '1', '8', '9', '2', '5'],  
              ['3', '1', '8', '9', '7', '5', '2', '6', '4'],  
              ['6', '4', '9', '1', '8', '2', '5', '7', '3'],  
              ['5', '2', '7', '4', '6', '3', '1', '9', '8']]  
}  
else,  
{  
    "result": "INVALID"  
}  
If an image is passed, the image will be scanned and the digits will be extracted. The output will be of the form  
{  
    "result": [['-', '-', '4', '-', '5', '-', '-', '-', '-'],  
              ['9', '-', '-', '7', '3', '4', '6', '-', '-'],  
              ['-', '-', '3', '-', '2', '1', '-', '4', '9'],  
              ['-', '3', '5', '-', '9', '-', '4', '8', '-'],  
              ['-', '9', '-', '-', '-', '-', '-', '3', '-'],  
              ['-', '7', '6', '-', '1', '-', '9', '2', '-'],  
              ['3', '1', '-', '9', '7', '-', '2', '-', '-'],  
              ['-', '-', '9', '1', '8', '2', '-', '-', '-'],  
              ['-', '-', '-', '-', '6', '-', '1', '-', '-']]  
}  
or if could not detect a board in the image,  
{  
    "result": []  
}