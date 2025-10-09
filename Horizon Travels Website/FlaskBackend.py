# Author: Aaron Antal-Bento ID: 23013693
from flask import Flask, render_template, redirect, url_for, request, jsonify, session, make_response
import dbfunc
from datetime import datetime, timedelta
from passlib.hash import sha256_crypt
import gc
from functools import wraps
import re
import weasyprint
import numpy as np

app = Flask(__name__)   #instatntiating flask app
app.secret_key = 'ZhcCDp8B5p'     #secret key for sessions

def selectcolumn(tablename, columnname, distinct=False, orderby=False):
   tablename = sanitizeVariable(tablename)
   columnname = sanitizeVariable(columnname)
   # Construct the SQL statement
   SQLstatement = ('SELECT ' +
      ('DISTINCT ' if distinct else '') +
      columnname +
      f' FROM {tablename}' +
      f' ORDER BY {columnname}' if orderby else '' +
      ';')
   return SanitizeAndExecuteSQL(SQLstatement, ())
def selectcolumnwhereequals(tablename, columnname, distinct, orderby, columnwhere, columnequals):
   tablename = sanitizeVariable(tablename)
   columnname = sanitizeVariable(columnname)
   columnwhere = sanitizeVariable(columnwhere)
   # Construct the SQL statement
   SQLstatement = (
    'SELECT ' +
    ('DISTINCT ' if distinct else '') +
    f'{columnname} FROM {tablename} '
    f'WHERE {columnwhere} = %s' +
    (f' ORDER BY {columnname}' if orderby else '') +
    ';')
   return SanitizeAndExecuteSQL(SQLstatement, (columnequals,))
def selectcolumns(tablename, columnnames, columnwhere, columnequals):
   tablename = sanitizeVariable(tablename)
   columnnames = [sanitizeVariable(name) for name in columnnames]
   columnwhere = sanitizeVariable(columnwhere)
   columnnamesSQL = ", ".join(columnnames)
   # Construct the SQL statement
   SQLstatement = (
    'SELECT ' +
    f'{columnnamesSQL} FROM {tablename} '
    f'WHERE {columnwhere} = %s' +
    ';')
   return SanitizeAndExecuteSQL(SQLstatement, (columnequals,))
def selectallcolumns(tablename, columnwhere, columnequals):
   tablename = sanitizeVariable(tablename)
   columnwhere = sanitizeVariable(columnwhere)
   # Construct the SQL statement
   SQLstatement = (
    'SELECT ' +
    f'* FROM {tablename} '
    f'WHERE {columnwhere} = %s' +
    ';')
   return SanitizeAndExecuteSQL(SQLstatement, (columnequals,))
def selectjourneys(origin, destination, weekday, date):
   params = []
   # Construct the SQL statement
   SQLstatement = """SELECT
      journeys.JourneyID, journeys.CompanyID,
      origin, DepartureTime,
      destination, ArrivalTime,
      TIMEDIFF(ArrivalTime, DepartureTime) AS Duration,
      price,
      company.EconomySeats - COALESCE(SUM(CASE WHEN bookings.cancelled = 0 THEN bookings.StandardSeats ELSE 0 END), 0) AS RemainingStandardSeats,
	   company.BusinessSeats - COALESCE(SUM(CASE WHEN bookings.cancelled = 0 THEN bookings.FirstClassSeats ELSE 0 END), 0) AS RemainingFirstClassSeats
      FROM journeys
      INNER JOIN traveldays ON journeys.CompanyID = traveldays.CompanyID
      INNER JOIN company ON journeys.CompanyID = company.CompanyID
      LEFT JOIN  bookings ON journeys.JourneyID = bookings.JourneyID
      AND bookings.JourneyDate = %s
      WHERE """
   params.append(date)
   if origin:
      SQLstatement += 'origin = %s ' 
      params.append(origin)

   if destination:
      SQLstatement += 'AND ' if origin else ''
      SQLstatement += 'destination = %s '
      params.append(destination)

   SQLstatement += 'AND ' if origin or destination else ''
   SQLstatement += 'Weekday = %s \
      GROUP BY journeys.JourneyID \
      ORDER BY DepartureTime;'
   params.append(weekday)

   return SanitizeAndExecuteSQL(SQLstatement, params)
def selectjourney(journeyID, date):
   # Construct the SQL statement
   SQLstatement = """SELECT
      journeys.CompanyID,
      origin, DepartureTime,
      destination, ArrivalTime,
      TIMEDIFF(ArrivalTime, DepartureTime) AS Duration,
      price,
      company.EconomySeats - COALESCE(SUM(CASE WHEN bookings.cancelled = 0 THEN bookings.StandardSeats ELSE 0 END), 0) AS RemainingStandardSeats,
	   company.BusinessSeats - COALESCE(SUM(CASE WHEN bookings.cancelled = 0 THEN bookings.FirstClassSeats ELSE 0 END), 0) AS RemainingFirstClassSeats
      FROM journeys
      INNER JOIN company ON journeys.CompanyID = company.CompanyID
      LEFT JOIN  bookings ON journeys.JourneyID = bookings.JourneyID
      AND bookings.JourneyDate = %s
      WHERE journeys.JourneyID = %s"""
   return SanitizeAndExecuteSQL(SQLstatement, (date, journeyID))
def selecttable(tablename):
   tablename = sanitizeVariable(tablename)
   return SanitizeAndExecuteSQL(f'SELECT * FROM {tablename};', ())
def selectusersjourneys(userID):
   # Construct the SQL statement
   SQLstatement = """SELECT BookingID, journeys.CompanyID, 
      journeys.Origin, journeys.DepartureTime, 
      journeys.Destination, journeys.ArrivalTime, 
      TIMEDIFF(ArrivalTime, DepartureTime) AS Duration,
      PricePaidPerSeat, 
      StandardSeats, FirstClassSeats, 
      BookingDate, JourneyDate, BookingRefrence, Cancelled
      FROM bookings 
      LEFT JOIN journeys ON bookings.JourneyID = journeys.JourneyID
      WHERE UserID = %s
      ORDER BY bookings.JourneyDate, journeys.DepartureTime;"""
   return SanitizeAndExecuteSQL(SQLstatement, (userID,))
def selectuserjourneysmin(userID):
   # Construct the SQL statement
   SQLstatement = """SELECT BookingID, journeys.CompanyID, 
      journeys.Origin, journeys.Destination,
      JourneyDate, journeys.DepartureTime,
      BookingDate, 
      BookingRefrence,
      StandardSeats, FirstClassSeats, 
      PricePaidPerSeat,
      Cancelled
      FROM bookings 
      LEFT JOIN journeys ON bookings.JourneyID = journeys.JourneyID
      WHERE UserID = %s
      ORDER BY bookings.JourneyDate, journeys.DepartureTime;"""
   return SanitizeAndExecuteSQL(SQLstatement, (userID,))
def selectbookingtimes(bookingID):
   SQLstatement = """SELECT journeys.DepartureTime, JourneyDate, Cancelled
      FROM bookings 
      LEFT JOIN journeys ON bookings.JourneyID = journeys.JourneyID
      WHERE BookingID = %s;"""
   return SanitizeAndExecuteSQL(SQLstatement, (bookingID,))
def selectbooking(bookingID):
   # Construct the SQL statement
   SQLstatement = """SELECT journeys.Origin, journeys.DepartureTime, 
      journeys.Destination,
      PricePaidPerSeat, 
      StandardSeats, FirstClassSeats, 
      BookingDate, JourneyDate, BookingRefrence
      FROM bookings 
      LEFT JOIN journeys ON bookings.JourneyID = journeys.JourneyID
      WHERE BookingID = %s;"""
   return SanitizeAndExecuteSQL(SQLstatement, (bookingID,))[0]
def selectbookingfull(bookingID):
   SQLstatement = """SELECT journeys.Origin, journeys.DepartureTime, 
      journeys.Destination, journeys.ArrivalTime, journeys.CompanyID,
      PricePaidPerSeat, 
      TIMEDIFF(journeys.ArrivalTime, journeys.DepartureTime) AS Duration,
      StandardSeats, FirstClassSeats, 
      BookingDate, JourneyDate, BookingRefrence, users.First_Name, users.Last_Name
      FROM bookings 
      LEFT JOIN journeys ON bookings.JourneyID = journeys.JourneyID
      LEFT JOIN users ON bookings.UserID = users.UserID
      WHERE BookingID = %s;"""
   return SanitizeAndExecuteSQL(SQLstatement, (bookingID,))[0]
def selectusersnames():
   return SanitizeAndExecuteSQL('SELECT UserID, First_Name, Last_Name, email FROM users;', ())
def getUserDetails(email):
   return SanitizeAndExecuteSQL('SELECT Password, UserID, First_Name, UserType FROM users WHERE email = %s;', (email,))
def getCurrentPassword(userID):
   return SanitizeAndExecuteSQL('SELECT Password FROM users WHERE UserID = %s;', (userID,))
def emailUnique(email):
   result = SanitizeAndExecuteSQL('SELECT * FROM users WHERE email = %s;', (email,))
   if not result:
      return True
   return False
def insertNewAccount(fname, lname, email, password):
   # Construct the SQL statement
   SQLstatement = 'INSERT INTO users (First_Name, Last_name, Email, Password, RegDate, RegTime) \
   VALUES (%s, %s, %s, %s, CURRENT_DATE, CURRENT_TIME)'
   SanitizeAndExecuteSQL(SQLstatement, (fname, lname, email, password,))
def insertNewCard(UserID, CardNumber, ExpDate, CVV, NameOnCard):
   # Construct the SQL statement
   SQLstatement = 'INSERT INTO cardinfo (UserID, CardNumber, ExpDate, CVV, NameOnCard) \
   VALUES (%s, %s, %s, %s, %s)'
   return SanitizeAndExecuteSQL(SQLstatement, (UserID, CardNumber, ExpDate, CVV, NameOnCard,))
