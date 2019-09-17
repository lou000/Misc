import time
import traceback
import logging
from os import system

max_response = 0
avg_response = 0
counter = 0
last_long_resp = 0
long_resp_time = []
# sleepTime = int(input("Wprowadź okres prób dostępu w sekundach:"))
sleepTime = 2

launchTime = time.time()
while True:
    try:
        startTime = time.time()
        file = open("H:\\EWA.png", "r")
        file.close()
        endTime = time.time()
        lapsedTime = float('%.3f'%(endTime-startTime))
        avg_response = float('%.5f'%(((avg_response * counter)+lapsedTime)/(counter+1)))
        if lapsedTime>max_response :
            max_response=lapsedTime
        if lapsedTime>2:
            if last_long_resp == 0:
                long_resp_time.append([lapsedTime, 0])
            else:
                long_resp_time.append([lapsedTime, last_long_resp-time.time()])
            last_long_resp = time.time()
        system("cls")
        counter+=1
        print("Liczba pomiarów:", counter)
        print("Czas odpowiedzi:", lapsedTime, "[s]")
        print("Średni czas odp:", avg_response, "[s]")
        print("Max czas odp:   ", max_response, "[s]")
        print("Czas działania: ", '%.1f'%((time.time() - launchTime)/60), "[m]")
        print("\n")
        print("Najdłuższe pomiary | Czas od ostatniego długiego pomiaru:\n")
        for i in range(len(long_resp_time)):
            if long_resp_time[i][0]>10:
                print('%.3f'%long_resp_time[i][0],"[s]         |           ", '%.1f'%(long_resp_time[i][1]/60), "[m]")
            else:
                print('%.3f' % long_resp_time[i][0], "[s]          |           ", '%.1f' % (long_resp_time[i][1] / 60),
                      "[m]")
        time.sleep(sleepTime)

    except Exception as e:
        logging.error(traceback.format_exc())
    except:
        print("Unexpected error:", sys.exc_info()[0])