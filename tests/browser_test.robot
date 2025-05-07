*** Settings ***
Library    SeleniumLibrary

Suite Setup      Open Remote Browser
Suite Teardown   Close All Browsers

*** Variables ***
${GRID_URL}      http://localhost:4444/wd/hub
${BASE_URL}      https://google.com
${BROWSER}       chrome

*** Keywords ***
Open Remote Browser
    Open Browser    ${BASE_URL}    ${BROWSER}    remote_url=${GRID_URL}

*** Test Cases ***
Verify Google Title
    [Documentation]    Open google.com on Grid and verify its title
    Title Should Be    Google
