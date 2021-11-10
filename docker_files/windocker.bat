ECHO OFF
CLS
:MENU
ECHO.
ECHO ...............................................
ECHO Docker compose menu (Windows)
ECHO ...............................................
ECHO.
ECHO 1 - Build
ECHO 2 - Up
ECHO 3 - Exec bash
ECHO 4 - Down
ECHO 5 - EXIT
ECHO.
SET /P M=Type 1, 2, 3, 4 or 5 then press ENTER:
IF %M%==1 GOTO BUILD
IF %M%==2 GOTO UP
IF %M%==3 GOTO BASH
IF %M%==4 GOTO DOWN
IF %M%==5 GOTO EOF
:BUILD
docker compose build
GOTO EOF
:UP
docker compose up
GOTO EOF
:BASH
docker compose exec web-teleop-host bash
GOTO EOF
:DOWN
docker compose down
GOTO EOF
:EOF
