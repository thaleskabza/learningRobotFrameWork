*** Settings ***
Library    SeleniumLibrary
Library    ../lib/DriverManager.py

Suite Setup      Open Managed Browser
Suite Teardown   Close All Browsers

*** Variables ***
${BASE_URL}    https://google.com
${BROWSER}     chrome

*** Keywords ***
Open Managed Browser
    # auto-download the correct driver, then open Chrome
    ${driver_path}=    Get Chrome Driver
    Open Browser      ${BASE_URL}    ${BROWSER}    executable_path=${driver_path}

*** Test Cases ***
Verify Google Title
    [Documentation]    Open google.com and verify its title
    Title Should Be    Google
