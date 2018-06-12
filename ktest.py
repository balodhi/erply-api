#!/usr/bin/env python
import threading, logging, time
import multiprocessing
from kafka import KafkaConsumer, KafkaProducer
import eapi


class Producer(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.stop_event = threading.Event()
        
    def stop(self):
        self.stop_event.set()

    def run(self):
        producer = KafkaProducer(bootstrap_servers='localhost:9092')

        while not self.stop_event.is_set():
            producer.send('my-topic', key=str.encode('key_{}'.format(i)), value = b"test")
            time.sleep(10)

        producer.close()

class Consumer(multiprocessing.Process):
    def __init__(self):
        multiprocessing.Process.__init__(self)
        self.stop_event = multiprocessing.Event()
        self.eap = eapi.EAPI(url='https://500238.erply.com/api/',clientCode='500238',username='balodhi@gmail.com',password='testpassword123!@#',sslCACertPath=None)
        
    def stop(self):
        self.stop_event.set()
        
    def run(self):
        consumer = KafkaConsumer(bootstrap_servers='localhost:9092',
                                 auto_offset_reset='earliest',
                                 consumer_timeout_ms=1000)
        consumer.subscribe(['my-topic'])

        while not self.stop_event.is_set():
            for message in consumer:
                res = self.searchProduct(self.eap, message)
                if not res['records']:
                    print("there is not product found. Adding now")
                    self.addProduct(self.eap,message)
                if self.stop_event.is_set():
                    break

        consumer.close()
    def addProduct(self,handle,productName):
        params = {  'groupID':1 ,
                    'name': productName
                }
        result = handle.sendRequest('saveProduct',params)
        results = result.json()
        if (results['status']['responseStatus']=='ok'):
            res = self.searchProduct(handle,productName)
            print('Product ',productName, ' Successfull added. with id = ',str(res['records'][0]['productID']))
        else:
            print("There is some problem in adding the product")
        return res

    def deleteProduct(self,handle,productID):
        params = {  'productID':productID 
                    
                }
        result = handle.sendRequest('deleteProduct',params)
        results = result.json()
        print(results)
        if (results['status']['responseStatus']=='ok'):
            print("product successfully deleted")
        else:
            print("There is some problem in deleting the product")

    def searchProduct(self,handle,productName):
        params = {  'findBestMatch':1 ,
                    'name': productName
                }
        result = handle.sendRequest('getProducts',params)
        results = result.json()
        return results
        
        
def main():
    tasks = [
        Producer(),
        Consumer()
    ]

    for t in tasks:
        t.start()

    time.sleep(10)
    
    for task in tasks:
        task.stop()

    for task in tasks:
        task.join()
        
        
if __name__ == "__main__":
    logging.basicConfig(
        format='%(asctime)s.%(msecs)s:%(name)s:%(thread)d:%(levelname)s:%(process)d:%(message)s',
        level=logging.INFO
        )
    main()