def insertNewCardNoUser(CardNumber, ExpDate, CVV, NameOnCard):
   # Construct the SQL statement
   SQLstatement = 'INSERT INTO cardinfo (CardNumber, ExpDate, CVV, NameOnCard) \
   VALUES (%s, %s, %s, %s)'
   return SanitizeAndExecuteSQL(SQLstatement, (CardNumber, ExpDate, CVV, NameOnCard,))
def insertNewBooking(UserID, CardID, JourneyID, StandardSeats, FirstClassSeats, PricePaidPerSeat, BookingDate, JourneyDate):
   # Construct the SQL statement
   SQLstatement = 'INSERT INTO bookings (UserID, CardID, JourneyID, \
      StandardSeats, FirstClassSeats, PricePaidPerSeat, BookingDate, JourneyDate) \
      VALUES (%s, %s, %s, %s, %s, %s, %s, %s)'
   return SanitizeAndExecuteSQL(SQLstatement, (UserID, CardID, JourneyID, StandardSeats, FirstClassSeats, PricePaidPerSeat, BookingDate, JourneyDate,))
def insertNewJourney(companyid, origin, departuretime, destination, arrivaltime, price):
   SQLstatement = 'INSERT INTO journeys (CompanyID, Origin, DepartureTime, Destination, ArrivalTime, Price) \
   VALUES (%s, %s, %s, %s, %s, %s)'
   return SanitizeAndExecuteSQL(SQLstatement, (companyid, origin, departuretime, destination, arrivaltime, price,))
def addBookingRef(BookingID, bookingRef):
   SQLstatement = "UPDATE bookings SET BookingRefrence = %s WHERE BookingID = %s"
   SanitizeAndExecuteSQL(SQLstatement, (bookingRef, BookingID,))
def getUserIDFromEmail(email):
   return SanitizeAndExecuteSQL('SELECT userID FROM users WHERE email = %s', (email,))[0][0]
def getCardInfo(userID, long=False, secure=True):
   # Construct the SQL statement
   if not long:
      SQLstatement = 'SELECT CardID, RIGHT(CardNumber, 4) FROM cardinfo WHERE UserID = %s;'
   elif not secure:
      SQLstatement = 'SELECT CardID, NameOnCard, CardNumber, ExpDate, CVV FROM cardinfo WHERE UserID = %s;'
   else:
      SQLstatement = 'SELECT CardID, NameOnCard, RIGHT(CardNumber, 4), ExpDate FROM cardinfo WHERE UserID = %s;'

   return SanitizeAndExecuteSQL(SQLstatement, (userID,))
def deleteRecord(tablename, columnwhere, columnequals):
   tablename = sanitizeVariable(tablename)
   columnwhere = sanitizeVariable(columnwhere)
   # Construct the SQL statement
   SQLstatement = ('DELETE' +
      f' FROM {tablename}' +
      f' WHERE {columnwhere} = %s' +
      ';')
   SanitizeAndExecuteSQL(SQLstatement, (columnequals, ))
def updateValue(tablename, columnwhere, columnequals, columnset, valueset):
   tablename = sanitizeVariable(tablename)
   columnwhere = sanitizeVariable(columnwhere)
   columnset = sanitizeVariable(columnset)
   # Construct the SQL statement
   SQLstatement = ('UPDATE ' +
      tablename +
      f' SET {columnset} = %s' +
      f' WHERE {columnwhere} = %s' +
      ';')
   SanitizeAndExecuteSQL(SQLstatement, (valueset, columnequals, ))
def updaterow(tablename, columnwhere, columnequals, columnanddata):
   tablename = sanitizeVariable(tablename)
   columnwhere = sanitizeVariable(columnwhere)

   # Construct the SQL statement
   SQLstatement = f'UPDATE {tablename} SET '
   SQLstatement += ', '.join([f"{key} = '{value}'" for key, value in columnanddata.items()])
   SQLstatement +=   f' WHERE {columnwhere} = %s;'
   return SanitizeAndExecuteSQL(SQLstatement, (columnequals, ))
def deleteValue(tablename, columnwhere, columnequals, columndel):
   tablename = sanitizeVariable(tablename)
   columnwhere = sanitizeVariable(columnwhere)
   columndel = sanitizeVariable(columndel)
   # Construct the SQL statement
   SQLstatement = ('UPDATE ' +
      tablename +
      f' SET {columndel} = NULL' +
      f' WHERE {columnwhere} = %s' +
      ';')
   SanitizeAndExecuteSQL(SQLstatement, (columnequals, ))
def userOwnsCard(cardid, userid):
    SQLstatement = "SELECT 1 FROM cardinfo WHERE userid = %s AND cardid = %s LIMIT 1;"
    result = SanitizeAndExecuteSQL(SQLstatement, (userid, cardid, ))
    
    if result:
        return True
    return False
def userOwnsBooking(bookingid, userid):
    SQLstatement = "SELECT 1 FROM bookings WHERE userid = %s AND bookingid = %s LIMIT 1;"
    result = SanitizeAndExecuteSQL(SQLstatement, (userid, bookingid, ))
    
    if result:
        return True
    return False
def fetchjourneysalesdata(times):
   SQLstatement = '''SELECT 
    j.JourneyID, j.CompanyID, j.DepartureTime, j.Origin, j.Destination,
    COALESCE(SUM(CASE WHEN b.cancelled = 0 THEN b.StandardSeats ELSE 0 END), 0) AS total_standard_seats,
    COALESCE(SUM(CASE WHEN b.cancelled = 0 THEN b.FirstClassSeats ELSE 0 END), 0) AS total_first_class_seats,
    COALESCE(SUM(CASE WHEN b.cancelled = 1 THEN b.FirstClassSeats ELSE 0 END), 0) + 
    COALESCE(SUM(CASE WHEN b.cancelled = 1 THEN b.StandardSeats ELSE 0 END), 0) AS total_cancelled_seats
   FROM journeys j
   LEFT JOIN bookings b
   ON j.JourneyID = b.JourneyID '''

   if times == 'monthly':
        SQLstatement += """
        WHERE (b.JourneyDate IS NULL OR
              (b.JourneyDate BETWEEN DATE_FORMAT(CURDATE(), '%Y-%m-01') AND LAST_DAY(CURDATE())))
        """
   elif times == 'annual':
        # For annual sales, show only bookings from the current year.
        SQLstatement += """
        WHERE (b.JourneyDate IS NULL OR YEAR(b.JourneyDate) = YEAR(CURDATE()))
        """

   SQLstatement += '''GROUP BY j.JourneyID
   ORDER BY j.CompanyID, j.DepartureTime;'''

   return SanitizeAndExecuteSQL(SQLstatement,())
def fetchjourneyrevenuedata(times):
    SQLstatement = '''SELECT 
        j.JourneyID, j.CompanyID,  j.DepartureTime, j.Origin, j.Destination,
        SUM(CASE 
            WHEN b.cancelled = 0 THEN (b.StandardSeats + b.FirstClassSeats) * b.PricePaidPerSeat
            WHEN b.cancelled = 1 THEN (b.StandardSeats + b.FirstClassSeats) * (b.PricePaidPerSeat - b.RefundAmount)
            ELSE 0 END) AS total_revenue,
        COALESCE(SUM(CASE WHEN b.cancelled = 1 THEN (b.StandardSeats + b.FirstClassSeats) * b.RefundAmount 
        ELSE 0 END), 0) AS revenue_from_cancellations
    FROM journeys j
    LEFT JOIN bookings b
    ON j.JourneyID = b.JourneyID '''

    # Apply filtering based on the time period (monthly or annual sales)
    if times == 'monthly':
        SQLstatement += """
        WHERE (b.JourneyDate IS NULL OR
              (b.JourneyDate BETWEEN DATE_FORMAT(CURDATE(), '%Y-%m-01') AND LAST_DAY(CURDATE())))
        """
    elif times == 'annual':
        SQLstatement += """
        WHERE (b.JourneyDate IS NULL OR YEAR(b.JourneyDate) = YEAR(CURDATE()))
        """

    # Add GROUP BY and ORDER BY clauses
    SQLstatement += '''GROUP BY j.JourneyID
    ORDER BY j.CompanyID, j.DepartureTime;'''

    # Execute and return the results
    return SanitizeAndExecuteSQL(SQLstatement, ())
def fetchsinglejourneyrevenuedata(id):
    SQLstatement = '''SELECT 
      JourneyDate, 
      SUM(CASE 
            WHEN b.cancelled = 0 THEN (b.StandardSeats + b.FirstClassSeats) * b.PricePaidPerSeat
            WHEN b.cancelled = 1 THEN (b.StandardSeats + b.FirstClassSeats) * (b.PricePaidPerSeat - b.RefundAmount)
            ELSE 0 END) AS TotalIncome
   FROM bookings AS b
   JOIN journeys AS j ON j.JourneyID = b.JourneyID
   WHERE b.JourneyID = %s 
   GROUP BY JourneyDate
   ORDER BY JourneyDate;'''
    
    SQL = '''SELECT JourneyID, CompanyID, DepartureTime, Origin, Destination FROM journeys WHERE JourneyID = %s;'''

    # Execute and return the results
    return [SanitizeAndExecuteSQL(SQL, (id,)), SanitizeAndExecuteSQL(SQLstatement, (id,))]
def selectTopCustomers():
   SQLstatement = '''SELECT 
         u.UserID,
         CONCAT(u.First_Name, ' ', u.Last_Name) AS FullName,
         u.Email,
         COUNT(b.BookingID) AS BookingCount,
         COALESCE(SUM(
            CASE 
            WHEN b.cancelled = 0 THEN (b.StandardSeats + b.FirstClassSeats) 
            ELSE 0 
            END
         ), 0) AS SeatsBooked,
         COALESCE(
         SUM(
            CASE 
            WHEN b.cancelled = 0 THEN (b.StandardSeats + b.FirstClassSeats) * b.PricePaidPerSeat 
            WHEN b.cancelled = 1 THEN (b.StandardSeats + b.FirstClassSeats) * (b.PricePaidPerSeat - b.RefundAmount)
            ELSE 0 
            END
         ),
         0
         ) AS AmountSpent,
         (
            SELECT b2.JourneyID
            FROM Bookings b2
            WHERE b2.UserID = u.UserID
            GROUP BY b2.JourneyID
            ORDER BY 
                  COUNT(*) DESC, 
                  COALESCE(SUM(b2.StandardSeats + b2.FirstClassSeats), 0) DESC
            LIMIT 1
         ) AS MostFrequentJourney
      FROM Users u
      LEFT JOIN Bookings b ON u.UserID = b.UserID
      GROUP BY 
         u.UserID, 
         u.First_Name, 
         u.Last_Name, 
         u.Email
      ORDER BY 
         AmountSpent DESC, 
         u.Last_Name, 
         u.First_Name;'''
   return SanitizeAndExecuteSQL(SQLstatement, ())
