import re
import socket
import smtplib
import dns.resolver
import pandas as pd
import time
import multiprocessing
import dns

fromAddress = 'govind@t-hub.co'

regex = '^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$'

def syntax_validator(inputAddress):
    addressToVerify = str(inputAddress)
    match = re.match(regex, addressToVerify)
    if match == None:
        message = 'Bad Syntax'
    else:
        message = 'Valid'
        
    return message

def mx_record_check(addressToVerify):
        
    splitAddress = addressToVerify.split('@')
    domain = str(splitAddress[1])
    
    try:
        records = dns.resolver.query(domain, 'MX')
        mxRecord = records[0].exchange
        mxRecord = str(mxRecord)
        
        message = 'Domain exists'
        
    except dns.resolver.NXDOMAIN:
        message = 'Domain does not exist.'
    
    return message, mxRecord

def smtp_check(addressToVerify,mxRecord):

    host = socket.gethostname()
    
    server = smtplib.SMTP()
    server.set_debuglevel(2)
    
    server.connect(mxRecord)
    server.helo(host)
    server.mail(fromAddress)
    code, message = server.rcpt(str(addressToVerify))
    server.quit()
    
    if code == 250:
        message = 'Success'
    else:
        message = 'Bad'
        
    return message

def worker(df,q):
    print 'worker:', q
    data = df
    for i in list(data.index.values):
            email = data.emails[i]
            test = syntax_validator(email)
            
            if test == 'Valid':
                mx = mx_record_check(email)
                
                if mx[0] == 'Domain exists':
                    start_time = time.time()
                    smtp = smtp_check(email, mx[1])
                    print "time taken", time.time() - start_time
                    print 'worker: ', q, ' starttime', start_time
                    if smtp == 'Success':
                        data.validity[data.emails == email] = 1
                        print email
                    else:
                        data.validity[data.emails == email] = 0
                        print email
                        
                else:
                    data.validity[data.emails == email] = 0
                    print email
            else:
                data.validity[data.emails == email] = 0
                print email
                
                
    name = 'data' + str(q) + '.csv'
    print 'Job' + '' + str(q) + '' + 'done'
    return data.to_csv(name)
 
    
    
data = pd.read_csv('email.csv', nrows=160)


if __name__ == '__main__':
    jobs = []
    k = 16
    for q in range(k):
        df = data.iloc[(q)*len(data)/k:(q+1)*len(data)/k]
        p = multiprocessing.Process(target=worker, args=(df, q))
        jobs.append(p)
        print 'start process id:', p._identity
        p.start()





