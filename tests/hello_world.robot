*** Settings ***
Library    BuiltIn

*** Test Cases ***
Hello World Should Pass
    Log    Hello, Robot Framework on macOS!
    Should Be True    ${True}    msg=Basic sanity check
