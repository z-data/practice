
"""
Columbia's COMS W4111.001 Introduction to Databases
Example Webserver
To run locally:
    python server.py
Go to http://localhost:8111 in your browser.
A debugger such as "pdb" may be helpful for debugging.
Read about it online.
"""
import os
  # accessible as a variable in index.html:
from sqlalchemy import *
from sqlalchemy.pool import NullPool
from flask import Flask, request, render_template, g, redirect, Response

tmpl_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
app = Flask(__name__, template_folder=tmpl_dir)


#connecting to our database on the remote server
DATABASEURI = "postgresql://rrp2131:8767@34.75.150.200/proj1part2" 


#
# This line creates a database engine that knows how to connect to the URI above.
#
engine = create_engine(DATABASEURI)





@app.before_request
def before_request():
  """
  This function is run at the beginning of every web request 
  (every time you enter an address in the web browser).
  We use it to setup a database connection that can be used throughout the request.

  The variable g is globally accessible.
  """
  try:
    g.conn = engine.connect()
  except:
    print("uh oh, problem connecting to database")
    import traceback; traceback.print_exc()
    g.conn = None

@app.teardown_request
def teardown_request(exception):
  """
  At the end of the web request, this makes sure to close the database connection.
  If you don't, the database could run out of memory!
  """
  try:
    g.conn.close()
  except Exception as e:
    pass


#
# @app.route is a decorator around index() that means:
#   run index() whenever the user tries to access the "/" path using a GET request
#
# If you wanted the user to go to, for example, localhost:8111/foobar/ with POST or GET then you could use:
#
#       @app.route("/foobar/", methods=["POST", "GET"])
#
# PROTIP: (the trailing / in the path is important)
# 
# see for routing: http://flask.pocoo.org/docs/0.10/quickstart/#routing
# see for decorators: http://simeonfranklin.com/blog/2012/jul/1/python-decorators-in-12-steps/
#
@app.route('/')
def index():
 
  return render_template("index.html")


## OUR NAVIGATION FUNCTIONS
@app.route('/region')
def region():
  return render_template("region.html")

#State Route
@app.route('/state')
def state():
  return render_template("state.html")

#Military Route
@app.route('/military')
def military():
  return render_template("military.html")

#Methods Route
@app.route('/methods')
def methods():
  return render_template("methods.html")



#SUBMIT NATIONAL
@app.route('/submitnational', methods=['POST'])
def submitnational():
    
    #get years from user inputs
    year1 = request.form['year1']
    year2 = request.form['year2']
    
    #ensures we get between the year options
    if year1 > year2:
                temp = year1
                year1 = year2
                year2 = temp
    
    #get selection options
    showciv = request.form.get('showciv')
    showvet = request.form.get('showvet')
    showmil = request.form.get('showmil')

     #creating an empty array for headings, need to change it for each query
    headings = []
            
    if showciv == 'on':
        if showvet == 'on':
            if showmil == 'on':
                #selects the annual information for civ, mil, vet by year              
                cursor = g.conn.execute('''SELECT DISTINCT S.year, S.tperson, S.count, S.rate, S.male, S.female
                                        FROM Suicides S
                                        WHERE s.sid LIKE '%%na%%' 
                                        AND S.year >= (%s) 
                                        AND S.year <= (%s)
                                        
                                        OR s.sid LIKE '%%all%%'
                                        AND S.year >= (%s) 
                                        AND S.year <= (%s)
                                        
                                        ORDER BY S.year DESC
                                        ''', year1,year2,year1,year2)
            elif showmil != 'on':
                #selects the annual information for civ, vet by year              
                cursor = g.conn.execute('''SELECT DISTINCT S.year, S.tperson, S.count, S.rate, S.male, S.female
                                        FROM Suicides S
                                        WHERE s.sid LIKE '%%na%%' 
                                        AND S.year >= (%s) 
                                        AND S.year <= (%s)
                                        
                                        ORDER BY S.year DESC
                                        ''', year1,year2)
                                        
        if showvet != 'on':
            if showmil == 'on':
                #selects the annual information for civ, milby year              
                cursor = g.conn.execute('''SELECT DISTINCT S.year, S.tperson, S.count, S.rate, S.male, S.female
                                        FROM Suicides S
                                        WHERE s.sid LIKE 'c%%na%%' 
                                        AND S.year >= (%s) 
                                        AND S.year <= (%s)
                                        
                                        OR s.sid LIKE '%%all%%'
                                        AND S.year >= (%s) 
                                        AND S.year <= (%s)
                                        
                                        ORDER BY S.year DESC
                                        ''', year1,year2,year1,year2)
            elif showmil != 'on':
                #selects the annual information for civ by year              
                cursor = g.conn.execute('''SELECT DISTINCT S.year, S.tperson, S.count, S.rate, S.male, S.female
                                        FROM Suicides S
                                        WHERE s.sid LIKE 'c%%na%%' 
                                        AND S.year >= (%s) 
                                        AND S.year <= (%s)
                                        
                                        ORDER BY S.year DESC
                                        ''', year1,year2)
    if showciv != 'on':
        if showvet == 'on':
            if showmil == 'on':
                #selects the annual information for  mil, vet by year              
                cursor = g.conn.execute('''SELECT DISTINCT S.year, S.tperson, S.count, S.rate, S.male, S.female
                                        FROM Suicides S
                                        WHERE s.sid LIKE 'v%%na%%' 
                                        AND S.year >= (%s) 
                                        AND S.year <= (%s)
                                        
                                        OR s.sid LIKE '%%all%%'
                                        AND S.year >= (%s) 
                                        AND S.year <= (%s)
                                        
                                        ORDER BY S.year DESC
                                        ''', year1,year2,year1,year2)
            elif showmil != 'on':
                #selects the annual information for vet by year              
                cursor = g.conn.execute('''SELECT DISTINCT S.year, S.tperson, S.count, S.rate, S.male, S.female
                                        FROM Suicides S
                                        WHERE s.sid LIKE 'v%%na%%' 
                                        AND S.year >= (%s) 
                                        AND S.year <= (%s)
                                        
                                        ORDER BY S.year DESC
                                        ''', year1,year2)
                                        
        if showvet != 'on':
            if showmil == 'on':
                #selects the annual information for mil by year              
                cursor = g.conn.execute('''SELECT DISTINCT S.year, S.tperson, S.count, S.rate, S.male, S.female
                                        FROM Suicides S
                                        WHERE s.sid LIKE '%%all%%'
                                        AND S.year >= (%s) 
                                        AND S.year <= (%s)
                                        
                                        ORDER BY S.year DESC
                                        ''', year1,year2)
            elif showmil != 'on':
                error = 'Please make at least one selection'
                return render_template("index.html", error=error)
                        
                            
    suicides = []
    for result in cursor:
        print(result)  
        suicides.append(result) 
    cursor.close()
    
    headings = ["Year", "Group", "Total Count", "Rate per 100,000", 
                "Male Deaths", "Female Deaths"]
    context = dict(national = suicides)
    return render_template("index.html", headings=headings, **context)




##SUBMIT REGION
@app.route('/submitregion', methods=['POST'])
def submitregion():
    year1 = request.form['year1']
    year2 = request.form['year2']
    reg1 = request.form['region1']
    reg2 = request.form['region2']
    
    #making sure year is in the right order
    if year1 > year2:
        temp = year1
        year1 = year2
        year2 = temp
    
    #creating a dict for transforming to correct input
    reg = {'S':'southern', 'W':'western', 'NER':'northeastern', 'MW':'midwestern'}
    #creating a list to return the proper query
    r = []
    
    #for one of the regions being ALL
    if (reg1 == 'ALL' or reg2 == 'ALL'):
        if reg1 == 'ALL':
            
            
    
            cursor2 = g.conn.execute('''SELECT S.year, P.rname, S.tperson, SUM(S.count)
                            FROM Lived_In L, Suicides S, Part_Of P
                            WHERE L.sid = S.sid AND S.year >= (%s) AND S.year <= (%s)
                            AND P.sname = L.sname
                            GROUP BY P.rname, S.year, S.tperson
                            ''', year1,year2)
            for result in cursor2:
                print(result)  
                r.append(result) 
            cursor2.close()

        else:
            cursor1 = g.conn.execute('''SELECT S.year, S.tperson, S.count
                            FROM Suicides S
                            WHERE year >= (%s) AND year <= (%s) 
                            AND S.sid NOT IN (SELECT L.sid
                            FROM Lived_In L)''' ,year1,year2)
            
            for result in cursor1:
                print(result)  
                r.append(result) 
            cursor1.close()
    
            cursor2 = g.conn.execute('''SELECT S.year, P.rname, S.tperson, SUM(S.count)
                            FROM Lived_In L, Suicides S, Part_Of P
                            WHERE L.sid = S.sid AND S.year >= (%s) AND S.year <= (%s)
                            AND P.rname = (%s) AND P.sname = L.sname
                            GROUP BY P.rname, S.year, S.tperson
                            ''', year1,year2,reg[reg1])
            
            for result in cursor2:
                print(result)  
                r.append(result) 
            cursor2.close()
   
    #looking at 2 different regions
    else:
    
        cursor1 = g.conn.execute('''SELECT S.year, P.rname, S.tperson, SUM(S.count)
                                FROM Lived_In L, Suicides S, Part_Of P
                                WHERE L.sid = S.sid AND S.year >= (%s) AND S.year <= (%s)
                                AND P.rname = (%s) AND P.sname = L.sname                               
                                GROUP BY P.rname, S.year, S.tperson
                                ORDER BY (S.year)::INTEGER DESC
                                ''', year1,year2,reg[reg1])
    
        for result in cursor1:
            print(result)  
            r.append(result) 
        cursor1.close()
        
        
        cursor2 = g.conn.execute('''SELECT S.year, P.rname, S.tperson, SUM(S.count)
                                FROM Lived_In L, Suicides S, Part_Of P                               
                                WHERE L.sid = S.sid AND S.year >= (%s) AND S.year <= (%s)
                                AND P.rname = (%s) AND P.sname = L.sname                                
                                GROUP BY P.rname, S.year, S.tperson
                                ORDER BY (S.year)::INTEGER DESC
                                ''', year1,year2,reg[reg2])
        
        for result in cursor2:
            print(result)  
            r.append(result) 
        cursor2.close()
        headings = ["Year", "Region", "Type of Person", "Total Count" ]
    context = dict(region = r)
    headings = ["Year", "Region", "Type of Person", "Total Count" ]   
    return render_template('region.html', headings=headings, **context)





#SUBMIT STATE
@app.route('/submitstate', methods=['POST'])
def submitestate():
    
    states = {'allstates':'All','AL':'Alabama', 'AK': 'Alaska', 'AZ': 'Arizona', 'AR':'Arkansas', 'CA':'California',
          'CO':'Colorado', 'CT':'Connecticut', 'DE':'Deleware', 'DC':'District of Columbia',
          'FL':'Florida', 'GA':'Georgia', 'HI':'Hawaii', 'ID':'Idaho', 'IL':'Illinois',
          'IN':'Indiana', 'IA':'Iowa', 'KS':'Kansas', 'KY':'Kentucy', 'LA':'Louisiana',
          'ME':'Maine', 'MD':'Maryland', 'MA':'Massachusetts', 'MI':'Michigan','MN':'Minnesota',
          'MS':'Mississippi', 'MO':'Missouri', 'MT':'Montana', 'NE':'Nebraska', 'NV':'Nevada',
          'NH':'New Hampshire', 'NJ':'New Jersey', 'NM':'New Mexico', 'NY':'New York',
          'NC':'North Carolina', 'ND':'North Dakota', 'OH':'Ohio', 'OK':'Oklahoma','OR':'Oregon',
          'PA':'Pennsylvania', 'RI':'Rhode Island', 'SC':'South Carolina', 'SD':'South Dakota',
          'TN':'Tennessee', 'TX':'Texas', 'UT':'Utah', 'VT':'Vermonet', 'VA':'Virginia',
          'WA':'Washington', 'WV':'West Virginia', 'WI':'Wisconsin', 'WY':'Wyoming'}
    
    #getting the year for the QUERY
    year1 = request.form['year1']
    year2 = request.form['year2']
    
    #making sure year is in the right order
    if year1 > year2:
        temp = year1
        year1 = year2
        year2 = temp
    
    #getting the state for the QUERY
    state1 = request.form['state1']
    state2 = request.form['state2']
    
    #getting the full state string
    state1 = states[state1]
    state2 = states[state2]
    
    #getting the gun laws from the checkboxes
    # NOTE: when a checkbox is selected, the value == on, else value == none
    allgun = request.form.get('all_gun')
    permitreq = request.form.get('permit_req')
    purchpermit = request.form.get('purch_permit')
    registration = request.form.get('registration')
    opencarry = request.form.get('open_carry')
    bcheck = request.form.get('bkgd_check_priv')
    
    #getting the mental health checkboxes
    # NOTE: when a checkbox is selected, the value == on, else value == none
    allmh = request.form.get('all_mh')
    arank = request.form.get('access_rank')
    orank = request.form.get('overall_rank')
    
    #creating an empty array for headings, need to change it for each query
   
    
    #running the Query
    states = []
    #all gun laws and no mental health
    if (state1 =='All' and state2 == 'All'):
        error = 'Please select at least one state to view. Thanks!'
        return render_template("state.html", error=error)
        
    elif (allgun == 'on' and allmh != 'on'):
        cursor1 = g.conn.execute('''SELECT S.year, L.sname, S.count, S.rate, G.permit_req,
                                 G.purch_permit_req, G.registration, G.open_carry, G.bkgd_check_priv
                            FROM Suicides S, Lived_In L, g_Law G
                            WHERE L.sname = (%s) AND L.sname = G.sname 
                            AND S.year >= (%s) AND S.year <= (%s) AND S.sid = L.sid
                            ''', state1, year1,year2)  
                            
        for result in cursor1:
            states.append(result) 
        cursor1.close()
    
        cursor2 = g.conn.execute('''SELECT S.year, L.sname, S.count, S.rate, G.permit_req,
                                 G.purch_permit_req, G.registration, G.open_carry, G.bkgd_check_priv
                            FROM Suicides S, Lived_In L, g_Law G
                            WHERE L.sname = (%s) AND L.sname = G.sname 
                            AND S.year >= (%s) AND S.year <= (%s) AND S.sid = L.sid
                            ''', state2, year1,year2)  
        for result in cursor2: 
            states.append(result) 
        cursor2.close()
        headings = ["Year", "State", "Total Count", "Rate per 100,000", "Permit Required",
                    "Purchase Permit", "Registration", "Open Carry Allowed", "Background Check"]
        
    #all gun laws and mental health rankings need to fix   
    elif (allgun == 'on' and allmh == 'on'):
        cursor1 = g.conn.execute('''SELECT S.year, L.sname, S.count, S.rate, G.permit_req,
                                 G.purch_permit_req, G.registration, G.open_carry, G.bkgd_check_priv,
                                 M.access_rank, M.overall_rank
                            FROM Suicides S, Lived_In L, g_Law G, h_rank M
                            WHERE L.sname = (%s) AND L.sname = G.sname AND L.sname = M.sname 
                            AND G.sname = M.sname AND S.year >= (%s) AND S.year <= (%s) 
                            AND S.sid = L.sid AND M.year >= (%s) AND M.year <= (%s)
                            ''', state1, year1,year2, year1,year2)  
                            
        for result in cursor1:
            states.append(result) 
        cursor1.close()
        
        cursor2 = g.conn.execute('''SELECT S.year, L.sname, S.count, S.rate, G.permit_req,
                                 G.purch_permit_req, G.registration, G.open_carry, G.bkgd_check_priv,
                                 M.access_rank, M.overall_rank
                            FROM Suicides S, Lived_In L, g_Law G, h_rank M
                            WHERE L.sname = (%s) AND L.sname = G.sname AND L.sname = M.sname 
                            AND G.sname = M.sname AND S.year >= (%s) AND S.year <= (%s) 
                            AND S.sid = L.sid 
                            ''', state2, year1,year2)  
        for result in cursor2: 
            states.append(result) 
        cursor2.close()  
        headings = ["Year", "State", "Total Count", "Rate per 100,000", "Permit Required",
                    "Purchase Permit", "Registration", "Open Carry Allowed", "Background Check",
                    "Mental Health Access Rank", "Overall Mental Health Rank"]
        
    #ownership permit required    
    elif (permitreq == 'on'):
        cursor1 = g.conn.execute('''SELECT S.year, L.sname, S.count, S.rate, G.permit_req 
                            FROM Suicides S, Lived_In L, g_Law G
                            WHERE L.sname = (%s) AND L.sname = G.sname AND S.year >= (%s) 
                            AND S.year <= (%s) AND S.sid = L.sid
                            ''', state1, year1,year2)  
        for result in cursor1:
            states.append(result) 
        cursor1.close()
        
        cursor2 = g.conn.execute('''SELECT S.year, L.sname, S.count, S.rate, G.permit_req 
                                FROM Suicides S, Lived_In L, g_Law G
                                WHERE L.sname = (%s) AND L.sname = G.sname AND S.year >= (%s) 
                                AND S.year <= (%s) AND S.sid = L.sid                           
                                ''', state2, year1,year2)  
        for result in cursor2: 
            states.append(result) 
        cursor2.close()
        headings = ["Year", "State", "Total Count", "Rate per 100,000", "Permit Required"]
    #purchase permit required 
    elif (purchpermit == 'on'):
        cursor1 = g.conn.execute('''SELECT S.year, L.sname, S.count, S.rate, G.purch_permit_req 
                            FROM Suicides S, Lived_In L, g_Law G
                            WHERE L.sname = (%s) AND L.sname = G.sname AND S.year >= (%s) 
                            AND S.year <= (%s) AND S.sid = L.sid
                            ''', state1, year1,year2)  
        for result in cursor1:
            states.append(result) 
        cursor1.close()
        
        cursor2 = g.conn.execute('''SELECT S.year, L.sname, S.count, S.rate, G.purch_permit_req 
                                FROM Suicides S, Lived_In L, g_Law G
                                WHERE L.sname = (%s) AND L.sname = G.sname AND S.year >= (%s) 
                                AND S.year <= (%s) AND S.sid = L.sid                           
                                ''', state2, year1,year2)  
        for result in cursor2: 
            states.append(result) 
        cursor2.close()    
        headings = ["Year", "State", "Total Count", "Rate per 100,000", "Purchase Permit Required"]
    #registration required 
    elif (registration == 'on'):
        cursor1 = g.conn.execute('''SELECT S.year, L.sname, S.count, S.rate, G.registration 
                            FROM Suicides S, Lived_In L, g_Law G
                            WHERE L.sname = (%s) AND L.sname = G.sname AND S.year >= (%s) 
                            AND S.year <= (%s) AND S.sid = L.sid
                            ''', state1, year1,year2)  
        for result in cursor1:
            states.append(result) 
        cursor1.close()
        
        cursor2 = g.conn.execute('''SELECT S.year, L.sname, S.count, S.rate, G.registration 
                                FROM Suicides S, Lived_In L, g_Law G
                                WHERE L.sname = (%s) AND L.sname = G.sname AND S.year >= (%s) 
                                AND S.year <= (%s) AND S.sid = L.sid                           
                                ''', state2, year1,year2)  
        for result in cursor2: 
            states.append(result) 
        cursor2.close()    
        headings = ["Year", "State", "Total Count", "Rate per 100,000", "Registration Required"]
    #opencarry allowed
    elif (opencarry == 'on'):
        cursor1 = g.conn.execute('''SELECT S.year, L.sname, S.count, S.rate, G.open_carry 
                            FROM Suicides S, Lived_In L, g_Law G
                            WHERE L.sname = (%s) AND L.sname = G.sname AND S.year >= (%s) 
                            AND S.year <= (%s) AND S.sid = L.sid
                            ''', state1, year1,year2)  
        for result in cursor1:
            states.append(result) 
        cursor1.close()
        
        cursor2 = g.conn.execute('''SELECT S.year, L.sname, S.count, S.rate, G.open_carry 
                                FROM Suicides S, Lived_In L, g_Law G
                                WHERE L.sname = (%s) AND L.sname = G.sname AND S.year >= (%s) 
                                AND S.year <= (%s) AND S.sid = L.sid                           
                                ''', state2, year1,year2)  
        for result in cursor2: 
            states.append(result) 
        cursor2.close()
        headings = ["Year", "State", "Total Count", "Rate per 100,000", "Open Carry Allowed"]
    #background check required
    elif (bcheck == 'on'):
        
        cursor1 = g.conn.execute('''SELECT S.year, L.sname, S.count, S.rate, G.bkgd_check_priv
                            FROM Suicides S, Lived_In L, g_Law G
                            WHERE L.sname = (%s) AND L.sname = G.sname AND S.year >= (%s) 
                            AND S.year <= (%s) AND S.sid = L.sid
                            ''', state1, year1,year2)  
        for result in cursor1:
            states.append(result) 
        cursor1.close()
        
        cursor2 = g.conn.execute('''SELECT S.year, L.sname, S.count, S.rate, G.bkgd_check_priv  
                                FROM Suicides S, Lived_In L, g_Law G
                                WHERE L.sname = (%s) AND L.sname = G.sname AND S.year >= (%s) 
                                AND S.year <= (%s) AND S.sid = L.sid                           
                                ''', state2, year1,year2)  
        for result in cursor2: 
            states.append(result) 
        cursor2.close()
        headings = ["Year", "State", "Total Count", "Rate per 100,000", "Private Background Checks"]
    #all Mental Health rankings       
    elif (allmh == 'on'):
        cursor1 = g.conn.execute('''SELECT S.year, L.sname, S.count, S.rate, 
                                 H.access_rank, H.overall_rank
                            FROM Suicides S, Lived_In L, h_rank H
                            WHERE H.sname = (%s) AND H.year >= (%s) 
                            AND H.year <= (%s) AND S.sid = L.sid AND L.sname = H.sname
                            AND S.year = H.year
                            ''', state1, year1,year2)  
        for result in cursor1:
            states.append(result) 
        cursor1.close()
        
        cursor2 = g.conn.execute('''SELECT S.year, L.sname, S.count, S.rate, 
                                 H.access_rank, H.overall_rank
                            FROM Suicides S, Lived_In L, h_rank H
                            WHERE L.sname = (%s) AND H.year >= (%s) 
                            AND H.year <= (%s) AND S.sid = L.sid  AND L.sname = H.sname
                            AND S.year = H.year
                            ''', state2, year1,year2)  
        for result in cursor2: 
            states.append(result) 
        cursor2.close()
        headings = ["Year", "State", "Total Count", "Rate per 100,000", 
                    "Mental Health Access Rank", "Overall Mental Health Rank"]
    #Mental Access Rank 
    elif (orank == 'on'):
        cursor1 = g.conn.execute('''SELECT S.year, L.sname, S.count, S.rate, 
                                 H.access_rank
                            FROM Suicides S, Lived_In L, h_rank H
                            WHERE L.sname = (%s) AND S.year >= (%s) 
                            AND S.year <= (%s) AND S.sid = L.sid  AND L.sname = H.sname
                            ''')  
        for result in cursor1:
            states.append(result) 
        cursor1.close()
        
        cursor2 = g.conn.execute('''SELECT S.year, L.sname, S.count, S.rate, 
                                 H.access_rank
                            FROM Suicides S, Lived_In L, h_rank H
                            WHERE L.sname = (%s) AND S.year >= (%s) 
                            AND S.year <= (%s) AND S.sid = L.sid  AND L.sname = H.sname                         
                                ''') 
        for result in cursor2: 
            states.append(result) 
        cursor2.close()
        headings = ["Year", "State", "Total Count", "Rate per 100,000", 
                    "Mental Health Overall Rank"]
    
    #Overall Mental Health Rank
    elif (arank == 'on'):
        cursor1 = g.conn.execute('''SELECT S.year, L.sname, S.count, S.rate, 
                                 H.access_rank
                            FROM Suicides S, Lived_In L, h_rank H
                            WHERE L.sname = (%s) AND S.year >= (%s) 
                            AND S.year <= (%s) AND S.sid = L.sid  AND L.sname = H.sname
                            ''')  
        for result in cursor1:
            states.append(result) 
        cursor1.close()
        
        cursor2 = g.conn.execute('''SELECT S.year, L.sname, S.count, S.rate, 
                                 H.access_rank
                            FROM Suicides S, Lived_In L, h_rank H
                            WHERE L.sname = (%s) AND S.year >= (%s) 
                            AND S.year <= (%s) AND S.sid = L.sid  AND L.sname = H.sname                         
                                ''') 
        for result in cursor2: 
            states.append(result) 
        cursor2.close()
        headings = ["Year", "State", "Total Count", "Rate per 100,000", 
                    "Mental Health Access Rank"]
    
    #just state comparisons
    else:
        cursor1 = g.conn.execute('''SELECT S.year, L.sname, S.count, S.rate 
                            FROM Suicides S, Lived_In L
                            WHERE L.sname = (%s) AND S.year >= (%s) AND S.year <= (%s)
                            AND S.sid = L.sid
                            ''', state1, year1,year2)  
        for result in cursor1:
            states.append(result) 
        cursor1.close()
        
        cursor2 = g.conn.execute('''SELECT S.year, L.sname, S.count, S.rate 
                                FROM Suicides S, Lived_In L
                                WHERE L.sname = (%s) AND S.year >= (%s) AND S.year <= (%s)
                                AND S.sid = L.sid                            
                                ''', state2, year1,year2)  
        for result in cursor2: 
            states.append(result) 
        cursor2.close()
        headings = ["Year", "State", "Total Count", "Rate per 100,000"]
    context = dict(states = states)
    print(context, " context")
    
    #return the results
    return render_template('state.html', headings=headings, **context)



 

#SUBMIT MILITARY
@app.route('/submitmilitary',methods=['POST'])
def submitmilitary():
    #getting the year for the QUERY
    year1 = request.form['year1']
    year2 = request.form['year2']
    
    #making sure year is in the right order
    if year1 > year2:
        temp = year1
        year1 = year2
        year2 = temp
    
    #getting the branches for the QUERY
    # NOTE: when a checkbox is selected, the value == on, else value == none
    combined = request.form.get('combined')
    army = request.form.get('army')
    navy = request.form.get('navy')
    marines = request.form.get('marines')
    airforce = request.form.get('airforce')

    
    #getting the view options
    # NOTE: when a checkbox is selected, the value == on, else value == none
    showrank = request.form.get('showrank')
    showmh = request.form.get('showmh')
    showaccess = request.form.get('showaccess')
 
    #creating a headings array that needs to be populated for each query
    headings = []
    
    #creating an empty array for the query results
    military = []
    
    #ANOTHE COMMEnT
    
    #running the Query
    if showaccess == "on":
        if showrank == "on":
            if showmh == "on":
                if combined == 'on':
                    if army == "on":
                        if navy =="on": 
                            if marines =="on": 
                                if airforce == "on":
                                    headings = ["Year", "Branch", "Count", "Rate", "Lower Enlisted", 
                                                "NCOs", "Officers", "Warrant Officers", 
                                                "Mental Health Diagnosis", "NO Mental Health Diagnosis",
                                                "TBI History", "NO TBI", "Previous Self-Harm", 
                                                "NO Previous Self-Harm", "Visited Health Services", "DID NOT visit",
                                                "Gun in Home", "No Gun in Home"]
                                    cursor1 = g.conn.execute('''SELECT S.year, B.branch, S.count, S.rate, 
                                                             R.e1_e4, R.e5_e9, R.officer, R.warrant_officer, M.health_diag_y,
                                                             M.health_diag_n, m.tbi_y, m.tbi_n, m.prev_self_harm_y, m.prev_self_harm_n,
                                                             m.health_ser_used_y, m.health_ser_used_n, a.in_home, a.not_in_home
                                                            FROM Suicides S, Military_Branch B, Rank R, Mental_Characteristics M, Access_To_Firearms A
                                                            WHERE s.sid = b.sid 
                                                            AND b.sid = r.sid
                                                            AND r.sid = m.sid
                                                            AND m.sid = a.sid
                                                            AND S.year >= (%s) 
                                                            AND S.year <= (%s)
                                                            ''', year1,year2)   
                                    for result in cursor1:
                                        military.append(result) 
                                    cursor1.close()
                                    
                                elif airforce != "on":
                                    headings = ["Year", "Branch", "Count", "Rate", "Lower Enlisted", 
                                                "NCOs", "Officers", "Warrant Officers", 
                                                "Mental Health Diagnosis", "NO Mental Health Diagnosis",
                                                "TBI History", "NO TBI", "Previous Self-Harm", 
                                                "NO Previous Self-Harm", "Visited Health Services", "DID NOT visit",
                                                "Gun in Home", "No Gun in Home"]
                                    cursor1 = g.conn.execute('''SELECT S.year, B.branch, S.count, S.rate, 
                                                             R.e1_e4, R.e5_e9, R.officer, R.warrant_officer, M.health_diag_y,
                                                             M.health_diag_n, m.tbi_y, m.tbi_n, m.prev_self_harm_y, m.prev_self_harm_n,
                                                             m.health_ser_used_y, m.health_ser_used_n, a.in_home, a.not_in_home
                                                            FROM Suicides S, Military_Branch B, Rank R, Mental_Characteristics M, Access_To_Firearms A
                                                            WHERE s.sid = b.sid 
                                                            AND b.sid = r.sid
                                                            AND r.sid = m.sid
                                                            AND m.sid = a.sid
                                                            AND S.year >= (%s) 
                                                            AND S.year <= (%s)
                                                            AND B.branch != 'Air Force'
                                                            ''', year1,year2)    
                                    for result in cursor1:
                                        military.append(result) 
                                    cursor1.close()
                                    
                            elif marines !="on": 
                                if airforce == "on":
                                    headings = ["Year", "Branch", "Count", "Rate", "Lower Enlisted", 
                                                "NCOs", "Officers", "Warrant Officers", 
                                                "Mental Health Diagnosis", "NO Mental Health Diagnosis",
                                                "TBI History", "NO TBI", "Previous Self-Harm", 
                                                "NO Previous Self-Harm", "Visited Health Services", "DID NOT visit",
                                                "Gun in Home", "No Gun in Home"]
                                    cursor1 = g.conn.execute('''SELECT S.year, B.branch, S.count, S.rate, 
                                                             R.e1_e4, R.e5_e9, R.officer, R.warrant_officer, M.health_diag_y,
                                                             M.health_diag_n, m.tbi_y, m.tbi_n, m.prev_self_harm_y, m.prev_self_harm_n,
                                                             m.health_ser_used_y, m.health_ser_used_n, a.in_home, a.not_in_home
                                                            FROM Suicides S, Military_Branch B, Rank R, Mental_Characteristics M, Access_To_Firearms A
                                                            WHERE s.sid = b.sid 
                                                            AND b.sid = r.sid
                                                            AND r.sid = m.sid
                                                            AND m.sid = a.sid
                                                            AND S.year >= (%s) 
                                                            AND S.year <= (%s)
                                                            AND B.branch != 'Marine Corps'
                                                            ''', year1,year2)    
                                    for result in cursor1:
                                        military.append(result) 
                                    cursor1.close()
                                    
                                elif airforce != "on":
                                    headings = ["Year", "Branch", "Count", "Rate", "Lower Enlisted", 
                                                "NCOs", "Officers", "Warrant Officers", 
                                                "Mental Health Diagnosis", "NO Mental Health Diagnosis",
                                                "TBI History", "NO TBI", "Previous Self-Harm", 
                                                "NO Previous Self-Harm", "Visited Health Services", "DID NOT visit",
                                                "Gun in Home", "No Gun in Home"]
                                    cursor1 = g.conn.execute('''SELECT S.year, B.branch, S.count, S.rate, 
                                                             R.e1_e4, R.e5_e9, R.officer, R.warrant_officer, M.health_diag_y,
                                                             M.health_diag_n, m.tbi_y, m.tbi_n, m.prev_self_harm_y, m.prev_self_harm_n,
                                                             m.health_ser_used_y, m.health_ser_used_n, a.in_home, a.not_in_home
                                                            FROM Suicides S, Military_Branch B, Rank R, Mental_Characteristics M, Access_To_Firearms A
                                                            WHERE s.sid = b.sid 
                                                            AND b.sid = r.sid
                                                            AND r.sid = m.sid
                                                            AND m.sid = a.sid
                                                            AND S.year >= (%s) 
                                                            AND S.year <= (%s)
                                                            AND B.branch != 'Air Force'
                                                            AND B.branch != 'Marine Corps'
                                                            ''', year1,year2)   
                                    for result in cursor1:
                                        military.append(result) 
                                    cursor1.close()
                                    
                        elif navy !="on": 
                            if marines =="on": 
                                if airforce == "on":
                                    headings = ["Year", "Branch", "Count", "Rate", "Lower Enlisted", 
                                                "NCOs", "Officers", "Warrant Officers", 
                                                "Mental Health Diagnosis", "NO Mental Health Diagnosis",
                                                "TBI History", "NO TBI", "Previous Self-Harm", 
                                                "NO Previous Self-Harm", "Visited Health Services", "DID NOT visit",
                                                "Gun in Home", "No Gun in Home"]
                                    cursor1 = g.conn.execute('''SELECT S.year, B.branch, S.count, S.rate, 
                                                             R.e1_e4, R.e5_e9, R.officer, R.warrant_officer, M.health_diag_y,
                                                             M.health_diag_n, m.tbi_y, m.tbi_n, m.prev_self_harm_y, m.prev_self_harm_n,
                                                             m.health_ser_used_y, m.health_ser_used_n, a.in_home, a.not_in_home
                                                            FROM Suicides S, Military_Branch B, Rank R, Mental_Characteristics M, Access_To_Firearms A
                                                            WHERE s.sid = b.sid 
                                                            AND b.sid = r.sid
                                                            AND r.sid = m.sid
                                                            AND m.sid = a.sid
                                                            AND S.year >= (%s) 
                                                            AND S.year <= (%s)
                                                            AND B.branch != 'Navy'
                                                            ''', year1,year2)  
                                    for result in cursor1:
                                        military.append(result) 
                                    cursor1.close()
                                    
                                elif airforce != "on":
                                    headings = ["Year", "Branch", "Count", "Rate", "Lower Enlisted", 
                                                "NCOs", "Officers", "Warrant Officers", 
                                                "Mental Health Diagnosis", "NO Mental Health Diagnosis",
                                                "TBI History", "NO TBI", "Previous Self-Harm", 
                                                "NO Previous Self-Harm", "Visited Health Services", "DID NOT visit",
                                                "Gun in Home", "No Gun in Home"]
                                    cursor1 = g.conn.execute('''SELECT S.year, B.branch, S.count, S.rate, 
                                                             R.e1_e4, R.e5_e9, R.officer, R.warrant_officer, M.health_diag_y,
                                                             M.health_diag_n, m.tbi_y, m.tbi_n, m.prev_self_harm_y, m.prev_self_harm_n,
                                                             m.health_ser_used_y, m.health_ser_used_n, a.in_home, a.not_in_home
                                                            FROM Suicides S, Military_Branch B, Rank R, Mental_Characteristics M, Access_To_Firearms A
                                                            WHERE s.sid = b.sid 
                                                            AND b.sid = r.sid
                                                            AND r.sid = m.sid
                                                            AND m.sid = a.sid
                                                            AND S.year >= (%s) 
                                                            AND S.year <= (%s)
                                                            AND B.branch != 'Navy'
                                                            AND B.branch != 'Air Force'
                                                            ''', year1,year2)  
                                    for result in cursor1:
                                        military.append(result) 
                                    cursor1.close()
                                    
                            elif marines !="on": 
                                if airforce == "on":
                                    headings = ["Year", "Branch", "Count", "Rate", "Lower Enlisted", 
                                                "NCOs", "Officers", "Warrant Officers", 
                                                "Mental Health Diagnosis", "NO Mental Health Diagnosis",
                                                "TBI History", "NO TBI", "Previous Self-Harm", 
                                                "NO Previous Self-Harm", "Visited Health Services", "DID NOT visit",
                                                "Gun in Home", "No Gun in Home"]
                                    cursor1 = g.conn.execute('''SELECT S.year, B.branch, S.count, S.rate, 
                                                             R.e1_e4, R.e5_e9, R.officer, R.warrant_officer, M.health_diag_y,
                                                             M.health_diag_n, m.tbi_y, m.tbi_n, m.prev_self_harm_y, m.prev_self_harm_n,
                                                             m.health_ser_used_y, m.health_ser_used_n, a.in_home, a.not_in_home
                                                            FROM Suicides S, Military_Branch B, Rank R, Mental_Characteristics M, Access_To_Firearms A
                                                            WHERE s.sid = b.sid 
                                                            AND b.sid = r.sid
                                                            AND r.sid = m.sid
                                                            AND m.sid = a.sid
                                                            AND S.year >= (%s) 
                                                            AND S.year <= (%s)
                                                            AND B.branch != 'Navy'
                                                            AND B.branch != 'Marine Corps'
                                                             ''', year1,year2)
                                    for result in cursor1:
                                        military.append(result) 
                                    cursor1.close()
                                    
                                elif airforce != "on":
                                    headings = ["Year", "Branch", "Count", "Rate", "Lower Enlisted", 
                                                "NCOs", "Officers", "Warrant Officers", 
                                                "Mental Health Diagnosis", "NO Mental Health Diagnosis",
                                                "TBI History", "NO TBI", "Previous Self-Harm", 
                                                "NO Previous Self-Harm", "Visited Health Services", "DID NOT visit",
                                                "Gun in Home", "No Gun in Home"]
                                    cursor1 = g.conn.execute('''SELECT S.year, B.branch, S.count, S.rate, 
                                                             R.e1_e4, R.e5_e9, R.officer, R.warrant_officer, M.health_diag_y,
                                                             M.health_diag_n, m.tbi_y, m.tbi_n, m.prev_self_harm_y, m.prev_self_harm_n,
                                                             m.health_ser_used_y, m.health_ser_used_n, a.in_home, a.not_in_home
                                                            FROM Suicides S, Military_Branch B, Rank R, Mental_Characteristics M, Access_To_Firearms A
                                                            WHERE s.sid = b.sid 
                                                            AND b.sid = r.sid
                                                            AND r.sid = m.sid
                                                            AND m.sid = a.sid
                                                            AND S.year >= (%s) 
                                                            AND S.year <= (%s)
                                                            AND B.branch != 'Navy'
                                                            AND B.branch != 'Marine Corps'
                                                            AND B.branch != 'Air Force'
                                                        ''', year1,year2)  
                                    for result in cursor1:
                                        military.append(result) 
                                    cursor1.close()
                                    
                    elif army !="on":
                        if navy =="on": 
                            if marines =="on": 
                                if airforce == "on":
                                    headings = ["Year", "Branch", "Count", "Rate", "Lower Enlisted", 
                                                "NCOs", "Officers", "Warrant Officers", 
                                                "Mental Health Diagnosis", "NO Mental Health Diagnosis",
                                                "TBI History", "NO TBI", "Previous Self-Harm", 
                                                "NO Previous Self-Harm", "Visited Health Services", "DID NOT visit",
                                                "Gun in Home", "No Gun in Home"]
                                    cursor1 = g.conn.execute('''SELECT S.year, B.branch, S.count, S.rate, 
                                                             R.e1_e4, R.e5_e9, R.officer, R.warrant_officer, M.health_diag_y,
                                                             M.health_diag_n, m.tbi_y, m.tbi_n, m.prev_self_harm_y, m.prev_self_harm_n,
                                                             m.health_ser_used_y, m.health_ser_used_n, a.in_home, a.not_in_home
                                                            FROM Suicides S, Military_Branch B, Rank R, Mental_Characteristics M, Access_To_Firearms A
                                                            WHERE s.sid = b.sid 
                                                            AND b.sid = r.sid
                                                            AND r.sid = m.sid
                                                            AND m.sid = a.sid
                                                            AND S.year >= (%s) 
                                                            AND S.year <= (%s)
                                                            AND B.branch != 'Army'
                                                            AND B.branch != 'Navy'
                                                            AND B.branch != 'Marine Corps'
                                                            AND B.branch != 'Air Force'
                                                        ''', year1,year2)  
                                    for result in cursor1:
                                        military.append(result) 
                                    cursor1.close()
                                    
                                elif airforce != "on":
                                    headings = ["Year", "Branch", "Count", "Rate", "Lower Enlisted", 
                                                "NCOs", "Officers", "Warrant Officers", 
                                                "Mental Health Diagnosis", "NO Mental Health Diagnosis",
                                                "TBI History", "NO TBI", "Previous Self-Harm", 
                                                "NO Previous Self-Harm", "Visited Health Services", "DID NOT visit",
                                                "Gun in Home", "No Gun in Home"]
                                    cursor1 = g.conn.execute('''SELECT S.year, B.branch, S.count, S.rate, 
                                                             R.e1_e4, R.e5_e9, R.officer, R.warrant_officer, M.health_diag_y,
                                                             M.health_diag_n, m.tbi_y, m.tbi_n, m.prev_self_harm_y, m.prev_self_harm_n,
                                                             m.health_ser_used_y, m.health_ser_used_n, a.in_home, a.not_in_home
                                                            FROM Suicides S, Military_Branch B, Rank R, Mental_Characteristics M, Access_To_Firearms A
                                                            WHERE s.sid = b.sid 
                                                            AND b.sid = r.sid
                                                            AND r.sid = m.sid
                                                            AND m.sid = a.sid
                                                            AND S.year >= (%s) 
                                                            AND S.year <= (%s)
                                                            AND B.branch != 'Army'
                                                            AND B.branch != 'Air Force'
                                                        ''', year1,year2)  
                                    for result in cursor1:
                                        military.append(result) 
                                    cursor1.close()
                                    
                            elif marines !="on": 
                                if airforce == "on":
                                    headings = ["Year", "Branch", "Count", "Rate", "Lower Enlisted", 
                                                "NCOs", "Officers", "Warrant Officers", 
                                                "Mental Health Diagnosis", "NO Mental Health Diagnosis",
                                                "TBI History", "NO TBI", "Previous Self-Harm", 
                                                "NO Previous Self-Harm", "Visited Health Services", "DID NOT visit",
                                                "Gun in Home", "No Gun in Home"]
                                    cursor1 = g.conn.execute('''SELECT S.year, B.branch, S.count, S.rate, 
                                                             R.e1_e4, R.e5_e9, R.officer, R.warrant_officer, M.health_diag_y,
                                                             M.health_diag_n, m.tbi_y, m.tbi_n, m.prev_self_harm_y, m.prev_self_harm_n,
                                                             m.health_ser_used_y, m.health_ser_used_n, a.in_home, a.not_in_home
                                                            FROM Suicides S, Military_Branch B, Rank R, Mental_Characteristics M, Access_To_Firearms A
                                                            WHERE s.sid = b.sid 
                                                            AND b.sid = r.sid
                                                            AND r.sid = m.sid
                                                            AND m.sid = a.sid
                                                            AND S.year >= (%s) 
                                                            AND S.year <= (%s)
                                                            AND B.branch != 'Army'
                                                            AND B.branch != 'Marine Corps'
                                                        ''', year1,year2)  
                                    for result in cursor1:
                                        military.append(result) 
                                    cursor1.close()
                                    
                                elif airforce != "on":
                                    headings = ["Year", "Branch", "Count", "Rate", "Lower Enlisted", 
                                                "NCOs", "Officers", "Warrant Officers", 
                                                "Mental Health Diagnosis", "NO Mental Health Diagnosis",
                                                "TBI History", "NO TBI", "Previous Self-Harm", 
                                                "NO Previous Self-Harm", "Visited Health Services", "DID NOT visit",
                                                "Gun in Home", "No Gun in Home"]
                                    cursor1 = g.conn.execute('''SELECT S.year, B.branch, S.count, S.rate, 
                                                             R.e1_e4, R.e5_e9, R.officer, R.warrant_officer, M.health_diag_y,
                                                             M.health_diag_n, m.tbi_y, m.tbi_n, m.prev_self_harm_y, m.prev_self_harm_n,
                                                             m.health_ser_used_y, m.health_ser_used_n, a.in_home, a.not_in_home
                                                            FROM Suicides S, Military_Branch B, Rank R, Mental_Characteristics M, Access_To_Firearms A
                                                            WHERE s.sid = b.sid 
                                                            AND b.sid = r.sid
                                                            AND r.sid = m.sid
                                                            AND m.sid = a.sid
                                                            AND S.year >= (%s) 
                                                            AND S.year <= (%s)
                                                        AND B.branch != 'Army'
                                                        AND B.branch != 'Marine Corps'
                                                        AND B.branch != 'Air Force'
                                                        ''', year1,year2)  
                                    for result in cursor1:
                                        military.append(result) 
                                    cursor1.close()
                                    
                        elif navy !="on": 
                            if marines =="on": 
                                if airforce == "on":
                                    headings = ["Year", "Branch", "Count", "Rate", "Lower Enlisted", 
                                                "NCOs", "Officers", "Warrant Officers", 
                                                "Mental Health Diagnosis", "NO Mental Health Diagnosis",
                                                "TBI History", "NO TBI", "Previous Self-Harm", 
                                                "NO Previous Self-Harm", "Visited Health Services", "DID NOT visit",
                                                "Gun in Home", "No Gun in Home"]
                                    cursor1 = g.conn.execute('''SELECT S.year, B.branch, S.count, S.rate, 
                                                             R.e1_e4, R.e5_e9, R.officer, R.warrant_officer, M.health_diag_y,
                                                             M.health_diag_n, m.tbi_y, m.tbi_n, m.prev_self_harm_y, m.prev_self_harm_n,
                                                             m.health_ser_used_y, m.health_ser_used_n, a.in_home, a.not_in_home
                                                            FROM Suicides S, Military_Branch B, Rank R, Mental_Characteristics M, Access_To_Firearms A
                                                            WHERE s.sid = b.sid 
                                                            AND b.sid = r.sid
                                                            AND r.sid = m.sid
                                                            AND m.sid = a.sid
                                                            AND S.year >= (%s) 
                                                            AND S.year <= (%s)
                                                            AND B.branch != 'Army'
                                                            AND B.branch != 'Navy'
                                                        ''', year1,year2)  
                                    for result in cursor1:
                                        military.append(result) 
                                    cursor1.close()
                                    
                                elif airforce != "on":
                                    headings = ["Year", "Branch", "Count", "Rate", "Lower Enlisted", 
                                                "NCOs", "Officers", "Warrant Officers", 
                                                "Mental Health Diagnosis", "NO Mental Health Diagnosis",
                                                "TBI History", "NO TBI", "Previous Self-Harm", 
                                                "NO Previous Self-Harm", "Visited Health Services", "DID NOT visit",
                                                "Gun in Home", "No Gun in Home"]
                                    cursor1 = g.conn.execute('''SELECT S.year, B.branch, S.count, S.rate, 
                                                             R.e1_e4, R.e5_e9, R.officer, R.warrant_officer, M.health_diag_y,
                                                             M.health_diag_n, m.tbi_y, m.tbi_n, m.prev_self_harm_y, m.prev_self_harm_n,
                                                             m.health_ser_used_y, m.health_ser_used_n, a.in_home, a.not_in_home
                                                            FROM Suicides S, Military_Branch B, Rank R, Mental_Characteristics M, Access_To_Firearms A
                                                            WHERE s.sid = b.sid 
                                                            AND b.sid = r.sid
                                                            AND r.sid = m.sid
                                                            AND m.sid = a.sid
                                                            AND S.year >= (%s) 
                                                            AND S.year <= (%s)
                                                            AND B.branch != 'Army'
                                                            AND B.branch != 'Navy'
                                                            AND B.branch != 'Air Force'
                                                        ''', year1,year2)  
                                    for result in cursor1:
                                        military.append(result) 
                                    cursor1.close()
                                    
                            elif marines !="on": 
                                if airforce == "on":
                                    headings = ["Year", "Branch", "Count", "Rate", "Lower Enlisted", 
                                                "NCOs", "Officers", "Warrant Officers", 
                                                "Mental Health Diagnosis", "NO Mental Health Diagnosis",
                                                "TBI History", "NO TBI", "Previous Self-Harm", 
                                                "NO Previous Self-Harm", "Visited Health Services", "DID NOT visit",
                                                "Gun in Home", "No Gun in Home"]
                                    cursor1 = g.conn.execute('''SELECT S.year, B.branch, S.count, S.rate, 
                                                             R.e1_e4, R.e5_e9, R.officer, R.warrant_officer, M.health_diag_y,
                                                             M.health_diag_n, m.tbi_y, m.tbi_n, m.prev_self_harm_y, m.prev_self_harm_n,
                                                             m.health_ser_used_y, m.health_ser_used_n, a.in_home, a.not_in_home
                                                            FROM Suicides S, Military_Branch B, Rank R, Mental_Characteristics M, Access_To_Firearms A
                                                            WHERE s.sid = b.sid 
                                                            AND b.sid = r.sid
                                                            AND r.sid = m.sid
                                                            AND m.sid = a.sid
                                                            AND S.year >= (%s) 
                                                            AND S.year <= (%s)
                                                            AND B.branch != 'Army'
                                                            AND B.branch != 'Navy'
                                                            AND B.branch != 'Marine Corps'
                                                        ''', year1,year2)  
                                    for result in cursor1:
                                        military.append(result) 
                                    cursor1.close()
                                    
                                elif airforce != "on":
                                    headings = ["Year", "Branch", "Count", "Rate", "Lower Enlisted", 
                                                "NCOs", "Officers", "Warrant Officers", 
                                                "Mental Health Diagnosis", "NO Mental Health Diagnosis",
                                                "TBI History", "NO TBI", "Previous Self-Harm", 
                                                "NO Previous Self-Harm", "Visited Health Services", "DID NOT visit",
                                                "Gun in Home", "No Gun in Home"]
                                    cursor1 = g.conn.execute('''SELECT S.year, B.branch, S.count, S.rate, 
                                                             R.e1_e4, R.e5_e9, R.officer, R.warrant_officer, M.health_diag_y,
                                                             M.health_diag_n, m.tbi_y, m.tbi_n, m.prev_self_harm_y, m.prev_self_harm_n,
                                                             m.health_ser_used_y, m.health_ser_used_n, a.in_home, a.not_in_home
                                                            FROM Suicides S, Military_Branch B, Rank R, Mental_Characteristics M, Access_To_Firearms A
                                                            WHERE s.sid = b.sid 
                                                            AND b.sid = r.sid
                                                            AND r.sid = m.sid
                                                            AND m.sid = a.sid
                                                            AND S.year >= (%s) 
                                                            AND S.year <= (%s)
                                                            AND B.branch != 'Army'
                                                            AND B.branch != 'Navy'
                                                            AND B.branch != 'Marine Corps'
                                                            AND B.branch != 'Air Force'
                                                        ''', year1,year2)  
                                    for result in cursor1:
                                        military.append(result) 
                                    cursor1.close()
                if combined != 'on':
                    if army == "on":
                        if navy =="on": 
                            if marines =="on": 
                                if airforce == "on":
                                    headings = ["Year", "Branch", "Count", "Rate", "Lower Enlisted", 
                                                "NCOs", "Officers", "Warrant Officers", 
                                                "Mental Health Diagnosis", "NO Mental Health Diagnosis",
                                                "TBI History", "NO TBI", "Previous Self-Harm", 
                                                "NO Previous Self-Harm", "Visited Health Services", "DID NOT visit",
                                                "Gun in Home", "No Gun in Home"]
                                    cursor1 = g.conn.execute('''SELECT S.year, B.branch, S.count, S.rate, 
                                                             R.e1_e4, R.e5_e9, R.officer, R.warrant_officer, M.health_diag_y,
                                                             M.health_diag_n, m.tbi_y, m.tbi_n, m.prev_self_harm_y, m.prev_self_harm_n,
                                                             m.health_ser_used_y, m.health_ser_used_n, a.in_home, a.not_in_home
                                                            FROM Suicides S, Military_Branch B, Rank R, Mental_Characteristics M, Access_To_Firearms A
                                                            WHERE s.sid = b.sid 
                                                            AND b.sid = r.sid
                                                            AND r.sid = m.sid
                                                            AND m.sid = a.sid
                                                            AND S.year >= (%s) 
                                                            AND S.year <= (%s)
                                                            AND B.branch != 'All'
                                                            ''', year1,year2)   
                                    for result in cursor1:
                                        military.append(result) 
                                    cursor1.close()
                                    
                                elif airforce != "on":
                                    headings = ["Year", "Branch", "Count", "Rate", "Lower Enlisted", 
                                                "NCOs", "Officers", "Warrant Officers", 
                                                "Mental Health Diagnosis", "NO Mental Health Diagnosis",
                                                "TBI History", "NO TBI", "Previous Self-Harm", 
                                                "NO Previous Self-Harm", "Visited Health Services", "DID NOT visit",
                                                "Gun in Home", "No Gun in Home"]
                                    cursor1 = g.conn.execute('''SELECT S.year, B.branch, S.count, S.rate, 
                                                             R.e1_e4, R.e5_e9, R.officer, R.warrant_officer, M.health_diag_y,
                                                             M.health_diag_n, m.tbi_y, m.tbi_n, m.prev_self_harm_y, m.prev_self_harm_n,
                                                             m.health_ser_used_y, m.health_ser_used_n, a.in_home, a.not_in_home
                                                            FROM Suicides S, Military_Branch B, Rank R, Mental_Characteristics M, Access_To_Firearms A
                                                            WHERE s.sid = b.sid 
                                                            AND b.sid = r.sid
                                                            AND r.sid = m.sid
                                                            AND m.sid = a.sid
                                                            AND S.year >= (%s) 
                                                            AND S.year <= (%s)
                                                            AND B.branch != 'Air Force'
                                                            AND B.branch != 'All'
                                                            ''', year1,year2)    
                                    for result in cursor1:
                                        military.append(result) 
                                    cursor1.close()
                                    
                            elif marines !="on": 
                                if airforce == "on":
                                    headings = ["Year", "Branch", "Count", "Rate", "Lower Enlisted", 
                                                "NCOs", "Officers", "Warrant Officers", 
                                                "Mental Health Diagnosis", "NO Mental Health Diagnosis",
                                                "TBI History", "NO TBI", "Previous Self-Harm", 
                                                "NO Previous Self-Harm", "Visited Health Services", "DID NOT visit",
                                                "Gun in Home", "No Gun in Home"]
                                    cursor1 = g.conn.execute('''SELECT S.year, B.branch, S.count, S.rate, 
                                                             R.e1_e4, R.e5_e9, R.officer, R.warrant_officer, M.health_diag_y,
                                                             M.health_diag_n, m.tbi_y, m.tbi_n, m.prev_self_harm_y, m.prev_self_harm_n,
                                                             m.health_ser_used_y, m.health_ser_used_n, a.in_home, a.not_in_home
                                                            FROM Suicides S, Military_Branch B, Rank R, Mental_Characteristics M, Access_To_Firearms A
                                                            WHERE s.sid = b.sid 
                                                            AND b.sid = r.sid
                                                            AND r.sid = m.sid
                                                            AND m.sid = a.sid
                                                            AND S.year >= (%s) 
                                                            AND S.year <= (%s)
                                                            AND B.branch != 'Marine Corps'
                                                            AND B.branch != 'All'
                                                            ''', year1,year2)    
                                    for result in cursor1:
                                        military.append(result) 
                                    cursor1.close()
                                    
                                elif airforce != "on":
                                    headings = ["Year", "Branch", "Count", "Rate", "Lower Enlisted", 
                                                "NCOs", "Officers", "Warrant Officers", 
                                                "Mental Health Diagnosis", "NO Mental Health Diagnosis",
                                                "TBI History", "NO TBI", "Previous Self-Harm", 
                                                "NO Previous Self-Harm", "Visited Health Services", "DID NOT visit",
                                                "Gun in Home", "No Gun in Home"]
                                    cursor1 = g.conn.execute('''SELECT S.year, B.branch, S.count, S.rate, 
                                                             R.e1_e4, R.e5_e9, R.officer, R.warrant_officer, M.health_diag_y,
                                                             M.health_diag_n, m.tbi_y, m.tbi_n, m.prev_self_harm_y, m.prev_self_harm_n,
                                                             m.health_ser_used_y, m.health_ser_used_n, a.in_home, a.not_in_home
                                                            FROM Suicides S, Military_Branch B, Rank R, Mental_Characteristics M, Access_To_Firearms A
                                                            WHERE s.sid = b.sid 
                                                            AND b.sid = r.sid
                                                            AND r.sid = m.sid
                                                            AND m.sid = a.sid
                                                            AND S.year >= (%s) 
                                                            AND S.year <= (%s)
                                                            AND B.branch != 'Air Force'
                                                            AND B.branch != 'Marine Corps'
                                                            AND B.branch != 'All'
                                                            ''', year1,year2)   
                                    for result in cursor1:
                                        military.append(result) 
                                    cursor1.close()
                                    
                        elif navy !="on": 
                            if marines =="on": 
                                if airforce == "on":
                                    headings = ["Year", "Branch", "Count", "Rate", "Lower Enlisted", 
                                                "NCOs", "Officers", "Warrant Officers", 
                                                "Mental Health Diagnosis", "NO Mental Health Diagnosis",
                                                "TBI History", "NO TBI", "Previous Self-Harm", 
                                                "NO Previous Self-Harm", "Visited Health Services", "DID NOT visit",
                                                "Gun in Home", "No Gun in Home"]
                                    cursor1 = g.conn.execute('''SELECT S.year, B.branch, S.count, S.rate, 
                                                             R.e1_e4, R.e5_e9, R.officer, R.warrant_officer, M.health_diag_y,
                                                             M.health_diag_n, m.tbi_y, m.tbi_n, m.prev_self_harm_y, m.prev_self_harm_n,
                                                             m.health_ser_used_y, m.health_ser_used_n, a.in_home, a.not_in_home
                                                            FROM Suicides S, Military_Branch B, Rank R, Mental_Characteristics M, Access_To_Firearms A
                                                            WHERE s.sid = b.sid 
                                                            AND b.sid = r.sid
                                                            AND r.sid = m.sid
                                                            AND m.sid = a.sid
                                                            AND S.year >= (%s) 
                                                            AND S.year <= (%s)
                                                            AND B.branch != 'Navy'
                                                            AND B.branch != 'All'
                                                            ''', year1,year2)  
                                    for result in cursor1:
                                        military.append(result) 
                                    cursor1.close()
                                    
                                elif airforce != "on":
                                    headings = ["Year", "Branch", "Count", "Rate", "Lower Enlisted", 
                                                "NCOs", "Officers", "Warrant Officers", 
                                                "Mental Health Diagnosis", "NO Mental Health Diagnosis",
                                                "TBI History", "NO TBI", "Previous Self-Harm", 
                                                "NO Previous Self-Harm", "Visited Health Services", "DID NOT visit",
                                                "Gun in Home", "No Gun in Home"]
                                    cursor1 = g.conn.execute('''SELECT S.year, B.branch, S.count, S.rate, 
                                                             R.e1_e4, R.e5_e9, R.officer, R.warrant_officer, M.health_diag_y,
                                                             M.health_diag_n, m.tbi_y, m.tbi_n, m.prev_self_harm_y, m.prev_self_harm_n,
                                                             m.health_ser_used_y, m.health_ser_used_n, a.in_home, a.not_in_home
                                                            FROM Suicides S, Military_Branch B, Rank R, Mental_Characteristics M, Access_To_Firearms A
                                                            WHERE s.sid = b.sid 
                                                            AND b.sid = r.sid
                                                            AND r.sid = m.sid
                                                            AND m.sid = a.sid
                                                            AND S.year >= (%s) 
                                                            AND S.year <= (%s)
                                                            AND B.branch != 'Navy'
                                                            AND B.branch != 'Air Force'
                                                            AND B.branch != 'All'
                                                            ''', year1,year2)  
                                    for result in cursor1:
                                        military.append(result) 
                                    cursor1.close()
                                    
                            elif marines !="on": 
                                if airforce == "on":
                                    headings = ["Year", "Branch", "Count", "Rate", "Lower Enlisted", 
                                                "NCOs", "Officers", "Warrant Officers", 
                                                "Mental Health Diagnosis", "NO Mental Health Diagnosis",
                                                "TBI History", "NO TBI", "Previous Self-Harm", 
                                                "NO Previous Self-Harm", "Visited Health Services", "DID NOT visit",
                                                "Gun in Home", "No Gun in Home"]
                                    cursor1 = g.conn.execute('''SELECT S.year, B.branch, S.count, S.rate, 
                                                             R.e1_e4, R.e5_e9, R.officer, R.warrant_officer, M.health_diag_y,
                                                             M.health_diag_n, m.tbi_y, m.tbi_n, m.prev_self_harm_y, m.prev_self_harm_n,
                                                             m.health_ser_used_y, m.health_ser_used_n, a.in_home, a.not_in_home
                                                            FROM Suicides S, Military_Branch B, Rank R, Mental_Characteristics M, Access_To_Firearms A
                                                            WHERE s.sid = b.sid 
                                                            AND b.sid = r.sid
                                                            AND r.sid = m.sid
                                                            AND m.sid = a.sid
                                                            AND S.year >= (%s) 
                                                            AND S.year <= (%s)
                                                            AND B.branch != 'Navy'
                                                            AND B.branch != 'Marine Corps'
                                                            AND B.branch != 'All'
                                                             ''', year1,year2)
                                    for result in cursor1:
                                        military.append(result) 
                                    cursor1.close()
                                    
                                elif airforce != "on":
                                    headings = ["Year", "Branch", "Count", "Rate", "Lower Enlisted", 
                                                "NCOs", "Officers", "Warrant Officers", 
                                                "Mental Health Diagnosis", "NO Mental Health Diagnosis",
                                                "TBI History", "NO TBI", "Previous Self-Harm", 
                                                "NO Previous Self-Harm", "Visited Health Services", "DID NOT visit",
                                                "Gun in Home", "No Gun in Home"]
                                    cursor1 = g.conn.execute('''SELECT S.year, B.branch, S.count, S.rate, 
                                                             R.e1_e4, R.e5_e9, R.officer, R.warrant_officer, M.health_diag_y,
                                                             M.health_diag_n, m.tbi_y, m.tbi_n, m.prev_self_harm_y, m.prev_self_harm_n,
                                                             m.health_ser_used_y, m.health_ser_used_n, a.in_home, a.not_in_home
                                                            FROM Suicides S, Military_Branch B, Rank R, Mental_Characteristics M, Access_To_Firearms A
                                                            WHERE s.sid = b.sid 
                                                            AND b.sid = r.sid
                                                            AND r.sid = m.sid
                                                            AND m.sid = a.sid
                                                            AND S.year >= (%s) 
                                                            AND S.year <= (%s)
                                                            AND B.branch != 'Navy'
                                                            AND B.branch != 'Marine Corps'
                                                            AND B.branch != 'Air Force'
                                                            AND B.branch != 'All'
                                                        ''', year1,year2)  
                                    for result in cursor1:
                                        military.append(result) 
                                    cursor1.close()
                                    
                    elif army !="on":
                        if navy =="on": 
                            if marines =="on": 
                                if airforce == "on":
                                    headings = ["Year", "Branch", "Count", "Rate", "Lower Enlisted", 
                                                "NCOs", "Officers", "Warrant Officers", 
                                                "Mental Health Diagnosis", "NO Mental Health Diagnosis",
                                                "TBI History", "NO TBI", "Previous Self-Harm", 
                                                "NO Previous Self-Harm", "Visited Health Services", "DID NOT visit",
                                                "Gun in Home", "No Gun in Home"]
                                    cursor1 = g.conn.execute('''SELECT S.year, B.branch, S.count, S.rate, 
                                                             R.e1_e4, R.e5_e9, R.officer, R.warrant_officer, M.health_diag_y,
                                                             M.health_diag_n, m.tbi_y, m.tbi_n, m.prev_self_harm_y, m.prev_self_harm_n,
                                                             m.health_ser_used_y, m.health_ser_used_n, a.in_home, a.not_in_home
                                                            FROM Suicides S, Military_Branch B, Rank R, Mental_Characteristics M, Access_To_Firearms A
                                                            WHERE s.sid = b.sid 
                                                            AND b.sid = r.sid
                                                            AND r.sid = m.sid
                                                            AND m.sid = a.sid
                                                            AND S.year >= (%s) 
                                                            AND S.year <= (%s)
                                                            AND B.branch != 'Army'
                                                            AND B.branch != 'Navy'
                                                            AND B.branch != 'Marine Corps'
                                                            AND B.branch != 'Air Force'
                                                            AND B.branch != 'All'
                                                        ''', year1,year2)  
                                    for result in cursor1:
                                        military.append(result) 
                                    cursor1.close()
                                    
                                elif airforce != "on":
                                    headings = ["Year", "Branch", "Count", "Rate", "Lower Enlisted", 
                                                "NCOs", "Officers", "Warrant Officers", 
                                                "Mental Health Diagnosis", "NO Mental Health Diagnosis",
                                                "TBI History", "NO TBI", "Previous Self-Harm", 
                                                "NO Previous Self-Harm", "Visited Health Services", "DID NOT visit",
                                                "Gun in Home", "No Gun in Home"]
                                    cursor1 = g.conn.execute('''SELECT S.year, B.branch, S.count, S.rate, 
                                                             R.e1_e4, R.e5_e9, R.officer, R.warrant_officer, M.health_diag_y,
                                                             M.health_diag_n, m.tbi_y, m.tbi_n, m.prev_self_harm_y, m.prev_self_harm_n,
                                                             m.health_ser_used_y, m.health_ser_used_n, a.in_home, a.not_in_home
                                                            FROM Suicides S, Military_Branch B, Rank R, Mental_Characteristics M, Access_To_Firearms A
                                                            WHERE s.sid = b.sid 
                                                            AND b.sid = r.sid
                                                            AND r.sid = m.sid
                                                            AND m.sid = a.sid
                                                            AND S.year >= (%s) 
                                                            AND S.year <= (%s)
                                                            AND B.branch != 'Army'
                                                            AND B.branch != 'Air Force'
                                                            AND B.branch != 'All'
                                                        ''', year1,year2)  
                                    for result in cursor1:
                                        military.append(result) 
                                    cursor1.close()
                                    
                            elif marines !="on": 
                                if airforce == "on":
                                    headings = ["Year", "Branch", "Count", "Rate", "Lower Enlisted", 
                                                "NCOs", "Officers", "Warrant Officers", 
                                                "Mental Health Diagnosis", "NO Mental Health Diagnosis",
                                                "TBI History", "NO TBI", "Previous Self-Harm", 
                                                "NO Previous Self-Harm", "Visited Health Services", "DID NOT visit",
                                                "Gun in Home", "No Gun in Home"]
                                    cursor1 = g.conn.execute('''SELECT S.year, B.branch, S.count, S.rate, 
                                                             R.e1_e4, R.e5_e9, R.officer, R.warrant_officer, M.health_diag_y,
                                                             M.health_diag_n, m.tbi_y, m.tbi_n, m.prev_self_harm_y, m.prev_self_harm_n,
                                                             m.health_ser_used_y, m.health_ser_used_n, a.in_home, a.not_in_home
                                                            FROM Suicides S, Military_Branch B, Rank R, Mental_Characteristics M, Access_To_Firearms A
                                                            WHERE s.sid = b.sid 
                                                            AND b.sid = r.sid
                                                            AND r.sid = m.sid
                                                            AND m.sid = a.sid
                                                            AND S.year >= (%s) 
                                                            AND S.year <= (%s)
                                                            AND B.branch != 'Army'
                                                            AND B.branch != 'Marine Corps'
                                                            AND B.branch != 'All'
                                                        ''', year1,year2)  
                                    for result in cursor1:
                                        military.append(result) 
                                    cursor1.close()
                                    
                                elif airforce != "on":
                                    headings = ["Year", "Branch", "Count", "Rate", "Lower Enlisted", 
                                                "NCOs", "Officers", "Warrant Officers", 
                                                "Mental Health Diagnosis", "NO Mental Health Diagnosis",
                                                "TBI History", "NO TBI", "Previous Self-Harm", 
                                                "NO Previous Self-Harm", "Visited Health Services", "DID NOT visit",
                                                "Gun in Home", "No Gun in Home"]
                                    cursor1 = g.conn.execute('''SELECT S.year, B.branch, S.count, S.rate, 
                                                             R.e1_e4, R.e5_e9, R.officer, R.warrant_officer, M.health_diag_y,
                                                             M.health_diag_n, m.tbi_y, m.tbi_n, m.prev_self_harm_y, m.prev_self_harm_n,
                                                             m.health_ser_used_y, m.health_ser_used_n, a.in_home, a.not_in_home
                                                            FROM Suicides S, Military_Branch B, Rank R, Mental_Characteristics M, Access_To_Firearms A
                                                            WHERE s.sid = b.sid 
                                                            AND b.sid = r.sid
                                                            AND r.sid = m.sid
                                                            AND m.sid = a.sid
                                                            AND S.year >= (%s) 
                                                            AND S.year <= (%s)
                                                        AND B.branch != 'Army'
                                                        AND B.branch != 'Marine Corps'
                                                        AND B.branch != 'Air Force'
                                                        AND B.branch != 'All'
                                                        ''', year1,year2)  
                                    for result in cursor1:
                                        military.append(result) 
                                    cursor1.close()
                                    
                        elif navy !="on": 
                            if marines =="on": 
                                if airforce == "on":
                                    headings = ["Year", "Branch", "Count", "Rate", "Lower Enlisted", 
                                                "NCOs", "Officers", "Warrant Officers", 
                                                "Mental Health Diagnosis", "NO Mental Health Diagnosis",
                                                "TBI History", "NO TBI", "Previous Self-Harm", 
                                                "NO Previous Self-Harm", "Visited Health Services", "DID NOT visit",
                                                "Gun in Home", "No Gun in Home"]
                                    cursor1 = g.conn.execute('''SELECT S.year, B.branch, S.count, S.rate, 
                                                             R.e1_e4, R.e5_e9, R.officer, R.warrant_officer, M.health_diag_y,
                                                             M.health_diag_n, m.tbi_y, m.tbi_n, m.prev_self_harm_y, m.prev_self_harm_n,
                                                             m.health_ser_used_y, m.health_ser_used_n, a.in_home, a.not_in_home
                                                            FROM Suicides S, Military_Branch B, Rank R, Mental_Characteristics M, Access_To_Firearms A
                                                            WHERE s.sid = b.sid 
                                                            AND b.sid = r.sid
                                                            AND r.sid = m.sid
                                                            AND m.sid = a.sid
                                                            AND S.year >= (%s) 
                                                            AND S.year <= (%s)
                                                            AND B.branch != 'Army'
                                                            AND B.branch != 'Navy'
                                                            AND B.branch != 'All'
                                                        ''', year1,year2)  
                                    for result in cursor1:
                                        military.append(result) 
                                    cursor1.close()
                                    
                                elif airforce != "on":
                                    headings = ["Year", "Branch", "Count", "Rate", "Lower Enlisted", 
                                                "NCOs", "Officers", "Warrant Officers", 
                                                "Mental Health Diagnosis", "NO Mental Health Diagnosis",
                                                "TBI History", "NO TBI", "Previous Self-Harm", 
                                                "NO Previous Self-Harm", "Visited Health Services", "DID NOT visit",
                                                "Gun in Home", "No Gun in Home"]
                                    cursor1 = g.conn.execute('''SELECT S.year, B.branch, S.count, S.rate, 
                                                             R.e1_e4, R.e5_e9, R.officer, R.warrant_officer, M.health_diag_y,
                                                             M.health_diag_n, m.tbi_y, m.tbi_n, m.prev_self_harm_y, m.prev_self_harm_n,
                                                             m.health_ser_used_y, m.health_ser_used_n, a.in_home, a.not_in_home
                                                            FROM Suicides S, Military_Branch B, Rank R, Mental_Characteristics M, Access_To_Firearms A
                                                            WHERE s.sid = b.sid 
                                                            AND b.sid = r.sid
                                                            AND r.sid = m.sid
                                                            AND m.sid = a.sid
                                                            AND S.year >= (%s) 
                                                            AND S.year <= (%s)
                                                            AND B.branch != 'Army'
                                                            AND B.branch != 'Navy'
                                                            AND B.branch != 'Air Force'
                                                            AND B.branch != 'All'
                                                        ''', year1,year2)  
                                    for result in cursor1:
                                        military.append(result) 
                                    cursor1.close()
                                    
                            elif marines !="on": 
                                if airforce == "on":
                                    headings = ["Year", "Branch", "Count", "Rate", "Lower Enlisted", 
                                                "NCOs", "Officers", "Warrant Officers", 
                                                "Mental Health Diagnosis", "NO Mental Health Diagnosis",
                                                "TBI History", "NO TBI", "Previous Self-Harm", 
                                                "NO Previous Self-Harm", "Visited Health Services", "DID NOT visit",
                                                "Gun in Home", "No Gun in Home"]
                                    cursor1 = g.conn.execute('''SELECT S.year, B.branch, S.count, S.rate, 
                                                             R.e1_e4, R.e5_e9, R.officer, R.warrant_officer, M.health_diag_y,
                                                             M.health_diag_n, m.tbi_y, m.tbi_n, m.prev_self_harm_y, m.prev_self_harm_n,
                                                             m.health_ser_used_y, m.health_ser_used_n, a.in_home, a.not_in_home
                                                            FROM Suicides S, Military_Branch B, Rank R, Mental_Characteristics M, Access_To_Firearms A
                                                            WHERE s.sid = b.sid 
                                                            AND b.sid = r.sid
                                                            AND r.sid = m.sid
                                                            AND m.sid = a.sid
                                                            AND S.year >= (%s) 
                                                            AND S.year <= (%s)
                                                            AND B.branch != 'Army'
                                                            AND B.branch != 'Navy'
                                                            AND B.branch != 'Marine Corps'
                                                            AND B.branch != 'All'
                                                        ''', year1,year2)  
                                    for result in cursor1:
                                        military.append(result) 
                                    cursor1.close()
                                    
                                elif airforce != "on":
                                    headings = ["Year", "Branch", "Count", "Rate", "Lower Enlisted", 
                                                "NCOs", "Officers", "Warrant Officers", 
                                                "Mental Health Diagnosis", "NO Mental Health Diagnosis",
                                                "TBI History", "NO TBI", "Previous Self-Harm", 
                                                "NO Previous Self-Harm", "Visited Health Services", "DID NOT visit",
                                                "Gun in Home", "No Gun in Home"]
                                    cursor1 = g.conn.execute('''SELECT S.year, B.branch, S.count, S.rate, 
                                                             R.e1_e4, R.e5_e9, R.officer, R.warrant_officer, M.health_diag_y,
                                                             M.health_diag_n, m.tbi_y, m.tbi_n, m.prev_self_harm_y, m.prev_self_harm_n,
                                                             m.health_ser_used_y, m.health_ser_used_n, a.in_home, a.not_in_home
                                                            FROM Suicides S, Military_Branch B, Rank R, Mental_Characteristics M, Access_To_Firearms A
                                                            WHERE s.sid = b.sid 
                                                            AND b.sid = r.sid
                                                            AND r.sid = m.sid
                                                            AND m.sid = a.sid
                                                            AND S.year >= (%s) 
                                                            AND S.year <= (%s)
                                                            AND B.branch != 'Army'
                                                            AND B.branch != 'Navy'
                                                            AND B.branch != 'Marine Corps'
                                                            AND B.branch != 'Air Force'
                                                            AND B.branch != 'All'
                                                        ''', year1,year2)  
                                    for result in cursor1:
                                        military.append(result) 
                                    cursor1.close()
            if showmh != "on":
                if combined == 'on':
                    if army == "on":
                        if navy =="on": 
                            if marines =="on": 
                                if airforce == "on":
                                    headings = ["Year", "Branch", "Count", "Rate", "Lower Enlisted", 
                                                "NCOs", "Officers", "Warrant Officers", 
                                                "Mental Health Diagnosis", "NO Mental Health Diagnosis",
                                                "TBI History", "NO TBI", "Previous Self-Harm", 
                                                "NO Previous Self-Harm", "Visited Health Services", "DID NOT visit",
                                                "Gun in Home", "No Gun in Home"]
                                    cursor1 = g.conn.execute('''SELECT S.year, B.branch, S.count, S.rate, 
                                                             R.e1_e4, R.e5_e9, R.officer, R.warrant_officer, M.health_diag_y,
                                                             M.health_diag_n, m.tbi_y, m.tbi_n, m.prev_self_harm_y, m.prev_self_harm_n,
                                                             m.health_ser_used_y, m.health_ser_used_n, a.in_home, a.not_in_home
                                                            FROM Suicides S, Military_Branch B, Rank R, Mental_Characteristics M, Access_To_Firearms A
                                                            WHERE s.sid = b.sid 
                                                            AND b.sid = r.sid
                                                            AND r.sid = m.sid
                                                            AND m.sid = a.sid
                                                            AND S.year >= (%s) 
                                                            AND S.year <= (%s)
                                                            ''', year1,year2)   
                                    for result in cursor1:
                                        military.append(result) 
                                    cursor1.close()
                                    
                                elif airforce != "on":
                                    headings = ["Year", "Branch", "Count", "Rate", "Lower Enlisted", 
                                                "NCOs", "Officers", "Warrant Officers", 
                                                "Mental Health Diagnosis", "NO Mental Health Diagnosis",
                                                "TBI History", "NO TBI", "Previous Self-Harm", 
                                                "NO Previous Self-Harm", "Visited Health Services", "DID NOT visit",
                                                "Gun in Home", "No Gun in Home"]
                                    cursor1 = g.conn.execute('''SELECT S.year, B.branch, S.count, S.rate, 
                                                             R.e1_e4, R.e5_e9, R.officer, R.warrant_officer, M.health_diag_y,
                                                             M.health_diag_n, m.tbi_y, m.tbi_n, m.prev_self_harm_y, m.prev_self_harm_n,
                                                             m.health_ser_used_y, m.health_ser_used_n, a.in_home, a.not_in_home
                                                            FROM Suicides S, Military_Branch B, Rank R, Mental_Characteristics M, Access_To_Firearms A
                                                            WHERE s.sid = b.sid 
                                                            AND b.sid = r.sid
                                                            AND r.sid = m.sid
                                                            AND m.sid = a.sid
                                                            AND S.year >= (%s) 
                                                            AND S.year <= (%s)
                                                            AND B.branch != 'Air Force'
                                                            ''', year1,year2)    
                                    for result in cursor1:
                                        military.append(result) 
                                    cursor1.close()
                                    
                            elif marines !="on": 
                                if airforce == "on":
                                    headings = ["Year", "Branch", "Count", "Rate", "Lower Enlisted", 
                                                "NCOs", "Officers", "Warrant Officers", 
                                                "Mental Health Diagnosis", "NO Mental Health Diagnosis",
                                                "TBI History", "NO TBI", "Previous Self-Harm", 
                                                "NO Previous Self-Harm", "Visited Health Services", "DID NOT visit",
                                                "Gun in Home", "No Gun in Home"]
                                    cursor1 = g.conn.execute('''SELECT S.year, B.branch, S.count, S.rate, 
                                                             R.e1_e4, R.e5_e9, R.officer, R.warrant_officer, M.health_diag_y,
                                                             M.health_diag_n, m.tbi_y, m.tbi_n, m.prev_self_harm_y, m.prev_self_harm_n,
                                                             m.health_ser_used_y, m.health_ser_used_n, a.in_home, a.not_in_home
                                                            FROM Suicides S, Military_Branch B, Rank R, Mental_Characteristics M, Access_To_Firearms A
                                                            WHERE s.sid = b.sid 
                                                            AND b.sid = r.sid
                                                            AND r.sid = m.sid
                                                            AND m.sid = a.sid
                                                            AND S.year >= (%s) 
                                                            AND S.year <= (%s)
                                                            AND B.branch != 'Marine Corps'
                                                            ''', year1,year2)    
                                    for result in cursor1:
                                        military.append(result) 
                                    cursor1.close()
                                    
                                elif airforce != "on":
                                    headings = ["Year", "Branch", "Count", "Rate", "Lower Enlisted", 
                                                "NCOs", "Officers", "Warrant Officers", 
                                                "Mental Health Diagnosis", "NO Mental Health Diagnosis",
                                                "TBI History", "NO TBI", "Previous Self-Harm", 
                                                "NO Previous Self-Harm", "Visited Health Services", "DID NOT visit",
                                                "Gun in Home", "No Gun in Home"]
                                    cursor1 = g.conn.execute('''SELECT S.year, B.branch, S.count, S.rate, 
                                                             R.e1_e4, R.e5_e9, R.officer, R.warrant_officer, M.health_diag_y,
                                                             M.health_diag_n, m.tbi_y, m.tbi_n, m.prev_self_harm_y, m.prev_self_harm_n,
                                                             m.health_ser_used_y, m.health_ser_used_n, a.in_home, a.not_in_home
                                                            FROM Suicides S, Military_Branch B, Rank R, Mental_Characteristics M, Access_To_Firearms A
                                                            WHERE s.sid = b.sid 
                                                            AND b.sid = r.sid
                                                            AND r.sid = m.sid
                                                            AND m.sid = a.sid
                                                            AND S.year >= (%s) 
                                                            AND S.year <= (%s)
                                                            AND B.branch != 'Air Force'
                                                            AND B.branch != 'Marine Corps'
                                                            ''', year1,year2)   
                                    for result in cursor1:
                                        military.append(result) 
                                    cursor1.close()
                                    
                        elif navy !="on": 
                            if marines =="on": 
                                if airforce == "on":
                                    headings = ["Year", "Branch", "Count", "Rate", "Lower Enlisted", 
                                                "NCOs", "Officers", "Warrant Officers", 
                                                "Mental Health Diagnosis", "NO Mental Health Diagnosis",
                                                "TBI History", "NO TBI", "Previous Self-Harm", 
                                                "NO Previous Self-Harm", "Visited Health Services", "DID NOT visit",
                                                "Gun in Home", "No Gun in Home"]
                                    cursor1 = g.conn.execute('''SELECT S.year, B.branch, S.count, S.rate, 
                                                             R.e1_e4, R.e5_e9, R.officer, R.warrant_officer, M.health_diag_y,
                                                             M.health_diag_n, m.tbi_y, m.tbi_n, m.prev_self_harm_y, m.prev_self_harm_n,
                                                             m.health_ser_used_y, m.health_ser_used_n, a.in_home, a.not_in_home
                                                            FROM Suicides S, Military_Branch B, Rank R, Mental_Characteristics M, Access_To_Firearms A
                                                            WHERE s.sid = b.sid 
                                                            AND b.sid = r.sid
                                                            AND r.sid = m.sid
                                                            AND m.sid = a.sid
                                                            AND S.year >= (%s) 
                                                            AND S.year <= (%s)
                                                            AND B.branch != 'Navy'
                                                            ''', year1,year2)  
                                    for result in cursor1:
                                        military.append(result) 
                                    cursor1.close()
                                    
                                elif airforce != "on":
                                    headings = ["Year", "Branch", "Count", "Rate", "Lower Enlisted", 
                                                "NCOs", "Officers", "Warrant Officers", 
                                                "Mental Health Diagnosis", "NO Mental Health Diagnosis",
                                                "TBI History", "NO TBI", "Previous Self-Harm", 
                                                "NO Previous Self-Harm", "Visited Health Services", "DID NOT visit",
                                                "Gun in Home", "No Gun in Home"]
                                    cursor1 = g.conn.execute('''SELECT S.year, B.branch, S.count, S.rate, 
                                                             R.e1_e4, R.e5_e9, R.officer, R.warrant_officer, M.health_diag_y,
                                                             M.health_diag_n, m.tbi_y, m.tbi_n, m.prev_self_harm_y, m.prev_self_harm_n,
                                                             m.health_ser_used_y, m.health_ser_used_n, a.in_home, a.not_in_home
                                                            FROM Suicides S, Military_Branch B, Rank R, Mental_Characteristics M, Access_To_Firearms A
                                                            WHERE s.sid = b.sid 
                                                            AND b.sid = r.sid
                                                            AND r.sid = m.sid
                                                            AND m.sid = a.sid
                                                            AND S.year >= (%s) 
                                                            AND S.year <= (%s)
                                                            AND B.branch != 'Navy'
                                                            AND B.branch != 'Air Force'
                                                            ''', year1,year2)  
                                    for result in cursor1:
                                        military.append(result) 
                                    cursor1.close()
                                    
                            elif marines !="on": 
                                if airforce == "on":
                                    headings = ["Year", "Branch", "Count", "Rate", "Lower Enlisted", 
                                                "NCOs", "Officers", "Warrant Officers", 
                                                "Mental Health Diagnosis", "NO Mental Health Diagnosis",
                                                "TBI History", "NO TBI", "Previous Self-Harm", 
                                                "NO Previous Self-Harm", "Visited Health Services", "DID NOT visit",
                                                "Gun in Home", "No Gun in Home"]
                                    cursor1 = g.conn.execute('''SELECT S.year, B.branch, S.count, S.rate, 
                                                             R.e1_e4, R.e5_e9, R.officer, R.warrant_officer, M.health_diag_y,
                                                             M.health_diag_n, m.tbi_y, m.tbi_n, m.prev_self_harm_y, m.prev_self_harm_n,
                                                             m.health_ser_used_y, m.health_ser_used_n, a.in_home, a.not_in_home
                                                            FROM Suicides S, Military_Branch B, Rank R, Mental_Characteristics M, Access_To_Firearms A
                                                            WHERE s.sid = b.sid 
                                                            AND b.sid = r.sid
                                                            AND r.sid = m.sid
                                                            AND m.sid = a.sid
                                                            AND S.year >= (%s) 
                                                            AND S.year <= (%s)
                                                            AND B.branch != 'Navy'
                                                            AND B.branch != 'Marine Corps'
                                                             ''', year1,year2)
                                    for result in cursor1:
                                        military.append(result) 
                                    cursor1.close()
                                    
                                elif airforce != "on":
                                    headings = ["Year", "Branch", "Count", "Rate", "Lower Enlisted", 
                                                "NCOs", "Officers", "Warrant Officers", 
                                                "Mental Health Diagnosis", "NO Mental Health Diagnosis",
                                                "TBI History", "NO TBI", "Previous Self-Harm", 
                                                "NO Previous Self-Harm", "Visited Health Services", "DID NOT visit",
                                                "Gun in Home", "No Gun in Home"]
                                    cursor1 = g.conn.execute('''SELECT S.year, B.branch, S.count, S.rate, 
                                                             R.e1_e4, R.e5_e9, R.officer, R.warrant_officer, M.health_diag_y,
                                                             M.health_diag_n, m.tbi_y, m.tbi_n, m.prev_self_harm_y, m.prev_self_harm_n,
                                                             m.health_ser_used_y, m.health_ser_used_n, a.in_home, a.not_in_home
                                                            FROM Suicides S, Military_Branch B, Rank R, Mental_Characteristics M, Access_To_Firearms A
                                                            WHERE s.sid = b.sid 
                                                            AND b.sid = r.sid
                                                            AND r.sid = m.sid
                                                            AND m.sid = a.sid
                                                            AND S.year >= (%s) 
                                                            AND S.year <= (%s)
                                                            AND B.branch != 'Navy'
                                                            AND B.branch != 'Marine Corps'
                                                            AND B.branch != 'Air Force'
                                                        ''', year1,year2)  
                                    for result in cursor1:
                                        military.append(result) 
                                    cursor1.close()
                                    
                    elif army !="on":
                        if navy =="on": 
                            if marines =="on": 
                                if airforce == "on":
                                    headings = ["Year", "Branch", "Count", "Rate", "Lower Enlisted", 
                                                "NCOs", "Officers", "Warrant Officers", 
                                                "Mental Health Diagnosis", "NO Mental Health Diagnosis",
                                                "TBI History", "NO TBI", "Previous Self-Harm", 
                                                "NO Previous Self-Harm", "Visited Health Services", "DID NOT visit",
                                                "Gun in Home", "No Gun in Home"]
                                    cursor1 = g.conn.execute('''SELECT S.year, B.branch, S.count, S.rate, 
                                                             R.e1_e4, R.e5_e9, R.officer, R.warrant_officer, M.health_diag_y,
                                                             M.health_diag_n, m.tbi_y, m.tbi_n, m.prev_self_harm_y, m.prev_self_harm_n,
                                                             m.health_ser_used_y, m.health_ser_used_n, a.in_home, a.not_in_home
                                                            FROM Suicides S, Military_Branch B, Rank R, Mental_Characteristics M, Access_To_Firearms A
                                                            WHERE s.sid = b.sid 
                                                            AND b.sid = r.sid
                                                            AND r.sid = m.sid
                                                            AND m.sid = a.sid
                                                            AND S.year >= (%s) 
                                                            AND S.year <= (%s)
                                                            AND B.branch != 'Army'
                                                            AND B.branch != 'Navy'
                                                            AND B.branch != 'Marine Corps'
                                                            AND B.branch != 'Air Force'
                                                        ''', year1,year2)  
                                    for result in cursor1:
                                        military.append(result) 
                                    cursor1.close()
                                    
                                elif airforce != "on":
                                    headings = ["Year", "Branch", "Count", "Rate", "Lower Enlisted", 
                                                "NCOs", "Officers", "Warrant Officers", 
                                                "Mental Health Diagnosis", "NO Mental Health Diagnosis",
                                                "TBI History", "NO TBI", "Previous Self-Harm", 
                                                "NO Previous Self-Harm", "Visited Health Services", "DID NOT visit",
                                                "Gun in Home", "No Gun in Home"]
                                    cursor1 = g.conn.execute('''SELECT S.year, B.branch, S.count, S.rate, 
                                                             R.e1_e4, R.e5_e9, R.officer, R.warrant_officer, M.health_diag_y,
                                                             M.health_diag_n, m.tbi_y, m.tbi_n, m.prev_self_harm_y, m.prev_self_harm_n,
                                                             m.health_ser_used_y, m.health_ser_used_n, a.in_home, a.not_in_home
                                                            FROM Suicides S, Military_Branch B, Rank R, Mental_Characteristics M, Access_To_Firearms A
                                                            WHERE s.sid = b.sid 
                                                            AND b.sid = r.sid
                                                            AND r.sid = m.sid
                                                            AND m.sid = a.sid
                                                            AND S.year >= (%s) 
                                                            AND S.year <= (%s)
                                                            AND B.branch != 'Army'
                                                            AND B.branch != 'Air Force'
                                                        ''', year1,year2)  
                                    for result in cursor1:
                                        military.append(result) 
                                    cursor1.close()
                                    
                            elif marines !="on": 
                                if airforce == "on":
                                    headings = ["Year", "Branch", "Count", "Rate", "Lower Enlisted", 
                                                "NCOs", "Officers", "Warrant Officers", 
                                                "Mental Health Diagnosis", "NO Mental Health Diagnosis",
                                                "TBI History", "NO TBI", "Previous Self-Harm", 
                                                "NO Previous Self-Harm", "Visited Health Services", "DID NOT visit",
                                                "Gun in Home", "No Gun in Home"]
                                    cursor1 = g.conn.execute('''SELECT S.year, B.branch, S.count, S.rate, 
                                                             R.e1_e4, R.e5_e9, R.officer, R.warrant_officer, M.health_diag_y,
                                                             M.health_diag_n, m.tbi_y, m.tbi_n, m.prev_self_harm_y, m.prev_self_harm_n,
                                                             m.health_ser_used_y, m.health_ser_used_n, a.in_home, a.not_in_home
                                                            FROM Suicides S, Military_Branch B, Rank R, Mental_Characteristics M, Access_To_Firearms A
                                                            WHERE s.sid = b.sid 
                                                            AND b.sid = r.sid
                                                            AND r.sid = m.sid
                                                            AND m.sid = a.sid
                                                            AND S.year >= (%s) 
                                                            AND S.year <= (%s)
                                                            AND B.branch != 'Army'
                                                            AND B.branch != 'Marine Corps'
                                                        ''', year1,year2)  
                                    for result in cursor1:
                                        military.append(result) 
                                    cursor1.close()
                                    
                                elif airforce != "on":
                                    headings = ["Year", "Branch", "Count", "Rate", "Lower Enlisted", 
                                                "NCOs", "Officers", "Warrant Officers", 
                                                "Mental Health Diagnosis", "NO Mental Health Diagnosis",
                                                "TBI History", "NO TBI", "Previous Self-Harm", 
                                                "NO Previous Self-Harm", "Visited Health Services", "DID NOT visit",
                                                "Gun in Home", "No Gun in Home"]
                                    cursor1 = g.conn.execute('''SELECT S.year, B.branch, S.count, S.rate, 
                                                             R.e1_e4, R.e5_e9, R.officer, R.warrant_officer, M.health_diag_y,
                                                             M.health_diag_n, m.tbi_y, m.tbi_n, m.prev_self_harm_y, m.prev_self_harm_n,
                                                             m.health_ser_used_y, m.health_ser_used_n, a.in_home, a.not_in_home
                                                            FROM Suicides S, Military_Branch B, Rank R, Mental_Characteristics M, Access_To_Firearms A
                                                            WHERE s.sid = b.sid 
                                                            AND b.sid = r.sid
                                                            AND r.sid = m.sid
                                                            AND m.sid = a.sid
                                                            AND S.year >= (%s) 
                                                            AND S.year <= (%s)
                                                        AND B.branch != 'Army'
                                                        AND B.branch != 'Marine Corps'
                                                        AND B.branch != 'Air Force'
                                                        ''', year1,year2)  
                                    for result in cursor1:
                                        military.append(result) 
                                    cursor1.close()
                                    
                        elif navy !="on": 
                            if marines =="on": 
                                if airforce == "on":
                                    headings = ["Year", "Branch", "Count", "Rate", "Lower Enlisted", 
                                                "NCOs", "Officers", "Warrant Officers", 
                                                "Mental Health Diagnosis", "NO Mental Health Diagnosis",
                                                "TBI History", "NO TBI", "Previous Self-Harm", 
                                                "NO Previous Self-Harm", "Visited Health Services", "DID NOT visit",
                                                "Gun in Home", "No Gun in Home"]
                                    cursor1 = g.conn.execute('''SELECT S.year, B.branch, S.count, S.rate, 
                                                             R.e1_e4, R.e5_e9, R.officer, R.warrant_officer, M.health_diag_y,
                                                             M.health_diag_n, m.tbi_y, m.tbi_n, m.prev_self_harm_y, m.prev_self_harm_n,
                                                             m.health_ser_used_y, m.health_ser_used_n, a.in_home, a.not_in_home
                                                            FROM Suicides S, Military_Branch B, Rank R, Mental_Characteristics M, Access_To_Firearms A
                                                            WHERE s.sid = b.sid 
                                                            AND b.sid = r.sid
                                                            AND r.sid = m.sid
                                                            AND m.sid = a.sid
                                                            AND S.year >= (%s) 
                                                            AND S.year <= (%s)
                                                            AND B.branch != 'Army'
                                                            AND B.branch != 'Navy'
                                                        ''', year1,year2)  
                                    for result in cursor1:
                                        military.append(result) 
                                    cursor1.close()
                                    
                                elif airforce != "on":
                                    headings = ["Year", "Branch", "Count", "Rate", "Lower Enlisted", 
                                                "NCOs", "Officers", "Warrant Officers", 
                                                "Mental Health Diagnosis", "NO Mental Health Diagnosis",
                                                "TBI History", "NO TBI", "Previous Self-Harm", 
                                                "NO Previous Self-Harm", "Visited Health Services", "DID NOT visit",
                                                "Gun in Home", "No Gun in Home"]
                                    cursor1 = g.conn.execute('''SELECT S.year, B.branch, S.count, S.rate, 
                                                             R.e1_e4, R.e5_e9, R.officer, R.warrant_officer, M.health_diag_y,
                                                             M.health_diag_n, m.tbi_y, m.tbi_n, m.prev_self_harm_y, m.prev_self_harm_n,
                                                             m.health_ser_used_y, m.health_ser_used_n, a.in_home, a.not_in_home
                                                            FROM Suicides S, Military_Branch B, Rank R, Mental_Characteristics M, Access_To_Firearms A
                                                            WHERE s.sid = b.sid 
                                                            AND b.sid = r.sid
                                                            AND r.sid = m.sid
                                                            AND m.sid = a.sid
                                                            AND S.year >= (%s) 
                                                            AND S.year <= (%s)
                                                            AND B.branch != 'Army'
                                                            AND B.branch != 'Navy'
                                                            AND B.branch != 'Air Force'
                                                        ''', year1,year2)  
                                    for result in cursor1:
                                        military.append(result) 
                                    cursor1.close()
                                    
                            elif marines !="on": 
                                if airforce == "on":
                                    headings = ["Year", "Branch", "Count", "Rate", "Lower Enlisted", 
                                                "NCOs", "Officers", "Warrant Officers", 
                                                "Mental Health Diagnosis", "NO Mental Health Diagnosis",
                                                "TBI History", "NO TBI", "Previous Self-Harm", 
                                                "NO Previous Self-Harm", "Visited Health Services", "DID NOT visit",
                                                "Gun in Home", "No Gun in Home"]
                                    cursor1 = g.conn.execute('''SELECT S.year, B.branch, S.count, S.rate, 
                                                             R.e1_e4, R.e5_e9, R.officer, R.warrant_officer, M.health_diag_y,
                                                             M.health_diag_n, m.tbi_y, m.tbi_n, m.prev_self_harm_y, m.prev_self_harm_n,
                                                             m.health_ser_used_y, m.health_ser_used_n, a.in_home, a.not_in_home
                                                            FROM Suicides S, Military_Branch B, Rank R, Mental_Characteristics M, Access_To_Firearms A
                                                            WHERE s.sid = b.sid 
                                                            AND b.sid = r.sid
                                                            AND r.sid = m.sid
                                                            AND m.sid = a.sid
                                                            AND S.year >= (%s) 
                                                            AND S.year <= (%s)
                                                            AND B.branch != 'Army'
                                                            AND B.branch != 'Navy'
                                                            AND B.branch != 'Marine Corps'
                                                        ''', year1,year2)  
                                    for result in cursor1:
                                        military.append(result) 
                                    cursor1.close()
                                    
                                elif airforce != "on":
                                    headings = ["Year", "Branch", "Count", "Rate", "Lower Enlisted", 
                                                "NCOs", "Officers", "Warrant Officers", 
                                                "Mental Health Diagnosis", "NO Mental Health Diagnosis",
                                                "TBI History", "NO TBI", "Previous Self-Harm", 
                                                "NO Previous Self-Harm", "Visited Health Services", "DID NOT visit",
                                                "Gun in Home", "No Gun in Home"]
                                    cursor1 = g.conn.execute('''SELECT S.year, B.branch, S.count, S.rate, 
                                                             R.e1_e4, R.e5_e9, R.officer, R.warrant_officer, M.health_diag_y,
                                                             M.health_diag_n, m.tbi_y, m.tbi_n, m.prev_self_harm_y, m.prev_self_harm_n,
                                                             m.health_ser_used_y, m.health_ser_used_n, a.in_home, a.not_in_home
                                                            FROM Suicides S, Military_Branch B, Rank R, Mental_Characteristics M, Access_To_Firearms A
                                                            WHERE s.sid = b.sid 
                                                            AND b.sid = r.sid
                                                            AND r.sid = m.sid
                                                            AND m.sid = a.sid
                                                            AND S.year >= (%s) 
                                                            AND S.year <= (%s)
                                                            AND B.branch != 'Army'
                                                            AND B.branch != 'Navy'
                                                            AND B.branch != 'Marine Corps'
                                                            AND B.branch != 'Air Force'
                                                        ''', year1,year2)  
                                    for result in cursor1:
                                        military.append(result) 
                                    cursor1.close()
                if combined != 'on':
                    if army == "on":
                        if navy =="on": 
                            if marines =="on": 
                                if airforce == "on":
                                    headings = ["Year", "Branch", "Count", "Rate", "Lower Enlisted", 
                                                "NCOs", "Officers", "Warrant Officers", 
                                                "Mental Health Diagnosis", "NO Mental Health Diagnosis",
                                                "TBI History", "NO TBI", "Previous Self-Harm", 
                                                "NO Previous Self-Harm", "Visited Health Services", "DID NOT visit",
                                                "Gun in Home", "No Gun in Home"]
                                    cursor1 = g.conn.execute('''SELECT S.year, B.branch, S.count, S.rate, 
                                                             R.e1_e4, R.e5_e9, R.officer, R.warrant_officer, M.health_diag_y,
                                                             M.health_diag_n, m.tbi_y, m.tbi_n, m.prev_self_harm_y, m.prev_self_harm_n,
                                                             m.health_ser_used_y, m.health_ser_used_n, a.in_home, a.not_in_home
                                                            FROM Suicides S, Military_Branch B, Rank R, Mental_Characteristics M, Access_To_Firearms A
                                                            WHERE s.sid = b.sid 
                                                            AND b.sid = r.sid
                                                            AND r.sid = m.sid
                                                            AND m.sid = a.sid
                                                            AND S.year >= (%s) 
                                                            AND S.year <= (%s)
                                                            AND B.branch != 'All'
                                                            ''', year1,year2)   
                                    for result in cursor1:
                                        military.append(result) 
                                    cursor1.close()
                                    
                                elif airforce != "on":
                                    headings = ["Year", "Branch", "Count", "Rate", "Lower Enlisted", 
                                                "NCOs", "Officers", "Warrant Officers", 
                                                "Mental Health Diagnosis", "NO Mental Health Diagnosis",
                                                "TBI History", "NO TBI", "Previous Self-Harm", 
                                                "NO Previous Self-Harm", "Visited Health Services", "DID NOT visit",
                                                "Gun in Home", "No Gun in Home"]
                                    cursor1 = g.conn.execute('''SELECT S.year, B.branch, S.count, S.rate, 
                                                             R.e1_e4, R.e5_e9, R.officer, R.warrant_officer, M.health_diag_y,
                                                             M.health_diag_n, m.tbi_y, m.tbi_n, m.prev_self_harm_y, m.prev_self_harm_n,
                                                             m.health_ser_used_y, m.health_ser_used_n, a.in_home, a.not_in_home
                                                            FROM Suicides S, Military_Branch B, Rank R, Mental_Characteristics M, Access_To_Firearms A
                                                            WHERE s.sid = b.sid 
                                                            AND b.sid = r.sid
                                                            AND r.sid = m.sid
                                                            AND m.sid = a.sid
                                                            AND S.year >= (%s) 
                                                            AND S.year <= (%s)
                                                            AND B.branch != 'Air Force'
                                                            AND B.branch != 'All'
                                                            ''', year1,year2)    
                                    for result in cursor1:
                                        military.append(result) 
                                    cursor1.close()
                                    
                            elif marines !="on": 
                                if airforce == "on":
                                    headings = ["Year", "Branch", "Count", "Rate", "Lower Enlisted", 
                                                "NCOs", "Officers", "Warrant Officers", 
                                                "Mental Health Diagnosis", "NO Mental Health Diagnosis",
                                                "TBI History", "NO TBI", "Previous Self-Harm", 
                                                "NO Previous Self-Harm", "Visited Health Services", "DID NOT visit",
                                                "Gun in Home", "No Gun in Home"]
                                    cursor1 = g.conn.execute('''SELECT S.year, B.branch, S.count, S.rate, 
                                                             R.e1_e4, R.e5_e9, R.officer, R.warrant_officer, M.health_diag_y,
                                                             M.health_diag_n, m.tbi_y, m.tbi_n, m.prev_self_harm_y, m.prev_self_harm_n,
                                                             m.health_ser_used_y, m.health_ser_used_n, a.in_home, a.not_in_home
                                                            FROM Suicides S, Military_Branch B, Rank R, Mental_Characteristics M, Access_To_Firearms A
                                                            WHERE s.sid = b.sid 
                                                            AND b.sid = r.sid
                                                            AND r.sid = m.sid
                                                            AND m.sid = a.sid
                                                            AND S.year >= (%s) 
                                                            AND S.year <= (%s)
                                                            AND B.branch != 'Marine Corps'
                                                            AND B.branch != 'All'
                                                            ''', year1,year2)    
                                    for result in cursor1:
                                        military.append(result) 
                                    cursor1.close()
                                    
                                elif airforce != "on":
                                    headings = ["Year", "Branch", "Count", "Rate", "Lower Enlisted", 
                                                "NCOs", "Officers", "Warrant Officers", 
                                                "Mental Health Diagnosis", "NO Mental Health Diagnosis",
                                                "TBI History", "NO TBI", "Previous Self-Harm", 
                                                "NO Previous Self-Harm", "Visited Health Services", "DID NOT visit",
                                                "Gun in Home", "No Gun in Home"]
                                    cursor1 = g.conn.execute('''SELECT S.year, B.branch, S.count, S.rate, 
                                                             R.e1_e4, R.e5_e9, R.officer, R.warrant_officer, M.health_diag_y,
                                                             M.health_diag_n, m.tbi_y, m.tbi_n, m.prev_self_harm_y, m.prev_self_harm_n,
                                                             m.health_ser_used_y, m.health_ser_used_n, a.in_home, a.not_in_home
                                                            FROM Suicides S, Military_Branch B, Rank R, Mental_Characteristics M, Access_To_Firearms A
                                                            WHERE s.sid = b.sid 
                                                            AND b.sid = r.sid
                                                            AND r.sid = m.sid
                                                            AND m.sid = a.sid
                                                            AND S.year >= (%s) 
                                                            AND S.year <= (%s)
                                                            AND B.branch != 'Air Force'
                                                            AND B.branch != 'Marine Corps'
                                                            AND B.branch != 'All'
                                                            ''', year1,year2)   
                                    for result in cursor1:
                                        military.append(result) 
                                    cursor1.close()
                                    
                        elif navy !="on": 
                            if marines =="on": 
                                if airforce == "on":
                                    headings = ["Year", "Branch", "Count", "Rate", "Lower Enlisted", 
                                                "NCOs", "Officers", "Warrant Officers", 
                                                "Mental Health Diagnosis", "NO Mental Health Diagnosis",
                                                "TBI History", "NO TBI", "Previous Self-Harm", 
                                                "NO Previous Self-Harm", "Visited Health Services", "DID NOT visit",
                                                "Gun in Home", "No Gun in Home"]
                                    cursor1 = g.conn.execute('''SELECT S.year, B.branch, S.count, S.rate, 
                                                             R.e1_e4, R.e5_e9, R.officer, R.warrant_officer, M.health_diag_y,
                                                             M.health_diag_n, m.tbi_y, m.tbi_n, m.prev_self_harm_y, m.prev_self_harm_n,
                                                             m.health_ser_used_y, m.health_ser_used_n, a.in_home, a.not_in_home
                                                            FROM Suicides S, Military_Branch B, Rank R, Mental_Characteristics M, Access_To_Firearms A
                                                            WHERE s.sid = b.sid 
                                                            AND b.sid = r.sid
                                                            AND r.sid = m.sid
                                                            AND m.sid = a.sid
                                                            AND S.year >= (%s) 
                                                            AND S.year <= (%s)
                                                            AND B.branch != 'Navy'
                                                            AND B.branch != 'All'
                                                            ''', year1,year2)  
                                    for result in cursor1:
                                        military.append(result) 
                                    cursor1.close()
                                    
                                elif airforce != "on":
                                    headings = ["Year", "Branch", "Count", "Rate", "Lower Enlisted", 
                                                "NCOs", "Officers", "Warrant Officers", 
                                                "Mental Health Diagnosis", "NO Mental Health Diagnosis",
                                                "TBI History", "NO TBI", "Previous Self-Harm", 
                                                "NO Previous Self-Harm", "Visited Health Services", "DID NOT visit",
                                                "Gun in Home", "No Gun in Home"]
                                    cursor1 = g.conn.execute('''SELECT S.year, B.branch, S.count, S.rate, 
                                                             R.e1_e4, R.e5_e9, R.officer, R.warrant_officer, M.health_diag_y,
                                                             M.health_diag_n, m.tbi_y, m.tbi_n, m.prev_self_harm_y, m.prev_self_harm_n,
                                                             m.health_ser_used_y, m.health_ser_used_n, a.in_home, a.not_in_home
                                                            FROM Suicides S, Military_Branch B, Rank R, Mental_Characteristics M, Access_To_Firearms A
                                                            WHERE s.sid = b.sid 
                                                            AND b.sid = r.sid
                                                            AND r.sid = m.sid
                                                            AND m.sid = a.sid
                                                            AND S.year >= (%s) 
                                                            AND S.year <= (%s)
                                                            AND B.branch != 'Navy'
                                                            AND B.branch != 'Air Force'
                                                            AND B.branch != 'All'
                                                            ''', year1,year2)  
                                    for result in cursor1:
                                        military.append(result) 
                                    cursor1.close()
                                    
                            elif marines !="on": 
                                if airforce == "on":
                                    headings = ["Year", "Branch", "Count", "Rate", "Lower Enlisted", 
                                                "NCOs", "Officers", "Warrant Officers", 
                                                "Mental Health Diagnosis", "NO Mental Health Diagnosis",
                                                "TBI History", "NO TBI", "Previous Self-Harm", 
                                                "NO Previous Self-Harm", "Visited Health Services", "DID NOT visit",
                                                "Gun in Home", "No Gun in Home"]
                                    cursor1 = g.conn.execute('''SELECT S.year, B.branch, S.count, S.rate, 
                                                             R.e1_e4, R.e5_e9, R.officer, R.warrant_officer, M.health_diag_y,
                                                             M.health_diag_n, m.tbi_y, m.tbi_n, m.prev_self_harm_y, m.prev_self_harm_n,
                                                             m.health_ser_used_y, m.health_ser_used_n, a.in_home, a.not_in_home
                                                            FROM Suicides S, Military_Branch B, Rank R, Mental_Characteristics M, Access_To_Firearms A
                                                            WHERE s.sid = b.sid 
                                                            AND b.sid = r.sid
                                                            AND r.sid = m.sid
                                                            AND m.sid = a.sid
                                                            AND S.year >= (%s) 
                                                            AND S.year <= (%s)
                                                            AND B.branch != 'Navy'
                                                            AND B.branch != 'Marine Corps'
                                                            AND B.branch != 'All'
                                                             ''', year1,year2)
                                    for result in cursor1:
                                        military.append(result) 
                                    cursor1.close()
                                    
                                elif airforce != "on":
                                    headings = ["Year", "Branch", "Count", "Rate", "Lower Enlisted", 
                                                "NCOs", "Officers", "Warrant Officers", 
                                                "Mental Health Diagnosis", "NO Mental Health Diagnosis",
                                                "TBI History", "NO TBI", "Previous Self-Harm", 
                                                "NO Previous Self-Harm", "Visited Health Services", "DID NOT visit",
                                                "Gun in Home", "No Gun in Home"]
                                    cursor1 = g.conn.execute('''SELECT S.year, B.branch, S.count, S.rate, 
                                                             R.e1_e4, R.e5_e9, R.officer, R.warrant_officer, M.health_diag_y,
                                                             M.health_diag_n, m.tbi_y, m.tbi_n, m.prev_self_harm_y, m.prev_self_harm_n,
                                                             m.health_ser_used_y, m.health_ser_used_n, a.in_home, a.not_in_home
                                                            FROM Suicides S, Military_Branch B, Rank R, Mental_Characteristics M, Access_To_Firearms A
                                                            WHERE s.sid = b.sid 
                                                            AND b.sid = r.sid
                                                            AND r.sid = m.sid
                                                            AND m.sid = a.sid
                                                            AND S.year >= (%s) 
                                                            AND S.year <= (%s)
                                                            AND B.branch != 'Navy'
                                                            AND B.branch != 'Marine Corps'
                                                            AND B.branch != 'Air Force'
                                                            AND B.branch != 'All'
                                                        ''', year1,year2)  
                                    for result in cursor1:
                                        military.append(result) 
                                    cursor1.close()
                                    
                    elif army !="on":
                        if navy =="on": 
                            if marines =="on": 
                                if airforce == "on":
                                    headings = ["Year", "Branch", "Count", "Rate", "Lower Enlisted", 
                                                "NCOs", "Officers", "Warrant Officers", 
                                                "Mental Health Diagnosis", "NO Mental Health Diagnosis",
                                                "TBI History", "NO TBI", "Previous Self-Harm", 
                                                "NO Previous Self-Harm", "Visited Health Services", "DID NOT visit",
                                                "Gun in Home", "No Gun in Home"]
                                    cursor1 = g.conn.execute('''SELECT S.year, B.branch, S.count, S.rate, 
                                                             R.e1_e4, R.e5_e9, R.officer, R.warrant_officer, M.health_diag_y,
                                                             M.health_diag_n, m.tbi_y, m.tbi_n, m.prev_self_harm_y, m.prev_self_harm_n,
                                                             m.health_ser_used_y, m.health_ser_used_n, a.in_home, a.not_in_home
                                                            FROM Suicides S, Military_Branch B, Rank R, Mental_Characteristics M, Access_To_Firearms A
                                                            WHERE s.sid = b.sid 
                                                            AND b.sid = r.sid
                                                            AND r.sid = m.sid
                                                            AND m.sid = a.sid
                                                            AND S.year >= (%s) 
                                                            AND S.year <= (%s)
                                                            AND B.branch != 'Army'
                                                            AND B.branch != 'Navy'
                                                            AND B.branch != 'Marine Corps'
                                                            AND B.branch != 'Air Force'
                                                            AND B.branch != 'All'
                                                        ''', year1,year2)  
                                    for result in cursor1:
                                        military.append(result) 
                                    cursor1.close()
                                    
                                elif airforce != "on":
                                    headings = ["Year", "Branch", "Count", "Rate", "Lower Enlisted", 
                                                "NCOs", "Officers", "Warrant Officers", 
                                                "Mental Health Diagnosis", "NO Mental Health Diagnosis",
                                                "TBI History", "NO TBI", "Previous Self-Harm", 
                                                "NO Previous Self-Harm", "Visited Health Services", "DID NOT visit",
                                                "Gun in Home", "No Gun in Home"]
                                    cursor1 = g.conn.execute('''SELECT S.year, B.branch, S.count, S.rate, 
                                                             R.e1_e4, R.e5_e9, R.officer, R.warrant_officer, M.health_diag_y,
                                                             M.health_diag_n, m.tbi_y, m.tbi_n, m.prev_self_harm_y, m.prev_self_harm_n,
                                                             m.health_ser_used_y, m.health_ser_used_n, a.in_home, a.not_in_home
                                                            FROM Suicides S, Military_Branch B, Rank R, Mental_Characteristics M, Access_To_Firearms A
                                                            WHERE s.sid = b.sid 
                                                            AND b.sid = r.sid
                                                            AND r.sid = m.sid
                                                            AND m.sid = a.sid
                                                            AND S.year >= (%s) 
                                                            AND S.year <= (%s)
                                                            AND B.branch != 'Army'
                                                            AND B.branch != 'Air Force'
                                                            AND B.branch != 'All'
                                                        ''', year1,year2)  
                                    for result in cursor1:
                                        military.append(result) 
                                    cursor1.close()
                                    
                            elif marines !="on": 
                                if airforce == "on":
                                    headings = ["Year", "Branch", "Count", "Rate", "Lower Enlisted", 
                                                "NCOs", "Officers", "Warrant Officers", 
                                                "Mental Health Diagnosis", "NO Mental Health Diagnosis",
                                                "TBI History", "NO TBI", "Previous Self-Harm", 
                                                "NO Previous Self-Harm", "Visited Health Services", "DID NOT visit",
                                                "Gun in Home", "No Gun in Home"]
                                    cursor1 = g.conn.execute('''SELECT S.year, B.branch, S.count, S.rate, 
                                                             R.e1_e4, R.e5_e9, R.officer, R.warrant_officer, M.health_diag_y,
                                                             M.health_diag_n, m.tbi_y, m.tbi_n, m.prev_self_harm_y, m.prev_self_harm_n,
                                                             m.health_ser_used_y, m.health_ser_used_n, a.in_home, a.not_in_home
                                                            FROM Suicides S, Military_Branch B, Rank R, Mental_Characteristics M, Access_To_Firearms A
                                                            WHERE s.sid = b.sid 
                                                            AND b.sid = r.sid
                                                            AND r.sid = m.sid
                                                            AND m.sid = a.sid
                                                            AND S.year >= (%s) 
                                                            AND S.year <= (%s)
                                                            AND B.branch != 'Army'
                                                            AND B.branch != 'Marine Corps'
                                                            AND B.branch != 'All'
                                                        ''', year1,year2)  
                                    for result in cursor1:
                                        military.append(result) 
                                    cursor1.close()
                                    
                                elif airforce != "on":
                                    headings = ["Year", "Branch", "Count", "Rate", "Lower Enlisted", 
                                                "NCOs", "Officers", "Warrant Officers", 
                                                "Mental Health Diagnosis", "NO Mental Health Diagnosis",
                                                "TBI History", "NO TBI", "Previous Self-Harm", 
                                                "NO Previous Self-Harm", "Visited Health Services", "DID NOT visit",
                                                "Gun in Home", "No Gun in Home"]
                                    cursor1 = g.conn.execute('''SELECT S.year, B.branch, S.count, S.rate, 
                                                             R.e1_e4, R.e5_e9, R.officer, R.warrant_officer, M.health_diag_y,
                                                             M.health_diag_n, m.tbi_y, m.tbi_n, m.prev_self_harm_y, m.prev_self_harm_n,
                                                             m.health_ser_used_y, m.health_ser_used_n, a.in_home, a.not_in_home
                                                            FROM Suicides S, Military_Branch B, Rank R, Mental_Characteristics M, Access_To_Firearms A
                                                            WHERE s.sid = b.sid 
                                                            AND b.sid = r.sid
                                                            AND r.sid = m.sid
                                                            AND m.sid = a.sid
                                                            AND S.year >= (%s) 
                                                            AND S.year <= (%s)
                                                        AND B.branch != 'Army'
                                                        AND B.branch != 'Marine Corps'
                                                        AND B.branch != 'Air Force'
                                                            AND B.branch != 'All'
                                                        ''', year1,year2)  
                                    for result in cursor1:
                                        military.append(result) 
                                    cursor1.close()
                                    
                        elif navy !="on": 
                            if marines =="on": 
                                if airforce == "on":
                                    headings = ["Year", "Branch", "Count", "Rate", "Lower Enlisted", 
                                                "NCOs", "Officers", "Warrant Officers", 
                                                "Mental Health Diagnosis", "NO Mental Health Diagnosis",
                                                "TBI History", "NO TBI", "Previous Self-Harm", 
                                                "NO Previous Self-Harm", "Visited Health Services", "DID NOT visit",
                                                "Gun in Home", "No Gun in Home"]
                                    cursor1 = g.conn.execute('''SELECT S.year, B.branch, S.count, S.rate, 
                                                             R.e1_e4, R.e5_e9, R.officer, R.warrant_officer, M.health_diag_y,
                                                             M.health_diag_n, m.tbi_y, m.tbi_n, m.prev_self_harm_y, m.prev_self_harm_n,
                                                             m.health_ser_used_y, m.health_ser_used_n, a.in_home, a.not_in_home
                                                            FROM Suicides S, Military_Branch B, Rank R, Mental_Characteristics M, Access_To_Firearms A
                                                            WHERE s.sid = b.sid 
                                                            AND b.sid = r.sid
                                                            AND r.sid = m.sid
                                                            AND m.sid = a.sid
                                                            AND S.year >= (%s) 
                                                            AND S.year <= (%s)
                                                            AND B.branch != 'Army'
                                                            AND B.branch != 'Navy'
                                                            AND B.branch != 'All'
                                                        ''', year1,year2)  
                                    for result in cursor1:
                                        military.append(result) 
                                    cursor1.close()
                                    
                                elif airforce != "on":
                                    headings = ["Year", "Branch", "Count", "Rate", "Lower Enlisted", 
                                                "NCOs", "Officers", "Warrant Officers", 
                                                "Mental Health Diagnosis", "NO Mental Health Diagnosis",
                                                "TBI History", "NO TBI", "Previous Self-Harm", 
                                                "NO Previous Self-Harm", "Visited Health Services", "DID NOT visit",
                                                "Gun in Home", "No Gun in Home"]
                                    cursor1 = g.conn.execute('''SELECT S.year, B.branch, S.count, S.rate, 
                                                             R.e1_e4, R.e5_e9, R.officer, R.warrant_officer, M.health_diag_y,
                                                             M.health_diag_n, m.tbi_y, m.tbi_n, m.prev_self_harm_y, m.prev_self_harm_n,
                                                             m.health_ser_used_y, m.health_ser_used_n, a.in_home, a.not_in_home
                                                            FROM Suicides S, Military_Branch B, Rank R, Mental_Characteristics M, Access_To_Firearms A
                                                            WHERE s.sid = b.sid 
                                                            AND b.sid = r.sid
                                                            AND r.sid = m.sid
                                                            AND m.sid = a.sid
                                                            AND S.year >= (%s) 
                                                            AND S.year <= (%s)
                                                            AND B.branch != 'Army'
                                                            AND B.branch != 'Navy'
                                                            AND B.branch != 'Air Force'
                                                            AND B.branch != 'All'
                                                        ''', year1,year2)  
                                    for result in cursor1:
                                        military.append(result) 
                                    cursor1.close()
                                    
                            elif marines !="on": 
                                if airforce == "on":
                                    headings = ["Year", "Branch", "Count", "Rate", "Lower Enlisted", 
                                                "NCOs", "Officers", "Warrant Officers", 
                                                "Mental Health Diagnosis", "NO Mental Health Diagnosis",
                                                "TBI History", "NO TBI", "Previous Self-Harm", 
                                                "NO Previous Self-Harm", "Visited Health Services", "DID NOT visit",
                                                "Gun in Home", "No Gun in Home"]
                                    cursor1 = g.conn.execute('''SELECT S.year, B.branch, S.count, S.rate, 
                                                             R.e1_e4, R.e5_e9, R.officer, R.warrant_officer, M.health_diag_y,
                                                             M.health_diag_n, m.tbi_y, m.tbi_n, m.prev_self_harm_y, m.prev_self_harm_n,
                                                             m.health_ser_used_y, m.health_ser_used_n, a.in_home, a.not_in_home
                                                            FROM Suicides S, Military_Branch B, Rank R, Mental_Characteristics M, Access_To_Firearms A
                                                            WHERE s.sid = b.sid 
                                                            AND b.sid = r.sid
                                                            AND r.sid = m.sid
                                                            AND m.sid = a.sid
                                                            AND S.year >= (%s) 
                                                            AND S.year <= (%s)
                                                            AND B.branch != 'Army'
                                                            AND B.branch != 'Navy'
                                                            AND B.branch != 'Marine Corps'
                                                            AND B.branch != 'All'
                                                        ''', year1,year2)  
                                    for result in cursor1:
                                        military.append(result) 
                                    cursor1.close()
                                    
                                elif airforce != "on":
                                    headings = ["Year", "Branch", "Count", "Rate", "Lower Enlisted", 
                                                "NCOs", "Officers", "Warrant Officers", 
                                                "Mental Health Diagnosis", "NO Mental Health Diagnosis",
                                                "TBI History", "NO TBI", "Previous Self-Harm", 
                                                "NO Previous Self-Harm", "Visited Health Services", "DID NOT visit",
                                                "Gun in Home", "No Gun in Home"]
                                    cursor1 = g.conn.execute('''SELECT S.year, B.branch, S.count, S.rate, 
                                                             R.e1_e4, R.e5_e9, R.officer, R.warrant_officer, M.health_diag_y,
                                                             M.health_diag_n, m.tbi_y, m.tbi_n, m.prev_self_harm_y, m.prev_self_harm_n,
                                                             m.health_ser_used_y, m.health_ser_used_n, a.in_home, a.not_in_home
                                                            FROM Suicides S, Military_Branch B, Rank R, Mental_Characteristics M, Access_To_Firearms A
                                                            WHERE s.sid = b.sid 
                                                            AND b.sid = r.sid
                                                            AND r.sid = m.sid
                                                            AND m.sid = a.sid
                                                            AND S.year >= (%s) 
                                                            AND S.year <= (%s)
                                                            AND B.branch != 'Army'
                                                            AND B.branch != 'Navy'
                                                            AND B.branch != 'Marine Corps'
                                                            AND B.branch != 'Air Force'
                                                            AND B.branch != 'All'
                                                        ''', year1,year2)  
                                    for result in cursor1:
                                        military.append(result) 
                                    cursor1.close()
                                    
        if showrank != "on":
            if showmh == "on":
                if combined == 'on':
                    if army == "on":
                        if navy =="on": 
                            if marines =="on": 
                                if airforce == "on":
                                    headings = ["Year", "Branch", "Count", "Rate", 
                                                "Mental Health Diagnosis", "NO Mental Health Diagnosis",
                                                "TBI History", "NO TBI", "Previous Self-Harm", 
                                                "NO Previous Self-Harm", "Visited Health Services", "DID NOT visit","Gun in Home", "No Gun in Home"]
                                    cursor1 = g.conn.execute('''SELECT S.year, B.branch, S.count, S.rate, M.health_diag_y,
                                                             M.health_diag_n, m.tbi_y, m.tbi_n, m.prev_self_harm_y, m.prev_self_harm_n,
                                                             m.health_ser_used_y, m.health_ser_used_n, a.in_home, a.not_in_home
                                                            FROM Suicides S, Military_Branch B, Mental_Characteristics M, Access_To_Firearms A
                                                            WHERE s.sid = b.sid 
                                                            AND b.sid = m.sid
                                                            AND m.sid = a.sid
                                                            AND S.year >= (%s) 
                                                            AND S.year <= (%s)
                                                            ''', year1,year2)   
                                    for result in cursor1:
                                        military.append(result) 
                                    cursor1.close()
                                    
                                elif airforce != "on":
                                    headings = ["Year", "Branch", "Count", "Rate", 
                                                "Mental Health Diagnosis", "NO Mental Health Diagnosis",
                                                "TBI History", "NO TBI", "Previous Self-Harm", 
                                                "NO Previous Self-Harm", "Visited Health Services", "DID NOT visit","Gun in Home", "No Gun in Home"]
                                    cursor1 = g.conn.execute('''SELECT S.year, B.branch, S.count, S.rate, M.health_diag_y,
                                                             M.health_diag_n, m.tbi_y, m.tbi_n, m.prev_self_harm_y, m.prev_self_harm_n,
                                                             m.health_ser_used_y, m.health_ser_used_n, a.in_home, a.not_in_home
                                                            FROM Suicides S, Military_Branch B, Mental_Characteristics M, Access_To_Firearms A
                                                            WHERE s.sid = b.sid 
                                                            AND b.sid = m.sid
                                                            AND m.sid = a.sid
                                                            AND S.year >= (%s) 
                                                            AND S.year <= (%s)
                                                            AND B.branch != 'Air Force'
                                                            
                                                        ''', year1,year2)  
                                    for result in cursor1:
                                        military.append(result) 
                                    cursor1.close()
                                    
                            elif marines !="on": 
                                if airforce == "on":
                                    headings = ["Year", "Branch", "Count", "Rate", 
                                                "Mental Health Diagnosis", "NO Mental Health Diagnosis",
                                                "TBI History", "NO TBI", "Previous Self-Harm", 
                                                "NO Previous Self-Harm", "Visited Health Services", "DID NOT visit","Gun in Home", "No Gun in Home"]
                                    cursor1 = g.conn.execute('''SELECT S.year, B.branch, S.count, S.rate, M.health_diag_y,
                                                             M.health_diag_n, m.tbi_y, m.tbi_n, m.prev_self_harm_y, m.prev_self_harm_n,
                                                             m.health_ser_used_y, m.health_ser_used_n, a.in_home, a.not_in_home
                                                            FROM Suicides S, Military_Branch B, Mental_Characteristics M, Access_To_Firearms A
                                                            WHERE s.sid = b.sid 
                                                            AND b.sid = m.sid
                                                            AND m.sid = a.sid
                                                            AND S.year >= (%s) 
                                                            AND S.year <= (%s)
                                                            AND B.branch != 'Marine Corps'
                                                        ''', year1,year2)  
                                    for result in cursor1:
                                        military.append(result) 
                                    cursor1.close()
                                    
                                elif airforce != "on":
                                    headings = ["Year", "Branch", "Count", "Rate", 
                                                "Mental Health Diagnosis", "NO Mental Health Diagnosis",
                                                "TBI History", "NO TBI", "Previous Self-Harm", 
                                                "NO Previous Self-Harm", "Visited Health Services", "DID NOT visit","Gun in Home", "No Gun in Home"]
                                    cursor1 = g.conn.execute('''SELECT S.year, B.branch, S.count, S.rate, M.health_diag_y,
                                                             M.health_diag_n, m.tbi_y, m.tbi_n, m.prev_self_harm_y, m.prev_self_harm_n,
                                                             m.health_ser_used_y, m.health_ser_used_n, a.in_home, a.not_in_home
                                                            FROM Suicides S, Military_Branch B, Mental_Characteristics M, Access_To_Firearms A
                                                            WHERE s.sid = b.sid 
                                                            AND b.sid = m.sid
                                                            AND m.sid = a.sid
                                                            AND S.year >= (%s) 
                                                            AND S.year <= (%s)
                                                            AND B.branch != 'Marine Corps'
                                                            AND B.branch != 'Air Force'
                                                        ''', year1,year2)  
                                    for result in cursor1:
                                        military.append(result) 
                                    cursor1.close()
                                    
                        elif navy !="on": 
                            if marines =="on": 
                                if airforce == "on":
                                    headings = ["Year", "Branch", "Count", "Rate", 
                                                "Mental Health Diagnosis", "NO Mental Health Diagnosis",
                                                "TBI History", "NO TBI", "Previous Self-Harm", 
                                                "NO Previous Self-Harm", "Visited Health Services", "DID NOT visit","Gun in Home", "No Gun in Home"]
                                    cursor1 = g.conn.execute('''SELECT S.year, B.branch, S.count, S.rate, M.health_diag_y,
                                                             M.health_diag_n, m.tbi_y, m.tbi_n, m.prev_self_harm_y, m.prev_self_harm_n,
                                                             m.health_ser_used_y, m.health_ser_used_n, a.in_home, a.not_in_home
                                                            FROM Suicides S, Military_Branch B, Mental_Characteristics M, Access_To_Firearms A
                                                            WHERE s.sid = b.sid 
                                                            AND b.sid = m.sid
                                                            AND m.sid = a.sid
                                                            AND S.year >= (%s) 
                                                            AND S.year <= (%s)
                                                            AND B.branch != 'Navy'
                                                        ''', year1,year2)  
                                    for result in cursor1:
                                        military.append(result) 
                                    cursor1.close()
                                    
                                elif airforce != "on":
                                    headings = ["Year", "Branch", "Count", "Rate", 
                                                "Mental Health Diagnosis", "NO Mental Health Diagnosis",
                                                "TBI History", "NO TBI", "Previous Self-Harm", 
                                                "NO Previous Self-Harm", "Visited Health Services", "DID NOT visit","Gun in Home", "No Gun in Home"]
                                    cursor1 = g.conn.execute('''SELECT S.year, B.branch, S.count, S.rate, M.health_diag_y,
                                                             M.health_diag_n, m.tbi_y, m.tbi_n, m.prev_self_harm_y, m.prev_self_harm_n,
                                                             m.health_ser_used_y, m.health_ser_used_n, a.in_home, a.not_in_home
                                                            FROM Suicides S, Military_Branch B, Mental_Characteristics M, Access_To_Firearms A
                                                            WHERE s.sid = b.sid 
                                                            AND b.sid = m.sid
                                                            AND m.sid = a.sid
                                                            AND S.year >= (%s) 
                                                            AND S.year <= (%s)
                                                            AND B.branch != 'Navy'
                                                            AND B.branch != 'Marine Corps'
                                                            AND B.branch != 'Air Force'
                                                        ''', year1,year2)  
                                    for result in cursor1:
                                        military.append(result) 
                                    cursor1.close()
                                    
                            elif marines !="on": 
                                if airforce == "on":
                                    headings = ["Year", "Branch", "Count", "Rate", 
                                                "Mental Health Diagnosis", "NO Mental Health Diagnosis",
                                                "TBI History", "NO TBI", "Previous Self-Harm", 
                                                "NO Previous Self-Harm", "Visited Health Services", "DID NOT visit","Gun in Home", "No Gun in Home"]
                                    cursor1 = g.conn.execute('''SELECT S.year, B.branch, S.count, S.rate, M.health_diag_y,
                                                             M.health_diag_n, m.tbi_y, m.tbi_n, m.prev_self_harm_y, m.prev_self_harm_n,
                                                             m.health_ser_used_y, m.health_ser_used_n, a.in_home, a.not_in_home
                                                            FROM Suicides S, Military_Branch B, Mental_Characteristics M, Access_To_Firearms A
                                                            WHERE s.sid = b.sid 
                                                            AND b.sid = m.sid
                                                            AND m.sid = a.sid
                                                            AND S.year >= (%s) 
                                                            AND S.year <= (%s)
                                                            AND B.branch != 'Navy'
                                                            AND B.branch != 'Marine Corps'
                                                        ''', year1,year2)  
                                    for result in cursor1:
                                        military.append(result) 
                                    cursor1.close()
                                    
                                elif airforce != "on":
                                    headings = ["Year", "Branch", "Count", "Rate", 
                                                "Mental Health Diagnosis", "NO Mental Health Diagnosis",
                                                "TBI History", "NO TBI", "Previous Self-Harm", 
                                                "NO Previous Self-Harm", "Visited Health Services", "DID NOT visit","Gun in Home", "No Gun in Home"]
                                    cursor1 = g.conn.execute('''SELECT S.year, B.branch, S.count, S.rate, M.health_diag_y,
                                                             M.health_diag_n, m.tbi_y, m.tbi_n, m.prev_self_harm_y, m.prev_self_harm_n,
                                                             m.health_ser_used_y, m.health_ser_used_n, a.in_home, a.not_in_home
                                                            FROM Suicides S, Military_Branch B, Mental_Characteristics M, Access_To_Firearms A
                                                            WHERE s.sid = b.sid 
                                                            AND b.sid = m.sid
                                                            AND m.sid = a.sid
                                                            AND S.year >= (%s) 
                                                            AND S.year <= (%s)
                                                            AND B.branch != 'Navy'
                                                            AND B.branch != 'Marine Corps'
                                                            AND B.branch != 'Air Force'
                                                        ''', year1,year2)  
                                    for result in cursor1:
                                        military.append(result) 
                                    cursor1.close()
                                    
                    elif army !="on":
                        if navy =="on": 
                            if marines =="on": 
                                if airforce == "on":
                                    headings = ["Year", "Branch", "Count", "Rate", 
                                                "Mental Health Diagnosis", "NO Mental Health Diagnosis",
                                                "TBI History", "NO TBI", "Previous Self-Harm", 
                                                "NO Previous Self-Harm", "Visited Health Services", "DID NOT visit","Gun in Home", "No Gun in Home"]
                                    cursor1 = g.conn.execute('''SELECT S.year, B.branch, S.count, S.rate, M.health_diag_y,
                                                             M.health_diag_n, m.tbi_y, m.tbi_n, m.prev_self_harm_y, m.prev_self_harm_n,
                                                             m.health_ser_used_y, m.health_ser_used_n, a.in_home, a.not_in_home
                                                            FROM Suicides S, Military_Branch B, Mental_Characteristics M, Access_To_Firearms A
                                                            WHERE s.sid = b.sid 
                                                            AND b.sid = m.sid
                                                            AND m.sid = a.sid
                                                            AND S.year >= (%s) 
                                                            AND S.year <= (%s)
                                                            AND B.branch != 'Army'
                                                        ''', year1,year2)  
                                    for result in cursor1:
                                        military.append(result) 
                                    cursor1.close()
                                    
                                elif airforce != "on":
                                    headings = ["Year", "Branch", "Count", "Rate", 
                                                "Mental Health Diagnosis", "NO Mental Health Diagnosis",
                                                "TBI History", "NO TBI", "Previous Self-Harm", 
                                                "NO Previous Self-Harm", "Visited Health Services", "DID NOT visit","Gun in Home", "No Gun in Home"]
                                    cursor1 = g.conn.execute('''SELECT S.year, B.branch, S.count, S.rate, M.health_diag_y,
                                                             M.health_diag_n, m.tbi_y, m.tbi_n, m.prev_self_harm_y, m.prev_self_harm_n,
                                                             m.health_ser_used_y, m.health_ser_used_n, a.in_home, a.not_in_home
                                                            FROM Suicides S, Military_Branch B, Mental_Characteristics M, Access_To_Firearms A
                                                            WHERE s.sid = b.sid 
                                                            AND b.sid = m.sid
                                                            AND m.sid = a.sid
                                                            AND S.year >= (%s) 
                                                            AND S.year <= (%s)
                                                            AND B.branch != 'Army'
                                                            AND B.branch != 'Air Force'
                                                        ''', year1,year2)  
                                    for result in cursor1:
                                        military.append(result) 
                                    cursor1.close()
                                    
                            elif marines !="on": 
                                if airforce == "on":
                                    headings = ["Year", "Branch", "Count", "Rate", 
                                                "Mental Health Diagnosis", "NO Mental Health Diagnosis",
                                                "TBI History", "NO TBI", "Previous Self-Harm", 
                                                "NO Previous Self-Harm", "Visited Health Services", "DID NOT visit","Gun in Home", "No Gun in Home"]
                                    cursor1 = g.conn.execute('''SELECT S.year, B.branch, S.count, S.rate, M.health_diag_y,
                                                             M.health_diag_n, m.tbi_y, m.tbi_n, m.prev_self_harm_y, m.prev_self_harm_n,
                                                             m.health_ser_used_y, m.health_ser_used_n, a.in_home, a.not_in_home
                                                            FROM Suicides S, Military_Branch B, Mental_Characteristics M, Access_To_Firearms A
                                                            WHERE s.sid = b.sid 
                                                            AND b.sid = m.sid
                                                            AND m.sid = a.sid
                                                            AND S.year >= (%s) 
                                                            AND S.year <= (%s)
                                                            AND B.branch != 'Army'
                                                            AND B.branch != 'Marine Corps'
                                                        ''', year1,year2)  
                                    for result in cursor1:
                                        military.append(result) 
                                    cursor1.close()
                                    
                                elif airforce != "on":
                                    headings = ["Year", "Branch", "Count", "Rate", 
                                                "Mental Health Diagnosis", "NO Mental Health Diagnosis",
                                                "TBI History", "NO TBI", "Previous Self-Harm", 
                                                "NO Previous Self-Harm", "Visited Health Services", "DID NOT visit","Gun in Home", "No Gun in Home"]
                                    cursor1 = g.conn.execute('''SELECT S.year, B.branch, S.count, S.rate, M.health_diag_y,
                                                             M.health_diag_n, m.tbi_y, m.tbi_n, m.prev_self_harm_y, m.prev_self_harm_n,
                                                             m.health_ser_used_y, m.health_ser_used_n, a.in_home, a.not_in_home
                                                            FROM Suicides S, Military_Branch B, Mental_Characteristics M, Access_To_Firearms A
                                                            WHERE s.sid = b.sid 
                                                            AND b.sid = m.sid
                                                            AND m.sid = a.sid
                                                            AND S.year >= (%s) 
                                                            AND S.year <= (%s)
                                                            AND B.branch != 'Army'
                                                            AND B.branch != 'Marine Corps'
                                                            AND B.branch != 'Air Force'
                                                        ''', year1,year2)  
                                    for result in cursor1:
                                        military.append(result) 
                                    cursor1.close()
                                    
                        elif navy !="on": 
                            if marines =="on": 
                                if airforce == "on":
                                    headings = ["Year", "Branch", "Count", "Rate", 
                                                "Mental Health Diagnosis", "NO Mental Health Diagnosis",
                                                "TBI History", "NO TBI", "Previous Self-Harm", 
                                                "NO Previous Self-Harm", "Visited Health Services", "DID NOT visit","Gun in Home", "No Gun in Home"]
                                    cursor1 = g.conn.execute('''SELECT S.year, B.branch, S.count, S.rate, M.health_diag_y,
                                                             M.health_diag_n, m.tbi_y, m.tbi_n, m.prev_self_harm_y, m.prev_self_harm_n,
                                                             m.health_ser_used_y, m.health_ser_used_n, a.in_home, a.not_in_home
                                                            FROM Suicides S, Military_Branch B, Mental_Characteristics M, Access_To_Firearms A
                                                            WHERE s.sid = b.sid 
                                                            AND b.sid = m.sid
                                                            AND m.sid = a.sid
                                                            AND S.year >= (%s) 
                                                            AND S.year <= (%s)
                                                            AND B.branch != 'Army'
                                                            AND B.branch != 'Navy''
                                                        ''', year1,year2)  
                                    for result in cursor1:
                                        military.append(result) 
                                    cursor1.close()
                                    
                                elif airforce != "on":
                                    headings = ["Year", "Branch", "Count", "Rate", 
                                                "Mental Health Diagnosis", "NO Mental Health Diagnosis",
                                                "TBI History", "NO TBI", "Previous Self-Harm", 
                                                "NO Previous Self-Harm", "Visited Health Services", "DID NOT visit","Gun in Home", "No Gun in Home"]
                                    cursor1 = g.conn.execute('''SELECT S.year, B.branch, S.count, S.rate, M.health_diag_y,
                                                             M.health_diag_n, m.tbi_y, m.tbi_n, m.prev_self_harm_y, m.prev_self_harm_n,
                                                             m.health_ser_used_y, m.health_ser_used_n, a.in_home, a.not_in_home
                                                            FROM Suicides S, Military_Branch B, Mental_Characteristics M, Access_To_Firearms A
                                                            WHERE s.sid = b.sid 
                                                            AND b.sid = m.sid
                                                            AND m.sid = a.sid
                                                            AND S.year >= (%s) 
                                                            AND S.year <= (%s)
                                                            AND B.branch != 'Air Force'
                                                        ''', year1,year2)  
                                    for result in cursor1:
                                        military.append(result) 
                                    cursor1.close()
                                    
                            elif marines !="on": 
                                if airforce == "on":
                                    headings = ["Year", "Branch", "Count", "Rate", 
                                                "Mental Health Diagnosis", "NO Mental Health Diagnosis",
                                                "TBI History", "NO TBI", "Previous Self-Harm", 
                                                "NO Previous Self-Harm", "Visited Health Services", "DID NOT visit","Gun in Home", "No Gun in Home"]
                                    cursor1 = g.conn.execute('''SELECT S.year, B.branch, S.count, S.rate, M.health_diag_y,
                                                             M.health_diag_n, m.tbi_y, m.tbi_n, m.prev_self_harm_y, m.prev_self_harm_n,
                                                             m.health_ser_used_y, m.health_ser_used_n, a.in_home, a.not_in_home
                                                            FROM Suicides S, Military_Branch B, Mental_Characteristics M, Access_To_Firearms A
                                                            WHERE s.sid = b.sid 
                                                            AND b.sid = m.sid
                                                            AND m.sid = a.sid
                                                            AND S.year >= (%s) 
                                                            AND S.year <= (%s)
                                                            AND B.branch != 'Army'
                                                            AND B.branch != 'Navy'
                                                            AND B.branch != 'Marine Corps'
                                                        ''', year1,year2)  
                                    for result in cursor1:
                                        military.append(result) 
                                    cursor1.close()
                                    
                                elif airforce != "on":
                                    headings = ["Year", "Branch", "Count", "Rate", 
                                                "Mental Health Diagnosis", "NO Mental Health Diagnosis",
                                                "TBI History", "NO TBI", "Previous Self-Harm", 
                                                "NO Previous Self-Harm", "Visited Health Services", "DID NOT visit","Gun in Home", "No Gun in Home"]
                                    cursor1 = g.conn.execute('''SELECT S.year, B.branch, S.count, S.rate, M.health_diag_y,
                                                             M.health_diag_n, m.tbi_y, m.tbi_n, m.prev_self_harm_y, m.prev_self_harm_n,
                                                             m.health_ser_used_y, m.health_ser_used_n, a.in_home, a.not_in_home
                                                            FROM Suicides S, Military_Branch B, Mental_Characteristics M, Access_To_Firearms A
                                                            WHERE s.sid = b.sid 
                                                            AND b.sid = m.sid
                                                            AND m.sid = a.sid
                                                            AND S.year >= (%s) 
                                                            AND S.year <= (%s)
                                                            AND B.branch != 'Army'
                                                            AND B.branch != 'Navy'
                                                            AND B.branch != 'Marine Corps'
                                                            AND B.branch != 'Air Force'
                                                        ''', year1,year2)  
                                    for result in cursor1:
                                        military.append(result) 
                                    cursor1.close()
                if combined != 'on':
                    if army == "on":
                        if navy =="on": 
                            if marines =="on": 
                                if airforce == "on":
                                    headings = ["Year", "Branch", "Count", "Rate", 
                                                "Mental Health Diagnosis", "NO Mental Health Diagnosis",
                                                "TBI History", "NO TBI", "Previous Self-Harm", 
                                                "NO Previous Self-Harm", "Visited Health Services", "DID NOT visit","Gun in Home", "No Gun in Home"]
                                    cursor1 = g.conn.execute('''SELECT S.year, B.branch, S.count, S.rate, M.health_diag_y,
                                                             M.health_diag_n, m.tbi_y, m.tbi_n, m.prev_self_harm_y, m.prev_self_harm_n,
                                                             m.health_ser_used_y, m.health_ser_used_n, a.in_home, a.not_in_home
                                                            FROM Suicides S, Military_Branch B, Mental_Characteristics M, Access_To_Firearms A
                                                            WHERE s.sid = b.sid 
                                                            AND b.sid = m.sid
                                                            AND m.sid = a.sid
                                                            AND S.year >= (%s) 
                                                            AND S.year <= (%s)
                                                            AND B.branch != 'All'
                                                            ''', year1,year2)   
                                    for result in cursor1:
                                        military.append(result) 
                                    cursor1.close()
                                    
                                elif airforce != "on":
                                    headings = ["Year", "Branch", "Count", "Rate", 
                                                "Mental Health Diagnosis", "NO Mental Health Diagnosis",
                                                "TBI History", "NO TBI", "Previous Self-Harm", 
                                                "NO Previous Self-Harm", "Visited Health Services", "DID NOT visit","Gun in Home", "No Gun in Home"]
                                    cursor1 = g.conn.execute('''SELECT S.year, B.branch, S.count, S.rate, M.health_diag_y,
                                                             M.health_diag_n, m.tbi_y, m.tbi_n, m.prev_self_harm_y, m.prev_self_harm_n,
                                                             m.health_ser_used_y, m.health_ser_used_n, a.in_home, a.not_in_home
                                                            FROM Suicides S, Military_Branch B, Mental_Characteristics M, Access_To_Firearms A
                                                            WHERE s.sid = b.sid 
                                                            AND b.sid = m.sid
                                                            AND m.sid = a.sid
                                                            AND S.year >= (%s) 
                                                            AND S.year <= (%s)
                                                            AND B.branch != 'Air Force'
                                                            AND B.branch != 'All'
                                                            
                                                        ''', year1,year2)  
                                    for result in cursor1:
                                        military.append(result) 
                                    cursor1.close()
                                    
                            elif marines !="on": 
                                if airforce == "on":
                                    headings = ["Year", "Branch", "Count", "Rate", 
                                                "Mental Health Diagnosis", "NO Mental Health Diagnosis",
                                                "TBI History", "NO TBI", "Previous Self-Harm", 
                                                "NO Previous Self-Harm", "Visited Health Services", "DID NOT visit","Gun in Home", "No Gun in Home"]
                                    cursor1 = g.conn.execute('''SELECT S.year, B.branch, S.count, S.rate, M.health_diag_y,
                                                             M.health_diag_n, m.tbi_y, m.tbi_n, m.prev_self_harm_y, m.prev_self_harm_n,
                                                             m.health_ser_used_y, m.health_ser_used_n, a.in_home, a.not_in_home
                                                            FROM Suicides S, Military_Branch B, Mental_Characteristics M, Access_To_Firearms A
                                                            WHERE s.sid = b.sid 
                                                            AND b.sid = m.sid
                                                            AND m.sid = a.sid
                                                            AND S.year >= (%s) 
                                                            AND S.year <= (%s)
                                                            AND B.branch != 'Marine Corps'
                                                            AND B.branch != 'All'
                                                        ''', year1,year2)  
                                    for result in cursor1:
                                        military.append(result) 
                                    cursor1.close()
                                    
                                elif airforce != "on":
                                    headings = ["Year", "Branch", "Count", "Rate", 
                                                "Mental Health Diagnosis", "NO Mental Health Diagnosis",
                                                "TBI History", "NO TBI", "Previous Self-Harm", 
                                                "NO Previous Self-Harm", "Visited Health Services", "DID NOT visit","Gun in Home", "No Gun in Home"]
                                    cursor1 = g.conn.execute('''SELECT S.year, B.branch, S.count, S.rate, M.health_diag_y,
                                                             M.health_diag_n, m.tbi_y, m.tbi_n, m.prev_self_harm_y, m.prev_self_harm_n,
                                                             m.health_ser_used_y, m.health_ser_used_n, a.in_home, a.not_in_home
                                                            FROM Suicides S, Military_Branch B, Mental_Characteristics M, Access_To_Firearms A
                                                            WHERE s.sid = b.sid 
                                                            AND b.sid = m.sid
                                                            AND m.sid = a.sid
                                                            AND S.year >= (%s) 
                                                            AND S.year <= (%s)
                                                            AND B.branch != 'Marine Corps'
                                                            AND B.branch != 'Air Force'
                                                            AND B.branch != 'All'
                                                        ''', year1,year2)  
                                    for result in cursor1:
                                        military.append(result) 
                                    cursor1.close()
                                    
                        elif navy !="on": 
                            if marines =="on": 
                                if airforce == "on":
                                    headings = ["Year", "Branch", "Count", "Rate", 
                                                "Mental Health Diagnosis", "NO Mental Health Diagnosis",
                                                "TBI History", "NO TBI", "Previous Self-Harm", 
                                                "NO Previous Self-Harm", "Visited Health Services", "DID NOT visit","Gun in Home", "No Gun in Home"]
                                    cursor1 = g.conn.execute('''SELECT S.year, B.branch, S.count, S.rate, M.health_diag_y,
                                                             M.health_diag_n, m.tbi_y, m.tbi_n, m.prev_self_harm_y, m.prev_self_harm_n,
                                                             m.health_ser_used_y, m.health_ser_used_n, a.in_home, a.not_in_home
                                                            FROM Suicides S, Military_Branch B, Mental_Characteristics M, Access_To_Firearms A
                                                            WHERE s.sid = b.sid 
                                                            AND b.sid = m.sid
                                                            AND m.sid = a.sid
                                                            AND S.year >= (%s) 
                                                            AND S.year <= (%s)
                                                            AND B.branch != 'Navy'
                                                            AND B.branch != 'All'
                                                        ''', year1,year2)  
                                    for result in cursor1:
                                        military.append(result) 
                                    cursor1.close()
                                    
                                elif airforce != "on":
                                    headings = ["Year", "Branch", "Count", "Rate", 
                                                "Mental Health Diagnosis", "NO Mental Health Diagnosis",
                                                "TBI History", "NO TBI", "Previous Self-Harm", 
                                                "NO Previous Self-Harm", "Visited Health Services", "DID NOT visit","Gun in Home", "No Gun in Home"]
                                    cursor1 = g.conn.execute('''SELECT S.year, B.branch, S.count, S.rate, M.health_diag_y,
                                                             M.health_diag_n, m.tbi_y, m.tbi_n, m.prev_self_harm_y, m.prev_self_harm_n,
                                                             m.health_ser_used_y, m.health_ser_used_n, a.in_home, a.not_in_home
                                                            FROM Suicides S, Military_Branch B, Mental_Characteristics M, Access_To_Firearms A
                                                            WHERE s.sid = b.sid 
                                                            AND b.sid = m.sid
                                                            AND m.sid = a.sid
                                                            AND S.year >= (%s) 
                                                            AND S.year <= (%s)
                                                            AND B.branch != 'Navy'
                                                            AND B.branch != 'Marine Corps'
                                                            AND B.branch != 'Air Force'
                                                            AND B.branch != 'All'
                                                        ''', year1,year2)  
                                    for result in cursor1:
                                        military.append(result) 
                                    cursor1.close()
                                    
                            elif marines !="on": 
                                if airforce == "on":
                                    headings = ["Year", "Branch", "Count", "Rate", 
                                                "Mental Health Diagnosis", "NO Mental Health Diagnosis",
                                                "TBI History", "NO TBI", "Previous Self-Harm", 
                                                "NO Previous Self-Harm", "Visited Health Services", "DID NOT visit","Gun in Home", "No Gun in Home"]
                                    cursor1 = g.conn.execute('''SELECT S.year, B.branch, S.count, S.rate, M.health_diag_y,
                                                             M.health_diag_n, m.tbi_y, m.tbi_n, m.prev_self_harm_y, m.prev_self_harm_n,
                                                             m.health_ser_used_y, m.health_ser_used_n, a.in_home, a.not_in_home
                                                            FROM Suicides S, Military_Branch B, Mental_Characteristics M, Access_To_Firearms A
                                                            WHERE s.sid = b.sid 
                                                            AND b.sid = m.sid
                                                            AND m.sid = a.sid
                                                            AND S.year >= (%s) 
                                                            AND S.year <= (%s)
                                                            AND B.branch != 'Navy'
                                                            AND B.branch != 'Marine Corps'
                                                            AND B.branch != 'All'
                                                        ''', year1,year2)  
                                    for result in cursor1:
                                        military.append(result) 
                                    cursor1.close()
                                    
                                elif airforce != "on":
                                    headings = ["Year", "Branch", "Count", "Rate", 
                                                "Mental Health Diagnosis", "NO Mental Health Diagnosis",
                                                "TBI History", "NO TBI", "Previous Self-Harm", 
                                                "NO Previous Self-Harm", "Visited Health Services", "DID NOT visit","Gun in Home", "No Gun in Home"]
                                    cursor1 = g.conn.execute('''SELECT S.year, B.branch, S.count, S.rate, M.health_diag_y,
                                                             M.health_diag_n, m.tbi_y, m.tbi_n, m.prev_self_harm_y, m.prev_self_harm_n,
                                                             m.health_ser_used_y, m.health_ser_used_n, a.in_home, a.not_in_home
                                                            FROM Suicides S, Military_Branch B, Mental_Characteristics M, Access_To_Firearms A
                                                            WHERE s.sid = b.sid 
                                                            AND b.sid = m.sid
                                                            AND m.sid = a.sid
                                                            AND S.year >= (%s) 
                                                            AND S.year <= (%s)
                                                            AND B.branch != 'Navy'
                                                            AND B.branch != 'Marine Corps'
                                                            AND B.branch != 'Air Force'
                                                            AND B.branch != 'All'
                                                        ''', year1,year2)  
                                    for result in cursor1:
                                        military.append(result) 
                                    cursor1.close()
                                    
                    elif army !="on":
                        if navy =="on": 
                            if marines =="on": 
                                if airforce == "on":
                                    headings = ["Year", "Branch", "Count", "Rate", 
                                                "Mental Health Diagnosis", "NO Mental Health Diagnosis",
                                                "TBI History", "NO TBI", "Previous Self-Harm", 
                                                "NO Previous Self-Harm", "Visited Health Services", "DID NOT visit","Gun in Home", "No Gun in Home"]
                                    cursor1 = g.conn.execute('''SELECT S.year, B.branch, S.count, S.rate, M.health_diag_y,
                                                             M.health_diag_n, m.tbi_y, m.tbi_n, m.prev_self_harm_y, m.prev_self_harm_n,
                                                             m.health_ser_used_y, m.health_ser_used_n, a.in_home, a.not_in_home
                                                            FROM Suicides S, Military_Branch B, Mental_Characteristics M, Access_To_Firearms A
                                                            WHERE s.sid = b.sid 
                                                            AND b.sid = m.sid
                                                            AND m.sid = a.sid
                                                            AND S.year >= (%s) 
                                                            AND S.year <= (%s)
                                                            AND B.branch != 'Army'
                                                            AND B.branch != 'All'
                                                        ''', year1,year2)  
                                    for result in cursor1:
                                        military.append(result) 
                                    cursor1.close()
                                    
                                elif airforce != "on":
                                    headings = ["Year", "Branch", "Count", "Rate", 
                                                "Mental Health Diagnosis", "NO Mental Health Diagnosis",
                                                "TBI History", "NO TBI", "Previous Self-Harm", 
                                                "NO Previous Self-Harm", "Visited Health Services", "DID NOT visit","Gun in Home", "No Gun in Home"]
                                    cursor1 = g.conn.execute('''SELECT S.year, B.branch, S.count, S.rate, M.health_diag_y,
                                                             M.health_diag_n, m.tbi_y, m.tbi_n, m.prev_self_harm_y, m.prev_self_harm_n,
                                                             m.health_ser_used_y, m.health_ser_used_n, a.in_home, a.not_in_home
                                                            FROM Suicides S, Military_Branch B, Mental_Characteristics M, Access_To_Firearms A
                                                            WHERE s.sid = b.sid 
                                                            AND b.sid = m.sid
                                                            AND m.sid = a.sid
                                                            AND S.year >= (%s) 
                                                            AND S.year <= (%s)
                                                            AND B.branch != 'Army'
                                                            AND B.branch != 'Air Force'
                                                            AND B.branch != 'All'
                                                        ''', year1,year2)  
                                    for result in cursor1:
                                        military.append(result) 
                                    cursor1.close()
                                    
                            elif marines !="on": 
                                if airforce == "on":
                                    headings = ["Year", "Branch", "Count", "Rate", 
                                                "Mental Health Diagnosis", "NO Mental Health Diagnosis",
                                                "TBI History", "NO TBI", "Previous Self-Harm", 
                                                "NO Previous Self-Harm", "Visited Health Services", "DID NOT visit","Gun in Home", "No Gun in Home"]
                                    cursor1 = g.conn.execute('''SELECT S.year, B.branch, S.count, S.rate, M.health_diag_y,
                                                             M.health_diag_n, m.tbi_y, m.tbi_n, m.prev_self_harm_y, m.prev_self_harm_n,
                                                             m.health_ser_used_y, m.health_ser_used_n, a.in_home, a.not_in_home
                                                            FROM Suicides S, Military_Branch B, Mental_Characteristics M, Access_To_Firearms A
                                                            WHERE s.sid = b.sid 
                                                            AND b.sid = m.sid
                                                            AND m.sid = a.sid
                                                            AND S.year >= (%s) 
                                                            AND S.year <= (%s)
                                                            AND B.branch != 'Army'
                                                            AND B.branch != 'Marine Corps'
                                                            AND B.branch != 'All'
                                                        ''', year1,year2)  
                                    for result in cursor1:
                                        military.append(result) 
                                    cursor1.close()
                                    
                                elif airforce != "on":
                                    headings = ["Year", "Branch", "Count", "Rate", 
                                                "Mental Health Diagnosis", "NO Mental Health Diagnosis",
                                                "TBI History", "NO TBI", "Previous Self-Harm", 
                                                "NO Previous Self-Harm", "Visited Health Services", "DID NOT visit","Gun in Home", "No Gun in Home"]
                                    cursor1 = g.conn.execute('''SELECT S.year, B.branch, S.count, S.rate, M.health_diag_y,
                                                             M.health_diag_n, m.tbi_y, m.tbi_n, m.prev_self_harm_y, m.prev_self_harm_n,
                                                             m.health_ser_used_y, m.health_ser_used_n, a.in_home, a.not_in_home
                                                            FROM Suicides S, Military_Branch B, Mental_Characteristics M, Access_To_Firearms A
                                                            WHERE s.sid = b.sid 
                                                            AND b.sid = m.sid
                                                            AND m.sid = a.sid
                                                            AND S.year >= (%s) 
                                                            AND S.year <= (%s)
                                                            AND B.branch != 'Army'
                                                            AND B.branch != 'Marine Corps'
                                                            AND B.branch != 'Air Force'
                                                            AND B.branch != 'All'
                                                        ''', year1,year2)  
                                    for result in cursor1:
                                        military.append(result) 
                                    cursor1.close()
                                    
                        elif navy !="on": 
                            if marines =="on": 
                                if airforce == "on":
                                    headings = ["Year", "Branch", "Count", "Rate", 
                                                "Mental Health Diagnosis", "NO Mental Health Diagnosis",
                                                "TBI History", "NO TBI", "Previous Self-Harm", 
                                                "NO Previous Self-Harm", "Visited Health Services", "DID NOT visit","Gun in Home", "No Gun in Home"]
                                    cursor1 = g.conn.execute('''SELECT S.year, B.branch, S.count, S.rate, M.health_diag_y,
                                                             M.health_diag_n, m.tbi_y, m.tbi_n, m.prev_self_harm_y, m.prev_self_harm_n,
                                                             m.health_ser_used_y, m.health_ser_used_n, a.in_home, a.not_in_home
                                                            FROM Suicides S, Military_Branch B, Mental_Characteristics M, Access_To_Firearms A
                                                            WHERE s.sid = b.sid 
                                                            AND b.sid = m.sid
                                                            AND m.sid = a.sid
                                                            AND S.year >= (%s) 
                                                            AND S.year <= (%s)
                                                            AND B.branch != 'Army'
                                                            AND B.branch != 'Navy''
                                                            AND B.branch != 'All'
                                                        ''', year1,year2)  
                                    for result in cursor1:
                                        military.append(result) 
                                    cursor1.close()
                                    
                                elif airforce != "on":
                                    headings = ["Year", "Branch", "Count", "Rate", 
                                                "Mental Health Diagnosis", "NO Mental Health Diagnosis",
                                                "TBI History", "NO TBI", "Previous Self-Harm", 
                                                "NO Previous Self-Harm", "Visited Health Services", "DID NOT visit","Gun in Home", "No Gun in Home"]
                                    cursor1 = g.conn.execute('''SELECT S.year, B.branch, S.count, S.rate, M.health_diag_y,
                                                             M.health_diag_n, m.tbi_y, m.tbi_n, m.prev_self_harm_y, m.prev_self_harm_n,
                                                             m.health_ser_used_y, m.health_ser_used_n, a.in_home, a.not_in_home
                                                            FROM Suicides S, Military_Branch B, Mental_Characteristics M, Access_To_Firearms A
                                                            WHERE s.sid = b.sid 
                                                            AND b.sid = m.sid
                                                            AND m.sid = a.sid
                                                            AND S.year >= (%s) 
                                                            AND S.year <= (%s)
                                                            AND B.branch != 'Air Force'
                                                            AND B.branch != 'All'
                                                        ''', year1,year2)  
                                    for result in cursor1:
                                        military.append(result) 
                                    cursor1.close()
                                    
                            elif marines !="on": 
                                if airforce == "on":
                                    headings = ["Year", "Branch", "Count", "Rate", 
                                                "Mental Health Diagnosis", "NO Mental Health Diagnosis",
                                                "TBI History", "NO TBI", "Previous Self-Harm", 
                                                "NO Previous Self-Harm", "Visited Health Services", "DID NOT visit","Gun in Home", "No Gun in Home"]
                                    cursor1 = g.conn.execute('''SELECT S.year, B.branch, S.count, S.rate, M.health_diag_y,
                                                             M.health_diag_n, m.tbi_y, m.tbi_n, m.prev_self_harm_y, m.prev_self_harm_n,
                                                             m.health_ser_used_y, m.health_ser_used_n, a.in_home, a.not_in_home
                                                            FROM Suicides S, Military_Branch B, Mental_Characteristics M, Access_To_Firearms A
                                                            WHERE s.sid = b.sid 
                                                            AND b.sid = m.sid
                                                            AND m.sid = a.sid
                                                            AND S.year >= (%s) 
                                                            AND S.year <= (%s)
                                                            AND B.branch != 'Army'
                                                            AND B.branch != 'Navy'
                                                            AND B.branch != 'Marine Corps'
                                                            AND B.branch != 'All'
                                                        ''', year1,year2)  
                                    for result in cursor1:
                                        military.append(result) 
                                    cursor1.close()
                                    
                                elif airforce != "on":
                                    headings = ["Year", "Branch", "Count", "Rate", 
                                                "Mental Health Diagnosis", "NO Mental Health Diagnosis",
                                                "TBI History", "NO TBI", "Previous Self-Harm", 
                                                "NO Previous Self-Harm", "Visited Health Services", "DID NOT visit","Gun in Home", "No Gun in Home"]
                                    cursor1 = g.conn.execute('''SELECT S.year, B.branch, S.count, S.rate, M.health_diag_y,
                                                             M.health_diag_n, m.tbi_y, m.tbi_n, m.prev_self_harm_y, m.prev_self_harm_n,
                                                             m.health_ser_used_y, m.health_ser_used_n, a.in_home, a.not_in_home
                                                            FROM Suicides S, Military_Branch B, Mental_Characteristics M, Access_To_Firearms A
                                                            WHERE s.sid = b.sid 
                                                            AND b.sid = m.sid
                                                            AND m.sid = a.sid
                                                            AND S.year >= (%s) 
                                                            AND S.year <= (%s)
                                                            AND B.branch != 'Army'
                                                            AND B.branch != 'Navy'
                                                            AND B.branch != 'Marine Corps'
                                                            AND B.branch != 'Air Force'
                                                            AND B.branch != 'All'
                                                        ''', year1,year2)  
                                    for result in cursor1:
                                        military.append(result) 
                                    cursor1.close()
            if showmh != "on":
                if combined == 'on':
                    if army == "on":
                        if navy =="on": 
                            if marines =="on": 
                                if airforce == "on":
                                    headings = ["Year", "Branch", "Count", "Rate", "Gun in Home", "NO Gun in Home"]
                                    cursor1 = g.conn.execute('''SELECT S.year, B.branch, S.count, S.rate, A.in_home, A.not_in_home
                                                            FROM Suicides S, Military_Branch B, Access_To_Firearms A
                                                            WHERE s.sid = b.sid 
                                                            AND b.sid = a.sid
                                                            AND S.year >= (%s) 
                                                            AND S.year <= (%s)
                                                            ''', year1,year2)   
                                    for result in cursor1:
                                        military.append(result) 
                                    cursor1.close()
                                    
                                elif airforce != "on":
                                    headings = ["Year", "Branch", "Count", "Rate", "Gun in Home", "NO Gun in Home"]
                                    cursor1 = g.conn.execute('''SELECT S.year, B.branch, S.count, S.rate, A.in_home, A.not_in_home
                                                            FROM Suicides S, Military_Branch B, Access_To_Firearms A
                                                            WHERE s.sid = b.sid 
                                                            AND b.sid = a.sid
                                                            AND S.year >= (%s) 
                                                            AND S.year <= (%s)
                                                            AND B.branch != 'Air Force'
                                                        ''', year1,year2)  
                                    for result in cursor1:
                                        military.append(result) 
                                    cursor1.close()
                                    
                            elif marines !="on": 
                                if airforce == "on":
                                    headings = ["Year", "Branch", "Count", "Rate", "Gun in Home", "NO Gun in Home"]
                                    cursor1 = g.conn.execute('''SELECT S.year, B.branch, S.count, S.rate, A.in_home, A.not_in_home
                                                            FROM Suicides S, Military_Branch B, Access_To_Firearms A
                                                            WHERE s.sid = b.sid 
                                                            AND b.sid = a.sid
                                                            AND S.year >= (%s) 
                                                            AND S.year <= (%s)
                                                            AND B.branch != 'Marine Corps'
                                                        ''', year1,year2)  
                                    for result in cursor1:
                                        military.append(result) 
                                    cursor1.close()
                                    
                                elif airforce != "on":
                                    headings = ["Year", "Branch", "Count", "Rate", "Gun in Home", "NO Gun in Home"]
                                    cursor1 = g.conn.execute('''SELECT S.year, B.branch, S.count, S.rate, A.in_home, A.not_in_home
                                                            FROM Suicides S, Military_Branch B, Access_To_Firearms A
                                                            WHERE s.sid = b.sid 
                                                            AND b.sid = a.sid
                                                            AND S.year >= (%s) 
                                                            AND S.year <= (%s)
                                                            AND B.branch != 'Marine Corps'
                                                            AND B.branch != 'Air Force'
                                                        ''', year1,year2)  
                                    for result in cursor1:
                                        military.append(result) 
                                    cursor1.close()
                                    
                        elif navy !="on": 
                            if marines =="on": 
                                if airforce == "on":
                                    headings = ["Year", "Branch", "Count", "Rate", "Gun in Home", "NO Gun in Home"]
                                    cursor1 = g.conn.execute('''SELECT S.year, B.branch, S.count, S.rate, A.in_home, A.not_in_home
                                                            FROM Suicides S, Military_Branch B, Access_To_Firearms A
                                                            WHERE s.sid = b.sid 
                                                            AND b.sid = a.sid
                                                            AND S.year >= (%s) 
                                                            AND S.year <= (%s)
                                                            AND B.branch != 'Navy'
                                                        ''', year1,year2)  
                                    for result in cursor1:
                                        military.append(result) 
                                    cursor1.close()
                                    
                                elif airforce != "on":
                                    headings = ["Year", "Branch", "Count", "Rate", "Gun in Home", "NO Gun in Home"]
                                    cursor1 = g.conn.execute('''SELECT S.year, B.branch, S.count, S.rate, A.in_home, A.not_in_home
                                                            FROM Suicides S, Military_Branch B, Access_To_Firearms A
                                                            WHERE s.sid = b.sid 
                                                            AND b.sid = a.sid
                                                            AND S.year >= (%s) 
                                                            AND S.year <= (%s)
                                                            AND B.branch != 'Navy'
                                                            AND B.branch != 'Marine Corps'
                                                            AND B.branch != 'Air Force'
                                                        ''', year1,year2)  
                                    for result in cursor1:
                                        military.append(result) 
                                    cursor1.close()
                                    
                            elif marines !="on": 
                                if airforce == "on":
                                    headings = ["Year", "Branch", "Count", "Rate", "Gun in Home", "NO Gun in Home"]
                                    cursor1 = g.conn.execute('''SELECT S.year, B.branch, S.count, S.rate, A.in_home, A.not_in_home
                                                            FROM Suicides S, Military_Branch B, Access_To_Firearms A
                                                            WHERE s.sid = b.sid 
                                                            AND b.sid = a.sid
                                                            AND S.year >= (%s) 
                                                            AND S.year <= (%s)
                                                            AND B.branch != 'Navy'
                                                            AND B.branch != 'Marine Corps'
                                                        ''', year1,year2)  
                                    for result in cursor1:
                                        military.append(result) 
                                    cursor1.close()
                                    
                                elif airforce != "on":
                                    headings = ["Year", "Branch", "Count", "Rate", "Gun in Home", "NO Gun in Home"]
                                    cursor1 = g.conn.execute('''SELECT S.year, B.branch, S.count, S.rate, A.in_home, A.not_in_home
                                                            FROM Suicides S, Military_Branch B, Access_To_Firearms A
                                                            WHERE s.sid = b.sid 
                                                            AND b.sid = a.sid
                                                            AND S.year >= (%s) 
                                                            AND S.year <= (%s)
                                                            AND B.branch != 'Navy'
                                                            AND B.branch != 'Marine Corps'
                                                            AND B.branch != 'Air Force'
                                                        ''', year1,year2)  
                                    for result in cursor1:
                                        military.append(result) 
                                    cursor1.close()
                                    
                    elif army !="on":
                        if navy =="on": 
                            if marines =="on": 
                                if airforce == "on":
                                    headings = ["Year", "Branch", "Count", "Rate", "Gun in Home", "NO Gun in Home"]
                                    cursor1 = g.conn.execute('''SELECT S.year, B.branch, S.count, S.rate, A.in_home, A.not_in_home
                                                            FROM Suicides S, Military_Branch B, Access_To_Firearms A
                                                            WHERE s.sid = b.sid 
                                                            AND b.sid = a.sid
                                                            AND S.year >= (%s) 
                                                            AND S.year <= (%s)
                                                            AND B.branch != 'Army'
                                                        ''', year1,year2)  
                                    for result in cursor1:
                                        military.append(result) 
                                    cursor1.close()
                                    
                                elif airforce != "on":
                                    headings = ["Year", "Branch", "Count", "Rate", "Gun in Home", "NO Gun in Home"]
                                    cursor1 = g.conn.execute('''SELECT S.year, B.branch, S.count, S.rate, A.in_home, A.not_in_home
                                                            FROM Suicides S, Military_Branch B, Access_To_Firearms A
                                                            WHERE s.sid = b.sid 
                                                            AND b.sid = a.sid
                                                            AND S.year >= (%s) 
                                                            AND S.year <= (%s)
                                                            AND B.branch != 'Air Force'
                                                        ''', year1,year2)  
                                    for result in cursor1:
                                        military.append(result) 
                                    cursor1.close()
                                    
                            elif marines !="on": 
                                if airforce == "on":
                                    headings = ["Year", "Branch", "Count", "Rate", "Gun in Home", "NO Gun in Home"]
                                    cursor1 = g.conn.execute('''SELECT S.year, B.branch, S.count, S.rate, A.in_home, A.not_in_home
                                                            FROM Suicides S, Military_Branch B, Access_To_Firearms A
                                                            WHERE s.sid = b.sid 
                                                            AND b.sid = a.sid
                                                            AND S.year >= (%s) 
                                                            AND S.year <= (%s)
                                                            AND B.branch != 'Army'
                                                            AND B.branch != 'Marine Corps'
                                                        ''', year1,year2)  
                                    for result in cursor1:
                                        military.append(result) 
                                    cursor1.close()
                                    
                                elif airforce != "on":
                                    headings = ["Year", "Branch", "Count", "Rate", "Gun in Home", "NO Gun in Home"]
                                    cursor1 = g.conn.execute('''SELECT S.year, B.branch, S.count, S.rate, A.in_home, A.not_in_home
                                                            FROM Suicides S, Military_Branch B, Access_To_Firearms A
                                                            WHERE s.sid = b.sid 
                                                            AND b.sid = a.sid
                                                            AND S.year >= (%s) 
                                                            AND S.year <= (%s)
                                                            AND B.branch != 'Army'
                                                            AND B.branch != 'Marine Corps'
                                                            AND B.branch != 'Air Force'
                                                        ''', year1,year2)  
                                    for result in cursor1:
                                        military.append(result) 
                                    cursor1.close()
                                    
                        elif navy !="on": 
                            if marines =="on": 
                                if airforce == "on":
                                    headings = ["Year", "Branch", "Count", "Rate", "Gun in Home", "NO Gun in Home"]
                                    cursor1 = g.conn.execute('''SELECT S.year, B.branch, S.count, S.rate, A.in_home, A.not_in_home
                                                            FROM Suicides S, Military_Branch B, Access_To_Firearms A
                                                            WHERE s.sid = b.sid 
                                                            AND b.sid = a.sid
                                                            AND S.year >= (%s) 
                                                            AND S.year <= (%s)
                                                            AND B.branch != 'Army'
                                                            AND B.branch != 'Navy''
                                                        ''', year1,year2)  
                                    for result in cursor1:
                                        military.append(result) 
                                    cursor1.close()
                                    
                                elif airforce != "on":
                                    headings = ["Year", "Branch", "Count", "Rate", "Gun in Home", "NO Gun in Home"]
                                    cursor1 = g.conn.execute('''SELECT S.year, B.branch, S.count, S.rate, A.in_home, A.not_in_home
                                                            FROM Suicides S, Military_Branch B, Access_To_Firearms A
                                                            WHERE s.sid = b.sid 
                                                            AND b.sid = a.sid
                                                            AND S.year >= (%s) 
                                                            AND S.year <= (%s)
                                                            AND B.branch != 'Army'
                                                            AND B.branch != 'Navy'
                                                            AND B.branch != 'Air Force'
                                                        ''', year1,year2)  
                                    for result in cursor1:
                                        military.append(result) 
                                    cursor1.close()
                                    
                            elif marines !="on": 
                                if airforce == "on":
                                    headings = ["Year", "Branch", "Count", "Rate", "Gun in Home", "NO Gun in Home"]
                                    cursor1 = g.conn.execute('''SELECT S.year, B.branch, S.count, S.rate, A.in_home, A.not_in_home
                                                            FROM Suicides S, Military_Branch B, Access_To_Firearms A
                                                            WHERE s.sid = b.sid 
                                                            AND b.sid = a.sid
                                                            AND S.year >= (%s) 
                                                            AND S.year <= (%s)
                                                            AND B.branch != 'Army'
                                                            AND B.branch != 'Navy'
                                                            AND B.branch != 'Marine Corps'
                                                        ''', year1,year2)  
                                    for result in cursor1:
                                        military.append(result) 
                                    cursor1.close()
                                    
                                elif airforce != "on":
                                    headings = ["Year", "Branch", "Count", "Rate", "Gun in Home", "NO Gun in Home"]
                                    cursor1 = g.conn.execute('''SELECT S.year, B.branch, S.count, S.rate, A.in_home, A.not_in_home
                                                            FROM Suicides S, Military_Branch B, Access_To_Firearms A
                                                            WHERE s.sid = b.sid 
                                                            AND b.sid = a.sid
                                                            AND S.year >= (%s) 
                                                            AND S.year <= (%s)
                                                            AND B.branch != 'Army'
                                                            AND B.branch != 'Navy'
                                                            AND B.branch != 'Marine Corps'
                                                            AND B.branch != 'Air Force'
                                                        ''', year1,year2)  
                                    for result in cursor1:
                                        military.append(result) 
                                    cursor1.close()
                if combined != 'on':
                    if army == "on":
                        if navy =="on": 
                            if marines =="on": 
                                if airforce == "on":
                                    headings = ["Year", "Branch", "Count", "Rate", "Gun in Home", "NO Gun in Home"]
                                    cursor1 = g.conn.execute('''SELECT S.year, B.branch, S.count, S.rate, A.in_home, A.not_in_home
                                                            FROM Suicides S, Military_Branch B, Access_To_Firearms A
                                                            WHERE s.sid = b.sid 
                                                            AND b.sid = a.sid
                                                            AND S.year >= (%s) 
                                                            AND S.year <= (%s)
                                                            AND B.branch != 'All'
                                                            ''', year1,year2)   
                                    for result in cursor1:
                                        military.append(result) 
                                    cursor1.close()
                                    
                                elif airforce != "on":
                                    headings = ["Year", "Branch", "Count", "Rate", "Gun in Home", "NO Gun in Home"]
                                    cursor1 = g.conn.execute('''SELECT S.year, B.branch, S.count, S.rate, A.in_home, A.not_in_home
                                                            FROM Suicides S, Military_Branch B, Access_To_Firearms A
                                                            WHERE s.sid = b.sid 
                                                            AND b.sid = a.sid
                                                            AND S.year >= (%s) 
                                                            AND S.year <= (%s)
                                                            AND B.branch != 'Air Force'
                                                            AND B.branch != 'All'
                                                            
                                                        ''', year1,year2)  
                                    for result in cursor1:
                                        military.append(result) 
                                    cursor1.close()
                                    
                            elif marines !="on": 
                                if airforce == "on":
                                    headings = ["Year", "Branch", "Count", "Rate", "Gun in Home", "NO Gun in Home"]
                                    cursor1 = g.conn.execute('''SELECT S.year, B.branch, S.count, S.rate, A.in_home, A.not_in_home
                                                            FROM Suicides S, Military_Branch B, Access_To_Firearms A
                                                            WHERE s.sid = b.sid 
                                                            AND b.sid = a.sid
                                                            AND S.year >= (%s) 
                                                            AND S.year <= (%s)
                                                            AND B.branch != 'Marine Corps'
                                                            AND B.branch != 'All'
                                                        ''', year1,year2)  
                                    for result in cursor1:
                                        military.append(result) 
                                    cursor1.close()
                                    
                                elif airforce != "on":
                                    headings = ["Year", "Branch", "Count", "Rate", "Gun in Home", "NO Gun in Home"]
                                    cursor1 = g.conn.execute('''SELECT S.year, B.branch, S.count, S.rate, A.in_home, A.not_in_home
                                                            FROM Suicides S, Military_Branch B, Access_To_Firearms A
                                                            WHERE s.sid = b.sid 
                                                            AND b.sid = a.sid
                                                            AND S.year >= (%s) 
                                                            AND S.year <= (%s)
                                                            AND B.branch != 'Marine Corps'
                                                            AND B.branch != 'Air Force'
                                                            AND B.branch != 'All'
                                                        ''', year1,year2)  
                                    for result in cursor1:
                                        military.append(result) 
                                    cursor1.close()
                                    
                        elif navy !="on": 
                            if marines =="on": 
                                if airforce == "on":
                                    headings = ["Year", "Branch", "Count", "Rate", "Gun in Home", "NO Gun in Home"]
                                    cursor1 = g.conn.execute('''SELECT S.year, B.branch, S.count, S.rate, A.in_home, A.not_in_home
                                                            FROM Suicides S, Military_Branch B, Access_To_Firearms A
                                                            WHERE s.sid = b.sid 
                                                            AND b.sid = a.sid
                                                            AND S.year >= (%s) 
                                                            AND S.year <= (%s)
                                                            AND B.branch != 'Navy'
                                                            AND B.branch != 'All'
                                                        ''', year1,year2)  
                                    for result in cursor1:
                                        military.append(result) 
                                    cursor1.close()
                                    
                                elif airforce != "on":
                                    headings = ["Year", "Branch", "Count", "Rate", "Gun in Home", "NO Gun in Home"]
                                    cursor1 = g.conn.execute('''SELECT S.year, B.branch, S.count, S.rate, A.in_home, A.not_in_home
                                                            FROM Suicides S, Military_Branch B, Access_To_Firearms A
                                                            WHERE s.sid = b.sid 
                                                            AND b.sid = a.sid
                                                            AND S.year >= (%s) 
                                                            AND S.year <= (%s)
                                                            AND B.branch != 'Navy'
                                                            AND B.branch != 'Marine Corps'
                                                            AND B.branch != 'Air Force'
                                                            AND B.branch != 'All'
                                                        ''', year1,year2)  
                                    for result in cursor1:
                                        military.append(result) 
                                    cursor1.close()
                                    
                            elif marines !="on": 
                                if airforce == "on":
                                    headings = ["Year", "Branch", "Count", "Rate", "Gun in Home", "NO Gun in Home"]
                                    cursor1 = g.conn.execute('''SELECT S.year, B.branch, S.count, S.rate, A.in_home, A.not_in_home
                                                            FROM Suicides S, Military_Branch B, Access_To_Firearms A
                                                            WHERE s.sid = b.sid 
                                                            AND b.sid = a.sid
                                                            AND S.year >= (%s) 
                                                            AND S.year <= (%s)
                                                            AND B.branch != 'Navy'
                                                            AND B.branch != 'Marine Corps'
                                                            AND B.branch != 'All'
                                                        ''', year1,year2)  
                                    for result in cursor1:
                                        military.append(result) 
                                    cursor1.close()
                                    
                                elif airforce != "on":
                                    headings = ["Year", "Branch", "Count", "Rate", "Gun in Home", "NO Gun in Home"]
                                    cursor1 = g.conn.execute('''SELECT S.year, B.branch, S.count, S.rate, A.in_home, A.not_in_home
                                                            FROM Suicides S, Military_Branch B, Access_To_Firearms A
                                                            WHERE s.sid = b.sid 
                                                            AND b.sid = a.sid
                                                            AND S.year >= (%s) 
                                                            AND S.year <= (%s)
                                                            AND B.branch != 'Navy'
                                                            AND B.branch != 'Marine Corps'
                                                            AND B.branch != 'Air Force'
                                                            AND B.branch != 'All'
                                                        ''', year1,year2)  
                                    for result in cursor1:
                                        military.append(result) 
                                    cursor1.close()
                                    
                    elif army !="on":
                        if navy =="on": 
                            if marines =="on": 
                                if airforce == "on":
                                    headings = ["Year", "Branch", "Count", "Rate", "Gun in Home", "NO Gun in Home"]
                                    cursor1 = g.conn.execute('''SELECT S.year, B.branch, S.count, S.rate, A.in_home, A.not_in_home
                                                            FROM Suicides S, Military_Branch B, Access_To_Firearms A
                                                            WHERE s.sid = b.sid 
                                                            AND b.sid = a.sid
                                                            AND S.year >= (%s) 
                                                            AND S.year <= (%s)
                                                            AND B.branch != 'Army'
                                                            AND B.branch != 'All'
                                                        ''', year1,year2)  
                                    for result in cursor1:
                                        military.append(result) 
                                    cursor1.close()
                                    
                                elif airforce != "on":
                                    headings = ["Year", "Branch", "Count", "Rate", "Gun in Home", "NO Gun in Home"]
                                    cursor1 = g.conn.execute('''SELECT S.year, B.branch, S.count, S.rate, A.in_home, A.not_in_home
                                                            FROM Suicides S, Military_Branch B, Access_To_Firearms A
                                                            WHERE s.sid = b.sid 
                                                            AND b.sid = a.sid
                                                            AND S.year >= (%s) 
                                                            AND S.year <= (%s)
                                                            AND B.branch != 'Army'
                                                            AND B.branch != 'Air Force'
                                                            AND B.branch != 'All'
                                                        ''', year1,year2)  
                                    for result in cursor1:
                                        military.append(result) 
                                    cursor1.close()
                                    
                            elif marines !="on": 
                                if airforce == "on":
                                    headings = ["Year", "Branch", "Count", "Rate", "Gun in Home", "NO Gun in Home"]
                                    cursor1 = g.conn.execute('''SELECT S.year, B.branch, S.count, S.rate, A.in_home, A.not_in_home
                                                            FROM Suicides S, Military_Branch B, Access_To_Firearms A
                                                            WHERE s.sid = b.sid 
                                                            AND b.sid = a.sid
                                                            AND S.year >= (%s) 
                                                            AND S.year <= (%s)
                                                            AND B.branch != 'Army'
                                                            AND B.branch != 'Marine Corps'
                                                            AND B.branch != 'All'
                                                        ''', year1,year2)  
                                    for result in cursor1:
                                        military.append(result) 
                                    cursor1.close()
                                    
                                elif airforce != "on":
                                    headings = ["Year", "Branch", "Count", "Rate", "Gun in Home", "NO Gun in Home"]
                                    cursor1 = g.conn.execute('''SELECT S.year, B.branch, S.count, S.rate, A.in_home, A.not_in_home
                                                            FROM Suicides S, Military_Branch B, Access_To_Firearms A
                                                            WHERE s.sid = b.sid 
                                                            AND b.sid = a.sid
                                                            AND S.year >= (%s) 
                                                            AND S.year <= (%s)
                                                            AND B.branch != 'Army'
                                                            AND B.branch != 'Marine Corps'
                                                            AND B.branch != 'Air Force'
                                                            AND B.branch != 'All'
                                                        ''', year1,year2)  
                                    for result in cursor1:
                                        military.append(result) 
                                    cursor1.close()
                                    
                        elif navy !="on": 
                            if marines =="on": 
                                if airforce == "on":
                                    headings = ["Year", "Branch", "Count", "Rate", "Gun in Home", "NO Gun in Home"]
                                    cursor1 = g.conn.execute('''SELECT S.year, B.branch, S.count, S.rate, A.in_home, A.not_in_home
                                                            FROM Suicides S, Military_Branch B, Access_To_Firearms A
                                                            WHERE s.sid = b.sid 
                                                            AND b.sid = a.sid
                                                            AND S.year >= (%s) 
                                                            AND S.year <= (%s)
                                                            AND B.branch != 'Army'
                                                            AND B.branch != 'Navy''
                                                            AND B.branch != 'All'
                                                        ''', year1,year2)  
                                    for result in cursor1:
                                        military.append(result) 
                                    cursor1.close()
                                    
                                elif airforce != "on":
                                    headings = ["Year", "Branch", "Count", "Rate", "Gun in Home", "NO Gun in Home"]
                                    cursor1 = g.conn.execute('''SELECT S.year, B.branch, S.count, S.rate, A.in_home, A.not_in_home
                                                            FROM Suicides S, Military_Branch B, Access_To_Firearms A
                                                            WHERE s.sid = b.sid 
                                                            AND b.sid = a.sid
                                                            AND S.year >= (%s) 
                                                            AND S.year <= (%s)
                                                            AND B.branch != 'Army'
                                                            AND B.branch != 'Navy'
                                                            AND B.branch != 'Air Force'
                                                            AND B.branch != 'All'
                                                        ''', year1,year2)  
                                    for result in cursor1:
                                        military.append(result) 
                                    cursor1.close()
                                    
                            elif marines !="on": 
                                if airforce == "on":
                                    headings = ["Year", "Branch", "Count", "Rate", "Gun in Home", "NO Gun in Home"]
                                    cursor1 = g.conn.execute('''SELECT S.year, B.branch, S.count, S.rate, A.in_home, A.not_in_home
                                                            FROM Suicides S, Military_Branch B, Access_To_Firearms A
                                                            WHERE s.sid = b.sid 
                                                            AND b.sid = a.sid
                                                            AND S.year >= (%s) 
                                                            AND S.year <= (%s)
                                                            AND B.branch != 'Army'
                                                            AND B.branch != 'Navy'
                                                            AND B.branch != 'Marine Corps'
                                                            AND B.branch != 'All'
                                                        ''', year1,year2)  
                                    for result in cursor1:
                                        military.append(result) 
                                    cursor1.close()
                                    
                                elif airforce != "on":
                                    headings = ["Year", "Branch", "Count", "Rate", "Gun in Home", "NO Gun in Home"]
                                    cursor1 = g.conn.execute('''SELECT S.year, B.branch, S.count, S.rate, A.in_home, A.not_in_home
                                                            FROM Suicides S, Military_Branch B, Access_To_Firearms A
                                                            WHERE s.sid = b.sid 
                                                            AND b.sid = a.sid
                                                            AND S.year >= (%s) 
                                                            AND S.year <= (%s)
                                                            AND B.branch != 'Army'
                                                            AND B.branch != 'Navy'
                                                            AND B.branch != 'Marine Corps'
                                                            AND B.branch != 'Air Force'
                                                            AND B.branch != 'All'
                                                        ''', year1,year2)  
                                    for result in cursor1:
                                        military.append(result) 
                                    cursor1.close()
                                    
    if showaccess != "on":
        if showrank == "on":
            if showmh == "on":
                if combined == 'on':
                    if army == "on":
                        if navy =="on": 
                            if marines =="on": 
                                if airforce == "on":
                                    headings = ["Year", "Branch", "Count", "Rate", "Lower Enlisted", 
                                                "NCOs", "Officers", "Warrant Officers", 
                                                "Mental Health Diagnosis", "NO Mental Health Diagnosis",
                                                "TBI History", "NO TBI", "Previous Self-Harm", 
                                                "NO Previous Self-Harm", "Visited Health Services", "DID NOT visit"]
                                    cursor1 = g.conn.execute('''SELECT S.year, B.branch, S.count, S.rate, 
                                                             R.e1_e4, R.e5_e9, R.officer, R.warrant_officer, M.health_diag_y,
                                                             M.health_diag_n, m.tbi_y, m.tbi_n, m.prev_self_harm_y, m.prev_self_harm_n,
                                                             m.health_ser_used_y, m.health_ser_used_n
                                                            FROM Suicides S, Military_Branch B, Rank R, Mental_Characteristics M
                                                            WHERE s.sid = b.sid 
                                                            AND b.sid = r.sid
                                                            AND r.sid = m.sid
                                                            AND S.year >= (%s) 
                                                            AND S.year <= (%s)
                                                            ''', year1,year2)   
                                    for result in cursor1:
                                        military.append(result) 
                                    cursor1.close()
                                    
                                elif airforce != "on":
                                    headings = ["Year", "Branch", "Count", "Rate", "Lower Enlisted", 
                                                "NCOs", "Officers", "Warrant Officers", 
                                                "Mental Health Diagnosis", "NO Mental Health Diagnosis",
                                                "TBI History", "NO TBI", "Previous Self-Harm", 
                                                "NO Previous Self-Harm", "Visited Health Services", "DID NOT visit"]
                                    cursor1 = g.conn.execute('''SELECT S.year, B.branch, S.count, S.rate, 
                                                             R.e1_e4, R.e5_e9, R.officer, R.warrant_officer, M.health_diag_y,
                                                             M.health_diag_n, m.tbi_y, m.tbi_n, m.prev_self_harm_y, m.prev_self_harm_n,
                                                             m.health_ser_used_y, m.health_ser_used_n
                                                            FROM Suicides S, Military_Branch B, Rank R, Mental_Characteristics M
                                                            WHERE s.sid = b.sid 
                                                            AND b.sid = r.sid
                                                            AND r.sid = m.sid
                                                            AND S.year >= (%s) 
                                                            AND S.year <= (%s)
                                                            AND B.branch != 'Air Force'
                                                            ''', year1,year2)    
                                    for result in cursor1:
                                        military.append(result) 
                                    cursor1.close()
                                    
                            elif marines !="on": 
                                if airforce == "on":
                                    headings = ["Year", "Branch", "Count", "Rate", "Lower Enlisted", 
                                                "NCOs", "Officers", "Warrant Officers", 
                                                "Mental Health Diagnosis", "NO Mental Health Diagnosis",
                                                "TBI History", "NO TBI", "Previous Self-Harm", 
                                                "NO Previous Self-Harm", "Visited Health Services", "DID NOT visit"]
                                    cursor1 = g.conn.execute('''SELECT S.year, B.branch, S.count, S.rate, 
                                                             R.e1_e4, R.e5_e9, R.officer, R.warrant_officer, M.health_diag_y,
                                                             M.health_diag_n, m.tbi_y, m.tbi_n, m.prev_self_harm_y, m.prev_self_harm_n,
                                                             m.health_ser_used_y, m.health_ser_used_n
                                                            FROM Suicides S, Military_Branch B, Rank R, Mental_Characteristics M
                                                            WHERE s.sid = b.sid 
                                                            AND b.sid = r.sid
                                                            AND r.sid = m.sid
                                                            AND S.year >= (%s) 
                                                            AND S.year <= (%s)
                                                            AND B.branch != 'Marine Corps'
                                                            ''', year1,year2)    
                                    for result in cursor1:
                                        military.append(result) 
                                    cursor1.close()
                                    
                                elif airforce != "on":
                                    headings = ["Year", "Branch", "Count", "Rate", "Lower Enlisted", 
                                                "NCOs", "Officers", "Warrant Officers", 
                                                "Mental Health Diagnosis", "NO Mental Health Diagnosis",
                                                "TBI History", "NO TBI", "Previous Self-Harm", 
                                                "NO Previous Self-Harm", "Visited Health Services", "DID NOT visit"]
                                    cursor1 = g.conn.execute('''SELECT S.year, B.branch, S.count, S.rate, 
                                                             R.e1_e4, R.e5_e9, R.officer, R.warrant_officer, M.health_diag_y,
                                                             M.health_diag_n, m.tbi_y, m.tbi_n, m.prev_self_harm_y, m.prev_self_harm_n,
                                                             m.health_ser_used_y, m.health_ser_used_n
                                                            FROM Suicides S, Military_Branch B, Rank R, Mental_Characteristics M
                                                            WHERE s.sid = b.sid 
                                                            AND b.sid = r.sid
                                                            AND r.sid = m.sid
                                                            AND S.year >= (%s) 
                                                            AND S.year <= (%s)
                                                            AND B.branch != 'Air Force'
                                                            AND B.branch != 'Marine Corps'
                                                            ''', year1,year2)   
                                    for result in cursor1:
                                        military.append(result) 
                                    cursor1.close()
                                    
                        elif navy !="on": 
                            if marines =="on": 
                                if airforce == "on":
                                    headings = ["Year", "Branch", "Count", "Rate", "Lower Enlisted", 
                                                "NCOs", "Officers", "Warrant Officers", 
                                                "Mental Health Diagnosis", "NO Mental Health Diagnosis",
                                                "TBI History", "NO TBI", "Previous Self-Harm", 
                                                "NO Previous Self-Harm", "Visited Health Services", "DID NOT visit"]
                                    cursor1 = g.conn.execute('''SELECT S.year, B.branch, S.count, S.rate, 
                                                             R.e1_e4, R.e5_e9, R.officer, R.warrant_officer, M.health_diag_y,
                                                             M.health_diag_n, m.tbi_y, m.tbi_n, m.prev_self_harm_y, m.prev_self_harm_n,
                                                             m.health_ser_used_y, m.health_ser_used_n
                                                            FROM Suicides S, Military_Branch B, Rank R, Mental_Characteristics M
                                                            WHERE s.sid = b.sid 
                                                            AND b.sid = r.sid
                                                            AND r.sid = m.sid
                                                            AND S.year >= (%s) 
                                                            AND S.year <= (%s)
                                                            AND B.branch != 'Navy'
                                                            ''', year1,year2)  
                                    for result in cursor1:
                                        military.append(result) 
                                    cursor1.close()
                                    
                                elif airforce != "on":
                                    headings = ["Year", "Branch", "Count", "Rate", "Lower Enlisted", 
                                                "NCOs", "Officers", "Warrant Officers", 
                                                "Mental Health Diagnosis", "NO Mental Health Diagnosis",
                                                "TBI History", "NO TBI", "Previous Self-Harm", 
                                                "NO Previous Self-Harm", "Visited Health Services", "DID NOT visit"]
                                    cursor1 = g.conn.execute('''SELECT S.year, B.branch, S.count, S.rate, 
                                                             R.e1_e4, R.e5_e9, R.officer, R.warrant_officer, M.health_diag_y,
                                                             M.health_diag_n, m.tbi_y, m.tbi_n, m.prev_self_harm_y, m.prev_self_harm_n,
                                                             m.health_ser_used_y, m.health_ser_used_n
                                                            FROM Suicides S, Military_Branch B, Rank R, Mental_Characteristics M
                                                            WHERE s.sid = b.sid 
                                                            AND b.sid = r.sid
                                                            AND r.sid = m.sid
                                                            AND S.year >= (%s) 
                                                            AND S.year <= (%s)
                                                            AND B.branch != 'Navy'
                                                            AND B.branch != 'Air Force'
                                                            ''', year1,year2)  
                                    for result in cursor1:
                                        military.append(result) 
                                    cursor1.close()
                                    
                            elif marines !="on": 
                                if airforce == "on":
                                    headings = ["Year", "Branch", "Count", "Rate", "Lower Enlisted", 
                                                "NCOs", "Officers", "Warrant Officers", 
                                                "Mental Health Diagnosis", "NO Mental Health Diagnosis",
                                                "TBI History", "NO TBI", "Previous Self-Harm", 
                                                "NO Previous Self-Harm", "Visited Health Services", "DID NOT visit"]
                                    cursor1 = g.conn.execute('''SELECT S.year, B.branch, S.count, S.rate, 
                                                             R.e1_e4, R.e5_e9, R.officer, R.warrant_officer, M.health_diag_y,
                                                             M.health_diag_n, m.tbi_y, m.tbi_n, m.prev_self_harm_y, m.prev_self_harm_n,
                                                             m.health_ser_used_y, m.health_ser_used_n
                                                            FROM Suicides S, Military_Branch B, Rank R, Mental_Characteristics M
                                                            WHERE s.sid = b.sid 
                                                            AND b.sid = r.sid
                                                            AND r.sid = m.sid
                                                            AND S.year >= (%s) 
                                                            AND S.year <= (%s)
                                                            AND B.branch != 'Navy'
                                                            AND B.branch != 'Marine Corps'
                                                             ''', year1,year2)
                                    for result in cursor1:
                                        military.append(result) 
                                    cursor1.close()
                                    
                                elif airforce != "on":
                                    headings = ["Year", "Branch", "Count", "Rate", "Lower Enlisted", 
                                                "NCOs", "Officers", "Warrant Officers", 
                                                "Mental Health Diagnosis", "NO Mental Health Diagnosis",
                                                "TBI History", "NO TBI", "Previous Self-Harm", 
                                                "NO Previous Self-Harm", "Visited Health Services", "DID NOT visit"]
                                    cursor1 = g.conn.execute('''SELECT S.year, B.branch, S.count, S.rate, 
                                                             R.e1_e4, R.e5_e9, R.officer, R.warrant_officer, M.health_diag_y,
                                                             M.health_diag_n, m.tbi_y, m.tbi_n, m.prev_self_harm_y, m.prev_self_harm_n,
                                                             m.health_ser_used_y, m.health_ser_used_n
                                                            FROM Suicides S, Military_Branch B, Rank R, Mental_Characteristics M
                                                            WHERE s.sid = b.sid 
                                                            AND b.sid = r.sid
                                                            AND r.sid = m.sid
                                                            AND S.year >= (%s) 
                                                            AND S.year <= (%s)
                                                            AND B.branch != 'Navy'
                                                            AND B.branch != 'Marine Corps'
                                                            AND B.branch != 'Air Force'
                                                        ''', year1,year2)  
                                    for result in cursor1:
                                        military.append(result) 
                                    cursor1.close()
                                    
                    elif army !="on":
                        if navy =="on": 
                            if marines =="on": 
                                if airforce == "on":
                                    headings = ["Year", "Branch", "Count", "Rate", "Lower Enlisted", 
                                                "NCOs", "Officers", "Warrant Officers", 
                                                "Mental Health Diagnosis", "NO Mental Health Diagnosis",
                                                "TBI History", "NO TBI", "Previous Self-Harm", 
                                                "NO Previous Self-Harm", "Visited Health Services", "DID NOT visit"]
                                    cursor1 = g.conn.execute('''SELECT S.year, B.branch, S.count, S.rate, 
                                                             R.e1_e4, R.e5_e9, R.officer, R.warrant_officer, M.health_diag_y,
                                                             M.health_diag_n, m.tbi_y, m.tbi_n, m.prev_self_harm_y, m.prev_self_harm_n,
                                                             m.health_ser_used_y, m.health_ser_used_n
                                                            FROM Suicides S, Military_Branch B, Rank R, Mental_Characteristics M
                                                            WHERE s.sid = b.sid 
                                                            AND b.sid = r.sid
                                                            AND r.sid = m.sid
                                                            AND S.year >= (%s) 
                                                            AND S.year <= (%s)
                                                            AND B.branch != 'Army'
                                                            AND B.branch != 'Navy'
                                                            AND B.branch != 'Marine Corps'
                                                            AND B.branch != 'Air Force'
                                                        ''', year1,year2)  
                                    for result in cursor1:
                                        military.append(result) 
                                    cursor1.close()
                                    
                                elif airforce != "on":
                                    headings = ["Year", "Branch", "Count", "Rate", "Lower Enlisted", 
                                                "NCOs", "Officers", "Warrant Officers", 
                                                "Mental Health Diagnosis", "NO Mental Health Diagnosis",
                                                "TBI History", "NO TBI", "Previous Self-Harm", 
                                                "NO Previous Self-Harm", "Visited Health Services", "DID NOT visit"]
                                    cursor1 = g.conn.execute('''SELECT S.year, B.branch, S.count, S.rate, 
                                                             R.e1_e4, R.e5_e9, R.officer, R.warrant_officer, M.health_diag_y,
                                                             M.health_diag_n, m.tbi_y, m.tbi_n, m.prev_self_harm_y, m.prev_self_harm_n,
                                                             m.health_ser_used_y, m.health_ser_used_n
                                                            FROM Suicides S, Military_Branch B, Rank R, Mental_Characteristics M
                                                            WHERE s.sid = b.sid 
                                                            AND b.sid = r.sid
                                                            AND r.sid = m.sid
                                                            AND S.year >= (%s) 
                                                            AND S.year <= (%s)
                                                            AND B.branch != 'Army'
                                                            AND B.branch != 'Air Force'
                                                        ''', year1,year2)  
                                    for result in cursor1:
                                        military.append(result) 
                                    cursor1.close()
                                    
                            elif marines !="on": 
                                if airforce == "on":
                                    headings = ["Year", "Branch", "Count", "Rate", "Lower Enlisted", 
                                                "NCOs", "Officers", "Warrant Officers", 
                                                "Mental Health Diagnosis", "NO Mental Health Diagnosis",
                                                "TBI History", "NO TBI", "Previous Self-Harm", 
                                                "NO Previous Self-Harm", "Visited Health Services", "DID NOT visit"]
                                    cursor1 = g.conn.execute('''SELECT S.year, B.branch, S.count, S.rate, 
                                                             R.e1_e4, R.e5_e9, R.officer, R.warrant_officer, M.health_diag_y,
                                                             M.health_diag_n, m.tbi_y, m.tbi_n, m.prev_self_harm_y, m.prev_self_harm_n,
                                                             m.health_ser_used_y, m.health_ser_used_n
                                                            FROM Suicides S, Military_Branch B, Rank R, Mental_Characteristics M
                                                            WHERE s.sid = b.sid 
                                                            AND b.sid = r.sid
                                                            AND r.sid = m.sid
                                                            AND S.year >= (%s) 
                                                            AND S.year <= (%s)
                                                            AND B.branch != 'Army'
                                                            AND B.branch != 'Marine Corps'
                                                        ''', year1,year2)  
                                    for result in cursor1:
                                        military.append(result) 
                                    cursor1.close()
                                    
                                elif airforce != "on":
                                    headings = ["Year", "Branch", "Count", "Rate"]
                                    cursor1 = g.conn.execute('''SELECT *
                                                        FROM Suicides S, Military_Branch B, Rank R, Mental_Characteristics M
                                                        WHERE s.sid = b.sid 
                                                        AND b.sid = r.sid
                                                        AND r.sid = m.sid
                                                        AND S.year >= (%s) 
                                                        AND S.year <= (%s)
                                                        AND B.branch != 'Army'
                                                        AND B.branch != 'Marine Corps'
                                                        AND B.branch != 'Air Force'
                                                        ''', year1,year2)  
                                    for result in cursor1:
                                        military.append(result) 
                                    cursor1.close()
                                    
                        elif navy !="on": 
                            if marines =="on": 
                                if airforce == "on":
                                    headings = ["Year", "Branch", "Count", "Rate", "Lower Enlisted", 
                                                "NCOs", "Officers", "Warrant Officers", 
                                                "Mental Health Diagnosis", "NO Mental Health Diagnosis",
                                                "TBI History", "NO TBI", "Previous Self-Harm", 
                                                "NO Previous Self-Harm", "Visited Health Services", "DID NOT visit"]
                                    cursor1 = g.conn.execute('''SELECT S.year, B.branch, S.count, S.rate, 
                                                             R.e1_e4, R.e5_e9, R.officer, R.warrant_officer, M.health_diag_y,
                                                             M.health_diag_n, m.tbi_y, m.tbi_n, m.prev_self_harm_y, m.prev_self_harm_n,
                                                             m.health_ser_used_y, m.health_ser_used_n
                                                            FROM Suicides S, Military_Branch B, Rank R, Mental_Characteristics M
                                                            WHERE s.sid = b.sid 
                                                            AND b.sid = r.sid
                                                            AND r.sid = m.sid
                                                            AND S.year >= (%s) 
                                                            AND S.year <= (%s)
                                                            AND B.branch != 'Army'
                                                            AND B.branch != 'Navy'
                                                        ''', year1,year2)  
                                    for result in cursor1:
                                        military.append(result) 
                                    cursor1.close()
                                    
                                elif airforce != "on":
                                    headings = ["Year", "Branch", "Count", "Rate", "Lower Enlisted", 
                                                "NCOs", "Officers", "Warrant Officers", 
                                                "Mental Health Diagnosis", "NO Mental Health Diagnosis",
                                                "TBI History", "NO TBI", "Previous Self-Harm", 
                                                "NO Previous Self-Harm", "Visited Health Services", "DID NOT visit"]
                                    cursor1 = g.conn.execute('''SELECT S.year, B.branch, S.count, S.rate, 
                                                             R.e1_e4, R.e5_e9, R.officer, R.warrant_officer, M.health_diag_y,
                                                             M.health_diag_n, m.tbi_y, m.tbi_n, m.prev_self_harm_y, m.prev_self_harm_n,
                                                             m.health_ser_used_y, m.health_ser_used_n
                                                            FROM Suicides S, Military_Branch B, Rank R, Mental_Characteristics M
                                                            WHERE s.sid = b.sid 
                                                            AND b.sid = r.sid
                                                            AND r.sid = m.sid
                                                            AND S.year >= (%s) 
                                                            AND S.year <= (%s)
                                                            AND B.branch != 'Army'
                                                            AND B.branch != 'Navy'
                                                            AND B.branch != 'Air Force'
                                                        ''', year1,year2)  
                                    for result in cursor1:
                                        military.append(result) 
                                    cursor1.close()
                                    
                            elif marines !="on": 
                                if airforce == "on":
                                    headings = ["Year", "Branch", "Count", "Rate", "Lower Enlisted", 
                                                "NCOs", "Officers", "Warrant Officers", 
                                                "Mental Health Diagnosis", "NO Mental Health Diagnosis",
                                                "TBI History", "NO TBI", "Previous Self-Harm", 
                                                "NO Previous Self-Harm", "Visited Health Services", "DID NOT visit"]
                                    cursor1 = g.conn.execute('''SELECT S.year, B.branch, S.count, S.rate, 
                                                             R.e1_e4, R.e5_e9, R.officer, R.warrant_officer, M.health_diag_y,
                                                             M.health_diag_n, m.tbi_y, m.tbi_n, m.prev_self_harm_y, m.prev_self_harm_n,
                                                             m.health_ser_used_y, m.health_ser_used_n
                                                            FROM Suicides S, Military_Branch B, Rank R, Mental_Characteristics M
                                                            WHERE s.sid = b.sid 
                                                            AND b.sid = r.sid
                                                            AND r.sid = m.sid
                                                            AND S.year >= (%s) 
                                                            AND S.year <= (%s)
                                                            AND B.branch != 'Army'
                                                            AND B.branch != 'Navy'
                                                            AND B.branch != 'Marine Corps'
                                                        ''', year1,year2)  
                                    for result in cursor1:
                                        military.append(result) 
                                    cursor1.close()
                                    
                                elif airforce != "on":
                                    headings = ["Year", "Branch", "Count", "Rate", "Lower Enlisted", 
                                                "NCOs", "Officers", "Warrant Officers", 
                                                "Mental Health Diagnosis", "NO Mental Health Diagnosis",
                                                "TBI History", "NO TBI", "Previous Self-Harm", 
                                                "NO Previous Self-Harm", "Visited Health Services", "DID NOT visit"]
                                    cursor1 = g.conn.execute('''SELECT S.year, B.branch, S.count, S.rate, 
                                                             R.e1_e4, R.e5_e9, R.officer, R.warrant_officer, M.health_diag_y,
                                                             M.health_diag_n, m.tbi_y, m.tbi_n, m.prev_self_harm_y, m.prev_self_harm_n,
                                                             m.health_ser_used_y, m.health_ser_used_n
                                                            FROM Suicides S, Military_Branch B, Rank R, Mental_Characteristics M
                                                            WHERE s.sid = b.sid 
                                                            AND b.sid = r.sid
                                                            AND r.sid = m.sid
                                                            AND S.year >= (%s) 
                                                            AND S.year <= (%s)
                                                            AND B.branch != 'Army'
                                                            AND B.branch != 'Navy'
                                                            AND B.branch != 'Marine Corps'
                                                            AND B.branch != 'Air Force'
                                                        ''', year1,year2)  
                                    for result in cursor1:
                                        military.append(result) 
                                    cursor1.close()
                if combined != 'on':
                    if army == "on":
                        if navy =="on": 
                            if marines =="on": 
                                if airforce == "on":
                                    headings = ["Year", "Branch", "Count", "Rate", "Lower Enlisted", 
                                                "NCOs", "Officers", "Warrant Officers", 
                                                "Mental Health Diagnosis", "NO Mental Health Diagnosis",
                                                "TBI History", "NO TBI", "Previous Self-Harm", 
                                                "NO Previous Self-Harm", "Visited Health Services", "DID NOT visit"]
                                    cursor1 = g.conn.execute('''SELECT S.year, B.branch, S.count, S.rate, 
                                                             R.e1_e4, R.e5_e9, R.officer, R.warrant_officer, M.health_diag_y,
                                                             M.health_diag_n, m.tbi_y, m.tbi_n, m.prev_self_harm_y, m.prev_self_harm_n,
                                                             m.health_ser_used_y, m.health_ser_used_n
                                                            FROM Suicides S, Military_Branch B, Rank R, Mental_Characteristics M
                                                            WHERE s.sid = b.sid 
                                                            AND b.sid = r.sid
                                                            AND r.sid = m.sid
                                                            AND S.year >= (%s) 
                                                            AND S.year <= (%s)
                                                            AND B.branch != 'All'
                                                            ''', year1,year2)   
                                    for result in cursor1:
                                        military.append(result) 
                                    cursor1.close()
                                    
                                elif airforce != "on":
                                    headings = ["Year", "Branch", "Count", "Rate", "Lower Enlisted", 
                                                "NCOs", "Officers", "Warrant Officers", 
                                                "Mental Health Diagnosis", "NO Mental Health Diagnosis",
                                                "TBI History", "NO TBI", "Previous Self-Harm", 
                                                "NO Previous Self-Harm", "Visited Health Services", "DID NOT visit"]
                                    cursor1 = g.conn.execute('''SELECT S.year, B.branch, S.count, S.rate, 
                                                             R.e1_e4, R.e5_e9, R.officer, R.warrant_officer, M.health_diag_y,
                                                             M.health_diag_n, m.tbi_y, m.tbi_n, m.prev_self_harm_y, m.prev_self_harm_n,
                                                             m.health_ser_used_y, m.health_ser_used_n
                                                            FROM Suicides S, Military_Branch B, Rank R, Mental_Characteristics M
                                                            WHERE s.sid = b.sid 
                                                            AND b.sid = r.sid
                                                            AND r.sid = m.sid
                                                            AND S.year >= (%s) 
                                                            AND S.year <= (%s)
                                                            AND B.branch != 'Air Force'
                                                            AND B.branch != 'All'
                                                            ''', year1,year2)    
                                    for result in cursor1:
                                        military.append(result) 
                                    cursor1.close()
                                    
                            elif marines !="on": 
                                if airforce == "on":
                                    headings = ["Year", "Branch", "Count", "Rate", "Lower Enlisted", 
                                                "NCOs", "Officers", "Warrant Officers", 
                                                "Mental Health Diagnosis", "NO Mental Health Diagnosis",
                                                "TBI History", "NO TBI", "Previous Self-Harm", 
                                                "NO Previous Self-Harm", "Visited Health Services", "DID NOT visit"]
                                    cursor1 = g.conn.execute('''SELECT S.year, B.branch, S.count, S.rate, 
                                                             R.e1_e4, R.e5_e9, R.officer, R.warrant_officer, M.health_diag_y,
                                                             M.health_diag_n, m.tbi_y, m.tbi_n, m.prev_self_harm_y, m.prev_self_harm_n,
                                                             m.health_ser_used_y, m.health_ser_used_n
                                                            FROM Suicides S, Military_Branch B, Rank R, Mental_Characteristics M
                                                            WHERE s.sid = b.sid 
                                                            AND b.sid = r.sid
                                                            AND r.sid = m.sid
                                                            AND S.year >= (%s) 
                                                            AND S.year <= (%s)
                                                            AND B.branch != 'Marine Corps'
                                                            AND B.branch != 'All'
                                                            ''', year1,year2)    
                                    for result in cursor1:
                                        military.append(result) 
                                    cursor1.close()
                                    
                                elif airforce != "on":
                                    headings = ["Year", "Branch", "Count", "Rate", "Lower Enlisted", 
                                                "NCOs", "Officers", "Warrant Officers", 
                                                "Mental Health Diagnosis", "NO Mental Health Diagnosis",
                                                "TBI History", "NO TBI", "Previous Self-Harm", 
                                                "NO Previous Self-Harm", "Visited Health Services", "DID NOT visit"]
                                    cursor1 = g.conn.execute('''SELECT S.year, B.branch, S.count, S.rate, 
                                                             R.e1_e4, R.e5_e9, R.officer, R.warrant_officer, M.health_diag_y,
                                                             M.health_diag_n, m.tbi_y, m.tbi_n, m.prev_self_harm_y, m.prev_self_harm_n,
                                                             m.health_ser_used_y, m.health_ser_used_n
                                                            FROM Suicides S, Military_Branch B, Rank R, Mental_Characteristics M
                                                            WHERE s.sid = b.sid 
                                                            AND b.sid = r.sid
                                                            AND r.sid = m.sid
                                                            AND S.year >= (%s) 
                                                            AND S.year <= (%s)
                                                            AND B.branch != 'Air Force'
                                                            AND B.branch != 'Marine Corps'
                                                            AND B.branch != 'All'
                                                            ''', year1,year2)   
                                    for result in cursor1:
                                        military.append(result) 
                                    cursor1.close()
                                    
                        elif navy !="on": 
                            if marines =="on": 
                                if airforce == "on":
                                    headings = ["Year", "Branch", "Count", "Rate", "Lower Enlisted", 
                                                "NCOs", "Officers", "Warrant Officers", 
                                                "Mental Health Diagnosis", "NO Mental Health Diagnosis",
                                                "TBI History", "NO TBI", "Previous Self-Harm", 
                                                "NO Previous Self-Harm", "Visited Health Services", "DID NOT visit"]
                                    cursor1 = g.conn.execute('''SELECT S.year, B.branch, S.count, S.rate, 
                                                             R.e1_e4, R.e5_e9, R.officer, R.warrant_officer, M.health_diag_y,
                                                             M.health_diag_n, m.tbi_y, m.tbi_n, m.prev_self_harm_y, m.prev_self_harm_n,
                                                             m.health_ser_used_y, m.health_ser_used_n
                                                            FROM Suicides S, Military_Branch B, Rank R, Mental_Characteristics M
                                                            WHERE s.sid = b.sid 
                                                            AND b.sid = r.sid
                                                            AND r.sid = m.sid
                                                            AND S.year >= (%s) 
                                                            AND S.year <= (%s)
                                                            AND B.branch != 'Navy'
                                                            AND B.branch != 'All'
                                                            ''', year1,year2)  
                                    for result in cursor1:
                                        military.append(result) 
                                    cursor1.close()
                                    
                                elif airforce != "on":
                                    headings = ["Year", "Branch", "Count", "Rate", "Lower Enlisted", 
                                                "NCOs", "Officers", "Warrant Officers", 
                                                "Mental Health Diagnosis", "NO Mental Health Diagnosis",
                                                "TBI History", "NO TBI", "Previous Self-Harm", 
                                                "NO Previous Self-Harm", "Visited Health Services", "DID NOT visit"]
                                    cursor1 = g.conn.execute('''SELECT S.year, B.branch, S.count, S.rate, 
                                                             R.e1_e4, R.e5_e9, R.officer, R.warrant_officer, M.health_diag_y,
                                                             M.health_diag_n, m.tbi_y, m.tbi_n, m.prev_self_harm_y, m.prev_self_harm_n,
                                                             m.health_ser_used_y, m.health_ser_used_n
                                                            FROM Suicides S, Military_Branch B, Rank R, Mental_Characteristics M
                                                            WHERE s.sid = b.sid 
                                                            AND b.sid = r.sid
                                                            AND r.sid = m.sid
                                                            AND S.year >= (%s) 
                                                            AND S.year <= (%s)
                                                            AND B.branch != 'Navy'
                                                            AND B.branch != 'Air Force'
                                                            AND B.branch != 'All'
                                                            ''', year1,year2)  
                                    for result in cursor1:
                                        military.append(result) 
                                    cursor1.close()
                                    
                            elif marines !="on": 
                                if airforce == "on":
                                    headings = ["Year", "Branch", "Count", "Rate", "Lower Enlisted", 
                                                "NCOs", "Officers", "Warrant Officers", 
                                                "Mental Health Diagnosis", "NO Mental Health Diagnosis",
                                                "TBI History", "NO TBI", "Previous Self-Harm", 
                                                "NO Previous Self-Harm", "Visited Health Services", "DID NOT visit"]
                                    cursor1 = g.conn.execute('''SELECT S.year, B.branch, S.count, S.rate, 
                                                             R.e1_e4, R.e5_e9, R.officer, R.warrant_officer, M.health_diag_y,
                                                             M.health_diag_n, m.tbi_y, m.tbi_n, m.prev_self_harm_y, m.prev_self_harm_n,
                                                             m.health_ser_used_y, m.health_ser_used_n
                                                            FROM Suicides S, Military_Branch B, Rank R, Mental_Characteristics M
                                                            WHERE s.sid = b.sid 
                                                            AND b.sid = r.sid
                                                            AND r.sid = m.sid
                                                            AND S.year >= (%s) 
                                                            AND S.year <= (%s)
                                                            AND B.branch != 'Navy'
                                                            AND B.branch != 'Marine Corps'
                                                            AND B.branch != 'All'
                                                             ''', year1,year2)
                                    for result in cursor1:
                                        military.append(result) 
                                    cursor1.close()
                                    
                                elif airforce != "on":
                                    headings = ["Year", "Branch", "Count", "Rate", "Lower Enlisted", 
                                                "NCOs", "Officers", "Warrant Officers", 
                                                "Mental Health Diagnosis", "NO Mental Health Diagnosis",
                                                "TBI History", "NO TBI", "Previous Self-Harm", 
                                                "NO Previous Self-Harm", "Visited Health Services", "DID NOT visit"]
                                    cursor1 = g.conn.execute('''SELECT S.year, B.branch, S.count, S.rate, 
                                                             R.e1_e4, R.e5_e9, R.officer, R.warrant_officer, M.health_diag_y,
                                                             M.health_diag_n, m.tbi_y, m.tbi_n, m.prev_self_harm_y, m.prev_self_harm_n,
                                                             m.health_ser_used_y, m.health_ser_used_n
                                                            FROM Suicides S, Military_Branch B, Rank R, Mental_Characteristics M
                                                            WHERE s.sid = b.sid 
                                                            AND b.sid = r.sid
                                                            AND r.sid = m.sid
                                                            AND S.year >= (%s) 
                                                            AND S.year <= (%s)
                                                            AND B.branch != 'Navy'
                                                            AND B.branch != 'Marine Corps'
                                                            AND B.branch != 'Air Force'
                                                            AND B.branch != 'All'
                                                        ''', year1,year2)  
                                    for result in cursor1:
                                        military.append(result) 
                                    cursor1.close()
                                    
                    elif army !="on":
                        if navy =="on": 
                            if marines =="on": 
                                if airforce == "on":
                                    headings = ["Year", "Branch", "Count", "Rate", "Lower Enlisted", 
                                                "NCOs", "Officers", "Warrant Officers", 
                                                "Mental Health Diagnosis", "NO Mental Health Diagnosis",
                                                "TBI History", "NO TBI", "Previous Self-Harm", 
                                                "NO Previous Self-Harm", "Visited Health Services", "DID NOT visit"]
                                    cursor1 = g.conn.execute('''SELECT S.year, B.branch, S.count, S.rate, 
                                                             R.e1_e4, R.e5_e9, R.officer, R.warrant_officer, M.health_diag_y,
                                                             M.health_diag_n, m.tbi_y, m.tbi_n, m.prev_self_harm_y, m.prev_self_harm_n,
                                                             m.health_ser_used_y, m.health_ser_used_n
                                                            FROM Suicides S, Military_Branch B, Rank R, Mental_Characteristics M
                                                            WHERE s.sid = b.sid 
                                                            AND b.sid = r.sid
                                                            AND r.sid = m.sid
                                                            AND S.year >= (%s) 
                                                            AND S.year <= (%s)
                                                            AND B.branch != 'Army'
                                                            AND B.branch != 'Navy'
                                                            AND B.branch != 'Marine Corps'
                                                            AND B.branch != 'Air Force'
                                                            AND B.branch != 'All'
                                                        ''', year1,year2)  
                                    for result in cursor1:
                                        military.append(result) 
                                    cursor1.close()
                                    
                                elif airforce != "on":
                                    headings = ["Year", "Branch", "Count", "Rate", "Lower Enlisted", 
                                                "NCOs", "Officers", "Warrant Officers", 
                                                "Mental Health Diagnosis", "NO Mental Health Diagnosis",
                                                "TBI History", "NO TBI", "Previous Self-Harm", 
                                                "NO Previous Self-Harm", "Visited Health Services", "DID NOT visit"]
                                    cursor1 = g.conn.execute('''SELECT S.year, B.branch, S.count, S.rate, 
                                                             R.e1_e4, R.e5_e9, R.officer, R.warrant_officer, M.health_diag_y,
                                                             M.health_diag_n, m.tbi_y, m.tbi_n, m.prev_self_harm_y, m.prev_self_harm_n,
                                                             m.health_ser_used_y, m.health_ser_used_n
                                                            FROM Suicides S, Military_Branch B, Rank R, Mental_Characteristics M
                                                            WHERE s.sid = b.sid 
                                                            AND b.sid = r.sid
                                                            AND r.sid = m.sid
                                                            AND S.year >= (%s) 
                                                            AND S.year <= (%s)
                                                            AND B.branch != 'Army'
                                                            AND B.branch != 'Air Force'
                                                            AND B.branch != 'All'
                                                        ''', year1,year2)  
                                    for result in cursor1:
                                        military.append(result) 
                                    cursor1.close()
                                    
                            elif marines !="on": 
                                if airforce == "on":
                                    headings = ["Year", "Branch", "Count", "Rate", "Lower Enlisted", 
                                                "NCOs", "Officers", "Warrant Officers", 
                                                "Mental Health Diagnosis", "NO Mental Health Diagnosis",
                                                "TBI History", "NO TBI", "Previous Self-Harm", 
                                                "NO Previous Self-Harm", "Visited Health Services", "DID NOT visit"]
                                    cursor1 = g.conn.execute('''SELECT S.year, B.branch, S.count, S.rate, 
                                                             R.e1_e4, R.e5_e9, R.officer, R.warrant_officer, M.health_diag_y,
                                                             M.health_diag_n, m.tbi_y, m.tbi_n, m.prev_self_harm_y, m.prev_self_harm_n,
                                                             m.health_ser_used_y, m.health_ser_used_n
                                                            FROM Suicides S, Military_Branch B, Rank R, Mental_Characteristics M
                                                            WHERE s.sid = b.sid 
                                                            AND b.sid = r.sid
                                                            AND r.sid = m.sid
                                                            AND S.year >= (%s) 
                                                            AND S.year <= (%s)
                                                            AND B.branch != 'Army'
                                                            AND B.branch != 'Marine Corps'
                                                            AND B.branch != 'All'
                                                        ''', year1,year2)  
                                    for result in cursor1:
                                        military.append(result) 
                                    cursor1.close()
                                    
                                elif airforce != "on":
                                    headings = ["Year", "Branch", "Count", "Rate"]
                                    cursor1 = g.conn.execute('''SELECT *
                                                        FROM Suicides S, Military_Branch B, Rank R, Mental_Characteristics M
                                                        WHERE s.sid = b.sid 
                                                        AND b.sid = r.sid
                                                        AND r.sid = m.sid
                                                        AND S.year >= (%s) 
                                                        AND S.year <= (%s)
                                                        AND B.branch != 'Army'
                                                        AND B.branch != 'Marine Corps'
                                                        AND B.branch != 'Air Force'
                                                        AND B.branch != 'All'
                                                        ''', year1,year2)  
                                    for result in cursor1:
                                        military.append(result) 
                                    cursor1.close()
                                    
                        elif navy !="on": 
                            if marines =="on": 
                                if airforce == "on":
                                    headings = ["Year", "Branch", "Count", "Rate", "Lower Enlisted", 
                                                "NCOs", "Officers", "Warrant Officers", 
                                                "Mental Health Diagnosis", "NO Mental Health Diagnosis",
                                                "TBI History", "NO TBI", "Previous Self-Harm", 
                                                "NO Previous Self-Harm", "Visited Health Services", "DID NOT visit"]
                                    cursor1 = g.conn.execute('''SELECT S.year, B.branch, S.count, S.rate, 
                                                             R.e1_e4, R.e5_e9, R.officer, R.warrant_officer, M.health_diag_y,
                                                             M.health_diag_n, m.tbi_y, m.tbi_n, m.prev_self_harm_y, m.prev_self_harm_n,
                                                             m.health_ser_used_y, m.health_ser_used_n
                                                            FROM Suicides S, Military_Branch B, Rank R, Mental_Characteristics M
                                                            WHERE s.sid = b.sid 
                                                            AND b.sid = r.sid
                                                            AND r.sid = m.sid
                                                            AND S.year >= (%s) 
                                                            AND S.year <= (%s)
                                                            AND B.branch != 'Army'
                                                            AND B.branch != 'Navy'
                                                            AND B.branch != 'All'
                                                        ''', year1,year2)  
                                    for result in cursor1:
                                        military.append(result) 
                                    cursor1.close()
                                    
                                elif airforce != "on":
                                    headings = ["Year", "Branch", "Count", "Rate", "Lower Enlisted", 
                                                "NCOs", "Officers", "Warrant Officers", 
                                                "Mental Health Diagnosis", "NO Mental Health Diagnosis",
                                                "TBI History", "NO TBI", "Previous Self-Harm", 
                                                "NO Previous Self-Harm", "Visited Health Services", "DID NOT visit"]
                                    cursor1 = g.conn.execute('''SELECT S.year, B.branch, S.count, S.rate, 
                                                             R.e1_e4, R.e5_e9, R.officer, R.warrant_officer, M.health_diag_y,
                                                             M.health_diag_n, m.tbi_y, m.tbi_n, m.prev_self_harm_y, m.prev_self_harm_n,
                                                             m.health_ser_used_y, m.health_ser_used_n
                                                            FROM Suicides S, Military_Branch B, Rank R, Mental_Characteristics M
                                                            WHERE s.sid = b.sid 
                                                            AND b.sid = r.sid
                                                            AND r.sid = m.sid
                                                            AND S.year >= (%s) 
                                                            AND S.year <= (%s)
                                                            AND B.branch != 'Army'
                                                            AND B.branch != 'Navy'
                                                            AND B.branch != 'Air Force'
                                                            AND B.branch != 'All'
                                                        ''', year1,year2)  
                                    for result in cursor1:
                                        military.append(result) 
                                    cursor1.close()
                                    
                            elif marines !="on": 
                                if airforce == "on":
                                    headings = ["Year", "Branch", "Count", "Rate", "Lower Enlisted", 
                                                "NCOs", "Officers", "Warrant Officers", 
                                                "Mental Health Diagnosis", "NO Mental Health Diagnosis",
                                                "TBI History", "NO TBI", "Previous Self-Harm", 
                                                "NO Previous Self-Harm", "Visited Health Services", "DID NOT visit"]
                                    cursor1 = g.conn.execute('''SELECT S.year, B.branch, S.count, S.rate, 
                                                             R.e1_e4, R.e5_e9, R.officer, R.warrant_officer, M.health_diag_y,
                                                             M.health_diag_n, m.tbi_y, m.tbi_n, m.prev_self_harm_y, m.prev_self_harm_n,
                                                             m.health_ser_used_y, m.health_ser_used_n
                                                            FROM Suicides S, Military_Branch B, Rank R, Mental_Characteristics M
                                                            WHERE s.sid = b.sid 
                                                            AND b.sid = r.sid
                                                            AND r.sid = m.sid
                                                            AND S.year >= (%s) 
                                                            AND S.year <= (%s)
                                                            AND B.branch != 'Army'
                                                            AND B.branch != 'Navy'
                                                            AND B.branch != 'Marine Corps'
                                                            AND B.branch != 'All'
                                                        ''', year1,year2)  
                                    for result in cursor1:
                                        military.append(result) 
                                    cursor1.close()
                                    
                                elif airforce != "on":
                                    headings = ["Year", "Branch", "Count", "Rate", "Lower Enlisted", 
                                                "NCOs", "Officers", "Warrant Officers", 
                                                "Mental Health Diagnosis", "NO Mental Health Diagnosis",
                                                "TBI History", "NO TBI", "Previous Self-Harm", 
                                                "NO Previous Self-Harm", "Visited Health Services", "DID NOT visit"]
                                    cursor1 = g.conn.execute('''SELECT S.year, B.branch, S.count, S.rate, 
                                                             R.e1_e4, R.e5_e9, R.officer, R.warrant_officer, M.health_diag_y,
                                                             M.health_diag_n, m.tbi_y, m.tbi_n, m.prev_self_harm_y, m.prev_self_harm_n,
                                                             m.health_ser_used_y, m.health_ser_used_n
                                                            FROM Suicides S, Military_Branch B, Rank R, Mental_Characteristics M
                                                            WHERE s.sid = b.sid 
                                                            AND b.sid = r.sid
                                                            AND r.sid = m.sid
                                                            AND S.year >= (%s) 
                                                            AND S.year <= (%s)
                                                            AND B.branch != 'Army'
                                                            AND B.branch != 'Navy'
                                                            AND B.branch != 'Marine Corps'
                                                            AND B.branch != 'Air Force'
                                                            AND B.branch != 'All'
                                                        ''', year1,year2)  
                                    for result in cursor1:
                                        military.append(result) 
                                    cursor1.close()
            if showmh != "on":
                if combined == 'on':
                    if army == "on":
                        if navy =="on": 
                            if marines =="on": 
                                if airforce == "on":
                                    headings = ["Year", "Branch", "Count", "Rate", "Lower Enlisted", 
                                                "NCOs", "Officers", "Warrant Officers"]
                                    cursor1 = g.conn.execute('''SELECT S.year, B.branch, S.count, S.rate, 
                                                             R.e1_e4, R.e5_e9, R.officer, R.warrant_officer
                                                            FROM Suicides S, Military_Branch B, Rank R
                                                            WHERE s.sid = b.sid 
                                                            AND b.sid = r.sid
                                                            AND S.year >= (%s) 
                                                            AND S.year <= (%s)
                                                            ''', year1,year2)   
                                    for result in cursor1:
                                        military.append(result) 
                                    cursor1.close()
                                    
                                elif airforce != "on":
                                    headings = ["Year", "Branch", "Count", "Rate", "Lower Enlisted", 
                                                "NCOs", "Officers", "Warrant Officers"]
                                    cursor1 = g.conn.execute('''SELECT S.year, B.branch, S.count, S.rate, 
                                                             R.e1_e4, R.e5_e9, R.officer, R.warrant_officer
                                                            FROM Suicides S, Military_Branch B, Rank R
                                                            WHERE s.sid = b.sid 
                                                            AND b.sid = r.sid
                                                            AND S.year >= (%s) 
                                                            AND S.year <= (%s)
                                                            AND B.branch != 'Air Force'
                                                            ''', year1,year2)    
                                    for result in cursor1:
                                        military.append(result) 
                                    cursor1.close()
                                    
                            elif marines !="on": 
                                if airforce == "on":
                                    headings = ["Year", "Branch", "Count", "Rate", "Lower Enlisted", 
                                                "NCOs", "Officers", "Warrant Officers"]
                                    cursor1 = g.conn.execute('''SELECT S.year, B.branch, S.count, S.rate, 
                                                             R.e1_e4, R.e5_e9, R.officer, R.warrant_officer
                                                            FROM Suicides S, Military_Branch B, Rank R
                                                            WHERE s.sid = b.sid 
                                                            AND b.sid = r.sid
                                                            AND S.year >= (%s) 
                                                            AND S.year <= (%s)
                                                            AND B.branch != 'Marine Corps'
                                                            ''', year1,year2)    
                                    for result in cursor1:
                                        military.append(result) 
                                    cursor1.close()
                                    
                                elif airforce != "on":
                                    headings = ["Year", "Branch", "Count", "Rate", "Lower Enlisted", 
                                                "NCOs", "Officers", "Warrant Officers"]
                                    cursor1 = g.conn.execute('''SELECT S.year, B.branch, S.count, S.rate, 
                                                             R.e1_e4, R.e5_e9, R.officer, R.warrant_officer
                                                            FROM Suicides S, Military_Branch B, Rank R
                                                            WHERE s.sid = b.sid 
                                                            AND b.sid = r.sid
                                                            AND S.year >= (%s) 
                                                            AND S.year <= (%s)
                                                            AND B.branch != 'Air Force'
                                                            AND B.branch != 'Marine Corps'
                                                            ''', year1,year2)   
                                    for result in cursor1:
                                        military.append(result) 
                                    cursor1.close()
                                    
                        elif navy !="on": 
                            if marines =="on": 
                                if airforce == "on":
                                    headings = ["Year", "Branch", "Count", "Rate", "Lower Enlisted", 
                                                "NCOs", "Officers", "Warrant Officers"]
                                    cursor1 = g.conn.execute('''SELECT S.year, B.branch, S.count, S.rate, 
                                                             R.e1_e4, R.e5_e9, R.officer, R.warrant_officer
                                                            FROM Suicides S, Military_Branch B, Rank R
                                                            WHERE s.sid = b.sid 
                                                            AND b.sid = r.sid
                                                            AND S.year >= (%s) 
                                                            AND S.year <= (%s)
                                                            AND B.branch != 'Navy'
                                                            ''', year1,year2)  
                                    for result in cursor1:
                                        military.append(result) 
                                    cursor1.close()
                                    
                                elif airforce != "on":
                                    headings = ["Year", "Branch", "Count", "Rate", "Lower Enlisted", 
                                                "NCOs", "Officers", "Warrant Officers"]
                                    cursor1 = g.conn.execute('''SELECT S.year, B.branch, S.count, S.rate, 
                                                             R.e1_e4, R.e5_e9, R.officer, R.warrant_officer
                                                            FROM Suicides S, Military_Branch B, Rank R
                                                            WHERE s.sid = b.sid 
                                                            AND b.sid = r.sid
                                                            AND S.year >= (%s) 
                                                            AND S.year <= (%s)
                                                            AND B.branch != 'Navy'
                                                            AND B.branch != 'Air Force'
                                                            ''', year1,year2)  
                                    for result in cursor1:
                                        military.append(result) 
                                    cursor1.close()
                                    
                            elif marines !="on": 
                                if airforce == "on":
                                    headings = ["Year", "Branch", "Count", "Rate", "Lower Enlisted", 
                                                "NCOs", "Officers", "Warrant Officers"]
                                    cursor1 = g.conn.execute('''SELECT S.year, B.branch, S.count, S.rate, 
                                                             R.e1_e4, R.e5_e9, R.officer, R.warrant_officer
                                                            FROM Suicides S, Military_Branch B, Rank R
                                                            WHERE s.sid = b.sid 
                                                            AND b.sid = r.sid
                                                            AND S.year >= (%s) 
                                                            AND S.year <= (%s)
                                                            AND B.branch != 'Navy'
                                                            AND B.branch != 'Marine Corps'
                                                             ''', year1,year2)
                                    for result in cursor1:
                                        military.append(result) 
                                    cursor1.close()
                                    
                                elif airforce != "on":
                                    headings = ["Year", "Branch", "Count", "Rate", "Lower Enlisted", 
                                                "NCOs", "Officers", "Warrant Officers"]
                                    cursor1 = g.conn.execute('''SELECT S.year, B.branch, S.count, S.rate, 
                                                             R.e1_e4, R.e5_e9, R.officer, R.warrant_officer
                                                            FROM Suicides S, Military_Branch B, Rank R
                                                            WHERE s.sid = b.sid 
                                                            AND b.sid = r.sid
                                                            AND S.year >= (%s) 
                                                            AND S.year <= (%s)
                                                            AND B.branch != 'Navy'
                                                            AND B.branch != 'Marine Corps'
                                                            AND B.branch != 'Air Force'
                                                        ''', year1,year2)  
                                    for result in cursor1:
                                        military.append(result) 
                                    cursor1.close()
                                    
                    elif army !="on":
                        if navy =="on": 
                            if marines =="on": 
                                if airforce == "on":
                                    headings = ["Year", "Branch", "Count", "Rate", "Lower Enlisted", 
                                                "NCOs", "Officers", "Warrant Officers"]
                                    cursor1 = g.conn.execute('''SELECT S.year, B.branch, S.count, S.rate, 
                                                             R.e1_e4, R.e5_e9, R.officer, R.warrant_officer
                                                            FROM Suicides S, Military_Branch B, Rank R
                                                            WHERE s.sid = b.sid 
                                                            AND b.sid = r.sid
                                                            AND S.year >= (%s) 
                                                            AND S.year <= (%s)
                                                            AND B.branch != 'Army'
                                                            AND B.branch != 'Navy'
                                                            AND B.branch != 'Marine Corps'
                                                            AND B.branch != 'Air Force'
                                                        ''', year1,year2)  
                                    for result in cursor1:
                                        military.append(result) 
                                    cursor1.close()
                                    
                                elif airforce != "on":
                                    headings = ["Year", "Branch", "Count", "Rate", "Lower Enlisted", 
                                                "NCOs", "Officers", "Warrant Officers"]
                                    cursor1 = g.conn.execute('''SELECT S.year, B.branch, S.count, S.rate, 
                                                             R.e1_e4, R.e5_e9, R.officer, R.warrant_officer
                                                            FROM Suicides S, Military_Branch B, Rank R
                                                            WHERE s.sid = b.sid 
                                                            AND b.sid = r.sid
                                                            AND S.year >= (%s) 
                                                            AND S.year <= (%s)
                                                            AND B.branch != 'Army'
                                                            AND B.branch != 'Air Force'
                                                        ''', year1,year2)  
                                    for result in cursor1:
                                        military.append(result) 
                                    cursor1.close()
                                    
                            elif marines !="on": 
                                if airforce == "on":
                                    headings = ["Year", "Branch", "Count", "Rate", "Lower Enlisted", 
                                                "NCOs", "Officers", "Warrant Officers"]
                                    cursor1 = g.conn.execute('''SELECT S.year, B.branch, S.count, S.rate, 
                                                             R.e1_e4, R.e5_e9, R.officer, R.warrant_officer
                                                            FROM Suicides S, Military_Branch B, Rank R
                                                            WHERE s.sid = b.sid 
                                                            AND b.sid = r.sid
                                                            AND S.year >= (%s) 
                                                            AND S.year <= (%s)
                                                            AND B.branch != 'Army'
                                                            AND B.branch != 'Marine Corps'
                                                        ''', year1,year2)  
                                    for result in cursor1:
                                        military.append(result) 
                                    cursor1.close()
                                    
                                elif airforce != "on":
                                    headings = ["Year", "Branch", "Count", "Rate", "Lower Enlisted", 
                                                "NCOs", "Officers", "Warrant Officers"]
                                    cursor1 = g.conn.execute('''SELECT S.year, B.branch, S.count, S.rate, 
                                                             R.e1_e4, R.e5_e9, R.officer, R.warrant_officer
                                                            FROM Suicides S, Military_Branch B, Rank R
                                                            WHERE s.sid = b.sid 
                                                            AND b.sid = r.sid
                                                            AND S.year >= (%s) 
                                                            AND S.year <= (%s)
                                                            AND B.branch != 'Army'
                                                            AND B.branch != 'Marine Corps'
                                                            AND B.branch != 'Air Force'
                                                        ''', year1,year2)  
                                    for result in cursor1:
                                        military.append(result) 
                                    cursor1.close()
                                    
                        elif navy !="on": 
                            if marines =="on": 
                                if airforce == "on":
                                    headings = ["Year", "Branch", "Count", "Rate", "Lower Enlisted", 
                                                "NCOs", "Officers", "Warrant Officers"]
                                    cursor1 = g.conn.execute('''SELECT S.year, B.branch, S.count, S.rate, 
                                                             R.e1_e4, R.e5_e9, R.officer, R.warrant_officer
                                                            FROM Suicides S, Military_Branch B, Rank R
                                                            WHERE s.sid = b.sid 
                                                            AND b.sid = r.sid
                                                            AND S.year >= (%s) 
                                                            AND S.year <= (%s)
                                                            AND B.branch != 'Army'
                                                            AND B.branch != 'Navy'
                                                        ''', year1,year2)  
                                    for result in cursor1:
                                        military.append(result) 
                                    cursor1.close()
                                    
                                elif airforce != "on":
                                    headings = ["Year", "Branch", "Count", "Rate", "Lower Enlisted", 
                                                "NCOs", "Officers", "Warrant Officers"]
                                    cursor1 = g.conn.execute('''SELECT S.year, B.branch, S.count, S.rate, 
                                                             R.e1_e4, R.e5_e9, R.officer, R.warrant_officer
                                                            FROM Suicides S, Military_Branch B, Rank R
                                                            WHERE s.sid = b.sid 
                                                            AND b.sid = r.sid
                                                            AND S.year >= (%s) 
                                                            AND S.year <= (%s)
                                                            AND B.branch != 'Army'
                                                            AND B.branch != 'Navy'
                                                            AND B.branch != 'Air Force'
                                                        ''', year1,year2)  
                                    for result in cursor1:
                                        military.append(result) 
                                    cursor1.close()
                                    
                            elif marines !="on": 
                                if airforce == "on":
                                    headings = ["Year", "Branch", "Count", "Rate", "Lower Enlisted", 
                                                "NCOs", "Officers", "Warrant Officers"]
                                    cursor1 = g.conn.execute('''SELECT S.year, B.branch, S.count, S.rate, 
                                                             R.e1_e4, R.e5_e9, R.officer, R.warrant_officer
                                                            FROM Suicides S, Military_Branch B, Rank R
                                                            WHERE s.sid = b.sid 
                                                            AND b.sid = r.sid
                                                            AND S.year >= (%s) 
                                                            AND S.year <= (%s)
                                                            AND B.branch != 'Army'
                                                            AND B.branch != 'Navy'
                                                            AND B.branch != 'Marine Corps'
                                                        ''', year1,year2)  
                                    for result in cursor1:
                                        military.append(result) 
                                    cursor1.close()
                                    
                                elif airforce != "on":
                                    headings = ["Year", "Branch", "Count", "Rate", "Lower Enlisted", 
                                                "NCOs", "Officers", "Warrant Officers"]
                                    cursor1 = g.conn.execute('''SELECT S.year, B.branch, S.count, S.rate, 
                                                             R.e1_e4, R.e5_e9, R.officer, R.warrant_officer
                                                            FROM Suicides S, Military_Branch B, Rank R
                                                            WHERE s.sid = b.sid 
                                                            AND b.sid = r.sid
                                                            AND S.year >= (%s) 
                                                            AND S.year <= (%s)
                                                            AND B.branch != 'Army'
                                                            AND B.branch != 'Navy'
                                                            AND B.branch != 'Marine Corps'
                                                            AND B.branch != 'Air Force'
                                                        ''', year1,year2)  
                                    for result in cursor1:
                                        military.append(result) 
                                    cursor1.close()
                if combined != 'on':
                    if army == "on":
                        if navy =="on": 
                            if marines =="on": 
                                if airforce == "on":
                                    headings = ["Year", "Branch", "Count", "Rate", "Lower Enlisted", 
                                                "NCOs", "Officers", "Warrant Officers"]
                                    cursor1 = g.conn.execute('''SELECT S.year, B.branch, S.count, S.rate, 
                                                             R.e1_e4, R.e5_e9, R.officer, R.warrant_officer
                                                            FROM Suicides S, Military_Branch B, Rank R
                                                            WHERE s.sid = b.sid 
                                                            AND b.sid = r.sid
                                                            AND S.year >= (%s) 
                                                            AND S.year <= (%s)
                                                            AND B.branch != 'All'
                                                            ''', year1,year2)   
                                    for result in cursor1:
                                        military.append(result) 
                                    cursor1.close()
                                    
                                elif airforce != "on":
                                    headings = ["Year", "Branch", "Count", "Rate", "Lower Enlisted", 
                                                "NCOs", "Officers", "Warrant Officers"]
                                    cursor1 = g.conn.execute('''SELECT S.year, B.branch, S.count, S.rate, 
                                                             R.e1_e4, R.e5_e9, R.officer, R.warrant_officer
                                                            FROM Suicides S, Military_Branch B, Rank R
                                                            WHERE s.sid = b.sid 
                                                            AND b.sid = r.sid
                                                            AND S.year >= (%s) 
                                                            AND S.year <= (%s)
                                                            AND B.branch != 'Air Force'
                                                            AND B.branch != 'All'
                                                            ''', year1,year2)    
                                    for result in cursor1:
                                        military.append(result) 
                                    cursor1.close()
                                    
                            elif marines !="on": 
                                if airforce == "on":
                                    headings = ["Year", "Branch", "Count", "Rate", "Lower Enlisted", 
                                                "NCOs", "Officers", "Warrant Officers"]
                                    cursor1 = g.conn.execute('''SELECT S.year, B.branch, S.count, S.rate, 
                                                             R.e1_e4, R.e5_e9, R.officer, R.warrant_officer
                                                            FROM Suicides S, Military_Branch B, Rank R
                                                            WHERE s.sid = b.sid 
                                                            AND b.sid = r.sid
                                                            AND S.year >= (%s) 
                                                            AND S.year <= (%s)
                                                            AND B.branch != 'Marine Corps'
                                                            AND B.branch != 'All'
                                                            ''', year1,year2)    
                                    for result in cursor1:
                                        military.append(result) 
                                    cursor1.close()
                                    
                                elif airforce != "on":
                                    headings = ["Year", "Branch", "Count", "Rate", "Lower Enlisted", 
                                                "NCOs", "Officers", "Warrant Officers"]
                                    cursor1 = g.conn.execute('''SELECT S.year, B.branch, S.count, S.rate, 
                                                             R.e1_e4, R.e5_e9, R.officer, R.warrant_officer
                                                            FROM Suicides S, Military_Branch B, Rank R
                                                            WHERE s.sid = b.sid 
                                                            AND b.sid = r.sid
                                                            AND S.year >= (%s) 
                                                            AND S.year <= (%s)
                                                            AND B.branch != 'Air Force'
                                                            AND B.branch != 'Marine Corps'
                                                            AND B.branch != 'All'
                                                            ''', year1,year2)   
                                    for result in cursor1:
                                        military.append(result) 
                                    cursor1.close()
                                    
                        elif navy !="on": 
                            if marines =="on": 
                                if airforce == "on":
                                    headings = ["Year", "Branch", "Count", "Rate", "Lower Enlisted", 
                                                "NCOs", "Officers", "Warrant Officers"]
                                    cursor1 = g.conn.execute('''SELECT S.year, B.branch, S.count, S.rate, 
                                                             R.e1_e4, R.e5_e9, R.officer, R.warrant_officer
                                                            FROM Suicides S, Military_Branch B, Rank R
                                                            WHERE s.sid = b.sid 
                                                            AND b.sid = r.sid
                                                            AND S.year >= (%s) 
                                                            AND S.year <= (%s)
                                                            AND B.branch != 'Navy'
                                                            AND B.branch != 'All'
                                                            ''', year1,year2)  
                                    for result in cursor1:
                                        military.append(result) 
                                    cursor1.close()
                                    
                                elif airforce != "on":
                                    headings = ["Year", "Branch", "Count", "Rate", "Lower Enlisted", 
                                                "NCOs", "Officers", "Warrant Officers"]
                                    cursor1 = g.conn.execute('''SELECT S.year, B.branch, S.count, S.rate, 
                                                             R.e1_e4, R.e5_e9, R.officer, R.warrant_officer
                                                            FROM Suicides S, Military_Branch B, Rank R
                                                            WHERE s.sid = b.sid 
                                                            AND b.sid = r.sid
                                                            AND S.year >= (%s) 
                                                            AND S.year <= (%s)
                                                            AND B.branch != 'Navy'
                                                            AND B.branch != 'Air Force'
                                                            AND B.branch != 'All'
                                                            ''', year1,year2)  
                                    for result in cursor1:
                                        military.append(result) 
                                    cursor1.close()
                                    
                            elif marines !="on": 
                                if airforce == "on":
                                    headings = ["Year", "Branch", "Count", "Rate", "Lower Enlisted", 
                                                "NCOs", "Officers", "Warrant Officers"]
                                    cursor1 = g.conn.execute('''SELECT S.year, B.branch, S.count, S.rate, 
                                                             R.e1_e4, R.e5_e9, R.officer, R.warrant_officer
                                                            FROM Suicides S, Military_Branch B, Rank R
                                                            WHERE s.sid = b.sid 
                                                            AND b.sid = r.sid
                                                            AND S.year >= (%s) 
                                                            AND S.year <= (%s)
                                                            AND B.branch != 'Navy'
                                                            AND B.branch != 'Marines'
                                                            AND B.branch != 'All'
                                                             ''', year1,year2)
                                    for result in cursor1:
                                        military.append(result) 
                                    cursor1.close()
                                    
                                elif airforce != "on":
                                    headings = ["Year", "Branch", "Count", "Rate", "Lower Enlisted", 
                                                "NCOs", "Officers", "Warrant Officers"]
                                    cursor1 = g.conn.execute('''SELECT S.year, B.branch, S.count, S.rate, 
                                                             R.e1_e4, R.e5_e9, R.officer, R.warrant_officer
                                                            FROM Suicides S, Military_Branch B, Rank R
                                                            WHERE s.sid = b.sid 
                                                            AND b.sid = r.sid
                                                            AND S.year >= (%s) 
                                                            AND S.year <= (%s)
                                                            AND B.branch != 'Navy'
                                                            AND B.branch != 'Marine Corps'
                                                            AND B.branch != 'Air Force'
                                                            AND B.branch != 'All'
                                                        ''', year1,year2)  
                                    for result in cursor1:
                                        military.append(result) 
                                    cursor1.close()
                                    
                    elif army !="on":
                        if navy =="on": 
                            if marines =="on": 
                                if airforce == "on":
                                    headings = ["Year", "Branch", "Count", "Rate", "Lower Enlisted", 
                                                "NCOs", "Officers", "Warrant Officers"]
                                    cursor1 = g.conn.execute('''SELECT S.year, B.branch, S.count, S.rate, 
                                                             R.e1_e4, R.e5_e9, R.officer, R.warrant_officer
                                                            FROM Suicides S, Military_Branch B, Rank R
                                                            WHERE s.sid = b.sid 
                                                            AND b.sid = r.sid
                                                            AND S.year >= (%s) 
                                                            AND S.year <= (%s)
                                                            AND B.branch != 'Army'
                                                            AND B.branch != 'Navy'
                                                            AND B.branch != 'Marine Corps'
                                                            AND B.branch != 'Air Force'
                                                            AND B.branch != 'All'
                                                        ''', year1,year2)  
                                    for result in cursor1:
                                        military.append(result) 
                                    cursor1.close()
                                    
                                elif airforce != "on":
                                    headings = ["Year", "Branch", "Count", "Rate", "Lower Enlisted", 
                                                "NCOs", "Officers", "Warrant Officers"]
                                    cursor1 = g.conn.execute('''SELECT S.year, B.branch, S.count, S.rate, 
                                                             R.e1_e4, R.e5_e9, R.officer, R.warrant_officer
                                                            FROM Suicides S, Military_Branch B, Rank R
                                                            WHERE s.sid = b.sid 
                                                            AND b.sid = r.sid
                                                            AND S.year >= (%s) 
                                                            AND S.year <= (%s)
                                                            AND B.branch != 'Army'
                                                            AND B.branch != 'Air Force'
                                                            AND B.branch != 'All'
                                                        ''', year1,year2)  
                                    for result in cursor1:
                                        military.append(result) 
                                    cursor1.close()
                                    
                            elif marines !="on": 
                                if airforce == "on":
                                    headings = ["Year", "Branch", "Count", "Rate", "Lower Enlisted", 
                                                "NCOs", "Officers", "Warrant Officers"]
                                    cursor1 = g.conn.execute('''SELECT S.year, B.branch, S.count, S.rate, 
                                                             R.e1_e4, R.e5_e9, R.officer, R.warrant_officer
                                                            FROM Suicides S, Military_Branch B, Rank R
                                                            WHERE s.sid = b.sid 
                                                            AND b.sid = r.sid
                                                            AND S.year >= (%s) 
                                                            AND S.year <= (%s)
                                                            AND B.branch != 'Army'
                                                            AND B.branch != 'Marine Corps'
                                                            AND B.branch != 'All'
                                                        ''', year1,year2)  
                                    for result in cursor1:
                                        military.append(result) 
                                    cursor1.close()
                                    
                                elif airforce != "on":
                                    headings = ["Year", "Branch", "Count", "Rate", "Lower Enlisted", 
                                                "NCOs", "Officers", "Warrant Officers"]
                                    cursor1 = g.conn.execute('''SELECT S.year, B.branch, S.count, S.rate, 
                                                             R.e1_e4, R.e5_e9, R.officer, R.warrant_officer
                                                            FROM Suicides S, Military_Branch B, Rank R
                                                            WHERE s.sid = b.sid 
                                                            AND b.sid = r.sid
                                                            AND S.year >= (%s) 
                                                            AND S.year <= (%s)
                                                        AND B.branch != 'Army'
                                                        AND B.branch != 'Marine Corps'
                                                        AND B.branch != 'Air Force'
                                                        AND B.branch != 'All'
                                                        ''', year1,year2)  
                                    for result in cursor1:
                                        military.append(result) 
                                    cursor1.close()
                                    
                        elif navy !="on": 
                            if marines =="on": 
                                if airforce == "on":
                                    headings = ["Year", "Branch", "Count", "Rate", "Lower Enlisted", 
                                                "NCOs", "Officers", "Warrant Officers"]
                                    cursor1 = g.conn.execute('''SELECT S.year, B.branch, S.count, S.rate, 
                                                             R.e1_e4, R.e5_e9, R.officer, R.warrant_officer
                                                            FROM Suicides S, Military_Branch B, Rank R
                                                            WHERE s.sid = b.sid 
                                                            AND b.sid = r.sid
                                                            AND S.year >= (%s) 
                                                            AND S.year <= (%s)
                                                            AND B.branch != 'Army'
                                                            AND B.branch != 'Navy'
                                                            AND B.branch != 'All'
                                                        ''', year1,year2)  
                                    for result in cursor1:
                                        military.append(result) 
                                    cursor1.close()
                                    
                                elif airforce != "on":
                                    headings = ["Year", "Branch", "Count", "Rate", "Lower Enlisted", 
                                                "NCOs", "Officers", "Warrant Officers"]
                                    cursor1 = g.conn.execute('''SELECT S.year, B.branch, S.count, S.rate, 
                                                             R.e1_e4, R.e5_e9, R.officer, R.warrant_officer
                                                            FROM Suicides S, Military_Branch B, Rank R
                                                            WHERE s.sid = b.sid 
                                                            AND b.sid = r.sid
                                                            AND S.year >= (%s) 
                                                            AND S.year <= (%s)
                                                            AND B.branch != 'Army'
                                                            AND B.branch != 'Navy'
                                                            AND B.branch != 'Air Force'
                                                            AND B.branch != 'All'
                                                        ''', year1,year2)  
                                    for result in cursor1:
                                        military.append(result) 
                                    cursor1.close()
                                    
                            elif marines !="on": 
                                if airforce == "on":
                                    headings = ["Year", "Branch", "Count", "Rate", "Lower Enlisted", 
                                                "NCOs", "Officers", "Warrant Officers"]
                                    cursor1 = g.conn.execute('''SELECT S.year, B.branch, S.count, S.rate, 
                                                             R.e1_e4, R.e5_e9, R.officer, R.warrant_officer
                                                            FROM Suicides S, Military_Branch B, Rank R
                                                            WHERE s.sid = b.sid 
                                                            AND b.sid = r.sid
                                                            AND S.year >= (%s) 
                                                            AND S.year <= (%s)
                                                            AND B.branch != 'Army'
                                                            AND B.branch != 'Navy'
                                                            AND B.branch != 'Marine Corps'
                                                            AND B.branch != 'All'
                                                        ''', year1,year2)  
                                    for result in cursor1:
                                        military.append(result) 
                                    cursor1.close()
                                    
                                elif airforce != "on":
                                    headings = ["Year", "Branch", "Count", "Rate", "Lower Enlisted", 
                                                "NCOs", "Officers", "Warrant Officers"]
                                    cursor1 = g.conn.execute('''SELECT S.year, B.branch, S.count, S.rate, 
                                                             R.e1_e4, R.e5_e9, R.officer, R.warrant_officer
                                                            FROM Suicides S, Military_Branch B, Rank R
                                                            WHERE s.sid = b.sid 
                                                            AND b.sid = r.sid
                                                            AND S.year >= (%s) 
                                                            AND S.year <= (%s)
                                                            AND B.branch != 'Army'
                                                            AND B.branch != 'Navy'
                                                            AND B.branch != 'Marine Corps'
                                                            AND B.branch != 'Air Force'
                                                            AND B.branch != 'All'
                                                        ''', year1,year2)  
                                    for result in cursor1:
                                        military.append(result) 
                                    cursor1.close()
                                    
        if showrank != "on":
            if showmh == "on":
                if combined == 'on':
                    if army == "on":
                        if navy =="on": 
                            if marines =="on": 
                                if airforce == "on":
                                    headings = ["Year", "Branch", "Count", "Rate", 
                                                "Mental Health Diagnosis", "NO Mental Health Diagnosis",
                                                "TBI History", "NO TBI", "Previous Self-Harm", 
                                                "NO Previous Self-Harm", "Visited Health Services", "DID NOT visit"]
                                    cursor1 = g.conn.execute('''SELECT S.year, B.branch, S.count, S.rate, M.health_diag_y,
                                                             M.health_diag_n, m.tbi_y, m.tbi_n, m.prev_self_harm_y, m.prev_self_harm_n,
                                                             m.health_ser_used_y, m.health_ser_used_n
                                                            FROM Suicides S, Military_Branch B, Mental_Characteristics M
                                                            WHERE s.sid = b.sid 
                                                            AND b.sid = m.sid
                                                            AND S.year >= (%s) 
                                                            AND S.year <= (%s)
                                                            ''', year1,year2)   
                                    for result in cursor1:
                                        military.append(result) 
                                    cursor1.close()
                                    
                                elif airforce != "on":
                                    headings = ["Year", "Branch", "Count", "Rate", 
                                                "Mental Health Diagnosis", "NO Mental Health Diagnosis",
                                                "TBI History", "NO TBI", "Previous Self-Harm", 
                                                "NO Previous Self-Harm", "Visited Health Services", "DID NOT visit"]
                                    cursor1 = g.conn.execute('''SELECT S.year, B.branch, S.count, S.rate, M.health_diag_y,
                                                             M.health_diag_n, m.tbi_y, m.tbi_n, m.prev_self_harm_y, m.prev_self_harm_n,
                                                             m.health_ser_used_y, m.health_ser_used_n
                                                            FROM Suicides S, Military_Branch B, Mental_Characteristics M
                                                            WHERE s.sid = b.sid 
                                                            AND b.sid = m.sid
                                                            AND S.year >= (%s) 
                                                            AND S.year <= (%s)
                                                            AND B.branch != 'Air Force'
                                                            
                                                        ''', year1,year2)  
                                    for result in cursor1:
                                        military.append(result) 
                                    cursor1.close()
                                    
                            elif marines !="on": 
                                if airforce == "on":
                                    headings = ["Year", "Branch", "Count", "Rate", 
                                                "Mental Health Diagnosis", "NO Mental Health Diagnosis",
                                                "TBI History", "NO TBI", "Previous Self-Harm", 
                                                "NO Previous Self-Harm", "Visited Health Services", "DID NOT visit"]
                                    cursor1 = g.conn.execute('''SELECT S.year, B.branch, S.count, S.rate, M.health_diag_y,
                                                             M.health_diag_n, m.tbi_y, m.tbi_n, m.prev_self_harm_y, m.prev_self_harm_n,
                                                             m.health_ser_used_y, m.health_ser_used_n
                                                            FROM Suicides S, Military_Branch B, Mental_Characteristics M
                                                            WHERE s.sid = b.sid 
                                                            AND b.sid = m.sid
                                                            AND S.year >= (%s) 
                                                            AND S.year <= (%s)
                                                            AND B.branch != 'Marine Corps'
                                                        ''', year1,year2)  
                                    for result in cursor1:
                                        military.append(result) 
                                    cursor1.close()
                                    
                                elif airforce != "on":
                                    headings = ["Year", "Branch", "Count", "Rate", 
                                                "Mental Health Diagnosis", "NO Mental Health Diagnosis",
                                                "TBI History", "NO TBI", "Previous Self-Harm", 
                                                "NO Previous Self-Harm", "Visited Health Services", "DID NOT visit"]
                                    cursor1 = g.conn.execute('''SELECT S.year, B.branch, S.count, S.rate, M.health_diag_y,
                                                             M.health_diag_n, m.tbi_y, m.tbi_n, m.prev_self_harm_y, m.prev_self_harm_n,
                                                             m.health_ser_used_y, m.health_ser_used_n
                                                            FROM Suicides S, Military_Branch B, Mental_Characteristics M
                                                            WHERE s.sid = b.sid 
                                                            AND b.sid = m.sid
                                                            AND S.year >= (%s) 
                                                            AND S.year <= (%s)
                                                            AND B.branch != 'Marine Corps'
                                                            AND B.branch != 'Air Force'
                                                        ''', year1,year2)  
                                    for result in cursor1:
                                        military.append(result) 
                                    cursor1.close()
                                    
                        elif navy !="on": 
                            if marines =="on": 
                                if airforce == "on":
                                    headings = ["Year", "Branch", "Count", "Rate", 
                                                "Mental Health Diagnosis", "NO Mental Health Diagnosis",
                                                "TBI History", "NO TBI", "Previous Self-Harm", 
                                                "NO Previous Self-Harm", "Visited Health Services", "DID NOT visit"]
                                    cursor1 = g.conn.execute('''SELECT S.year, B.branch, S.count, S.rate, M.health_diag_y,
                                                             M.health_diag_n, m.tbi_y, m.tbi_n, m.prev_self_harm_y, m.prev_self_harm_n,
                                                             m.health_ser_used_y, m.health_ser_used_n
                                                            FROM Suicides S, Military_Branch B, Mental_Characteristics M
                                                            WHERE s.sid = b.sid 
                                                            AND b.sid = m.sid
                                                            AND S.year >= (%s) 
                                                            AND S.year <= (%s)
                                                            AND B.branch != 'Navy'
                                                        ''', year1,year2)  
                                    for result in cursor1:
                                        military.append(result) 
                                    cursor1.close()
                                    
                                elif airforce != "on":
                                    headings = ["Year", "Branch", "Count", "Rate", 
                                                "Mental Health Diagnosis", "NO Mental Health Diagnosis",
                                                "TBI History", "NO TBI", "Previous Self-Harm", 
                                                "NO Previous Self-Harm", "Visited Health Services", "DID NOT visit"]
                                    cursor1 = g.conn.execute('''SELECT S.year, B.branch, S.count, S.rate, M.health_diag_y,
                                                             M.health_diag_n, m.tbi_y, m.tbi_n, m.prev_self_harm_y, m.prev_self_harm_n,
                                                             m.health_ser_used_y, m.health_ser_used_n
                                                            FROM Suicides S, Military_Branch B, Mental_Characteristics M
                                                            WHERE s.sid = b.sid 
                                                            AND b.sid = m.sid
                                                            AND S.year >= (%s) 
                                                            AND S.year <= (%s)
                                                            AND B.branch != 'Navy'
                                                            AND B.branch != 'Marine Corps'
                                                            AND B.branch != 'Air Force'
                                                        ''', year1,year2)  
                                    for result in cursor1:
                                        military.append(result) 
                                    cursor1.close()
                                    
                            elif marines !="on": 
                                if airforce == "on":
                                    headings = ["Year", "Branch", "Count", "Rate", 
                                                "Mental Health Diagnosis", "NO Mental Health Diagnosis",
                                                "TBI History", "NO TBI", "Previous Self-Harm", 
                                                "NO Previous Self-Harm", "Visited Health Services", "DID NOT visit"]
                                    cursor1 = g.conn.execute('''SELECT S.year, B.branch, S.count, S.rate, M.health_diag_y,
                                                             M.health_diag_n, m.tbi_y, m.tbi_n, m.prev_self_harm_y, m.prev_self_harm_n,
                                                             m.health_ser_used_y, m.health_ser_used_n
                                                            FROM Suicides S, Military_Branch B, Mental_Characteristics M
                                                            WHERE s.sid = b.sid 
                                                            AND b.sid = m.sid
                                                            AND S.year >= (%s) 
                                                            AND S.year <= (%s)
                                                            AND S.year >= (%s) 
                                                            AND S.year <= (%s)
                                                            AND B.branch != 'Navy'
                                                            AND B.branch != 'Marine Corps'
                                                        ''', year1,year2)  
                                    for result in cursor1:
                                        military.append(result) 
                                    cursor1.close()
                                    
                                elif airforce != "on":
                                    headings = ["Year", "Branch", "Count", "Rate", 
                                                "Mental Health Diagnosis", "NO Mental Health Diagnosis",
                                                "TBI History", "NO TBI", "Previous Self-Harm", 
                                                "NO Previous Self-Harm", "Visited Health Services", "DID NOT visit"]
                                    cursor1 = g.conn.execute('''SELECT S.year, B.branch, S.count, S.rate, M.health_diag_y,
                                                             M.health_diag_n, m.tbi_y, m.tbi_n, m.prev_self_harm_y, m.prev_self_harm_n,
                                                             m.health_ser_used_y, m.health_ser_used_n
                                                            FROM Suicides S, Military_Branch B, Mental_Characteristics M
                                                            WHERE s.sid = b.sid 
                                                            AND b.sid = m.sid
                                                            AND S.year >= (%s) 
                                                            AND S.year <= (%s)
                                                            AND B.branch != 'Navy'
                                                            AND B.branch != 'Marine Corps'
                                                            AND B.branch != 'Air Force'
                                                        ''', year1,year2)  
                                    for result in cursor1:
                                        military.append(result) 
                                    cursor1.close()
                                    
                    elif army !="on":
                        if navy =="on": 
                            if marines =="on": 
                                if airforce == "on":
                                    headings = ["Year", "Branch", "Count", "Rate", 
                                                "Mental Health Diagnosis", "NO Mental Health Diagnosis",
                                                "TBI History", "NO TBI", "Previous Self-Harm", 
                                                "NO Previous Self-Harm", "Visited Health Services", "DID NOT visit"]
                                    cursor1 = g.conn.execute('''SELECT S.year, B.branch, S.count, S.rate, M.health_diag_y,
                                                             M.health_diag_n, m.tbi_y, m.tbi_n, m.prev_self_harm_y, m.prev_self_harm_n,
                                                             m.health_ser_used_y, m.health_ser_used_n
                                                            FROM Suicides S, Military_Branch B, Mental_Characteristics M
                                                            WHERE s.sid = b.sid 
                                                            AND b.sid = m.sid
                                                            AND S.year >= (%s) 
                                                            AND S.year <= (%s)
                                                            AND B.branch != 'Army'
                                                        ''', year1,year2)  
                                    for result in cursor1:
                                        military.append(result) 
                                    cursor1.close()
                                    
                                elif airforce != "on":
                                    headings = ["Year", "Branch", "Count", "Rate", 
                                                "Mental Health Diagnosis", "NO Mental Health Diagnosis",
                                                "TBI History", "NO TBI", "Previous Self-Harm", 
                                                "NO Previous Self-Harm", "Visited Health Services", "DID NOT visit"]
                                    cursor1 = g.conn.execute('''SELECT S.year, B.branch, S.count, S.rate, M.health_diag_y,
                                                             M.health_diag_n, m.tbi_y, m.tbi_n, m.prev_self_harm_y, m.prev_self_harm_n,
                                                             m.health_ser_used_y, m.health_ser_used_n
                                                            FROM Suicides S, Military_Branch B, Mental_Characteristics M
                                                            WHERE s.sid = b.sid 
                                                            AND b.sid = m.sid
                                                            AND S.year >= (%s) 
                                                            AND S.year <= (%s)
                                                            AND B.branch != 'Army'
                                                            AND B.branch != 'Air Force'
                                                        ''', year1,year2)  
                                    for result in cursor1:
                                        military.append(result) 
                                    cursor1.close()
                                    
                            elif marines !="on": 
                                if airforce == "on":
                                    headings = ["Year", "Branch", "Count", "Rate", 
                                                "Mental Health Diagnosis", "NO Mental Health Diagnosis",
                                                "TBI History", "NO TBI", "Previous Self-Harm", 
                                                "NO Previous Self-Harm", "Visited Health Services", "DID NOT visit"]
                                    cursor1 = g.conn.execute('''SELECT S.year, B.branch, S.count, S.rate, M.health_diag_y,
                                                             M.health_diag_n, m.tbi_y, m.tbi_n, m.prev_self_harm_y, m.prev_self_harm_n,
                                                             m.health_ser_used_y, m.health_ser_used_n
                                                            FROM Suicides S, Military_Branch B, Mental_Characteristics M
                                                            WHERE s.sid = b.sid 
                                                            AND b.sid = m.sid
                                                            AND S.year >= (%s) 
                                                            AND S.year <= (%s)
                                                            AND B.branch != 'Army'
                                                            AND B.branch != 'Marine Corps'
                                                        ''', year1,year2)  
                                    for result in cursor1:
                                        military.append(result) 
                                    cursor1.close()
                                    
                                elif airforce != "on":
                                    headings = ["Year", "Branch", "Count", "Rate", 
                                                "Mental Health Diagnosis", "NO Mental Health Diagnosis",
                                                "TBI History", "NO TBI", "Previous Self-Harm", 
                                                "NO Previous Self-Harm", "Visited Health Services", "DID NOT visit"]
                                    cursor1 = g.conn.execute('''SELECT S.year, B.branch, S.count, S.rate, M.health_diag_y,
                                                             M.health_diag_n, m.tbi_y, m.tbi_n, m.prev_self_harm_y, m.prev_self_harm_n,
                                                             m.health_ser_used_y, m.health_ser_used_n
                                                            FROM Suicides S, Military_Branch B, Mental_Characteristics M
                                                            WHERE s.sid = b.sid 
                                                            AND b.sid = m.sid
                                                            AND S.year >= (%s) 
                                                            AND S.year <= (%s)
                                                            AND B.branch != 'Army'
                                                            AND B.branch != 'Marine Corps'
                                                            AND B.branch != 'Air Force'
                                                        ''', year1,year2)  
                                    for result in cursor1:
                                        military.append(result) 
                                    cursor1.close()
                                    
                        elif navy !="on": 
                            if marines =="on": 
                                if airforce == "on":
                                    headings = ["Year", "Branch", "Count", "Rate", 
                                                "Mental Health Diagnosis", "NO Mental Health Diagnosis",
                                                "TBI History", "NO TBI", "Previous Self-Harm", 
                                                "NO Previous Self-Harm", "Visited Health Services", "DID NOT visit"]
                                    cursor1 = g.conn.execute('''SELECT S.year, B.branch, S.count, S.rate, M.health_diag_y,
                                                             M.health_diag_n, m.tbi_y, m.tbi_n, m.prev_self_harm_y, m.prev_self_harm_n,
                                                             m.health_ser_used_y, m.health_ser_used_n
                                                            FROM Suicides S, Military_Branch B, Mental_Characteristics M
                                                            WHERE s.sid = b.sid 
                                                            AND b.sid = m.sid
                                                            AND S.year >= (%s) 
                                                            AND S.year <= (%s)
                                                            AND B.branch != 'Army'
                                                            AND B.branch != 'Navy''
                                                        ''', year1,year2)  
                                    for result in cursor1:
                                        military.append(result) 
                                    cursor1.close()
                                    
                                elif airforce != "on":
                                    headings = ["Year", "Branch", "Count", "Rate", 
                                                "Mental Health Diagnosis", "NO Mental Health Diagnosis",
                                                "TBI History", "NO TBI", "Previous Self-Harm", 
                                                "NO Previous Self-Harm", "Visited Health Services", "DID NOT visit"]
                                    cursor1 = g.conn.execute('''SELECT S.year, B.branch, S.count, S.rate, M.health_diag_y,
                                                             M.health_diag_n, m.tbi_y, m.tbi_n, m.prev_self_harm_y, m.prev_self_harm_n,
                                                             m.health_ser_used_y, m.health_ser_used_n
                                                            FROM Suicides S, Military_Branch B, Mental_Characteristics M
                                                            WHERE s.sid = b.sid 
                                                            AND b.sid = m.sid
                                                            AND S.year >= (%s) 
                                                            AND S.year <= (%s)
                                                            AND B.branch != 'Army'
                                                            AND B.branch != 'Navy'
                                                            AND B.branch != 'Air Force'
                                                        ''', year1,year2)  
                                    for result in cursor1:
                                        military.append(result) 
                                    cursor1.close()
                                    
                            elif marines !="on": 
                                if airforce == "on":
                                    headings = ["Year", "Branch", "Count", "Rate", 
                                                "Mental Health Diagnosis", "NO Mental Health Diagnosis",
                                                "TBI History", "NO TBI", "Previous Self-Harm", 
                                                "NO Previous Self-Harm", "Visited Health Services", "DID NOT visit"]
                                    cursor1 = g.conn.execute('''SELECT S.year, B.branch, S.count, S.rate, M.health_diag_y,
                                                             M.health_diag_n, m.tbi_y, m.tbi_n, m.prev_self_harm_y, m.prev_self_harm_n,
                                                             m.health_ser_used_y, m.health_ser_used_n
                                                            FROM Suicides S, Military_Branch B, Mental_Characteristics M
                                                            WHERE s.sid = b.sid 
                                                            AND b.sid = m.sid
                                                            AND S.year >= (%s) 
                                                            AND S.year <= (%s)
                                                            AND B.branch != 'Army'
                                                            AND B.branch != 'Navy'
                                                            AND B.branch != 'Marine Corps'
                                                        ''', year1,year2)  
                                    for result in cursor1:
                                        military.append(result) 
                                    cursor1.close()
                                    
                                elif airforce != "on":
                                    headings = ["Year", "Branch", "Count", "Rate", 
                                                "Mental Health Diagnosis", "NO Mental Health Diagnosis",
                                                "TBI History", "NO TBI", "Previous Self-Harm", 
                                                "NO Previous Self-Harm", "Visited Health Services", "DID NOT visit"]
                                    cursor1 = g.conn.execute('''SELECT S.year, B.branch, S.count, S.rate, M.health_diag_y,
                                                             M.health_diag_n, m.tbi_y, m.tbi_n, m.prev_self_harm_y, m.prev_self_harm_n,
                                                             m.health_ser_used_y, m.health_ser_used_n
                                                            FROM Suicides S, Military_Branch B, Mental_Characteristics M
                                                            WHERE s.sid = b.sid 
                                                            AND b.sid = m.sid
                                                            AND S.year >= (%s) 
                                                            AND S.year <= (%s)
                                                            AND B.branch != 'Army'
                                                            AND B.branch != 'Navy'
                                                            AND B.branch != 'Marine Corps'
                                                            AND B.branch != 'Air Force'
                                                        ''', year1,year2)  
                                    for result in cursor1:
                                        military.append(result) 
                                    cursor1.close()
                if combined != 'on':
                    if army == "on":
                        if navy =="on": 
                            if marines =="on": 
                                if airforce == "on":
                                    headings = ["Year", "Branch", "Count", "Rate", 
                                                "Mental Health Diagnosis", "NO Mental Health Diagnosis",
                                                "TBI History", "NO TBI", "Previous Self-Harm", 
                                                "NO Previous Self-Harm", "Visited Health Services", "DID NOT visit"]
                                    cursor1 = g.conn.execute('''SELECT S.year, B.branch, S.count, S.rate, M.health_diag_y,
                                                             M.health_diag_n, m.tbi_y, m.tbi_n, m.prev_self_harm_y, m.prev_self_harm_n,
                                                             m.health_ser_used_y, m.health_ser_used_n
                                                            FROM Suicides S, Military_Branch B, Mental_Characteristics M
                                                            WHERE s.sid = b.sid 
                                                            AND b.sid = m.sid
                                                            AND S.year >= (%s) 
                                                            AND S.year <= (%s)
                                                            AND B.branch != 'All'
                                                            ''', year1,year2)   
                                    for result in cursor1:
                                        military.append(result) 
                                    cursor1.close()
                                    
                                elif airforce != "on":
                                    headings = ["Year", "Branch", "Count", "Rate", 
                                                "Mental Health Diagnosis", "NO Mental Health Diagnosis",
                                                "TBI History", "NO TBI", "Previous Self-Harm", 
                                                "NO Previous Self-Harm", "Visited Health Services", "DID NOT visit"]
                                    cursor1 = g.conn.execute('''SELECT S.year, B.branch, S.count, S.rate, M.health_diag_y,
                                                             M.health_diag_n, m.tbi_y, m.tbi_n, m.prev_self_harm_y, m.prev_self_harm_n,
                                                             m.health_ser_used_y, m.health_ser_used_n
                                                            FROM Suicides S, Military_Branch B, Mental_Characteristics M
                                                            WHERE s.sid = b.sid 
                                                            AND b.sid = m.sid
                                                            AND S.year >= (%s) 
                                                            AND S.year <= (%s)
                                                            AND B.branch != 'Air Force'
                                                            AND B.branch != 'All'
                                                        ''', year1,year2)  
                                    for result in cursor1:
                                        military.append(result) 
                                    cursor1.close()
                                    
                            elif marines !="on": 
                                if airforce == "on":
                                    headings = ["Year", "Branch", "Count", "Rate", 
                                                "Mental Health Diagnosis", "NO Mental Health Diagnosis",
                                                "TBI History", "NO TBI", "Previous Self-Harm", 
                                                "NO Previous Self-Harm", "Visited Health Services", "DID NOT visit"]
                                    cursor1 = g.conn.execute('''SELECT S.year, B.branch, S.count, S.rate, M.health_diag_y,
                                                             M.health_diag_n, m.tbi_y, m.tbi_n, m.prev_self_harm_y, m.prev_self_harm_n,
                                                             m.health_ser_used_y, m.health_ser_used_n
                                                            FROM Suicides S, Military_Branch B, Mental_Characteristics M
                                                            WHERE s.sid = b.sid 
                                                            AND b.sid = m.sid
                                                            AND S.year >= (%s) 
                                                            AND S.year <= (%s)
                                                            AND B.branch != 'Marine Corps'
                                                            AND B.branch != 'All'
                                                        ''', year1,year2)  
                                    for result in cursor1:
                                        military.append(result) 
                                    cursor1.close()
                                    
                                elif airforce != "on":
                                    headings = ["Year", "Branch", "Count", "Rate", 
                                                "Mental Health Diagnosis", "NO Mental Health Diagnosis",
                                                "TBI History", "NO TBI", "Previous Self-Harm", 
                                                "NO Previous Self-Harm", "Visited Health Services", "DID NOT visit"]
                                    cursor1 = g.conn.execute('''SELECT S.year, B.branch, S.count, S.rate, M.health_diag_y,
                                                             M.health_diag_n, m.tbi_y, m.tbi_n, m.prev_self_harm_y, m.prev_self_harm_n,
                                                             m.health_ser_used_y, m.health_ser_used_n
                                                            FROM Suicides S, Military_Branch B, Mental_Characteristics M
                                                            WHERE s.sid = b.sid 
                                                            AND b.sid = m.sid
                                                            AND S.year >= (%s) 
                                                            AND S.year <= (%s)
                                                            AND B.branch != 'Marine Corps'
                                                            AND B.branch != 'Air Force'
                                                            AND B.branch != 'All'
                                                        ''', year1,year2)  
                                    for result in cursor1:
                                        military.append(result) 
                                    cursor1.close()
                                    
                        elif navy !="on": 
                            if marines =="on": 
                                if airforce == "on":
                                    headings = ["Year", "Branch", "Count", "Rate", 
                                                "Mental Health Diagnosis", "NO Mental Health Diagnosis",
                                                "TBI History", "NO TBI", "Previous Self-Harm", 
                                                "NO Previous Self-Harm", "Visited Health Services", "DID NOT visit"]
                                    cursor1 = g.conn.execute('''SELECT S.year, B.branch, S.count, S.rate, M.health_diag_y,
                                                             M.health_diag_n, m.tbi_y, m.tbi_n, m.prev_self_harm_y, m.prev_self_harm_n,
                                                             m.health_ser_used_y, m.health_ser_used_n
                                                            FROM Suicides S, Military_Branch B, Mental_Characteristics M
                                                            WHERE s.sid = b.sid 
                                                            AND b.sid = m.sid
                                                            AND S.year >= (%s) 
                                                            AND S.year <= (%s)
                                                            AND B.branch != 'Navy'
                                                            AND B.branch != 'All'
                                                        ''', year1,year2)  
                                    for result in cursor1:
                                        military.append(result) 
                                    cursor1.close()
                                    
                                elif airforce != "on":
                                    headings = ["Year", "Branch", "Count", "Rate", 
                                                "Mental Health Diagnosis", "NO Mental Health Diagnosis",
                                                "TBI History", "NO TBI", "Previous Self-Harm", 
                                                "NO Previous Self-Harm", "Visited Health Services", "DID NOT visit"]
                                    cursor1 = g.conn.execute('''SELECT S.year, B.branch, S.count, S.rate, M.health_diag_y,
                                                             M.health_diag_n, m.tbi_y, m.tbi_n, m.prev_self_harm_y, m.prev_self_harm_n,
                                                             m.health_ser_used_y, m.health_ser_used_n
                                                            FROM Suicides S, Military_Branch B, Mental_Characteristics M
                                                            WHERE s.sid = b.sid 
                                                            AND b.sid = m.sid
                                                            AND S.year >= (%s) 
                                                            AND S.year <= (%s)
                                                            AND B.branch != 'Navy'
                                                            AND B.branch != 'Marine Corps'
                                                            AND B.branch != 'Air Force'
                                                            AND B.branch != 'All'
                                                        ''', year1,year2)  
                                    for result in cursor1:
                                        military.append(result) 
                                    cursor1.close()
                                    
                            elif marines !="on": 
                                if airforce == "on":
                                    headings = ["Year", "Branch", "Count", "Rate", 
                                                "Mental Health Diagnosis", "NO Mental Health Diagnosis",
                                                "TBI History", "NO TBI", "Previous Self-Harm", 
                                                "NO Previous Self-Harm", "Visited Health Services", "DID NOT visit"]
                                    cursor1 = g.conn.execute('''SELECT S.year, B.branch, S.count, S.rate, M.health_diag_y,
                                                             M.health_diag_n, m.tbi_y, m.tbi_n, m.prev_self_harm_y, m.prev_self_harm_n,
                                                             m.health_ser_used_y, m.health_ser_used_n
                                                            FROM Suicides S, Military_Branch B, Mental_Characteristics M
                                                            WHERE s.sid = b.sid 
                                                            AND b.sid = m.sid
                                                            AND S.year >= (%s) 
                                                            AND S.year <= (%s)
                                                            AND S.year >= (%s) 
                                                            AND S.year <= (%s)
                                                            AND B.branch != 'Navy'
                                                            AND B.branch != 'Marine Corps'
                                                            AND B.branch != 'All'
                                                        ''', year1,year2)  
                                    for result in cursor1:
                                        military.append(result) 
                                    cursor1.close()
                                    
                                elif airforce != "on":
                                    headings = ["Year", "Branch", "Count", "Rate", 
                                                "Mental Health Diagnosis", "NO Mental Health Diagnosis",
                                                "TBI History", "NO TBI", "Previous Self-Harm", 
                                                "NO Previous Self-Harm", "Visited Health Services", "DID NOT visit"]
                                    cursor1 = g.conn.execute('''SELECT S.year, B.branch, S.count, S.rate, M.health_diag_y,
                                                             M.health_diag_n, m.tbi_y, m.tbi_n, m.prev_self_harm_y, m.prev_self_harm_n,
                                                             m.health_ser_used_y, m.health_ser_used_n
                                                            FROM Suicides S, Military_Branch B, Mental_Characteristics M
                                                            WHERE s.sid = b.sid 
                                                            AND b.sid = m.sid
                                                            AND S.year >= (%s) 
                                                            AND S.year <= (%s)
                                                            AND B.branch != 'Navy'
                                                            AND B.branch != 'Marine Corps'
                                                            AND B.branch != 'Air Force'
                                                            AND B.branch != 'All'
                                                        ''', year1,year2)  
                                    for result in cursor1:
                                        military.append(result) 
                                    cursor1.close()
                                    
                    elif army !="on":
                        if navy =="on": 
                            if marines =="on": 
                                if airforce == "on":
                                    headings = ["Year", "Branch", "Count", "Rate", 
                                                "Mental Health Diagnosis", "NO Mental Health Diagnosis",
                                                "TBI History", "NO TBI", "Previous Self-Harm", 
                                                "NO Previous Self-Harm", "Visited Health Services", "DID NOT visit"]
                                    cursor1 = g.conn.execute('''SELECT S.year, B.branch, S.count, S.rate, M.health_diag_y,
                                                             M.health_diag_n, m.tbi_y, m.tbi_n, m.prev_self_harm_y, m.prev_self_harm_n,
                                                             m.health_ser_used_y, m.health_ser_used_n
                                                            FROM Suicides S, Military_Branch B, Mental_Characteristics M
                                                            WHERE s.sid = b.sid 
                                                            AND b.sid = m.sid
                                                            AND S.year >= (%s) 
                                                            AND S.year <= (%s)
                                                            AND B.branch != 'Army'
                                                            AND B.branch != 'All'
                                                        ''', year1,year2)  
                                    for result in cursor1:
                                        military.append(result) 
                                    cursor1.close()
                                    
                                elif airforce != "on":
                                    headings = ["Year", "Branch", "Count", "Rate", 
                                                "Mental Health Diagnosis", "NO Mental Health Diagnosis",
                                                "TBI History", "NO TBI", "Previous Self-Harm", 
                                                "NO Previous Self-Harm", "Visited Health Services", "DID NOT visit"]
                                    cursor1 = g.conn.execute('''SELECT S.year, B.branch, S.count, S.rate, M.health_diag_y,
                                                             M.health_diag_n, m.tbi_y, m.tbi_n, m.prev_self_harm_y, m.prev_self_harm_n,
                                                             m.health_ser_used_y, m.health_ser_used_n
                                                            FROM Suicides S, Military_Branch B, Mental_Characteristics M
                                                            WHERE s.sid = b.sid 
                                                            AND b.sid = m.sid
                                                            AND S.year >= (%s) 
                                                            AND S.year <= (%s)
                                                            AND B.branch != 'Army'
                                                            AND B.branch != 'Air Force'
                                                            AND B.branch != 'All'
                                                        ''', year1,year2)  
                                    for result in cursor1:
                                        military.append(result) 
                                    cursor1.close()
                                    
                            elif marines !="on": 
                                if airforce == "on":
                                    headings = ["Year", "Branch", "Count", "Rate", 
                                                "Mental Health Diagnosis", "NO Mental Health Diagnosis",
                                                "TBI History", "NO TBI", "Previous Self-Harm", 
                                                "NO Previous Self-Harm", "Visited Health Services", "DID NOT visit"]
                                    cursor1 = g.conn.execute('''SELECT S.year, B.branch, S.count, S.rate, M.health_diag_y,
                                                             M.health_diag_n, m.tbi_y, m.tbi_n, m.prev_self_harm_y, m.prev_self_harm_n,
                                                             m.health_ser_used_y, m.health_ser_used_n
                                                            FROM Suicides S, Military_Branch B, Mental_Characteristics M
                                                            WHERE s.sid = b.sid 
                                                            AND b.sid = m.sid
                                                            AND S.year >= (%s) 
                                                            AND S.year <= (%s)
                                                            AND B.branch != 'Army'
                                                            AND B.branch != 'Marines'
                                                            AND B.branch != 'All'
                                                        ''', year1,year2)  
                                    for result in cursor1:
                                        military.append(result) 
                                    cursor1.close()
                                    
                                elif airforce != "on":
                                    headings = ["Year", "Branch", "Count", "Rate", 
                                                "Mental Health Diagnosis", "NO Mental Health Diagnosis",
                                                "TBI History", "NO TBI", "Previous Self-Harm", 
                                                "NO Previous Self-Harm", "Visited Health Services", "DID NOT visit"]
                                    cursor1 = g.conn.execute('''SELECT S.year, B.branch, S.count, S.rate, M.health_diag_y,
                                                             M.health_diag_n, m.tbi_y, m.tbi_n, m.prev_self_harm_y, m.prev_self_harm_n,
                                                             m.health_ser_used_y, m.health_ser_used_n
                                                            FROM Suicides S, Military_Branch B, Mental_Characteristics M
                                                            WHERE s.sid = b.sid 
                                                            AND b.sid = m.sid
                                                            AND S.year >= (%s) 
                                                            AND S.year <= (%s)
                                                            AND B.branch != 'Army'
                                                            AND B.branch != 'Marine Corps'
                                                            AND B.branch != 'Air Force'
                                                            AND B.branch != 'All'
                                                        ''', year1,year2)  
                                    for result in cursor1:
                                        military.append(result) 
                                    cursor1.close()
                                    
                        elif navy !="on": 
                            if marines =="on": 
                                if airforce == "on":
                                    headings = ["Year", "Branch", "Count", "Rate", 
                                                "Mental Health Diagnosis", "NO Mental Health Diagnosis",
                                                "TBI History", "NO TBI", "Previous Self-Harm", 
                                                "NO Previous Self-Harm", "Visited Health Services", "DID NOT visit"]
                                    cursor1 = g.conn.execute('''SELECT S.year, B.branch, S.count, S.rate, M.health_diag_y,
                                                             M.health_diag_n, m.tbi_y, m.tbi_n, m.prev_self_harm_y, m.prev_self_harm_n,
                                                             m.health_ser_used_y, m.health_ser_used_n
                                                            FROM Suicides S, Military_Branch B, Mental_Characteristics M
                                                            WHERE s.sid = b.sid 
                                                            AND b.sid = m.sid
                                                            AND S.year >= (%s) 
                                                            AND S.year <= (%s)
                                                            AND B.branch != 'Army'
                                                            AND B.branch != 'Navy''
                                                            AND B.branch != 'All'
                                                        ''', year1,year2)  
                                    for result in cursor1:
                                        military.append(result) 
                                    cursor1.close()
                                    
                                elif airforce != "on":
                                    headings = ["Year", "Branch", "Count", "Rate", 
                                                "Mental Health Diagnosis", "NO Mental Health Diagnosis",
                                                "TBI History", "NO TBI", "Previous Self-Harm", 
                                                "NO Previous Self-Harm", "Visited Health Services", "DID NOT visit"]
                                    cursor1 = g.conn.execute('''SELECT S.year, B.branch, S.count, S.rate, M.health_diag_y,
                                                             M.health_diag_n, m.tbi_y, m.tbi_n, m.prev_self_harm_y, m.prev_self_harm_n,
                                                             m.health_ser_used_y, m.health_ser_used_n
                                                            FROM Suicides S, Military_Branch B, Mental_Characteristics M
                                                            WHERE s.sid = b.sid 
                                                            AND b.sid = m.sid
                                                            AND S.year >= (%s) 
                                                            AND S.year <= (%s)
                                                            AND B.branch != 'Army'
                                                            AND B.branch != 'Navy'
                                                            AND B.branch != 'Air Force'
                                                            AND B.branch != 'All'
                                                        ''', year1,year2)  
                                    for result in cursor1:
                                        military.append(result) 
                                    cursor1.close()
                                    
                            elif marines !="on": 
                                if airforce == "on":
                                    headings = ["Year", "Branch", "Count", "Rate", 
                                                "Mental Health Diagnosis", "NO Mental Health Diagnosis",
                                                "TBI History", "NO TBI", "Previous Self-Harm", 
                                                "NO Previous Self-Harm", "Visited Health Services", "DID NOT visit"]
                                    cursor1 = g.conn.execute('''SELECT S.year, B.branch, S.count, S.rate, M.health_diag_y,
                                                             M.health_diag_n, m.tbi_y, m.tbi_n, m.prev_self_harm_y, m.prev_self_harm_n,
                                                             m.health_ser_used_y, m.health_ser_used_n
                                                            FROM Suicides S, Military_Branch B, Mental_Characteristics M
                                                            WHERE s.sid = b.sid 
                                                            AND b.sid = m.sid
                                                            AND S.year >= (%s) 
                                                            AND S.year <= (%s)
                                                            AND B.branch != 'Army'
                                                            AND B.branch != 'Navy'
                                                            AND B.branch != 'Marine Corps'
                                                            AND B.branch != 'All'
                                                        ''', year1,year2)  
                                    for result in cursor1:
                                        military.append(result) 
                                    cursor1.close()
                                    
                                elif airforce != "on":
                                    headings = ["Year", "Branch", "Count", "Rate", 
                                                "Mental Health Diagnosis", "NO Mental Health Diagnosis",
                                                "TBI History", "NO TBI", "Previous Self-Harm", 
                                                "NO Previous Self-Harm", "Visited Health Services", "DID NOT visit"]
                                    cursor1 = g.conn.execute('''SELECT S.year, B.branch, S.count, S.rate, M.health_diag_y,
                                                             M.health_diag_n, m.tbi_y, m.tbi_n, m.prev_self_harm_y, m.prev_self_harm_n,
                                                             m.health_ser_used_y, m.health_ser_used_n
                                                            FROM Suicides S, Military_Branch B, Mental_Characteristics M
                                                            WHERE s.sid = b.sid 
                                                            AND b.sid = m.sid
                                                            AND S.year >= (%s) 
                                                            AND S.year <= (%s)
                                                            AND B.branch != 'Army'
                                                            AND B.branch != 'Navy'
                                                            AND B.branch != 'Marine Corps'
                                                            AND B.branch != 'Air Force'
                                                            AND B.branch != 'All'
                                                        ''', year1,year2)  
                                    for result in cursor1:
                                        military.append(result) 
                                    cursor1.close()
            if showmh != "on":
                if combined == 'on':
                    if army == "on":
                        if navy =="on": 
                            if marines =="on": 
                                if airforce == "on":
                                    headings = ["Year", "Branch", "Count", "Rate"]
                                    cursor1 = g.conn.execute('''SELECT S.year, B.branch, S.count, S.rate
                                                            FROM Suicides S, Military_Branch B
                                                            WHERE s.sid = b.sid 
                                                            AND S.year >= (%s) 
                                                            AND S.year <= (%s)
                                                            ''', year1,year2)   
                                    for result in cursor1:
                                        military.append(result) 
                                    cursor1.close()
                                    
                                elif airforce != "on":
                                    headings = ["Year", "Branch", "Count", "Rate"]
                                    cursor1 = g.conn.execute('''SELECT S.year, B.branch, S.count, S.rate
                                                            FROM Suicides S, Military_Branch B
                                                            WHERE s.sid = b.sid 
                                                            AND S.year >= (%s) 
                                                            AND S.year <= (%s)
                                                            AND B.branch != 'Air Force'
                                                            
                                                        ''', year1,year2)  
                                    for result in cursor1:
                                        military.append(result) 
                                    cursor1.close()
                                    
                            elif marines !="on": 
                                if airforce == "on":
                                    headings = ["Year", "Branch", "Count", "Rate"]
                                    cursor1 = g.conn.execute('''SELECT S.year, B.branch, S.count, S.rate
                                                            FROM Suicides S, Military_Branch B
                                                            WHERE s.sid = b.sid 
                                                            AND S.year >= (%s) 
                                                            AND S.year <= (%s)
                                                            AND B.branch != 'Marine Corps'
                                                        ''', year1,year2)  
                                    for result in cursor1:
                                        military.append(result) 
                                    cursor1.close()
                                    
                                elif airforce != "on":
                                    headings = ["Year", "Branch", "Count", "Rate"]
                                    cursor1 = g.conn.execute('''SELECT S.year, B.branch, S.count, S.rate
                                                            FROM Suicides S, Military_Branch B
                                                            WHERE s.sid = b.sid 
                                                            AND S.year >= (%s) 
                                                            AND S.year <= (%s)
                                                            AND B.branch != 'Marine Corps'
                                                            AND B.branch != 'Air Force'
                                                        ''', year1,year2)  
                                    for result in cursor1:
                                        military.append(result) 
                                    cursor1.close()
                                    
                        elif navy !="on": 
                            if marines =="on": 
                                if airforce == "on":
                                    headings = ["Year", "Branch", "Count", "Rate"]
                                    cursor1 = g.conn.execute('''SELECT S.year, B.branch, S.count, S.rate
                                                            FROM Suicides S, Military_Branch B
                                                            WHERE s.sid = b.sid 
                                                            AND S.year >= (%s) 
                                                            AND S.year <= (%s)
                                                            AND B.branch != 'Navy'
                                                        ''', year1,year2)  
                                    for result in cursor1:
                                        military.append(result) 
                                    cursor1.close()
                                    
                                elif airforce != "on":
                                    headings = ["Year", "Branch", "Count", "Rate"]
                                    cursor1 = g.conn.execute('''SELECT S.year, B.branch, S.count, S.rate
                                                            FROM Suicides S, Military_Branch B
                                                            WHERE s.sid = b.sid 
                                                            AND S.year >= (%s) 
                                                            AND S.year <= (%s)
                                                            AND B.branch != 'Navy'
                                                            AND B.branch != 'Marine Corps'
                                                            AND B.branch != 'Air Force'
                                                        ''', year1,year2)  
                                    for result in cursor1:
                                        military.append(result) 
                                    cursor1.close()
                                    
                            elif marines !="on": 
                                if airforce == "on":
                                    headings = ["Year", "Branch", "Count", "Rate"]
                                    cursor1 = g.conn.execute('''SELECT S.year, B.branch, S.count, S.rate
                                                            FROM Suicides S, Military_Branch B
                                                            WHERE s.sid = b.sid 
                                                            AND S.year >= (%s) 
                                                            AND S.year <= (%s)
                                                            AND B.branch != 'Navy'
                                                            AND B.branch != 'Marine Corps'
                                                        ''', year1,year2)  
                                    for result in cursor1:
                                        military.append(result) 
                                    cursor1.close()
                                    
                                elif airforce != "on":
                                    headings = ["Year", "Branch", "Count", "Rate"]
                                    cursor1 = g.conn.execute('''SELECT S.year, B.branch, S.count, S.rate
                                                            FROM Suicides S, Military_Branch B
                                                            WHERE s.sid = b.sid 
                                                            AND S.year >= (%s) 
                                                            AND S.year <= (%s)
                                                            AND B.branch != 'Navy'
                                                            AND B.branch != 'Marine Corps'
                                                            AND B.branch != 'Air Force'
                                                        ''', year1,year2)  
                                    for result in cursor1:
                                        military.append(result) 
                                    cursor1.close()
                                    
                    elif army !="on":
                        if navy =="on": 
                            if marines =="on": 
                                if airforce == "on":
                                    headings = ["Year", "Branch", "Count", "Rate"]
                                    cursor1 = g.conn.execute('''SELECT S.year, B.branch, S.count, S.rate
                                                            FROM Suicides S, Military_Branch B
                                                            WHERE s.sid = b.sid 
                                                            AND S.year >= (%s) 
                                                            AND S.year <= (%s)
                                                            AND B.branch != 'Army'
                                                        ''', year1,year2)  
                                    for result in cursor1:
                                        military.append(result) 
                                    cursor1.close()
                                    
                                elif airforce != "on":
                                    headings = ["Year", "Branch", "Count", "Rate"]
                                    cursor1 = g.conn.execute('''SELECT S.year, B.branch, S.count, S.rate
                                                            FROM Suicides S, Military_Branch B
                                                            WHERE s.sid = b.sid 
                                                            AND S.year >= (%s) 
                                                            AND S.year <= (%s)
                                                            AND B.branch != 'Army'
                                                            AND B.branch != 'Air Force'
                                                        ''', year1,year2)  
                                    for result in cursor1:
                                        military.append(result) 
                                    cursor1.close()
                                    
                            elif marines !="on": 
                                if airforce == "on":
                                    headings = ["Year", "Branch", "Count", "Rate"]
                                    cursor1 = g.conn.execute('''SELECT S.year, B.branch, S.count, S.rate
                                                            FROM Suicides S, Military_Branch B
                                                            WHERE s.sid = b.sid 
                                                            AND S.year >= (%s) 
                                                            AND S.year <= (%s)
                                                            AND B.branch != 'Army'
                                                            AND B.branch != 'Marine Corps'
                                                        ''', year1,year2)  
                                    for result in cursor1:
                                        military.append(result) 
                                    cursor1.close()
                                    
                                elif airforce != "on":
                                    headings = ["Year", "Branch", "Count", "Rate"]
                                    cursor1 = g.conn.execute('''SELECT S.year, B.branch, S.count, S.rate
                                                            FROM Suicides S, Military_Branch B
                                                            WHERE s.sid = b.sid 
                                                            AND S.year >= (%s) 
                                                            AND S.year <= (%s)
                                                            AND B.branch != 'Army'
                                                            AND B.branch != 'Marine Corps'
                                                            AND B.branch != 'Air Force'
                                                        ''', year1,year2)  
                                    for result in cursor1:
                                        military.append(result) 
                                    cursor1.close()
                                    
                        elif navy !="on": 
                            if marines =="on": 
                                if airforce == "on":
                                    headings = ["Year", "Branch", "Count", "Rate"]
                                    cursor1 = g.conn.execute('''SELECT S.year, B.branch, S.count, S.rate
                                                            FROM Suicides S, Military_Branch B
                                                            WHERE s.sid = b.sid 
                                                            AND S.year >= (%s) 
                                                            AND S.year <= (%s)
                                                            AND B.branch != 'Army'
                                                            AND B.branch != 'Navy''
                                                        ''', year1,year2)  
                                    for result in cursor1:
                                        military.append(result) 
                                    cursor1.close()
                                    
                                elif airforce != "on":
                                    headings = ["Year", "Branch", "Count", "Rate"]
                                    cursor1 = g.conn.execute('''SELECT S.year, B.branch, S.count, S.rate
                                                            FROM Suicides S, Military_Branch B
                                                            WHERE s.sid = b.sid 
                                                            AND S.year >= (%s) 
                                                            AND S.year <= (%s)
                                                            AND B.branch != 'Army'
                                                            AND B.branch != 'Navy'
                                                            AND B.branch != 'Air Force'
                                                        ''', year1,year2)  
                                    for result in cursor1:
                                        military.append(result) 
                                    cursor1.close()
                                    
                            elif marines !="on": 
                                if airforce == "on":
                                    headings = ["Year", "Branch", "Count", "Rate"]
                                    cursor1 = g.conn.execute('''SELECT S.year, B.branch, S.count, S.rate
                                                            FROM Suicides S, Military_Branch B
                                                            WHERE s.sid = b.sid 
                                                            AND S.year >= (%s) 
                                                            AND S.year <= (%s)
                                                            AND B.branch != 'Army'
                                                            AND B.branch != 'Navy'
                                                            AND B.branch != 'Marine Corps'
                                                        ''', year1,year2)  
                                    for result in cursor1:
                                        military.append(result) 
                                    cursor1.close()
                                    
                                elif airforce != "on":
                                    headings = ["Year", "Branch", "Count", "Rate"]
                                    cursor1 = g.conn.execute('''SELECT S.year, B.branch, S.count, S.rate
                                                            FROM Suicides S, Military_Branch B
                                                            WHERE s.sid = b.sid 
                                                            AND S.year >= (%s) 
                                                            AND S.year <= (%s)
                                                            AND B.branch != 'Army'
                                                            AND B.branch != 'Navy'
                                                            AND B.branch != 'Marine Corps'
                                                            AND B.branch != 'Air Force'
                                                        ''', year1,year2)  
                                    for result in cursor1:
                                        military.append(result) 
                                    cursor1.close()
                if combined != 'on':
                    if army == "on":
                        if navy =="on": 
                            if marines =="on": 
                                if airforce == "on":
                                    headings = ["Year", "Branch", "Count", "Rate"]
                                    cursor1 = g.conn.execute('''SELECT S.year, B.branch, S.count, S.rate
                                                            FROM Suicides S, Military_Branch B
                                                            WHERE s.sid = b.sid 
                                                            AND S.year >= (%s) 
                                                            AND S.year <= (%s)
                                                            AND S.year >= (%s) 
                                                            AND S.year <= (%s)
                                                            AND B.branch != 'All'
                                                            ''', year1,year2)   
                                    for result in cursor1:
                                        military.append(result) 
                                    cursor1.close()
                                    
                                elif airforce != "on":
                                    headings = ["Year", "Branch", "Count", "Rate"]
                                    cursor1 = g.conn.execute('''SELECT S.year, B.branch, S.count, S.rate
                                                            FROM Suicides S, Military_Branch B
                                                            WHERE s.sid = b.sid 
                                                            AND S.year >= (%s) 
                                                            AND S.year <= (%s)
                                                            AND B.branch != 'Air Force'
                                                            AND B.branch != 'All'
                                                            
                                                        ''', year1,year2)  
                                    for result in cursor1:
                                        military.append(result) 
                                    cursor1.close()
                                    
                            elif marines !="on": 
                                if airforce == "on":
                                    headings = ["Year", "Branch", "Count", "Rate"]
                                    cursor1 = g.conn.execute('''SELECT S.year, B.branch, S.count, S.rate
                                                            FROM Suicides S, Military_Branch B
                                                            WHERE s.sid = b.sid 
                                                            AND S.year >= (%s) 
                                                            AND S.year <= (%s)
                                                            AND B.branch != 'Marine Corps'
                                                            AND B.branch != 'All'
                                                        ''', year1,year2)  
                                    for result in cursor1:
                                        military.append(result) 
                                    cursor1.close()
                                    
                                elif airforce != "on":
                                    headings = ["Year", "Branch", "Count", "Rate"]
                                    cursor1 = g.conn.execute('''SELECT S.year, B.branch, S.count, S.rate
                                                            FROM Suicides S, Military_Branch B
                                                            WHERE s.sid = b.sid 
                                                            AND S.year >= (%s) 
                                                            AND S.year <= (%s)
                                                            AND B.branch != 'Marine Corps'
                                                            AND B.branch != 'Air Force'
                                                            AND B.branch != 'All'
                                                        ''', year1,year2)  
                                    for result in cursor1:
                                        military.append(result) 
                                    cursor1.close()
                                    
                        elif navy !="on": 
                            if marines =="on": 
                                if airforce == "on":
                                    headings = ["Year", "Branch", "Count", "Rate"]
                                    cursor1 = g.conn.execute('''SELECT S.year, B.branch, S.count, S.rate
                                                            FROM Suicides S, Military_Branch B
                                                            WHERE s.sid = b.sid 
                                                            AND S.year >= (%s) 
                                                            AND S.year <= (%s)
                                                            AND B.branch != 'Navy'
                                                            AND B.branch != 'All'
                                                        ''', year1,year2)  
                                    for result in cursor1:
                                        military.append(result) 
                                    cursor1.close()
                                    
                                elif airforce != "on":
                                    headings = ["Year", "Branch", "Count", "Rate"]
                                    cursor1 = g.conn.execute('''SELECT S.year, B.branch, S.count, S.rate
                                                            FROM Suicides S, Military_Branch B
                                                            WHERE s.sid = b.sid 
                                                            AND S.year >= (%s) 
                                                            AND S.year <= (%s)
                                                            AND B.branch != 'Navy'
                                                            AND B.branch != 'Marine Corps'
                                                            AND B.branch != 'Air Force'
                                                            AND B.branch != 'All'
                                                        ''', year1,year2)  
                                    for result in cursor1:
                                        military.append(result) 
                                    cursor1.close()
                                    
                            elif marines !="on": 
                                if airforce == "on":
                                    headings = ["Year", "Branch", "Count", "Rate"]
                                    cursor1 = g.conn.execute('''SELECT S.year, B.branch, S.count, S.rate
                                                            FROM Suicides S, Military_Branch B
                                                            WHERE s.sid = b.sid 
                                                            AND S.year >= (%s) 
                                                            AND S.year <= (%s)
                                                            AND B.branch != 'Navy'
                                                            AND B.branch != 'Marine Corps'
                                                            AND B.branch != 'All'
                                                        ''', year1,year2)  
                                    for result in cursor1:
                                        military.append(result) 
                                    cursor1.close()
                                    
                                elif airforce != "on":
                                    headings = ["Year", "Branch", "Count", "Rate"]
                                    cursor1 = g.conn.execute('''SELECT S.year, B.branch, S.count, S.rate
                                                            FROM Suicides S, Military_Branch B
                                                            WHERE s.sid = b.sid 
                                                            AND S.year >= (%s) 
                                                            AND S.year <= (%s)
                                                            AND B.branch != 'Navy'
                                                            AND B.branch != 'Marine Corps'
                                                            AND B.branch != 'Air Force'
                                                            AND B.branch != 'All'
                                                        ''', year1,year2)  
                                    for result in cursor1:
                                        military.append(result) 
                                    cursor1.close()
                                    
                    elif army !="on":
                        if navy =="on": 
                            if marines =="on": 
                                if airforce == "on":
                                    headings = ["Year", "Branch", "Count", "Rate"]
                                    cursor1 = g.conn.execute('''SELECT S.year, B.branch, S.count, S.rate
                                                            FROM Suicides S, Military_Branch B
                                                            WHERE s.sid = b.sid 
                                                            AND S.year >= (%s) 
                                                            AND S.year <= (%s)
                                                            AND B.branch != 'Army'
                                                            AND B.branch != 'All'
                                                        ''', year1,year2)  
                                    for result in cursor1:
                                        military.append(result) 
                                    cursor1.close()
                                    
                                elif airforce != "on":
                                    headings = ["Year", "Branch", "Count", "Rate"]
                                    cursor1 = g.conn.execute('''SELECT S.year, B.branch, S.count, S.rate
                                                            FROM Suicides S, Military_Branch B
                                                            WHERE s.sid = b.sid 
                                                            AND S.year >= (%s) 
                                                            AND S.year <= (%s)
                                                            AND B.branch != 'Army'
                                                            AND B.branch != 'Air Force'
                                                            AND B.branch != 'All'
                                                        ''', year1,year2)  
                                    for result in cursor1:
                                        military.append(result) 
                                    cursor1.close()
                                    
                            elif marines !="on": 
                                if airforce == "on":
                                    headings = ["Year", "Branch", "Count", "Rate"]
                                    cursor1 = g.conn.execute('''SELECT S.year, B.branch, S.count, S.rate
                                                            FROM Suicides S, Military_Branch B
                                                            WHERE s.sid = b.sid 
                                                            AND S.year >= (%s) 
                                                            AND S.year <= (%s)
                                                            AND B.branch != 'Army'
                                                            AND B.branch != 'Marine Corps'
                                                            AND B.branch != 'All'
                                                        ''', year1,year2)  
                                    for result in cursor1:
                                        military.append(result) 
                                    cursor1.close()
                                    
                                elif airforce != "on":
                                    headings = ["Year", "Branch", "Count", "Rate"]
                                    cursor1 = g.conn.execute('''SELECT S.year, B.branch, S.count, S.rate
                                                            FROM Suicides S, Military_Branch B
                                                            WHERE s.sid = b.sid 
                                                            AND S.year >= (%s) 
                                                            AND S.year <= (%s)
                                                            AND B.branch != 'Army'
                                                            AND B.branch != 'Marine Corps'
                                                            AND B.branch != 'Air Force'
                                                            AND B.branch != 'All'
                                                        ''', year1,year2)  
                                    for result in cursor1:
                                        military.append(result) 
                                    cursor1.close()
                                    
                        elif navy !="on": 
                            if marines =="on": 
                                if airforce == "on":
                                    headings = ["Year", "Branch", "Count", "Rate"]
                                    cursor1 = g.conn.execute('''SELECT S.year, B.branch, S.count, S.rate
                                                            FROM Suicides S, Military_Branch B
                                                            WHERE s.sid = b.sid 
                                                            AND S.year >= (%s) 
                                                            AND S.year <= (%s)
                                                            AND B.branch != 'Army'
                                                            AND B.branch != 'Navy''
                                                            AND B.branch != 'All'
                                                        ''', year1,year2)  
                                    for result in cursor1:
                                        military.append(result) 
                                    cursor1.close()
                                    
                                elif airforce != "on":
                                    headings = ["Year", "Branch", "Count", "Rate"]
                                    cursor1 = g.conn.execute('''SELECT S.year, B.branch, S.count, S.rate
                                                            FROM Suicides S, Military_Branch B
                                                            WHERE s.sid = b.sid 
                                                            AND S.year >= (%s) 
                                                            AND S.year <= (%s)
                                                            AND B.branch != 'Army'
                                                            AND B.branch != 'Navy'
                                                            AND B.branch != 'Air Force'
                                                            AND B.branch != 'All'
                                                        ''', year1,year2)  
                                    for result in cursor1:
                                        military.append(result) 
                                    cursor1.close()
                                    
                            elif marines !="on": 
                                if airforce == "on":
                                    headings = ["Year", "Branch", "Count", "Rate"]
                                    cursor1 = g.conn.execute('''SELECT S.year, B.branch, S.count, S.rate
                                                            FROM Suicides S, Military_Branch B
                                                            WHERE s.sid = b.sid 
                                                            AND S.year >= (%s) 
                                                            AND S.year <= (%s)
                                                            AND B.branch != 'Army'
                                                            AND B.branch != 'Navy'
                                                            AND B.branch != 'Marine Corps'
                                                            AND B.branch != 'All'
                                                        ''', year1,year2)  
                                    for result in cursor1:
                                        military.append(result) 
                                    cursor1.close()
                                    
                                elif airforce != "on":
                                    error = 'Please enter select a branch to view. Thanks!'
                                    return render_template("military.html", error=error)
        
            
    context = dict(military = military)
    print(context, " context")
    return render_template("military.html", headings=headings, **context)





#SUBMIT Methods
@app.route('/submitmethods',methods=['POST'])
def submitmethods():
    
    #state dictionary for easy access
    states = {'AL':'Alabama', 'AK': 'Alaska', 'AZ': 'Arizona', 'AR':'Arkansas', 'CA':'California',
          'CO':'Colorado', 'CT':'Connecticut', 'DE':'Deleware', 'DC':'District of Columbia',
          'FL':'Florida', 'GA':'Georgia', 'HI':'Hawaii', 'ID':'Idaho', 'IL':'Illinois',
          'IN':'Indiana', 'IA':'Iowa', 'KS':'Kansas', 'KY':'Kentucy', 'LA':'Louisiana',
          'ME':'Maine', 'MD':'Maryland', 'MA':'Massachusetts', 'MI':'Michigan','MN':'Minnesota',
          'MS':'Mississippi', 'MO':'Missouri', 'MT':'Montana', 'NE':'Nebraska', 'NV':'Nevada',
          'NH':'New Hampshire', 'NJ':'New Jersey', 'NM':'New Mexico', 'NY':'New York',
          'NC':'North Carolina', 'ND':'North Dakota', 'OH':'Ohio', 'OK':'Oklahoma','OR':'Oregon',
          'PA':'Pennsylvania', 'RI':'Rhode Island', 'SC':'South Carolina', 'SD':'South Dakota',
          'TN':'Tennessee', 'TX':'Texas', 'UT':'Utah', 'VT':'Vermonet', 'VA':'Virginia',
          'WA':'Washington', 'WV':'West Virginia', 'WI':'Wisconsin', 'WY':'Wyoming'}
    
    #getting the year for the QUERY
    year1 = request.form['year1']
    year2 = request.form['year2']
    
    #making sure year is in the right order
    if year1 > year2:
        temp = year1
        year1 = year2
        year2 = temp
        
    #get selection options
    showciv = request.form.get('showciv')
    showvet = request.form.get('showvet')
    showmil = request.form.get('showmil')
    
    #getting the branches for the QUERY
    # NOTE: when a checkbox is selected, the value == on, else value == none
    showmethod = request.form.get('showmethod')
          
    #getting user input
    rate = request.form['rate']
    print(rate, " :rate")

    
    #creating an empty array for the query results
    methods = []
    headings = []
    
    #running the Query
    #all branches
    if showciv =='on':
        if showvet == 'on':
            if showmil == 'on':
                if showmethod =='on':
                    if rate !='':
                        headings =['Year', 'Overall Rate', 'Group', 'Count', 'Method']
                        cursor = g.conn.execute('''SELECT DISTINCT S.year, S.rate, S.tperson, M.total, M.method
                                                    FROM Suicides S, Death_by M
                                                    WHERE s.sid IN (SELECT m1.sid
                                                                    FROM Death_by M1
                                                                    WHERE m1.sid LIKE '%%all%%'
                                                                    OR m1.sid LIKE '%%na%%')
                                                    AND S.year >= (%s) 
                                                    AND S.year <= (%s)
                                                    AND s.sid = m.sid
                                                    AND S.rate >= (%s)
                                                    ORDER BY S.year DESC, S.tperson, M.total DESC
                                                    ''', year1,year2, rate)
                        for result in cursor:
                            methods.append(result) 
                        cursor.close()
                        
                    elif rate =='':
                        headings =['Year', 'Overall Rate', 'Group', 'Count', 'Method']
                        cursor = g.conn.execute('''SELECT DISTINCT S.year, S.rate, S.tperson, M.total, M.method
                                                    FROM Suicides S, Death_by M
                                                    WHERE s.sid IN (SELECT m1.sid
                                                                    FROM Death_by M1
                                                                    WHERE m1.sid LIKE '%%all%%'
                                                                    OR m1.sid LIKE '%%na%%')
                                                    AND s.sid = m.sid
                                                    ORDER BY S.year DESC, S.tperson, M.total DESC
                                                    ''', year1,year2)
                        for result in cursor:
                            methods.append(result) 
                        cursor.close()
                        
                elif showmethod !='on':
                    if rate != '':
                        headings =['Year', 'Group', 'Overall Rate', 'Count']
                        cursor = g.conn.execute('''SELECT DISTINCT S.year, S.tperson, S.rate, S.count
                                                    FROM Suicides S
                                                    WHERE S.sid LIKE '%%all%%' OR S.sid LIKE '%%na%%'
                                                    AND S.year >= (%s) 
                                                    AND S.year <= (%s)
                                                    ORDER BY S.year DESC, S.rate DESC
                                                    AND S.rate >= (%s)
                                                    ''', year1,year2, rate)
                        for result in cursor:
                            methods.append(result) 
                        cursor.close()
                        
                    elif rate =='':
                        error = 'Please enter a rate or check "Show Method of Suicide". Thanks!'
                        return render_template("methods.html", error=error)
            elif showmil != 'on':
                if showmethod =='on':
                    if rate !='':
                        headings =['Year', 'Overall Rate', 'Group', 'Count', 'Method']
                        cursor = g.conn.execute('''SELECT DISTINCT S.year, S.rate, S.tperson, M.total, M.method
                                                    FROM Suicides S, Death_by M
                                                    WHERE s.sid IN (SELECT m1.sid
                                                                    FROM Death_by M1
                                                                    WHERE m1.sid LIKE '%%na%%')
                                                    AND S.year >= (%s) 
                                                    AND S.year <= (%s)
                                                    AND s.sid = m.sid
                                                    AND S.rate >= (%s)
                                                    ORDER BY S.year DESC, S.tperson, M.total DESC
                                                    ''', year1,year2, rate)
                        for result in cursor:
                            methods.append(result) 
                        cursor.close()
                        
                    elif rate =='':
                        headings =['Year', 'Overall Rate', 'Group', 'Count', 'Method']
                        cursor = g.conn.execute('''SELECT DISTINCT S.year, S.rate, S.tperson, M.total, M.method
                                                    FROM Suicides S, Death_by M
                                                    WHERE s.sid IN (SELECT m1.sid
                                                                    FROM Death_by M1
                                                                    WHERE m1.sid LIKE '%%na%%')
                                                    AND s.sid = m.sid
                                                    ORDER BY S.year DESC, S.tperson, M.total DESC
                                                    ''', year1,year2)
                        for result in cursor:
                            methods.append(result) 
                        cursor.close()
                        
                elif showmethod !='on':
                    if rate != '':
                        headings =['Year', 'Group', 'Overall Rate', 'Count']
                        cursor = g.conn.execute('''SELECT DISTINCT S.year, S.tperson, S.rate, S.count
                                                    FROM Suicides S
                                                    WHERE S.sid LIKE '%%na%%'
                                                    AND S.year >= (%s) 
                                                    AND S.year <= (%s)
                                                    AND S.rate >= (%s)
                                                    ORDER BY S.year DESC, S.rate DESC
                                                    ''', year1,year2, rate)
                        for result in cursor:
                            methods.append(result) 
                        cursor.close()
                        
                    elif rate =='':
                        error = 'Please enter a rate or check "Show Method of Suicide". Thanks!'
                        return render_template("methods.html", error=error)
                    
                    
        elif showvet != 'on':
            if showmil == 'on':
                if showmethod =='on':
                    if rate !='':
                        headings =['Year', 'Overall Rate', 'Group', 'Count', 'Method']
                        cursor = g.conn.execute('''SELECT DISTINCT S.year, S.rate, S.tperson, M.total, M.method
                                                    FROM Suicides S, Death_by M
                                                    WHERE s.sid IN (SELECT m1.sid
                                                                    FROM Death_by M1
                                                                    WHERE m1.sid LIKE '%%all%%'
                                                                    OR m1.sid LIKE 'c%%na%%')
                                                    AND S.year >= (%s) 
                                                    AND S.year <= (%s)
                                                    AND s.sid = m.sid
                                                    AND S.rate >= (%s)
                                                    ORDER BY S.year DESC, S.tperson, M.total DESC
                                                    ''', year1,year2,rate)
                        for result in cursor:
                            methods.append(result) 
                        cursor.close()
                        
                    elif rate =='':
                        headings =['Year', 'Overall Rate', 'Group', 'Count', 'Method']
                        cursor = g.conn.execute('''SELECT DISTINCT S.year, S.rate, S.tperson, M.total, M.method
                                                    FROM Suicides S, Death_by M
                                                    WHERE s.sid IN (SELECT m1.sid
                                                                    FROM Death_by M1
                                                                    WHERE m1.sid LIKE '%%all%%'
                                                                    OR m1.sid LIKE 'c%%na%%')
                                                    AND s.sid = m.sid
                                                    ORDER BY S.year DESC, S.tperson, M.total DESC
                                                    ''', year1,year2)
                        for result in cursor:
                            methods.append(result) 
                        cursor.close()
                        
                elif showmethod !='on':
                    if rate != '':
                        headings =['Year', 'Group', 'Overall Rate', 'Count']
                        cursor = g.conn.execute('''SELECT DISTINCT S.year, S.tperson, S.rate, S.count
                                                    FROM Suicides S
                                                    WHERE S.sid LIKE '%%all%%' OR S.sid LIKE 'c%%na%%'
                                                    AND S.year >= (%s) 
                                                    AND S.year <= (%s)
                                                    AND S.rate >= (%s)
                                                    ORDER BY S.year DESC, S.rate DESC
                                                    ''', year1,year2,rate)
                        for result in cursor:
                            methods.append(result) 
                        cursor.close()
                        
                    elif rate =='':
                        error = 'Please enter a rate or check "Show Method of Suicide". Thanks!'
                        return render_template("methods.html", error=error)
            elif showmil != 'on':
                if showmethod =='on':
                    if rate !='':
                        headings =['Year', 'Overall Rate', 'Group', 'Count', 'Method']
                        cursor = g.conn.execute('''SELECT DISTINCT S.year, S.rate, S.tperson, M.total, M.method
                                                    FROM Suicides S, Death_by M
                                                    WHERE s.sid IN (SELECT m1.sid
                                                                    FROM Death_by M1
                                                                    WHERE m1.sid LIKE 'c%%na%%')
                                                    AND S.year >= (%s) 
                                                    AND S.year <= (%s)
                                                    AND s.sid = m.sid
                                                    AND S.rate >= (%s)
                                                    ORDER BY S.year DESC, S.tperson, M.total DESC
                                                    ''', year1,year2,rate)
                        for result in cursor:
                            methods.append(result) 
                        cursor.close()
                        
                    elif rate =='':
                        headings =['Year', 'Overall Rate', 'Group', 'Count', 'Method']
                        cursor = g.conn.execute('''SELECT DISTINCT S.year, S.rate, S.tperson, M.total, M.method
                                                    FROM Suicides S, Death_by M
                                                    WHERE s.sid IN (SELECT m1.sid
                                                                    FROM Death_by M1
                                                                    WHERE m1.sid LIKE 'c%%na%%')
                                                    AND s.sid = m.sid
                                                    ORDER BY S.year DESC, S.tperson, M.total DESC
                                                    ''', year1,year2)
                        for result in cursor:
                            methods.append(result) 
                        cursor.close()
                        
                elif showmethod !='on':
                    if rate != '':
                        headings =['Year', 'Group', 'Overall Rate', 'Count']
                        cursor = g.conn.execute('''SELECT DISTINCT S.year, S.tperson, S.rate, S.count
                                                    FROM Suicides S
                                                    WHERE S.sid LIKE 'c%%na%%'
                                                    AND S.year >= (%s) 
                                                    AND S.year <= (%s)
                                                    AND S.rate >= (%s)
                                                    ORDER BY S.year DESC, S.rate DESC
                                                    ''', year1,year2,rate)
                        for result in cursor:
                            methods.append(result) 
                        cursor.close()
                        
                    elif rate =='':
                        error = 'Please enter a rate or check "Show Method of Suicide". Thanks!'
                        return render_template("methods.html", error=error)
    if showciv !='on':
        if showvet == 'on':
            if showmil == 'on':
                if showmethod =='on':
                    if rate !='':
                        headings =['Year', 'Overall Rate', 'Group', 'Count', 'Method']
                        cursor = g.conn.execute('''SELECT DISTINCT S.year, S.rate, S.tperson, M.total, M.method
                                                    FROM Suicides S, Death_by M
                                                    WHERE s.sid IN (SELECT m1.sid
                                                                    FROM Death_by M1
                                                                    WHERE m1.sid LIKE '%%all%%'
                                                                    OR m1.sid LIKE 'v%%na%%')
                                                    AND S.year >= (%s) 
                                                    AND S.year <= (%s)
                                                    AND s.sid = m.sid
                                                    AND S.rate >= (%s)
                                                    ORDER BY S.year DESC, S.tperson, M.total DESC
                                                    ''', year1,year2,rate)
                        for result in cursor:
                            methods.append(result) 
                        cursor.close()
                        
                    elif rate =='':
                        headings =['Year', 'Overall Rate', 'Group', 'Count', 'Method']
                        cursor = g.conn.execute('''SELECT DISTINCT S.year, S.rate, S.tperson, M.total, M.method
                                                    FROM Suicides S, Death_by M
                                                    WHERE s.sid IN (SELECT m1.sid
                                                                    FROM Death_by M1
                                                                    WHERE m1.sid LIKE '%%all%%'
                                                                    OR m1.sid LIKE 'v%%na%%')
                                                    AND s.sid = m.sid
                                                    ORDER BY S.year DESC, S.tperson, M.total DESC
                                                    ''', year1,year2)
                        for result in cursor:
                            methods.append(result) 
                        cursor.close()
                        
                elif showmethod !='on':
                    if rate != '':
                        headings =['Year', 'Group', 'Overall Rate', 'Count']
                        cursor = g.conn.execute('''SELECT DISTINCT S.year, S.tperson, S.rate, S.count
                                                    FROM Suicides S
                                                    WHERE S.sid LIKE '%%all%%' OR S.sid LIKE 'v%%na%%'
                                                    AND S.year >= (%s) 
                                                    AND S.year <= (%s)
                                                    AND S.rate >= (%s)
                                                    ORDER BY S.year DESC, S.rate DESC
                                                    ''', year1,year2,rate)
                        for result in cursor:
                            methods.append(result) 
                        cursor.close()
                        
                    elif rate =='':
                        error = 'Please enter a rate or check "Show Method of Suicide". Thanks!'
                        return render_template("methods.html", error=error)
            elif showmil != 'on':
                if showmethod =='on':
                    if rate !='':
                        headings =['Year', 'Overall Rate', 'Group', 'Count', 'Method']
                        cursor = g.conn.execute('''SELECT DISTINCT S.year, S.rate, S.tperson, M.total, M.method
                                                    FROM Suicides S, Death_by M
                                                    WHERE s.sid IN (SELECT m1.sid
                                                                    FROM Death_by M1
                                                                    WHERE m1.sid LIKE 'v%%na%%')
                                                    AND S.year >= (%s) 
                                                    AND S.year <= (%s)
                                                    AND s.sid = m.sid
                                                    AND S.rate >= (%s)
                                                    ORDER BY S.year DESC, S.tperson, M.total DESC
                                                    ''', year1,year2,rate)
                        for result in cursor:
                            methods.append(result) 
                        cursor.close()
                        
                    elif rate =='':
                        headings =['Year', 'Overall Rate', 'Group', 'Count', 'Method']
                        cursor = g.conn.execute('''SELECT DISTINCT S.year, S.rate, S.tperson, M.total, M.method
                                                    FROM Suicides S, Death_by M
                                                    WHERE s.sid IN (SELECT m1.sid
                                                                    FROM Death_by M1
                                                                    WHERE m1.sid LIKE 'v%%na%%')
                                                    AND s.sid = m.sid
                                                    ORDER BY S.year DESC, S.tperson, M.total DESC
                                                    ''', year1,year2)
                        for result in cursor:
                            methods.append(result) 
                        cursor.close()
                        
                elif showmethod !='on':
                    if rate != '':
                        headings =['Year', 'Group', 'Overall Rate', 'Count']
                        cursor = g.conn.execute('''SELECT DISTINCT S.year, S.tperson, S.rate, S.count
                                                    FROM Suicides S
                                                    WHERE S.sid LIKE 'v%%na%%'
                                                    AND S.year >= (%s) 
                                                    AND S.year <= (%s)
                                                    AND S.rate >= (%s)
                                                    ORDER BY S.year DESC, S.rate DESC
                                                    ''', year1,year2,rate)
                        for result in cursor:
                            methods.append(result) 
                        cursor.close()
                        
                    elif rate =='':
                        error = 'Please enter a rate or check "Show Method of Suicide". Thanks!'
                        return render_template("methods.html", error=error)
                    
                    
        elif showvet != 'on':
            if showmil == 'on':
                if showmethod =='on':
                    if rate !='':
                        headings =['Year', 'Overall Rate', 'Group', 'Count', 'Method']
                        cursor = g.conn.execute('''SELECT DISTINCT S.year, S.rate, S.tperson, M.total, M.method
                                                    FROM Suicides S, Death_by M
                                                    WHERE s.sid IN (SELECT m1.sid
                                                                    FROM Death_by M1
                                                                    WHERE m1.sid LIKE '%%all%%')
                                                    AND S.year >= (%s) 
                                                    AND S.year <= (%s)
                                                    AND s.sid = m.sid
                                                    AND S.rate >= (%s)
                                                    ORDER BY S.year DESC, S.tperson, M.total DESC
                                                    ''', year1,year2,rate)
                        for result in cursor:
                            methods.append(result) 
                        cursor.close()
                        
                    elif rate =='':
                        headings =['Year', 'Overall Rate', 'Group', 'Count', 'Method']
                        cursor = g.conn.execute('''SELECT DISTINCT S.year, S.rate, S.tperson, M.total, M.method
                                                    FROM Suicides S, Death_by M
                                                    WHERE s.sid IN (SELECT m1.sid
                                                                    FROM Death_by M1
                                                                    WHERE m1.sid LIKE '%%all%%')
                                                    AND s.sid = m.sid
                                                    ORDER BY S.year DESC, S.tperson, M.total DESC
                                                    ''', year1,year2)
                        for result in cursor:
                            methods.append(result) 
                        cursor.close()
                        
                elif showmethod !='on':
                    if rate != '':
                        headings =['Year', 'Group', 'Overall Rate', 'Count']
                        cursor = g.conn.execute('''SELECT DISTINCT S.year, S.tperson, S.rate, S.count
                                                    FROM Suicides S
                                                    WHERE S.sid LIKE '%%all%%'
                                                    AND S.year >= (%s) 
                                                    AND S.year <= (%s)
                                                    AND S.rate >= (%s)
                                                    ORDER BY S.year DESC, S.rate DESC
                                                    ''', year1,year2,rate)
                        for result in cursor:
                            methods.append(result) 
                        cursor.close()
                        
                    elif rate =='':
                        error = 'Please make at least one selection'
                        return render_template("methods.html", error=error)
            elif showmil != 'on':
                error = 'Please enter a rate or check "Show Method of Suicide". Thanks!'
                return render_template("methods.html", error=error)
                    
            

    context = dict(methods = methods)
    print(context, " context")

    return render_template("methods.html", headings=headings, **context)




###########CLASS CODE BELOW - DO NOT TOUCH######## 

@app.route('/login')
def login():
    abort(401)
    this_is_never_executed()


if __name__ == "__main__":
  import click

  @click.command()
  @click.option('--debug', is_flag=True)
  @click.option('--threaded', is_flag=True)
  @click.argument('HOST', default='0.0.0.0')
  @click.argument('PORT', default=8111, type=int)
  def run(debug, threaded, host, port):
    """
    This function handles command line parameters.
    Run the server using:

        python server.py

    Show the help text using:

        python server.py --help

    """

    HOST, PORT = host, port
    print("running on %s:%d" % (HOST, PORT))
    app.run(host=HOST, port=PORT, debug=debug, threaded=threaded)

  run()