def selectCompanyBookingData():
   SQLstatement = '''SELECT 
  -- Total income from non-cancelled bookings:
  COALESCE(
    SUM(
      CASE 
        WHEN b.cancelled = 0 THEN (b.StandardSeats + b.FirstClassSeats) * b.PricePaidPerSeat 
        WHEN b.cancelled = 1 THEN (b.StandardSeats + b.FirstClassSeats) * (b.PricePaidPerSeat - b.RefundAmount)
        ELSE 0 
      END
    ), 0) AS TotalRevenue,
  -- Total seats (standard + first class) for non-cancelled bookings:
  COALESCE(
    SUM(
      CASE 
        WHEN b.cancelled = 0 
        THEN (b.StandardSeats + b.FirstClassSeats)
        ELSE 0 
      END
    ), 0) AS TotalSeats,
  -- Percentage of first class seats relative to the total (non-cancelled):
  CASE 
    WHEN COALESCE(
           SUM(
             CASE 
               WHEN b.cancelled = 0 
               THEN (b.StandardSeats + b.FirstClassSeats)
               ELSE 0 
             END
           ), 0) > 0
    THEN ROUND(
           COALESCE(
             SUM(
               CASE 
                 WHEN b.cancelled = 0 
                 THEN b.FirstClassSeats
                 ELSE 0 
               END
             ), 0) * 100.0 /
           COALESCE(
             SUM(
               CASE 
                 WHEN b.cancelled = 0 
                 THEN (b.StandardSeats + b.FirstClassSeats)
                 ELSE 0 
               END
             ), 0)
         , 1)
    ELSE 0
  END AS FirstClassPercentage,
  -- Total seats cancelled:
  COALESCE(
    SUM(
      CASE 
        WHEN b.cancelled = 1 
        THEN (b.StandardSeats + b.FirstClassSeats)
        ELSE 0 
      END
    ), 0) AS TotalSeatsCancelled
FROM journeys j
LEFT JOIN Bookings b ON j.JourneyID = b.JourneyID
GROUP BY j.CompanyID;
'''
   return SanitizeAndExecuteSQL(SQLstatement, ())
def selectCompanyJourneyData():
   SQLstatement = '''SELECT 
  jc.JourneyCount,
  uc.UniqueCities
FROM
  (
    SELECT CompanyID, COUNT(JourneyID) AS JourneyCount
    FROM journeys
    GROUP BY CompanyID
  ) AS jc
JOIN
  (
    SELECT CompanyID, COUNT(DISTINCT city) AS UniqueCities
    FROM (
      SELECT CompanyID, origin AS city FROM journeys
      UNION
      SELECT CompanyID, destination AS city FROM journeys
    ) AS AllCities
    GROUP BY CompanyID
  ) AS uc
ON jc.CompanyID = uc.CompanyID;
'''
   return SanitizeAndExecuteSQL(SQLstatement, ())
def selectBookingInfo():
   SQLstatement = '''SELECT 
    Origin,
    DepartureTime,
    Destination,
    ArrivalTime,
    JourneyDate,
    TIMEDIFF(ArrivalTime, DepartureTime) AS Duration,
    COALESCE(SUM(CASE
                WHEN bookings.cancelled = 0 THEN bookings.StandardSeats
                ELSE 0
            END), 0) AS StandardSeats,
    company.EconomySeats,
    COALESCE(SUM(CASE
                WHEN bookings.cancelled = 0 THEN bookings.FirstClassSeats
                ELSE 0
            END), 0) AS FirstClassSeats,
    company.BusinessSeats,
    COALESCE(SUM(CASE 
                WHEN bookings.cancelled = 1 THEN StandardSeats 
                ELSE 0 
            END), 0) AS total_cancelled_seats,
    COUNT(*) AS IndividualBookings, 
    SUM(CASE 
            WHEN cancelled = 0 THEN (StandardSeats + FirstClassSeats) * PricePaidPerSeat
            WHEN cancelled = 1 THEN (StandardSeats + FirstClassSeats) * (PricePaidPerSeat - RefundAmount)
            ELSE 0 END) AS total_revenue 
FROM
    bookings
        INNER JOIN journeys ON journeys.JourneyID = bookings.JourneyID
        INNER JOIN company ON journeys.CompanyID = company.CompanyID
WHERE
    JourneyDate >= CURDATE()
GROUP BY journeys.JourneyID, JourneyDate
ORDER BY JourneyDate, DepartureTime;'''
   return SanitizeAndExecuteSQL(SQLstatement, ())
def SanitizeAndExecuteSQL(query, parameters):
   print(query, parameters)

   try:
      connection = dbfunc.getConnection()    #Connect to MySQL database
      cursor = connection.cursor()
      
      # Execute the parameterized query
      cursor.execute(query, parameters)
      
      # Fetch results for SELECT queries
      if query.strip().upper().startswith("SELECT"):
         results = cursor.fetchall()
         return results
      elif query.strip().upper().startswith("INSERT"):
         connection.commit()
         return cursor.lastrowid
      else:
         connection.commit()
   except Exception as e:
      print(f"Database error: {e}")
      return e

   finally:
      # Close the connection
      if connection.is_connected():
         cursor.close()
         connection.close()

def sanitizeVariable(variable):
   # Replace any non-alphanumeric characters or underscores with an empty string
   sanitized_variable = re.sub(r'[^a-zA-Z0-9_]', '', variable)
   # Return the sanitized variable
   return sanitized_variable
def sanitizeName(name):
   sanitized_name = re.sub(r'[^\w\'\-]', '', name)
   return sanitized_name
def sanitizeFullName(name):
   sanitized_name = re.sub(r'[^a-zA-Z \'\-]', '', name)
   return sanitized_name
def sanitizeCity(city):
   sanitized_city = re.sub(r'[^a-zA-Z ]', '', city)
   return sanitized_city
def sanitizeOriginDest(origindest):
   if (origindest == "origin" or origindest == "destination"):
      return origindest
   return None
def sanitizeEmail(email):
    # Regular expression to match valid email format
    match = re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email)
    if match:
        # If email is valid, return it
        return email
    else:
        # If invalid, return None or a sanitized alternative (optional)
        return ''
def sanitizePassword(password):
   # Replace any non-alphanumeric characters or underscores with an empty string
   sanitized_password = re.sub(r'[^a-zA-Z0-9!@#$%^&*(),.?:{}|<>_-~+=\\]', '', password)
   # Return the sanitized variable
   return sanitized_password
def validate_date(date_str):
   if not date_str:
      return None
   try:
      # Attempt to parse the date in the correct format
      valid_date = datetime.strptime(date_str, "%Y-%m-%d")
      return valid_date
   except ValueError as e:
      return None
def validate_passengers(passengers):
   if not passengers:
      return '1'
   elif not passengers.isdigit():
      passengers = '1'
   elif int(passengers) > 8:
      passengers = '8'
   else:
      passengers = '1'
   return passengers
def validate_digit(digit):
   if digit.isdigit():
      return digit
   return None
def validate_seattype(seattype):
   # Define valid options
   valid_seat_types = ['Standard', 'First class']
   if seattype in valid_seat_types:
      return seattype
   return None

def testCardNumber(number):
   # Define the regular expression pattern
    pattern = r'^(\d{4} ){3}\d{4}$'
    
    # Use re.match to check if the input matches the pattern
    return bool(re.match(pattern, number))
def testExpDate(date):
    pattern = r'^(0[1-9]|1[0-2])\/\d{2}$'
    
    if not re.match(pattern, date):
        return False  # Invalid format

    month, year = map(int, date.split('/'))
    now = datetime.now()
    current_month = now.month
    current_year = now.year % 100

    if year < current_year or (year == current_year and month < current_month):
        return False  # The date has expired
    return True
def isExpiredCard(cardID):
   expDate = SanitizeAndExecuteSQL('SELECT ExpDate FROM cardinfo WHERE CardID = %s', (cardID,))[0]
   expDate = datetime.strptime(expDate[0], '%m/%y')
   if expDate < datetime.today():  # Compare ExpDate with today's date
      return True  # Card is expired
   else:
      return False  # Card is not expired
def testCVV(number):
   # Define the regular expression pattern
    pattern = r'^(\d){3}$'
    
    # Use re.match to check if the input matches the pattern
    return bool(re.match(pattern, number))

def formatCity(list):
   return [row[0] for row in list]
def formattime(journeytime, long=False):
   hours = journeytime // 3600
   mins = (journeytime % 3600) // 60
   timestr = ''
   if hours > 0:
      timestr = f'{hours} hour' + ('s' if hours != 1 else '')
   if mins > 9:
      if long:
         timestr += f' and {mins:02d} minute' + ('s' if mins != 1 else '')
      else:
         timestr += f' {mins:02d} min' + ('s' if mins != 1 else '')
   elif mins > 0:
      if long:
         timestr += f' and {mins:12d} minute' + ('s' if mins != 1 else '')
      else:
         timestr += f' {mins:12d} min' + ('s' if mins != 1 else '')

   return timestr
def timeStr(journeytime):
   hours = journeytime // 3600
   mins = (journeytime % 3600) // 60
   timestr = ''
   if hours > 0:
      timestr = f'{hours} hour'
   if mins > 9:
         timestr += f' {mins:02d} min'
   elif mins > 0:
         timestr += f' {mins:12d} min'

   return timestr
