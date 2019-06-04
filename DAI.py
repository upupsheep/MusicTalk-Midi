import time, DAN, requests, random

ServerURL = 'https://test.iottalk.tw'  #with no secure connection
#ServerURL = 'https://DomainName' #with SSL connection
Reg_addr = None  #if None, Reg_addr = MAC address

DAN.profile['dm_name'] = 'Dummy_Device'
DAN.profile['df_list'] = ['Dummy_Sensor', 'Dummy_Control']
#DAN.profile['df_list'] = ['Sandy_I', 'Sandy_O']
DAN.profile['d_name'] = None  # None for autoNaming
DAN.device_registration_with_retry(ServerURL, Reg_addr)

tag = 0
cnt = 0
sum_delay = 0
#now_time = 0

while True:
    try:
        #Pull data from a device feature called "Dummy_Control"
        value1 = DAN.pull('Dummy_Control')
        #value1 = DAN.pull('Sandy_O')
        # if value1[0] > 0:
        #     print(value1[0])
        if cnt > 100:
            print("result delay:")
            print(sum_delay / 100)
        if value1 != None and cnt <= 100:
            cnt = cnt + 1
            # print(value1)
            print("now delay: ")
            delay = time.time() - value1[0]
            sum_delay = sum_delay + delay
            print(delay)

        #Push data to a device feature called "Dummy_Sensor"
        # value2 = random.uniform(1, 10)
        now_time = time.time()
        #print(now_time)
        #DAN.push('Dummy_Sensor', value2, value2)
        DAN.push('Dummy_Sensor', now_time)
        #print(now_time)
        #DAN.push('Sandy_I', value2, value2)

    except Exception as e:
        print(e)
        if str(e).find('mac_addr not found:') != -1:
            print('Reg_addr is not found. Try to re-register...')
            DAN.device_registration_with_retry(ServerURL, Reg_addr)
        else:
            print('Connection failed due to unknow reasons.')
            time.sleep(1)

    #time.sleep(0.2)