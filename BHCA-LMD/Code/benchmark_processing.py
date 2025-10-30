# Need: Delay time per task
# Have:
#   1. Allocated worker ID --> worker speed --> travelling distance to allocated task
#   2. Expected Arrival time per task
# Problem: Commulative delay for multiple task allocation per worker, we need actual arrival time for processed tasks in sequence.

import pandas as pd
#import xlrd
# Get Data from csv
data = pd.read_excel(r'C:/Users/israa/OneDrive/Desktop/Blockchain simulation results - with thresholds.xlsx', sheet_name='data')

tasksData = pd.DataFrame(data[['x', 'y', 'Assigned worker', 'Assigned worker speed','Actual Delivery Time', 'submission time', 'ETA']]).dropna()
tasksData.insert(0, 'task_id', range(0, len(tasksData)))
tasksData['real delivery time'] = 0
tasksData['delay'] = 0

# duration of delivery is = actual arrival time - submission time
# the duration is accumulated to get the real delivery time
# Group tasks per worker ID
# sort tasks
# accumulate time

assignedWorkerIds = tasksData['Assigned worker'].unique()

for id in assignedWorkerIds:
    if id == 0:
        continue
    
    workerTasks = tasksData.loc[tasksData['Assigned worker'] == id, 'task_id']
    workerTasks = sorted(workerTasks)

    # print(f"worker id: {id}")
    # print(workerTasks)
    time = tasksData.loc[tasksData['task_id']==workerTasks[0],'submission time'].tolist()[0] # starting time of worker's first task

    # print(f"starting time: {time}")
    firstTaskFlag = 1
    previousTaskId = -1
    for t in workerTasks:
        if firstTaskFlag: ## starting from working coordinates
            time -= tasksData.loc[tasksData['task_id']==t,'submission time'].tolist()[0]
            time = time + tasksData.loc[tasksData['task_id']==t,'Actual Delivery Time'].tolist()[0]

        else: ## starting from last completed task coordinates
            # print(f"previous:{previousTaskId}")
            # print(f"current: {t}")

            x1 = tasksData.loc[tasksData['task_id']==previousTaskId,'x'].tolist()[0] ## previous task coords
            y1 = tasksData.loc[tasksData['task_id']==previousTaskId,'x'].tolist()[0]
            x2 = tasksData.loc[tasksData['task_id']==t,'y'].tolist()[0] ## current task coords
            y2 = tasksData.loc[tasksData['task_id']==t,'y'].tolist()[0]

            speed = tasksData.loc[tasksData['task_id']==t,'Assigned worker speed'].tolist()[0] ## allocated worker speed

            distance = ((x1-x2)**2+(y1-y2)**2)**0.5
            newTime = distance/speed
            time = time + newTime

        tasksData.loc[tasksData['task_id']==t,'real delivery time'] = time
        tasksData.loc[tasksData['task_id']==t,'delay'] = tasksData.loc[tasksData['task_id']==t,'ETA'].tolist()[0] - tasksData.loc[tasksData['task_id']==t,'real delivery time'].tolist()[0]
        firstTaskFlag = 0
        previousTaskId = t

# print(f"finishing time: {time}")
print(tasksData.loc[(tasksData['delay']>-10) & (tasksData['delay']!=0),'delay'])

averageDelay5= tasksData.loc[(tasksData['delay']>=-5) & (tasksData['delay']!=0),'delay'].mean()
averageDelay10 = tasksData.loc[(tasksData['delay']>=-10) & (tasksData['delay']!=0),'delay'].mean()

countIf5 = len(tasksData.loc[(tasksData['delay']>=-5) & (tasksData['delay']!=0),'delay'])
countIf10 = len(tasksData.loc[(tasksData['delay']>=-10) & (tasksData['delay']!=0),'delay'])

total = 50
print("for 5 minute threshold:")
print(f"allocation: {countIf5/total} %")
print(f"delay: {averageDelay5}")

print("for 10 minute threshold:")
print(f"allocation: {countIf10/total} %")
print(f"delay: {averageDelay10}")