def orderWeekdays(date):
   dayfromdate = date.weekday()
   days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
   ordereddays = []
   for i in range(7):
      ordereddays.append(days[dayfromdate])
      dayfromdate += 1
      if dayfromdate >= 7:
         dayfromdate = 0
   return ordereddays
def getSuffix(i):
    if 4 <= i <= 20 or 24 <= i <= 30:
        return "th"
    else:
        return ["st", "nd", "rd"][i % 10 - 1]
def getMonth(i):
   months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
   return months[i-1]
def getWeekday(i):
   months = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
   return months[i]
def createDateString(weekday, d, datetimeToday):
   if d.date() == datetimeToday.date():
      return 'Today'
   elif d.date() == (datetimeToday + timedelta(days=1)).date():
      return 'Tomorrow'
   return '%s the %d%s of %s %d' % (weekday, d.day, getSuffix(d.day), getMonth(d.month), d.year)
def createDateStringDate(weekday, d, datetimeToday):
   if d == datetimeToday.date():
      return 'Today'
   elif d == (datetimeToday + timedelta(days=1)).date():
      return 'Tomorrow'
   return '%s the %d%s of %s %d' % (weekday, d.day, getSuffix(d.day), getMonth(d.month), d.year)
def getDiscountMultiplier(datetoday, dateofbooking):
   datedifference = dateofbooking - datetoday
   if datedifference >= timedelta(days=80):
      return 0.75
   elif datedifference >= timedelta(days=60):
      return 0.85
   elif datedifference >= timedelta(days=45):
      return 0.90
   else:
      return 1
def generateBookingRef(CompanyID, BookingID, To, From):
   travelMethod = 'P' if CompanyID == 0 else 'T'
   bookingIDRef = convertToHexadecimal(int(BookingID))
   bookingRef = "%c-%s-%s-%s" % (travelMethod, bookingIDRef, abbreviateCity(To), abbreviateCity(From))
   return bookingRef
def abbreviateCity(city):
   city_abbreviations = {
      "Newcastle": "NC",
      "Bristol": "BR",
      "Cardiff": "CF",
      "Manchester": "MA",
      "London": "LD",
      "Glasgow": "GL",
      "Portsmouth": "PO",
      "Dundee": "DU",
      "Edinburgh": "ED",
      "Southampton": "SO",
      "Birmingham": "BM",
      "Aberdeen": "AB"
   }
   if city in city_abbreviations:
        return city_abbreviations[city]

   existing_abbreviations = set(city_abbreviations.values())
   abbreviation = city[:2].upper()

   i = 2
   while abbreviation in existing_abbreviations:
      if i < len(city):
         abbreviation = (city[0] + city[i]).upper()
         i += 1
      else:
         abbreviation = city[:2].upper() + city[-1].upper()
         break

   return abbreviation
def convertToHexadecimal(number):
    if number < 0:
        return '00'
    return hex(number)[2:].upper().zfill(2)
def makeDaysUntilJourneyStr(daysUntilJourney):
   if (daysUntilJourney == 0):
      return "This journey is today"
   elif (daysUntilJourney == 1):
      return "This journey is tommorow"
   elif (daysUntilJourney == -1):
      return "This journey was yesterday"
   elif (daysUntilJourney < 0):
      daysUntilJourney = abs(daysUntilJourney)
      return f"This journey was {daysUntilJourney} day{'s' if daysUntilJourney != 1 else ''} ago" 
   else:
      return f"This journey is in {daysUntilJourney} day{'s' if daysUntilJourney != 1 else ''}" 

def checkIfDeparted(journeydate, bookingdate, departureTime):
   if isinstance(journeydate, datetime):
      journeydate = journeydate.date()

   currentTime = datetime.today().time()
   timeFromStartOfDay = timedelta(hours=currentTime.hour, minutes=currentTime.minute, seconds=currentTime.second)
   isBeforeToday = journeydate < bookingdate.date()
   journeyToday = journeydate == bookingdate.date()
   return ((departureTime.seconds < timeFromStartOfDay.total_seconds() and journeyToday) or isBeforeToday)
def areSeatsLeft(seattype, seatsToBook, standardSeatsLeft, firstclassSeatsLeft):
   return (int(standardSeatsLeft)>=int(seatsToBook)) if seattype == 'Standard' else (int(firstclassSeatsLeft)>=int(seatsToBook))

@app.route('/')  # Flask variable
@app.route('/HorizonTravels')
def home():  # Function associated with the decorator
    if 'next' in session:
      session.pop('next')

    destinations = formatCity(selectcolumn('journeys', 'destination', True, True))
    origins = formatCity(selectcolumn('journeys', 'origin', True, True))
    return render_template('HorizonTravels.html', dest=destinations, orgn=origins, cookies='cookie_consent' not in session)

@app.route('/getcities', methods=['POST']) #gets the cities available when a destination or origin is selected by the user
def getcities():
   city = sanitizeCity(request.form.get('city'))
   constriantOriginDest = sanitizeOriginDest(request.form.get('constriantOriginDest'))
   availableOriginDest = sanitizeOriginDest(request.form.get('availableOriginDest'))

   if city != 'all':
      validCities = formatCity(selectcolumnwhereequals('journeys', availableOriginDest, True, True, constriantOriginDest, city))
   else:
      validCities = formatCity(selectcolumn('journeys', availableOriginDest, True, True))

   return jsonify(validCities)

@app.route('/HorizonTravels/signin', methods=['POST', 'GET'])
def signin():
   form={}
   error = ''

   if request.method == "POST":
      email = sanitizeEmail(request.form.get('email').lower())
      password = sanitizePassword(request.form.get('password'))
      form = request.form

      if email != '' and password != '':
         userdata = getUserDetails(email)
         
         if not userdata: #this means no user exists
            error = "Failed to sign in, please check your details and try again."
            return render_template("SignIn.html", form=form, error=error)
         else:
            userdata = userdata[0]
            # verify passoword hash and password received from user 
            if sha256_crypt.verify(password, str(userdata[0])):
               if request.form.get('remember'):
                  session.permanent = True
               else:
                  session.permanent = False

               session['logged_in'] = True     #set session variables
               session['username'] = str(userdata[2])
               session['UserID'] = userdata[1]
               session['usertype'] = str(userdata[3])
               session['cookie_consent'] = True
               print("You are now logged in")

               if 'next' in session:
                  return redirect(session.pop('next'))
               return redirect(url_for('home'))
            else:
               error = "Failed to sign in, please check your details and try again."
         gc.collect()
      else:
         error = "Error submitting information, please enter valid details."
   return render_template('SignIn.html', form=form, error=error)

@app.route('/getusersname')
def getusersname():
   if "username" in session:
      if len(session['username']) > 8:
         return session['username'][0]
      return session['username']
   return ''

@app.route('/HorizonTravels/register', methods=['POST', 'GET'])
def register():
   form={}
   error = ''

   if request.method == "POST":
      fname = sanitizeName(request.form.get('Fname'))
      lname = sanitizeName(request.form.get('Lname'))
      email = sanitizeEmail(request.form.get('email').lower())
      password = sanitizePassword(request.form.get('password'))
      form = request.form

      if email != '' and len(password) >= 8 and fname != '':
         password = sha256_crypt.hash((str(password)))
         if emailUnique(email):
            insertNewAccount(fname, lname, email, password)
            gc.collect()                        
            if request.form.get('remember'):
               session.permanent = True
            else:
               session.permanent = False

            session['logged_in'] = True 
            session['username'] = fname
            session['UserID'] = getUserIDFromEmail(email)
            session['usertype'] = 'Standard'
            session['cookie_consent'] = True
            print("You are now logged in")

            if 'next' in session:
               return redirect(session.pop('next'))
            return redirect(url_for('home'))
         else:
            error = "An account already exists with this email, please sign in."
            render_template('Register.html', form=form, error=error)
         gc.collect()
      else:
         invalid = 'vaild details'
         if email == '': invalid = 'a valid email'
         elif fname == '' : invalid = 'a valid first name'
         error = f"Error submitting information, please enter {invalid}."
   return render_template('Register.html', form=form, error=error)

def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:            
            return redirect(url_for('signin'))
    return wrap
def admin_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if ('logged_in' in session) and (session['usertype'] == 'Admin'):
            return f(*args, **kwargs)
        else:            
            return redirect(url_for('signin'))
    return wrap
def active_booking(f):
   @wraps(f)
   def wrap(*args, **kwargs):
      if 'ActiveBooking' in session:
         return f(*args, **kwargs)
      else:
         return redirect(url_for('journeys'))
   return wrap

@app.route("/logout")
@login_required
def logout():
    # Clear all session variables stored on the server side
    session.clear()
    resp = make_response(redirect(url_for('home')))
    resp.delete_cookie('origin')
    resp.delete_cookie('destination')
    resp.delete_cookie('passengers')
    resp.delete_cookie('date')

    print("You have been logged out!")
    gc.collect()
    return resp

@app.route("/deleteaccount")
@login_required
def deleteaccount():
   deleteValue('cardinfo', 'UserID', session['UserID'], 'UserID')
   updateValue('bookings', 'UserID', session['UserID'], 'Cancelled', '1')
   deleteValue('bookings', 'UserID', session['UserID'], 'UserID')
   deleteRecord('users', 'UserID', session['UserID'])
   session.clear()
   resp = make_response(redirect(url_for('home')))
   resp.delete_cookie('origin')
   resp.delete_cookie('destination')
   resp.delete_cookie('passengers')
   resp.delete_cookie('date')   

   print("You have been logged out!")
   gc.collect()
   return resp

@app.route("/admindeleteaccount/<int:userID>")
@login_required
@admin_required
def admindeleteaccount(userID):
   try:
      deleteValue('cardinfo', 'UserID', userID, 'UserID')
      updateValue('bookings', 'UserID', userID, 'Cancelled', '1')
      deleteValue('bookings', 'UserID', userID, 'UserID')
      deleteRecord('users', 'UserID', userID)
      return redirect(url_for('adminpanel'))
   except Exception as e:
      print(f"Error while deleting card: {e}")
      return "", 500  # Return an error status code

