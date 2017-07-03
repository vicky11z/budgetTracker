# budgetTracker
Send texts to keep you on top of your budget.

Integrates Mint, Google Sheets, and Twilio to create a very simple budgeting tool that performs the one task you need: a way to alert you of how much you've spent today and how much you can spend for the rest of the month.

Set this tool up to specify how often it runs, and `init()` will construct a text message based off what your expected spending habits should be and what they actually are, and sends your number a text message with just the facts.

Check out the awesome open-source Mintapi here: https://github.com/mrooney/mintapi
And the just as awesome open-source gspread here: https://github.com/burnash/gspread
To install necessary dependencies: `pip install -r requirements.txt`

This is a work in progress. More functionality (hopefully) to come.

**Tips**

To find cookies on chrome, go to chrome://settings/cookies

For `ius_session`, find under accounts.intuit.com; for `thx_guid`, find under pf.intuit.com.
