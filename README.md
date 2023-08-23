# Burnaby Golf Course Tee Time Booking Script

This Python script uses Selenium to book a tee time at any of the two Burnaby golf courses. It is aimed to book tee times at the earliest time they become available.

You will need an existing account with [Golf Burnaby](https://www.golfburnaby.ca)

The script will do the following:

1.  Get the current date and calculate the earliest available day for booking (+5 days)
2.  Inititate a Chrome browser for the script to run on
3.  Set the booking options to 4 golfers and click on the earliest day available
4.  From that day's available times, select the earliest time
5.  Using environment variables, enter the user's email and password to login
6.  Finalize the confirmation by accepting the terms and clicking "Reserve"

The user should get a reservation confirmation email shortly after!
