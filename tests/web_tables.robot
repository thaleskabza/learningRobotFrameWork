*** Settings ***
Library    ../lib/WebTablesLibrary.py

Suite Setup    Open Web Tables    http://selenium-hub:4444/wd/hub    chrome
Suite Teardown Close Browser

*** Variables ***
${CSV_FILE}    users.csv
@{EXPECTED_HEADERS}
...    First Name    Last Name    User Name    Customer    Role    E-mail    Cell Phone    Locked

*** Test Cases ***
Validate User List Table
    Verify User List Table Displayed
    ${headers}=    Get Header List
    Should Be Equal As Lists    ${headers}    @{EXPECTED_HEADERS}

Add User From CSV And Verify
    ${username}=    Add User From CSV    ${CSV_FILE}    0
    User Should Be Present In List    ${username}