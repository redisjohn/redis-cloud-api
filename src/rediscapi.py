#!/usr/bin/python3

from re import sub
import sys, getopt, requests, json, platform

global apikeys
apikeys = None 

global keyfile
keyfile = 'keys.json'

global action
action = 'help'

global baseURL
baseURL = "https://api.redislabs.com/v1"

global subscriptionId
subscriptionid = None

global databaseId 
databaseId = None

global jsonfile 
jsonfile = None

global taskfile
taskfile = 'task.tmp' if platform.system() == 'Windows' else '/tmp/task.tmp'

def usage():
    print("\nrediscapi - A command line interface to the Redis Cloud API\n")
    print("usage: rediscapi.py -k {keys.json} | -x {action} | -f {jsonfile} ] | -s {subscriptionId} | -d {databaseId}")
    print("\n")
    print("where {action} is:\n")
    print("\tdata-persistence|cloud-accounts|payment-methods|")
    print("\taccount|users|modules|")
    print("\tcreate-subscription|subscriptions|delete-subscription|")
    print("\tdatabases|database-byid|create-database|update-database|")
    print("\tlogs|status|tasks\n")
    print("\nNotes:")
    print("\tYou must edit keys.json to include apikey and api-secret-key\n")
    print("\t-x {action} is closely matched to https://api.redislabs.com/v1/swagger-ui.html\n")
    print("\t-k {keys.json} can be used to specify a path to the json file\n")
    print("\t-f {jsonfile} a json request body\n\n")
    print("\tLong running requests return a 201 status code")
    print("\tWhen this happens the taskid is parsed from the response")
    print("\tand stored in a local file /tmp/task.tmp")
    print("\t-x status will read this file and gets the status of the last long running request")
    print("\nSome Examples:")
    print("\nCreating a subscription:\n")
    print("\t\trediscapi.py -x create-subscription -f create-sub.json")
    print("\nDelete a subscription:\n")
    print("\t\trediscapi.py -x delete-subscription -s 439429")
    print("\nCreating a Database:\n")
    print("\t\trediscapi.py -x create-database -f create-db.json")
    print("\nUpdate a Database:\n")
    print("\t\trediscapi.py -x update-database -s 439429 -d 46201 -f create-db.json")
    print("\nDelete a Database:\n")
    print("\t\trediscapi.py -x delete-database -s 439429 -d 46201")
    print("\nCheck the status of the task from the last long running request (201 response code)\n")
    print("\t\trediscapi.py -x status\n") 
    sys.exit(1)     

def check_subscription_id():
    if subscriptionid == None:
        print("-s {subscriptionId} required")
        sys.exit(2)

def check_database_id():
    if databaseId == None:
        print("-d {databaseId} required")
        sys.exit(2)

def process_keyfile():
    global apikeys
    try:
        f = open(keyfile)
        data = json.load(f)
        apikeys = {'x-api-key' : data['apikey'], 'x-api-secret-key' : data['secretkey']}
        f.close()
    except: 
        print("Invalid Key File")
        sys.exit(2)
    
    if apikeys is None:
        print("error: missing apikeys")
        sys.exit(1)

def process_jsonfile():
    if jsonfile is None:
        print("-f {jsonfile} is required")
        sys.exit(1)
    try:
        f = open(jsonfile)    
        data = json.load(f)
        f.close()
        return data
    except:
        print("Invalid Json File")
        sys.exit(1)

def save_task(data):
    print("task id:",data["taskId"])
    print("description:",data["description"])
    try:
        f = open(taskfile,'w')
        f.write(data["taskId"])
        f.close()
    except Exception as ex:
        print(ex)

