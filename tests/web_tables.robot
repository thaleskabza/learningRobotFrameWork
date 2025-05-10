*** Settings ***
Library           Collections
Library           ../lib/WebTablesLibrary.py

Suite Setup       Open Web Tables    http://selenium-hub:4444/wd/hub    chrome
Suite Teardown    Close Browser

*** Variables ***
${CSV_FILE}       users.csv

@{EXPECTED_HEADERS}
...    First Name
...    Last Name
...    User Name
...    Customer
...    Role
...    E-mail
...    Cell Phone
...    Locked

*** Test Cases ***
Verify Browser Initialization
    [Documentation]    Smoke test to verify browser is initialized
    ${status}=    Is Browser Open
    Should Be True    ${status}    Browser initialization failed

Validate User List Table
    [Documentation]    Verify that the user list table and headers are present (including 'Action')
    Validate User List Table    @{EXPECTED_HEADERS}


