### About

This project is a Python application that collects and stores CNPJ information from a public API. The program allows the user to enter a CNPJ and save the returned data in a CSV file.

### Requirements
- Python 3.x
- Python libraries: requests, csv, tqdm, tkinter
- [API](https://www.cnpj.ws/docs/intro)


### Functionalities
- data (cnpj): Function that makes a request to the public API to obtain information about the provided CNPJ.
- type(natureza_juridica): Function that determines the type of legal nature (Municipal, State, Federal).
- save(cnpj, data, file): Function that saves CNPJ data into a CSV file.
- menu(): Function that displays the menu for the user to enter the CNPJ or exit the program.

### Methods

- Download and open the executable file [here](https://github.com/pizza2u/CNPJ_Consult/blob/main/dist/tkk.exe) - In moment, doesnt work
> You can do this:
> 
> 0º git clone
> 
> 1º pip install pyinstaller;
> 
> 2º pyinstaller -onefile --windowed tkintertest.py
> 
> 3º You must find the .exe in path ´dist´
> 
- Or run script.py

- Check the legal nature codes [here](https://www.gov.br/pncp/pt-br/acesso-a-informacao/manuais/ManualPNCPAPIConsultasVerso1.0.pdf)