def handle_action():
    match action:
        case 'help':
            usage()

        case 'data-persistence':
            data = process_get("/data-persistence")
            print(json.dumps(data, indent = 1))   

        case 'cloud-accounts':
            data = process_get("/cloud-accounts")
            print(json.dumps(data, indent = 1))     

        case 'tasks':
            data = process_get("/tasks")
            print(json.dumps(data, indent = 1)) 

        case 'users':
            data = process_get("/users")
            print(json.dumps(data, indent = 1)) 

        case 'modules':
            data = process_get("/database-modules")
            print(json.dumps(data, indent = 1)) 

        case 'logs':
            data = process_get("/logs")
            print(json.dumps(data, indent = 1)) 

        case 'subscriptions':
            data = process_get("/subscriptions")
            print(json.dumps(data, indent = 1)) 

        case 'account':
            data = process_get("")
            print(json.dumps(data, indent = 1)) 

        case 'payment-methods':
            data = process_get("/payment-methods")
            print(json.dumps(data, indent = 1)) 
            
        case 'create-subscription':
            payload = process_jsonfile()
            data = process_post("/subscriptions",payload)
            save_task(data)

        case 'delete-subscription':
            check_subscription_id()
            data = process_delete("/subscriptions/" + subscriptionid)
            save_task(data)

        case 'databases':
            check_subscription_id()
            data = process_get("/subscriptions/" + subscriptionid + "/databases")
            print(json.dumps(data, indent = 1)) 
        
        case 'database-byid':
            check_subscription_id()
            check_database_id()
            data = process_get("/subscriptions/" + subscriptionid + "/databases" + databaseId)
            print(json.dumps(data, indent = 1)) 

        case 'create-database':
            check_subscription_id()            
            payload = process_jsonfile()
            data = process_post("/subscriptions/" + subscriptionid + "/databases", payload)
            save_task(data)

        case 'update-database':
            check_subscription_id()
            check_database_id()
            payload = process_jsonfile()
            data = process_put("/subscriptions/" + subscriptionid + "/databases/" + databaseId, payload)
            save_task(data)

        case 'delete-database':
            check_subscription_id()
            check_database_id()
            data = process_delete("/subscriptions/" + subscriptionid + "/databases/" + databaseId)
            save_task(data)

        case 'status':
            try: 
                f = open(taskfile)
                task = f.read().rstrip()
                f.close()
            except Exception as ex:
                print(ex)
            data=process_get("/tasks/" + task)
            print(json.dumps(data, indent=1))

        case default:
            usage()

def process_get(request):
    try: 
        req = baseURL + request       
        response = requests.get(req,headers=apikeys)
        data = json.loads(response.content)
        return data
    except requests.exceptions.HTTPError as errh:
        print(errh)
        sys.exit(1)
    except requests.exceptions.ConnectionError as errc:
        print(errc)
        sys.exit(1)
    except requests.exceptions.Timeout as errt:
        print(errt)
        sys.exit(1)
    except requests.exceptions.RequestException as err:
        print(err)    
        sys.exit(1)
    except: 
        print("Status Code",response.status_code)
        sys.exit(1)


def process_delete(request):
    try: 
        req = baseURL + request       
        response = requests.delete(req,headers=apikeys)
        data = json.loads(response.content)
        return data
    except requests.exceptions.HTTPError as errh:
        print(errh)
        sys.exit(1)
    except requests.exceptions.ConnectionError as errc:
        print(errc)
        sys.exit(1)
    except requests.exceptions.Timeout as errt:
        print(errt)
        sys.exit(1)
    except requests.exceptions.RequestException as err:
        print(err)    
        sys.exit(1)
    except: 
        print("Status Code",response.status_code)
        sys.exit(1)
            
                    
def process_post(request,payload):    
    try: 
        req = baseURL + request
        response = requests.post(req,headers=apikeys,json=payload)
        data = json.loads(response.content)
        return data
    except requests.exceptions.HTTPError as errh:
        print(errh)
        sys.exit(1)
    except requests.exceptions.ConnectionError as errc:
        print(errc)
        sys.exit(1)
    except requests.exceptions.Timeout as errt:
        print(errt)
        sys.exit(1)
    except requests.exceptions.RequestException as err:
        print(err)    
        sys.exit(1)               
    except: 
        print("Status Code",response.status_code)
        sys.exit(1)

def process_put(request,payload):
    try: 
        req = baseURL + request
        response = requests.put(req,headers=apikeys,json=payload)
        data = json.loads(response.content)
        return data
    except requests.exceptions.HTTPError as errh:
        print(errh)
        sys.exit(1)
    except requests.exceptions.ConnectionError as errc:
        print(errc)
        sys.exit(1)
    except requests.exceptions.Timeout as errt:
        print(errt)
        sys.exit(1)
    except requests.exceptions.RequestException as err:
        print(err)    
        sys.exit(1)                    
    except: 
        print("Status Code",response.status_code)
        sys.exit(1)


def process_args(argv):
  global apikeys, keyfile, action, jsonfile, taskfile, databaseId, subscriptionid

  if (len(argv) == 0):
        usage()
        
  try:
    opts, args = getopt.getopt(argv,"hk:x:s:d:f:")
  except getopt.GetoptError:
    usage()

  for opt, arg in opts:
    if opt == '-k':
        keyfile = arg      
    elif opt == '-x':
      action = arg 
    elif opt == '-f':
        jsonfile = arg    
    elif opt == '-d':
        databaseId = arg
    elif opt == '-s':
        subscriptionid = arg
    elif opt == '-h':
        usage()

def main(argv):
    process_args(argv)
    process_keyfile()
    handle_action()
 
if __name__ == "__main__":
  main(sys.argv[1:])