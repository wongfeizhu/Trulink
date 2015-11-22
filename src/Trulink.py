'''
@author: l3og3tz l3og3tz@gmail.com
@version: Dec 28, 2013
@author Wong Fei Zhu



'''
import urllib2
import urllib
import re
from optparse import OptionParser
import subprocess
import sys

def print_logo():
    '''
    Draws logo
    '''
    
    if("windows" in sys.platform.lower()):
        subprocess.call(["cls"])
    elif ("linux" or "unix" in sys.platform.lower()):
        subprocess.call(["clear"])

    print """
    
    ********************************************
    *    _____          _     _       _        *
    *   |_   _|        | |   (_)     | |       *
    *     | |_ __ _   _| |    _ _ __ | | __    *
    *     | | '__| | | | |   | | '_ \| |/ /    *
    *     | | |  | |_| | |___| | | | |   <     *
    *     \_/_|   \__,_\_____/_|_| |_|_|\_\    *
    *                                          *
    *             by l3og3tz                   * 
    *       For the Top-Hat-Sec Family         *
    *          Click Your Links Wisely :)      *
    ********************************************
    
    """
    

def printTrueLink(short_link, response):
    '''
    Prints the true link for shortened
    '''
    target = 'resultURL2"><a href="'  # enables extraction of the link from the HTML results page returned
    
    for line in response.readlines():  # iterating through HTML lines
        # print line  # was just for  debug purposes
        
        if target in line:  # searching for target string
            the_true_url = re.search(r'resultURL2"><a href="[\'"]?([^\'" >]+)', line)  # search the line and extract true link URL
            if the_true_url:  # if a URL is found print
                print "Short Link : {0}".format(short_link)
                print "True Link  : {0}".format(the_true_url.group(0).split(target)[1])
                print ""         
            
def find_trulink(short_link, url="http://urlxray.com/display.php", user_agent='Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'):
    '''
    Finds the true link for the specified shortened link
    '''
    headers = { 'Host' : 'urlxray.com',
           'User-Agent' : user_agent,
           'DNT' : 1,
           'Connection' : 'keep-alive' }
    data = {}
    data['url'] = short_link

    url_values = urllib.urlencode(data)

    full_url = url + '?' + url_values
    my_get_request = urllib2.Request(full_url, None, headers)
    response = urllib2.urlopen(my_get_request)
    printTrueLink(short_link, response)  # print the true link

def open_links_file(the_links_file):
    try:
        my_pass_file = open(the_links_file)
        print ("[+] Successfully opened short links file ""{0}"" for reading...".format(the_links_file))
        return my_pass_file
    except IOError as ioerror:
        print ("[-] {}".format(ioerror)) 
            
def main():  # main, starts program
    '''
    Runs main.
    '''
    print_logo()
    
    parser = OptionParser("usage%prog -l <short link> -f <short link file>\n")  # Command line options required for execution.
    parser.add_option("-l", "--shortlink", dest="short_link", type="string", help="Specify the shortened link")
    parser.add_option("-f", "--shortlinkfile", dest="shortlink_file", type="string", help="Specify a file containing list of shortened link(1 each line")
    options, args = parser.parse_args()
    
    # exits program and displays user info if the right number of arguments are not provided.
    if(options.short_link == None) and (options.shortlink_file == None): 
        print (parser.usage)
        exit(0)
    elif(options.short_link) and (options.shortlink_file): 
        print (parser.usage)
        print "You need to use either the single link option or file option, please don't combine them"
        exit(0)
    elif(options.short_link) and (options.shortlink_file == None): 
        find_trulink(options.short_link)
    else:  # continues with normal execution
        links_file = open_links_file(options.shortlink_file)
        if(links_file):                
            # print ("Successfully opened file.")
            for line in links_file.readlines():
                
                line = line.strip("\n")
                find_trulink(short_link=line)
                # print ""
        try:
            links_file.close()
        except IOError as ioerror:
            print(ioerror) 
        return 
    


main()
        