@app.route("/HorizonTravels/account/email", methods=['POST'])
@login_required
def changeemail():
   form={}
   error = ''
   email = sanitizeEmail(request.form.get('email').lower())
   form = request.form

   if email != '':
      if emailUnique(email):
         updateValue('users', 'UserID', session.get('UserID'), 'email', email)
         gc.collect()
      else:
         error = "An account already exists with this email, please sign in."
      gc.collect()
   else:
      invalid = 'vaild details'
      if email == '': invalid = 'a valid email'
      error = f"Error submitting information, please enter {invalid}."
   
   if error:
      accountdata = selectcolumns('users', ['First_Name', 'Last_Name', 'email', 'RegDate'], 'UserID', session['UserID'])
      regDateStr = ''
      if accountdata[0][3]:
         regDateStr = accountdata[0][3].strftime("%d/%m/%Y")
      return render_template('Account.html', username=accountdata[0][0], lastname=accountdata[0][1], email=accountdata[0][2], regDate=regDateStr, usertype=session['usertype'], form=form, emailerrormsg=error)
   return redirect(url_for('account'))

@app.route("/HorizonTravels/account/password", methods=['POST'])
@login_required
def changepassword():
   form={}
   error = ''
   oldpassword = sanitizePassword(request.form.get('oldpassword'))
   password = sanitizePassword(request.form.get('password'))
   form = request.form

   if len(password) >= 8 and oldpassword != password:
      password = sha256_crypt.hash((str(password)))
      
      userdata = getCurrentPassword(session.get('UserID'))
      if not userdata: #this means no user exists
         error = "Failed to find account, please try to signin again."
      else:
         userdata = userdata[0]
         # verify passoword hash and password received from user 
         if sha256_crypt.verify(oldpassword, str(userdata[0])):
            updateValue('users', 'UserID', session.get('UserID'), 'password', password)
         else:
            error = "Incorrect password, please enter your old password correctly."
      gc.collect()
   elif oldpassword == password:
      error = "Please enter a password different from your old one."
   else:
      error = "Error submitting details, please enter a vaild password."

   if error:
      accountdata = selectcolumns('users', ['First_Name', 'Last_Name', 'email', 'RegDate'], 'UserID', session['UserID'])
      regDateStr = ''
      if accountdata[0][3]:
         regDateStr = accountdata[0][3].strftime("%d/%m/%Y")
      return render_template('Account.html', username=accountdata[0][0], lastname=accountdata[0][1], email=accountdata[0][2], regDate=regDateStr, usertype=session['usertype'], form=form, passerrormsg=error)
   return redirect(url_for('account'))

@app.route('/HorizonTravels/about')
def about():
   return render_template('About.html')

@app.route('/save_cookie_preference', methods=['POST'])
def save_cookie_preference():
    # Get the JSON data from the request
    data = request.get_json()
    consent = data.get('cookieConsent')
    
    session['cookie_consent'] = True if consent == 'accepted' else False

    # Return a JSON response indicating success.
    return jsonify({
        "status": "success",
        "preference": consent
    })

