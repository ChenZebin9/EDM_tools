@ECHO OFF
TITLE Python Version PDM Installation (2020.04.25)
SET DIST_PATH = D:\setup_rom\App_4_TengYing

ECHO Create Dist Program
C:\Users\chen_\AppData\Local\Programs\Python\Python37\Scripts\pyinstaller --distpath D:\setup_rom\python_temp App_4_TengYing.spec
ECHO **** Finish Create.

SET TEMP_PATH = D:\setup_rom\python_temp\TengYingNcMix
SET EXE_PATH = D:\setup_rom\App_4_TengYing\TengYingNcMix

COPY D:\setup_rom\python_temp\TengYingNcMix\TengYingNcMix.exe D:\setup_rom\App_4_TengYing\TengYingNcMix
ECHO Delete Cache
RD /s %CD%\build
ECHO **** Finish Delete.

ECHO Copy other components
COPY config.ini D:\setup_rom\App_4_TengYing\TengYingNcMix
COPY MainApp.ico D:\setup_rom\App_4_TengYing\TengYingNcMix
ECHO **** Finish Copy.

ECHO All Finished.
