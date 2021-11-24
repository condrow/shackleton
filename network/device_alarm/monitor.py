from scapy.all import ARP, Ether, srp
from send_mail import Email
from scheduler import Schedule
import csv
import time
import datetime
import logging
import logging.handlers
import os
 
handler = logging.handlers.WatchedFileHandler(
    os.environ.get("LOGFILE", "monitor_app.log"))
formatter = logging.Formatter(logging.BASIC_FORMAT)
handler.setFormatter(formatter)
root = logging.getLogger()
root.setLevel(os.environ.get("LOGLEVEL", "INFO"))
root.addHandler(handler)
ignore_list = []


class DeviceSniff:

    def __init__(self):
        # IP Address for the destination
        self.target_ip = "192.168.68.1/24"
        # List of mac addresses to searh for
        self.device_mac_list = 'databas.csv'
        self.m1 = Email()

    def read_db(self):
        """Read a list of MAC addresses from our CSV"""
        try:
            with open(self.device_mac_list) as csv_file:
                csv_reader = csv.reader(csv_file, delimiter=',')
                line_count = 0
                db_list = []
                for row in csv_reader:
                    if line_count == 0:
                        line_count += 1
                    else:
                        line_count += 1
                        db_list.append(row[0])
        except Exception:
            logging.exception("[DeviceSniff][read_db]")
            #exit(1)
        print(f'Processed {line_count} lines from database')
        return db_list

    def find_devices(self):
        """Send a broadcast request to locate devices on the network"""
        try:            
            # create ARP packet
            arp = ARP(pdst=self.target_ip)
            # create the Ether broadcast packet
            # ff:ff:ff:ff:ff:ff MAC address indicates broadcasting
            ether = Ether(dst="ff:ff:ff:ff:ff:ff")
            # stack them
            packet = ether/arp
            result = srp(packet, timeout=5, verbose=0)[0]
            # a list of clients, we will fill this in the upcoming loop
            clients = []
            mac_client = []
            for sent, received in result:
                # for each response, append ip and mac address to `clients` list
                clients.append({'ip': received.psrc, 'mac': received.hwsrc})
                mac_client.append(received.hwsrc)
            print("Available devices in the network:")
            print("IP" + " "*18+"MAC")
            for client in clients:
                print("{:16}    {}".format(client['ip'], client['mac']))
        except Exception:
            logging.exception("[DeviceSniff][find_devices]")
        return mac_client

    def alarm_trigger(self, db_result, device_result):
        """Send an email alert if we find a device online"""
        try:
            for device in device_result:
                for db_mac in db_result:
                    if device == db_mac and device not in ignore_list:
                        print(f"Found: {device} matching {db_mac}")
                        ignore_list.append(device)
                        self.m1.send_email(device)
                        return True
        except Exception:
            logging.exception("[DeviceSniff][alarm_trigger]")


def main():
    """This function should find devices that are online and compare them with our known list. If
    the found device matches our list, then we send a notification email"""
    search = DeviceSniff()
    db_result = search.read_db()
    device_result = search.find_devices()
    alarm_result = search.alarm_trigger(db_result, device_result)
    print(f"Alarm: {alarm_result}")
    print("**********************************")
    time.sleep(10) # Sleep for X seconds    

if __name__ == "__main__":
    """We only want our network monitored during the assigned schedule.
    This function should check the time every 5 minutes before initiating a search"""
    s1 = Schedule()
    while True:
        if s1.schedule():
            print("Monitor Status: Online")
            main() 
        else:
            print("Monitor Status: Offline")
            ignore_list = []
            time.sleep(300) # Sleep for 5 minutes
