To build an executable:

1) Navigate to CommunicationsBus directory
2) Execute `pyinstaller --onefile --windowed --specpath=".../CommunicationsBus/Assets" --exclude-module tkinter startUp.py`
3) Executable will be generated into /CommunicationsBus/dist directory
4) Distribute /dist folder INCLUDING /dist/AssetsV1 

To run from command line:

`python startUp.py`

