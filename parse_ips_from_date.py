import sys
import os
import json

time_format = 'YYYY-MM-DDTHH:MM:SS'

def check_time_format(t):
    splt = t.split('T')
    if len(splt) != 2:
        return False
    attrs = splt[0].split('-') + splt[1].split(':')
    for attr in attrs:
        try:
            int(attr)
        except Exception as e:
            print(e)
            return False
    return True

def is_earlier_than(t1, t2):
    """Returns true if t1 is earlier than t2"""
    splt1 = t1.split('T')
    splt2 = t2.split('T')
    attrs1 = splt1[0].split('-') + splt1[1].split(':')
    attrs2 = splt2[0].split('-') + splt2[1].split(':')
    for i in range(len(attrs1)):
        if attrs1[i] == attrs2[i]:
            continue
        if attrs1[i] < attrs2[i]:
            return True
        else:
            return False
    return False


if __name__ == '__main__':
    
    os.system('heroku logs --app saroyr-com -n 1500 > site_logs.txt')

    try:
        with open('site_logs.txt', 'r') as f:
            log_lines = f.readlines()
    except Exception as e:
        print(e)
        sys.exit()

    # dict that counts the number of times an IP address occurs in the logs
    ip_dict = {}
    last_time_updated = log_lines[0][:len(time_format)]

    try:
        with open('ips.txt', 'r') as g:
            ip_info = json.load(g)
            ip_dict = ip_info['ip_dict']
            last_time_updated = ip_info['last_time_updated']
    except Exception as e:
        print(e)

    for line in log_lines:
        
        current_time = line[:len(time_format)]
        if is_earlier_than(current_time, last_time_updated):
            continue

        # we are interested only in lines having heroku[router]
        if line.find('heroku[router]') == -1:
            continue

        fwd_splt = line.split('fwd=')
        ip = fwd_splt[1].split('"')[1].split(', ')[0]

        if ip in ip_dict.keys():
            ip_dict[ip] += 1
        else:
            ip_dict[ip] = 1

    ip_dict = dict(sorted(ip_dict.items()))

    last_time_updated = log_lines[-1][:len(time_format)]
    ip_info = {
        'last_time_updated': last_time_updated,
        'ip_dict': ip_dict
    }

    with open('ips.txt', 'w+') as g:
        json.dump(ip_info, g, indent=4)

    print('Done')