@app.route('/HorizonTravels/journeys', methods=['GET'])
def journeys():
   if 'next' in session:
      session.pop('next')

   datetimeToday = datetime.today()

   origin = request.args.get('origin', request.cookies.get('origin', 'all'))
   destination = request.args.get('destination', request.cookies.get('destination', 'all'))
   passengers = request.args.get('passengers', request.cookies.get('passengers', '1'))
   date = request.args.get('date', request.cookies.get('date', str(datetimeToday.date())))

   # Check if passengers is a valid number between 1 and 8
   if not passengers or not passengers.isdigit() or int(passengers) < 1 or int(passengers) > 8:
      passengers = validate_passengers(passengers)
      return redirect(url_for('journeys', origin=origin, destination=destination, passengers=passengers, date=date))

   # Check if the date is before today's date
   if(validate_date(date)):
      if str(date) < str(datetimeToday.date()):
         date = str(datetimeToday.date())
         return redirect(url_for('journeys', origin=origin, destination=destination, passengers=passengers, date=date))
   else:
      date = str(datetimeToday.date())
      return redirect(url_for('journeys', origin=origin, destination=destination, passengers=passengers, date=date))

   datetimeBooking = datetime.strptime(date, "%Y-%m-%d")

   if origin == 'all':
      origin = ''
   if destination == 'all':
      destination = ''

   journeycount = 0
   maxjourneycount = 10
   datetimeJourney = datetimeBooking

   weekdays = orderWeekdays(datetimeBooking)
   journeyWeek = []
   for weekday in weekdays:
      if journeycount >= maxjourneycount:
         break
      
      datestring = createDateString(weekday, datetimeJourney, datetimeToday)
      
      journeydata = selectjourneys(origin, destination, weekday, datetimeJourney.date()) # filter by week day

      journeys = []
      for j in journeydata:
         if(datetimeJourney-datetimeToday > timedelta(days=90)): continue

         standardprice = j[7] // 100
         earlyBookingDiscount = getDiscountMultiplier(datetimeToday, datetimeJourney)
         currentTime = datetime.today().time()
         timeFromStartOfDay = timedelta(hours=currentTime.hour, minutes=currentTime.minute, seconds=currentTime.second)
         hasDeparted = (j[3].seconds < timeFromStartOfDay.total_seconds() and weekday == getWeekday(datetimeToday.weekday()))

         journeys.append({
            "JourneyID" : j[0],
            "CompanyID" : j[1],
            "Origin" : j[2],
            "DepartureTime" : '%02d:%02d' % (j[3].seconds // 3600, (j[3].seconds % 3600) // 60), # Extract HH:MM from HH:MM:SS for departure time
            "Destination" : j[4], # Extract HH:MM from HH:MM:SS for journey time
            "ArrivalTime" : '%02d:%02d' % (j[5].seconds // 3600, (j[5].seconds % 3600) // 60), # Extract HH:MM from HH:MM:SS for arrival time
            "JourneyDuration" : formattime(j[6].seconds),
            "StandardTicketPrice" : int(standardprice * earlyBookingDiscount),
            "FirstClassTicketPrice" : int(standardprice * 2 * earlyBookingDiscount),
            "StandardSeatsLeft" : j[8],
            "FirstClassSeatsLeft" : j[9],
            "HasDeparted" : hasDeparted,
            "JourneyDate" : datetimeJourney.date(),
         })

         if hasDeparted == False: # only count journeys that have not departed 
            journeycount += 1
      journeyWeek.append({"Journeys" : journeys, "DateString" : datestring})
      datetimeJourney += timedelta(days=1)

   are_all_empty = all(len(item["Journeys"]) == 0 for item in journeyWeek)
   if are_all_empty:
      if(datetimeJourney-datetimeToday > timedelta(days=90)):
         message = "Bookings can only be made up to 3 months in advance."
         return render_template('NoJourneys.html', message=message)
      return render_template('NoJourneys.html')

   response = make_response(render_template('Journeys.html', journeyWeek=journeyWeek, seats=passengers))
   if(session.get('cookie_consent', False)):
      response.set_cookie('origin', origin, max_age=3600)
      response.set_cookie('destination', destination, max_age=3600)
      response.set_cookie('passengers', passengers, max_age=3600)
      response.set_cookie('date', date, max_age=3600)
   return response

@app.route('/HorizonTravels/journeys/storebooking', methods=['POST'])
def storebooking():
   journeyID = validate_digit(request.form.get('journeyID'))
   seats = request.form.get('seats')
   if not seats.isdigit() or int(seats) < 1 or int(seats) > 8:
      seats = validate_passengers(seats)
   seattype = validate_seattype(request.form.get('seattype'))
   journeydate = request.form.get('journeydate')
   session['ActiveBooking'] = [journeyID, seats, seattype, journeydate]

   if not journeydate or not seattype or not journeydate:
      return redirect(url_for('journeys'))

   session['next'] = url_for('bookticket')
   return redirect(url_for('bookticket'))

@app.route('/HorizonTravels/journeys/bookticket', methods=['POST', 'GET'])
@login_required
@active_booking
def bookticket():
   journeyID, seats, seattype, journeydate = session.get('ActiveBooking')

   journeydate = validate_date(journeydate)
   bookingdate = datetime.now()
   weekday = journeydate.weekday()

   cards = getCardInfo(session.get('UserID'))
   cards = [list(card) + [isExpiredCard(card[0])] for card in cards]

   journeyData = selectjourney(journeyID, journeydate)[0]
   
   standardprice = journeyData[6] // 100
   earlyBookingDiscount = getDiscountMultiplier(bookingdate, journeydate)
   ticketPrice = int(standardprice * earlyBookingDiscount * (1 if seattype == 'Standard' else 2))
   datestring = createDateString(getWeekday(weekday), journeydate, bookingdate)

   journey = {
               "CompanyID" : journeyData[0],
               "Origin" : journeyData[1],
               "DepartureTime" : '%02d:%02d' % (journeyData[2].seconds // 3600, (journeyData[2].seconds % 3600) // 60), # Extract HH:MM from HH:MM:SS for departure time
               "Destination" : journeyData[3],
               "ArrivalTime" : '%02d:%02d' % (journeyData[4].seconds // 3600, (journeyData[4].seconds % 3600) // 60), # Extract HH:MM from HH:MM:SS for arrival time
               "JourneyDuration" : formattime(journeyData[5].seconds, True),
               "TicketPrice" : ticketPrice,
               "TotalPrice" : int(ticketPrice) * int(seats),
               "SeatsLeft": areSeatsLeft(seattype, seats, journeyData[7], journeyData[8]),
               "HasDeparted" : checkIfDeparted(journeydate, bookingdate, journeyData[2]),
               "JourneyDate" : request.form.get('journeydate'),
               "JourneyID" : journeyID
            }
   
   return render_template('BookJourney.html', journey=journey, dateStr=datestring, passengers=seats, seattype=seattype, cards=cards, dataerror=request.args.get('dataerror', default=False, type=bool))

@app.route('/HorizonTravels/journeys/bookticket/changeseat')
@login_required
@active_booking
def changeSeatType():
    if session['ActiveBooking'][2] == 'Standard':
        session['ActiveBooking'][2] = 'First class'
    else:
        session['ActiveBooking'][2] = 'Standard'

    session.modified = True
    return redirect(url_for('bookticket'))

@app.route('/HorizonTravels/journeys/bookticket/confirm', methods=['POST'])
@login_required
@active_booking
def finalisebooking():
   userID = session.get('UserID')
   journeyID, seats, seattype, journeydate = session.get('ActiveBooking')
   journeydate = validate_date(journeydate)
   journeyData = selectjourney(journeyID, journeydate)[0]
   bookingdate = datetime.today()

   if checkIfDeparted(journeydate, bookingdate, journeyData[2]):
      return render_template('FinaliseBookingError.html', Message='This journey has already departed.')
   if not areSeatsLeft(seattype, seats, journeyData[7], journeyData[8]):
      return render_template('FinaliseBookingError.html', Message='There are no seats remaining for this journey.')

   if (request.form.get('carddetailsmethod') == 'cardid'):
      cardID = request.form.get('card')
      if not userOwnsCard(cardID, userID):
         return redirect(url_for('bookticket', dataerror=True))
   elif (request.form.get('carddetailsmethod') == 'newcard'):
      fullName = sanitizeFullName(request.form.get('name'))
      cardnumber = request.form.get('card-number')
      expdate = request.form.get('exp-date')
      cvv = request.form.get('cvv')

      if len(fullName) > 0 and testCardNumber(cardnumber) and testExpDate(expdate) and testCVV(cvv):
         if (request.form.get('remembercard')):
            cardID = insertNewCard(userID, cardnumber, expdate, cvv, fullName)
         else:
            cardID = insertNewCardNoUser(cardnumber, expdate, cvv, fullName)
      else:
         return redirect(url_for('bookticket', dataerror=True))
   else:
      return redirect(url_for('bookticket', dataerror=True))
   
   standardSeats = seats if seattype == 'Standard' else 0
   firstclassSeats = seats if seattype != 'Standard' else 0
   standardprice = journeyData[6] // 100
   earlyBookingDiscount = getDiscountMultiplier(bookingdate, journeydate)
   ticketPrice = int(standardprice * earlyBookingDiscount * (1 if seattype == 'Standard' else 2))
   bookingID = insertNewBooking(userID, cardID, journeyID, standardSeats, firstclassSeats, ticketPrice, bookingdate, journeydate)
   bookingRef = generateBookingRef(journeyData[0], bookingID, journeyData[1], journeyData[3])
   addBookingRef(bookingID, bookingRef)

   time = '%02d:%02d' % (journeyData[2].seconds // 3600, (journeyData[2].seconds % 3600) // 60)
   date = journeydate.strftime("%d/%m/%Y")
   session.pop('ActiveBooking')
   if 'next' in session:
      session.pop('next')
   return render_template('FinaliseBooking.html', origin=journeyData[1], destination=journeyData[3], time=time, 
                          date=date, seats=seats, seattype=seattype, bookingRef=bookingRef, bookingID=bookingID)

@app.route('/HorizonTravels/destinations')
def destinations():
   return render_template('Destinations.html')

@app.route('/HorizonTravels/account')
@login_required
def account():
   accountdata = selectcolumns('users', ['First_Name', 'Last_Name', 'email', 'RegDate'], 'UserID', session['UserID'])
   regDateStr = ''
   if accountdata[0][3]:
      regDateStr = accountdata[0][3].strftime("%d/%m/%Y")
   
   paymentcards = getCardInfo(session.get('UserID'), True)
   paymentcards = [list(card) + [isExpiredCard(card[0])] for card in paymentcards]

   return render_template('Account.html', username=accountdata[0][0], lastname=accountdata[0][1], email=accountdata[0][2], 
                          regDate=regDateStr, usertype=session['usertype'], cards=paymentcards)

@app.route('/HorizonTravels/account/deletecard/<int:cardID>')
@login_required
def deletecard(cardID):
   if userOwnsCard(cardID, session.get('UserID')):
      deleteValue('cardinfo', 'CardID', cardID, 'UserID')
   return redirect(url_for('account'))

@app.route('/admindeletecard/<int:cardID>', methods=['DELETE'])
@login_required
@admin_required
def admindeletecard(cardID):
    try:
        deleteValue('cardinfo', 'CardID', cardID, 'UserID')
        return "", 200  # Return a successful status code
    except Exception as e:
        print(f"Error while deleting card: {e}")
        return "", 500  # Return an error status code

@app.route('/admindeletebooking/<int:bookingID>', methods=['DELETE'])
@login_required
@admin_required
def admindeletebooking(bookingID):
    try:
        deleteValue('bookings', 'BookingID', bookingID, 'UserID')
        return "", 200  # Return a successful status code
    except Exception as e:
        print(f"Error while deleting booking: {e}")
        return "", 500  # Return an error status code

@app.route('/admindeletejourney/<int:journeyID>', methods=['DELETE'])
@login_required
@admin_required
def admindeletejourney(journeyID):
    try:
        deleteRecord('bookings', 'JourneyID', journeyID)
        deleteRecord('journeys', 'JourneyID', journeyID)
        return "", 200  # Return a successful status code
    except Exception as e:
        print(f"Error while deleting booking: {e}")
        return "", 500  # Return an error status code

@app.route('/HorizonTravels/account/managebookings')
@login_required
def managebookings():
   journeydata = selectusersjourneys(session.get('UserID')) # filter by week day

   journeys = []
   for j in journeydata:
      currentTime = datetime.today()
      bookingdate = j[10]
      journeydate = datetime.combine(j[11], datetime.min.time())
      hasDeparted = checkIfDeparted(journeydate, currentTime, j[3])
      seatsBooked = j[8] + j[9]
      seattype = 'standard' if j[8] > 0 else 'first class'

      daysUntilJourney = (journeydate.date() - currentTime.date()).days
      daysUntilJourneyStr = makeDaysUntilJourneyStr(daysUntilJourney)

      journeys.append({
         "BookingID" : j[0],
         "CompanyID" : j[1],
         "Origin" : j[2],
         "DepartureTime" : '%02d:%02d' % (j[3].seconds // 3600, (j[3].seconds % 3600) // 60), # Extract HH:MM from HH:MM:SS for departure time
         "Destination" : j[4], # Extract HH:MM from HH:MM:SS for journey time
         "ArrivalTime" : '%02d:%02d' % (j[5].seconds // 3600, (j[5].seconds % 3600) // 60), # Extract HH:MM from HH:MM:SS for arrival time
         "JourneyDuration" : formattime(j[6].seconds),
         "PricePaid" : "{:,}".format(j[7] * seatsBooked),
         "SeatType" : seattype,
         "SeatsBooked" : seatsBooked,
         "HasDeparted" : hasDeparted,
         "Cancelled" : True if j[13] == 1 else False,
         "BookingDate" : f'{bookingdate.date().strftime("%d/%m/%Y")} at {bookingdate.time().strftime("%H:%M")}',
         "JourneyDate" : journeydate.date().strftime("%d/%m/%Y"),
         "DaysUntilJourney" : daysUntilJourneyStr,
         "BookingRef" : j[12]
      })
   
   errormsg = request.args.get('error', 'false')
   frompage = request.args.get('frompage', 'upcoming')
   return render_template('ManageBookings.html', journeys=journeys, error=errormsg, frompage=frompage)

@app.route('/HorizonTravels/account/managebookings/remove/<int:bookingID>/<string:frompage>')
@login_required
def removebooking(bookingID, frompage):
   if not userOwnsBooking(bookingID, session.get('UserID')):
      return redirect(url_for('managebookings', error='true', frompage=frompage))
   times = selectbookingtimes(bookingID)[0]
   if not checkIfDeparted(times[1], datetime.today(), times[0]) and times[2] != 1:
      return redirect(url_for('cancelbooking'))
   
   deleteValue('bookings', 'BookingID', bookingID, 'UserID')
   return redirect(url_for('managebookings', frompage=frompage))

@app.route('/HorizonTravels/account/managebookings/cancel/<int:bookingID>')
@login_required
def cancelbooking(bookingID):
   if not userOwnsBooking(bookingID, session.get('UserID')):
      return redirect(url_for('managebookings', error='true'))
   times = selectbookingtimes(bookingID)[0]
   if checkIfDeparted(times[1], datetime.today(), times[0]) or times[2] == 1:
      return redirect(url_for('managebookings', error='true'))
   
   bookingdata = selectbooking(bookingID)
   seatsBooked = bookingdata[4] + bookingdata[5]
   seattype = 'standard' if bookingdata[4] > 0 else 'first class'

   daysToJourney = (bookingdata[7] - datetime.today().date()).days
   if daysToJourney > 60:
      bookingChargePercentage = 0
   elif 30 <= daysToJourney <= 60:
      bookingChargePercentage = 40  # 40% charge
   else:
      bookingChargePercentage = 100  # 100% charge within 30 days

   pricePaid = bookingdata[3] * seatsBooked
   totalRefund = pricePaid * (1 - bookingChargePercentage / 100)

   journey = {
      "Origin": bookingdata[0],
      "DepartureTime": '%02d:%02d' % (bookingdata[1].seconds // 3600, (bookingdata[1].seconds % 3600) // 60),
      "Destination": bookingdata[2],
      "PricePaidPerSeat": "{:,}".format(bookingdata[3]),
      "PricePaid": "{:,}".format(pricePaid),
      "SeatType": seattype,
      "SeatsBooked": seatsBooked,
      "BookingDate": f'{bookingdata[6].date().strftime("%d/%m/%Y")} at {bookingdata[6].time().strftime("%H:%M")}',
      "JourneyDate": bookingdata[7].strftime("%d/%m/%Y"),
      "BookingRef": bookingdata[8],
      "BookingChargePercentage": bookingChargePercentage,
      "TotalRefund": f"{int(totalRefund):,}"
   }

   return render_template('ConfirmCancelation.html', journey=journey, bookingID=bookingID)

@app.route('/HorizonTravels/account/managebookings/cancel/confirm/<int:bookingID>')
@login_required
def confirmcancelation(bookingID):
   if not userOwnsBooking(bookingID, session.get('UserID')):
      return redirect(url_for('managebookings', error='true'))
   times = selectbookingtimes(bookingID)[0]
   if checkIfDeparted(times[1], datetime.today(), times[0]) or times[2] == 1:
      return redirect(url_for('managebookings', error='true'))
   
   updateValue('bookings', 'BookingID', bookingID, 'Cancelled', '1')

   bookingdata = selectbooking(bookingID)
   daysToJourney = (bookingdata[7] - datetime.today().date()).days
   if daysToJourney > 60:
      bookingChargePercentage = 0
   elif 30 <= daysToJourney <= 60:
      bookingChargePercentage = 40  # 40% charge
   else:
      bookingChargePercentage = 100  # 100% charge within 30 days
   pricePaid = bookingdata[3]
   totalRefund = pricePaid * (1 - bookingChargePercentage / 100)
   updateValue('bookings', 'BookingID', bookingID, 'RefundAmount', totalRefund)

   return redirect(url_for('managebookings'))

@app.route('/HorizonTravels/account/adminpanel')
@login_required
@admin_required
def adminpanel():
   return render_template('AdminPanel.html')

@app.route ('/ajax_users/', methods = ['POST', 'GET'])
@login_required
@admin_required
def ajax_users():    
   if request.method == 'GET':
      q = request.args.get('q')
      a = selectusersnames()

      hint = []
      if q == '*':
         hint = a
      elif q is not None:
         q = str.lower(q)
         length = len(q)
         for name in a:
            fnamelower = name[1].lower()
            lnamelower = name[2].lower()
            emaillower = name[3].lower()
            if q in fnamelower[0:length]:
               hint.append(name)
            elif q in lnamelower[0:length]:
               hint.append(name)
            elif q in emaillower[0:length]:
               hint.append(name)
      
      if len(hint) < 1:
            output = {"suggestions": "no suggestion"}
      else:
         output = [
                {"userid": name[0], 
                 "userstr": f"First name: {name[1] or 'None'}, Last name: {name[2] or 'None'}, Email: {name[3] or 'None'}"}
                for name in hint
            ]

      return jsonify(output)
@app.route ('/getuserinfo/', methods = ['POST', 'GET'])
@login_required
@admin_required
def getuserinfo():
   if request.method == 'GET':
      userid = request.args.get('id')

      # Fetch user details from the database using `selectcolumns` method
      userdetails = selectcolumns('users', ['First_Name', 'Last_Name', 'email', 'RegDate', 'RegTime', 'UserType'], 'UserID', userid)[0]
      paymentcards = getCardInfo(userid, True, False)
      paymentcards = [list(card) + [isExpiredCard(card[0])] for card in paymentcards]
      bookings = selectuserjourneysmin(userid)
      bookings = [list(booking) + [checkIfDeparted(booking[4], datetime.today(), booking[5])] for booking in bookings]
      for booking in bookings:
         booking[4] = booking[4].strftime("%Y-%m-%d") if booking[4] else ""
         booking[5] = '%02d:%02d' % (booking[5].seconds // 3600, (booking[5].seconds % 3600) // 60) if booking[5] else ""
         booking[6] = booking[6].strftime("%Y-%m-%d %H:%M:%S") if booking[6] else ""

         seatsBooked = booking[8] + booking[9]
         seattype = 'standard' if booking[8] > 0 else 'first class'
         booking[8] = seatsBooked
         booking[9] = seattype

      if userdetails is not None:
         userinfo = {
            "FirstName": userdetails[0],
            "LastName": userdetails[1],
            "Email": userdetails[2],
            "RegDate": userdetails[3].strftime("%Y-%m-%d") if userdetails[3] else "",
            "RegTime": '%d:%d:%d' % (userdetails[4].seconds // 3600, (userdetails[4].seconds % 3600) // 60, userdetails[4].seconds % 60) if userdetails[4] else "",
            "UserType": userdetails[5],
            "Cards" : paymentcards,
            "Bookings" : bookings
         }
         return jsonify(userinfo)

      # Return an empty dictionary if no user details are found
      return jsonify({})
@app.route ('/updateuserinfo/', methods = ['POST', 'GET'])
@login_required
@admin_required
def updateuserinfo():
   data = request.get_json()
   userid = request.args.get('id')

   column_map = {
    'fname': 'First_Name',
    'lname': 'Last_Name',
    'email': 'Email',
    'password': 'Password',
    'rdate': 'RegDate',
    'rtime': 'RegTime',
    'usertype': 'UserType'}
   filtered_data = {column_map[key]: value for key, value in data.items()}

   if 'Password' in filtered_data and filtered_data['Password']:
      filtered_data['Password'] = sha256_crypt.hash((str(filtered_data['Password'])))

   result = updaterow('users', 'UserID', userid, filtered_data)
   # Check if the result is an instance of Exception
   if isinstance(result, Exception):
      print(f"An error occurred: {result}")
      return False  # Handle the error by returning False
   else:
      return 'Complete'
@app.route ('/updateuserbooking/', methods = ['POST', 'GET'])
@login_required
@admin_required
def updateuserbooking():
   data = request.get_json()
   bookingid = request.args.get('id')

   if 'Seats' in data and 'Seattype' in data:
      if data['Seattype'] == 'standard':  # Check if Seattype is 'standard'
         data['StandardSeats'] = data['Seats']  # Add StandardSeats key with value from Seats
         data['FirstClassSeats'] = '0'
      else:
         data['FirstClassSeats'] = data['Seats']  # Add StandardSeats key with value from Seats
         data['StandardSeats'] = '0'

      del data['Seats']
      del data['Seattype']

   if 'Cancelled' in data:
      data['Cancelled'] = '1' if data['Cancelled'] == 'true' else '0'


   result = updaterow('bookings', 'BookingID', bookingid, data)
   # Check if the result is an instance of Exception
   if isinstance(result, Exception):
      print(f"An error occurred: {result}")
      return False  # Handle the error by returning False
   else:
      return 'Complete'
@app.route ('/updatejourney/', methods = ['POST', 'GET'])
@login_required
@admin_required
def updatejourney():
   data = request.get_json()
   journeyid = request.args.get('id')

   if 'departuretime' in data:
      data['departuretime'] += ":00"  # Add seconds to the time
   if 'arrivaltime' in data:
      data['arrivaltime'] += ":00"  # Add seconds to the time
   if 'companyid' in data:
      data['companyid'] = '1' if data['companyid'] == 'UKAir' else '2'
   if 'price' in data:
      data['price'] = 100 * int(data['price'])

   result = updaterow('journeys', 'JourneyID', journeyid, data)
   # Check if the result is an instance of Exception
   if isinstance(result, Exception):
      print(f"An error occurred: {result}")
      return False  # Handle the error by returning False
   else:
      return 'Complete'
@app.route ('/getjourneys/', methods = ['POST', 'GET'])
@login_required
@admin_required
def getjourneys():
   if request.method == 'GET':
      journeys = selecttable('journeys')

      journeydata = []
      if journeys is not None:
         for journey in journeys:
            journey = {
               "journeyid": journey[0],
               "companyid": 'UKAir' if journey[1] == 1 else 'BritishTrains',
               "origin": journey[2],
               "departuretime": '%02d:%02d' % (journey[3].seconds // 3600, (journey[3].seconds % 3600) // 60) if journey[3] else "",
               "destination": journey[4],
               "arrivaltime": '%02d:%02d' % (journey[5].seconds // 3600, (journey[5].seconds % 3600) // 60) if journey[5] else "",
               "price" : journey[6] / 100
            }
            journeydata.append(journey)
         return jsonify(journeydata)

   return jsonify({})
@app.route("/addnewjourney/", methods=["POST"])
@login_required
@admin_required
def addnewjourney():
    data = request.get_json()

    # Validate data on the server side
    required_fields = ["companyid", "origin", "departuretime", "destination", "arrivaltime", "price"]
    for field in required_fields:
        if field not in data or not data[field]:
            return jsonify({"error": f"Missing field: {field}"}), 400
   
    data['companyid'] = '1' if data['companyid'] == 'UKAir' else '2'
    data['price'] = 100 * int(data['price'])

    try:
        result = insertNewJourney(data["companyid"], data["origin"], data["departuretime"], data["destination"], data["arrivaltime"], data["price"])
        if result:
            return jsonify({"success": "Journey added successfully."}), 200
        else:
            return jsonify({"error": "Failed to add journey to the database."}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def get_booking(booking_id):
   data = selectbookingfull(booking_id)
   seatsBooked = data[7] + data[8]
   seattype = 'standard' if data[7] > 0 else 'first class'

   return {
      "o_city": abbreviateCity(data[0]),
      "travel_method": 'Flight' if data[4] == 1 else 'Train',
      "d_city": abbreviateCity(data[2]),
      "customer_name": data[12] + " " + data[13],
      "seats": seatsBooked,
      "seat_type": seattype,
      "origin": data[0], 
      "destination": data[2],
      "journey_date": data[10].strftime("%d/%m/%Y"),
      "booking_date": data[9].strftime("%d/%m/%Y %H:%M"),
      "departure_time": '%02d:%02d' % (data[1].seconds // 3600, (data[1].seconds % 3600) // 60),
      "arrival_time": '%02d:%02d' % (data[3].seconds // 3600, (data[3].seconds % 3600) // 60),
      "journey_duration": formattime(data[6].seconds),
      "company": 'UkAir' if data[4] == 1 else 'BritishTrains',
      "price_paid": data[5] * seatsBooked,
      "price_paid_per_ticket": data[5],
      "booking_ref": data[11]
   }
@app.route('/download_receipt/<booking_id>')
@login_required
def download_receipt(booking_id):
    if not userOwnsBooking(booking_id, session.get('UserID')):
      return redirect(url_for('managebookings'))

    booking = get_booking(booking_id)
    rendered_html = render_template('BookingReceipt.html', booking=booking)
    
    pdf = weasyprint.HTML(string=rendered_html).write_pdf()
    
    response = make_response(pdf)
    response.headers['Content-Type'] = 'application/pdf'
    filename = booking.get('booking_ref') or f"HT-{booking_id}"
    response.headers['Content-Disposition'] = f'attachment; filename="{filename}_ticket.pdf"'
    return response

@app.route('/getjourneysales/')
@login_required
@admin_required
def getjourneysales():
   sales_type = request.args.get('salesType', 'alltime')
   data = fetchjourneysalesdata(sales_type)
   array = np.array(data).T
   graphdata = []

   array[0] = [str(a) + '.' for a in array[0]]
   array[1] = ['Plane:' if a == 1 else 'Train:' for a in array[1]]
   array[2] = [f"{int(a.total_seconds() // 3600):02}:{int((a.total_seconds() % 3600) // 60):02}" for a in array[2]]
   array[3] = ['| ' +abbreviateCity(a) for a in array[3]]
   array[4] = ['to ' + abbreviateCity(a) for a in array[4]]
   combined_strings = [" ".join(str(array[row][col]) for row in range(5)) for col in range(len(array[0]))]
   graphdata.append(combined_strings)

   graphdata.append(array[5].astype(int).tolist())  # Standard seats
   graphdata.append(array[6].astype(int).tolist())  # First class seats
   graphdata.append(array[7].astype(int).tolist())  # Cancelled seats

   return jsonify(graphdata)
@app.route('/getjourneyrevenue/')
@login_required
@admin_required
def getjourneyrevenue():
   sales_type = request.args.get('salesType', 'alltime')
   data = fetchjourneyrevenuedata(sales_type)
   array = np.array(data).T
   graphdata = []

   array[0] = [str(a) + '.' for a in array[0]]
   array[1] = ['Plane:' if a == 1 else 'Train:' for a in array[1]]
   array[2] = [f"{int(a.total_seconds() // 3600):02}:{int((a.total_seconds() % 3600) // 60):02}" for a in array[2]]
   array[3] = ['| ' +abbreviateCity(a) for a in array[3]]
   array[4] = ['to ' + abbreviateCity(a) for a in array[4]]
   combined_strings = [" ".join(str(array[row][col]) for row in range(5)) for col in range(len(array[0]))]
   graphdata.append(combined_strings)

   graphdata.append(array[5].astype(int).tolist())
   graphdata.append(array[6].astype(int).tolist())

   return jsonify(graphdata)
@app.route('/getsinglejourneysales/')
@login_required
@admin_required
def getsinglejourneysales():
   journey1id = request.args.get('journey1ID')
   journey2id = request.args.get('journey2ID')

   settingJ2 = False
   if not journey1id and journey2id:
      journey1id = journey2id
      journey2id = None
      settingJ2 = True

   if not journey2id:
      data = fetchsinglejourneyrevenuedata(journey1id)
      today = datetime.today().date()
      x, y = get_dates_and_values(data[1], today)

      min_day = min(x[0], today)
      max_day = max(x[-1], today)
      if (min_day == max_day):
         min_day -= timedelta(days=1)
      number_of_days = (max_day - min_day + timedelta(days=1)).days

      union_dates_index = [i for i in range(number_of_days)]
      union_dates = [min_day + timedelta(days=i) for i in range(number_of_days)]
      union_labels = [("Today" if d == today else d.strftime("%d/%m/%y")) for d in union_dates]
      series = build_series(union_dates_index, x, y, min_day)
      title = get_title(data[0])

      final_graph_data = {
         "labels": union_labels,
         "datasets": [
            {
                  "label": title,
                  "data": series,
                  "borderColor": "green" if settingJ2 else "blue",
                  "fill": False,
                  "borderWidth": 2,
                  "tension": 0,
                  "spanGaps": True,
            }
         ]
      }
   elif journey1id and journey2id:
      data1 = fetchsinglejourneyrevenuedata(journey1id)
      data2 = fetchsinglejourneyrevenuedata(journey2id)

      today = datetime.today().date()

      dates1, revs1 = get_dates_and_values(data1[1], today)
      dates2, revs2 = get_dates_and_values(data2[1], today)

      min_day = min(dates1[0], dates2[0])
      max_day = max(dates1[-1], dates2[-1])
      if min_day == max_day:
         min_day -= timedelta(days=1)
      number_of_days = (max_day - min_day + timedelta(days=1)).days

      union_dates_index = [i for i in range(number_of_days)]
      union_dates = [min_day + timedelta(days=i) for i in range(number_of_days)]
      union_labels = [("Today" if d == today else d.strftime("%d/%m/%y")) for d in union_dates]
      series1 = build_series(union_dates_index, dates1, revs1, min_day)
      series2 = build_series(union_dates_index, dates2, revs2, min_day)
      title1 = get_title(data1[0])
      title2 = get_title(data2[0])

      final_graph_data = {
         "labels": union_labels,
         "datasets": [
            {
                  "label": title1,
                  "data": series1,
                  "borderColor": "blue",
                  "fill": False,
                  "borderWidth": 2,
                  "tension": 0,
                  "spanGaps": True,
            },
            {
                  "label": title2,
                  "data": series2,
                  "borderColor": "red",
                  "fill": False,
                  "borderWidth": 2,
                  "tension": 0,
                  "spanGaps": True,
            }
         ]
      }
   else:
      return
   # Return as JSON
   return jsonify(final_graph_data)

def get_title(data):
    if data:
        title = list(data[0])
        title[0] = 'Journey:' + str(title[0])
        title[1] = '- Plane at' if title[1] == 1 else '- Train at'
        title[2] = f"{int(title[2].total_seconds() // 3600):02}:{int((title[2].total_seconds() % 3600) // 60):02}"
        title[3] = '| ' + abbreviateCity(title[3])
        title[4] = 'to ' + abbreviateCity(title[4])
        return ' '.join(str(item) for item in title)
    else:
        return 'None'
def get_dates_and_values(data, default_date):
    arr = np.array(data).T
    if arr.size == 0:
        arr = np.array([[default_date], [0]])
    return arr[0], arr[1]
def build_series(union_dates, dataset_dates, dataset_values, min_day):
    # Convert dataset_dates to a list for easier lookup.
    dates_list = list(dataset_dates)
    values_list = list(dataset_values)
    series = []
    for d in union_dates:
        try:
            # If the date is in the dataset dates, return its value
            idx = dates_list.index(min_day + timedelta(days=d))
            series.append(values_list[idx])
        except ValueError:
            series.append(0)
    return series

@app.route ('/gettopcustomers/', methods = ['POST', 'GET'])
@login_required
@admin_required
def gettopcustomers():
   # Fetch user details from the database using `selectcolumns` method
   topCustomers = selectTopCustomers()

   if topCustomers is not None:
      return jsonify(topCustomers)

   # Return an empty dictionary if no user details are found
   return jsonify({})

@app.route('/getcompanydata/', methods=['GET'])
@login_required
@admin_required
def get_company_data():
    """
    Returns company data in the following format (as a JSON array):
    0: List of company names.
    1: List of total revenues.
    2: List of total seats booked.
    3: List of first class seats.
    4: List of total seats cancelled.
    5: List of journeys running.
    6: List of cities in network.
    7: List of days in service.
    """
    bookingData = selectCompanyBookingData()
    journeyData = selectCompanyJourneyData()

    company_names = ["UkAir", "BritishTrains"]
    total_revenues = [bookingData[0][0], bookingData[1][0]]
    total_seats_booked = [bookingData[0][1], bookingData[1][1]]
    first_class_seats = [bookingData[0][2], bookingData[1][2]]
    cancelled_seats = [bookingData[0][3], bookingData[1][3]]
    journeys_running = [journeyData[0][0], journeyData[1][0]]
    cities_in_network = [journeyData[0][1], journeyData[1][1]]
    days_in_service = ["Mon, Tue, Wed, Thu, Fri", "Mon, Tue, Wed, Thu, Fri, Sat, Sun"]

    # Combine the values into a single array.
    data = [
        company_names,
        total_revenues,
        total_seats_booked,
        first_class_seats,
        cancelled_seats,
        journeys_running,
        cities_in_network,
        days_in_service,
    ]

    return jsonify(data)

@app.route("/booking-info", methods=["GET"])
@login_required
@admin_required
def booking_info():
    # Fetch data from the database using your helper function
    data = selectBookingInfo()
    currentDate = datetime.today()
    
    bookingInfo = []
    currentJourneyDate = None
    for d in data:
       if currentJourneyDate != d[4]:
          journeydate = d[4]
          weekday = journeydate.weekday()
          b = [False, createDateStringDate(getWeekday(weekday), journeydate, datetime.now())]
          currentJourneyDate = d[4]
          bookingInfo.append(b)

       b = [
         True,
         abbreviateCity(d[0]),
         abbreviateCity(d[2]),
         " at %s on %s" % ('%02d:%02d' % (d[1].seconds // 3600, (d[1].seconds % 3600) // 60),
            d[4].strftime("%d/%m/%y")),
         makeDaysUntilJourneyStr((d[4] - currentDate.date()).days),
         "%s journey, arrives at %s" % (timeStr(d[5].seconds), '%02d:%02d' % (d[3].seconds // 3600, (d[3].seconds % 3600) // 60)),
         d[6], d[7],
         d[8], d[9],
         d[10],
         d[11],
         f"{d[12]:,}"
       ]
       bookingInfo.append(b)

    return jsonify(bookingInfo)

if __name__ == '__main__':
    for i in range(13000, 18000):
      try:
         app.run(debug = False, port = i)
         break
      except OSError as e:
         print("Port {i} not available".format(i))