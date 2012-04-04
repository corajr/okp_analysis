from forum.models import *
import pytz
from pytz import timezone
import sys
from bs4 import BeautifulSoup
import re, datetime

page = open('okp_tidy.html')
pageSource = page.read()
page.close()
#soup = BeautifulSoup(pageSource, 'html.parser')
soup = BeautifulSoup(pageSource, 'html.parser')

alltables = soup.find_all("table", {"cellspacing": "1", "cellpadding": "3"})

# compile regular expressions

eastern = timezone('US/Eastern')

_u_id_re = re.compile("u_id=([0-9]*)")
_since_re = re.compile(".*([A-z]{3} [0-9]{2})[A-z]{2}( [0-9]{4})")
_responding_to_re = re.compile("#([0-9]*)")
_mesg_num_re = re.compile("([0-9]*)\\. ")

for table in alltables:
    try:
        _header = table.find_all("span", "dcauthorinfo")    
        # message info
        _mesg_id = int(table.find("a").get('name'))
        _posting_time = table.find("span", "dcdate").get_text()
        _date_time = datetime.datetime.strptime(_posting_time, "%a %b-%d-%y %I:%M %p")
        _date_time = _date_time.replace(tzinfo=eastern) #.astimezone(utc)
        # user info
        author_link = table.find("a", "dcauthorlink")
        _name = author_link.string
        _profile_url = author_link.get('href')
        _u_id = _u_id_re.search(_profile_url).group(1)
        _since = _header[0].string
        _since = re.sub(_since_re, "\\1\\2", _since)
        if _since == "Charter member":
            _since = "Jan 01 2000"
        _member_since = datetime.datetime.strptime(_since, "%b %d %Y")
        _member_since = _member_since.replace(tzinfo=eastern) #.astimezone(utc)
        
        
        if author_link.next_sibling != None:
            if "team_icon" in author_link.next_sibling.get("src"):
                _okp_team = True
        else:
            _okp_team = False
    
        _avatar = table.find("img", {"height": 60})
        if _avatar != None:
            _avatar_url = _avatar.get("src")
        else:
            _avatar_url = ""
        
        _posts = int(_header[1].get_text().split()[0])
        
        _subject = table.find("td", {"class": "dclite", "colspan": "2"}).find("strong").get_text()
        _mesg_num = _mesg_num_re.match(_subject)
        if _mesg_num != None:
            _mesg_num = int(_mesg_num.group(1))
        else:
            _mesg_num = 0
        _subject = re.sub(_mesg_num_re, "", _subject)[1:-1].replace("\n"," ")
        
        _message_body = table.find_all("p", "dcmessage")
        _text = _message_body[0].get_text()
        if len(_message_body) > 1:
            _signature = _message_body[1].get_text()
        else:
            _signature = ""
            
        if len(_header) > 2:
            _responding_to_link = _header[2].find("a").get("href")
            _responding_to = int(_responding_to_re.search(_responding_to_link).group(1))
        else:
            _responding_to = 0
        
        if not Author.objects.filter(u_id = _u_id).exists():
            a = Author(name = _name,
                u_id = _u_id,
                posts = _posts,
                okp_team = _okp_team,
                member_since = _member_since,
                profile_url = _profile_url,
                avatar_url = _avatar_url)
            a.save()
            print "Added author " + _name
        else:
            a = Author.objects.get(u_id = _u_id)
     
        if not Message.objects.filter(mesg_id = _mesg_id).exists():
            message = Message(mesg_id = _mesg_id,
                                mesg_num = _mesg_num,
                                date_time = _date_time,
                                subject = _subject,
                                author = a,
                                text = _text,
                                signature = _signature)
            if _responding_to != 0:
                message.responding_to = Message.objects.get(mesg_id = _responding_to)
            message.save()
            print "Added message " + str(_mesg_id)
    except:
        print "***PROBLEM***", sys.exc_info()[0]
        if type(_mesg_id) == int:
            print _mesg_id
    
#    print _name, _u_id, _posts, _okp_team, _member_since, _profile_url, _avatar_url
#    print _mesg_id, _mesg_num, _date_time, _subject, _name, _responding_to, _text, _signature