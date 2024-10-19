
import requests
import json
#this project assumes, that a workload Id is started and stopped exactly once

url = "http://assessment:8080/v1/dataset"
response=requests.get(url)
responseAsJson=response.json()
data =responseAsJson
print(data)
dictornaryForCalculation={}
dictornaryTotal={}
# Dictionaries to hold the interim data
dictornaryForCalculation = {}  # To store ongoing workload timings (start times)
dictornaryTotal = {}  # To store the final aggregated runtimes per customer
arr=[]
data['events'] = sorted(data['events'], key=lambda x: x['timestamp'])
# Iterate over all the events
for i in data['events']:
    customer = i['customerId']
    workload = i['workloadId']
    timestamp = i['timestamp']
    eventType = i['eventType']
    arr.append(customer)
    # Check if customer is already part of the dictionary
    if customer not in dictornaryForCalculation:
        dictornaryForCalculation[customer] = {}  # Initialize new customer entry

    # Handle "start" and "stop" event types
    if eventType == "start":
        # Store the start time for the workload under the customer
        dictornaryForCalculation[customer][workload] = timestamp
    elif eventType == "stop":
        # Ensure there's a "start" before calculating the runtime
        if workload in dictornaryForCalculation[customer]:
            # Calculate the runtime by subtracting the start timestamp from the stop timestamp
            start_time = dictornaryForCalculation[customer][workload]
            runtime = timestamp - start_time

            # Add the runtime to the customer's total consumption
            if customer in dictornaryTotal:
                dictornaryTotal[customer] += runtime
            else:
                dictornaryTotal[customer] = runtime

            # Remove the workload from the ongoing calculations as it's completed
            del dictornaryForCalculation[customer][workload]

# Prepare the final result in the required format
print(len(arr))
print(len( list(set(arr))))
print
result = []
for customerId, consumption in dictornaryTotal.items():
    result.append({
        "customerId": customerId,
        "consumption": consumption
    })
#result.append({"customerId": "48fd2ca0-d253-4f0a-9ba5-4444a21966c0","consumption": 0})
print(len(result))
# Output the result
# Extracting the customer IDs from the result
result_customer_ids = [entry['customerId'] for entry in result]

# Finding missing IDs
missing_ids = set(list(set(arr))) - set(result_customer_ids)

# Output the missing IDs
resultDict={}
resultDict["result"]=result
resultAsJson=json.dumps(resultDict)
url= "http://assessment:8080/v1/result"
headers = {'Content-Type': 'application/json'}
request=requests.post(url=url,json=resultDict,headers=headers)
print("Response Text:", request.text)
