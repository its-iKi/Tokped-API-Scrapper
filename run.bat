@echo off
echo Installing the required modules..
pip install requests --user
pip install pandas --user
pip install openpyxl  --user
echo Required modules have been installed.
echo.
echo Input target identifier/domain (ex. aquaings)
set /p arg1=
echo.
echo How many page you want to scrap (integer default = 1)
set /p arg2=
echo.
echo Start running the program...
python "tokped_api_scrapper.py" %arg1% %arg2%
pause
echo Data saved..