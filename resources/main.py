from initial import *
from functions import *


class RunApp(Thread):
    def __init__(self, device, index):
        super(RunApp, self).__init__()
        self.device = device
        self.index = index

    def run(self):
        for i in range(numLoop):
            cmd('{0}\\dnconsole.exe modify --index {1} --imei auto --androidid auto --mac auto'.format(pathLdPlayer, i))
            print("Start:", self.index)
            installAppication(self.device, pathApplication)
            grantPermissions(self.device)
            if settings['useWarp']:
                startWarp(self.device)
            startLite(self.device, self.index)
            cmd('{0}\\dnconsole.exe setprop --index {1} --key "phone.imei" --value "auto"'.format(pathLdPlayer, i))
            cmd('{0}\\dnconsole.exe setprop --index {1} --key "phone.imsi" --value "auto"'.format(pathLdPlayer, i))
            cmd('{0}\\dnconsole.exe setprop --index {1} --key "phone.simserial" --value "auto"'.format(pathLdPlayer, i))

def main():
    client = AdbClient(host="127.0.0.1", port=5037)
    devices = client.devices()

    threads = []
    for i in range(len(devices)):
        threads.append(RunApp(devices[i], i))

    for thread in threads:
        thread.start()


def startLdPlayer(num):
    for i in range(num):
        cmd('{0}\\dnconsole.exe modify --index {1} --imei auto --androidid auto --mac auto'.format(pathLdPlayer, i))
        cmd('{0}\\dnconsole.exe launch --index {1}'.format(pathLdPlayer, i))
        cmd('{0}\\dnconsole.exe setprop --index {1} --key "phone.imei" --value "auto"'.format(pathLdPlayer, i))
        cmd('{0}\\dnconsole.exe setprop --index {1} --key "phone.imsi" --value "auto"'.format(pathLdPlayer, i))
        cmd('{0}\\dnconsole.exe setprop --index {1} --key "phone.simserial" --value "auto"'.format(pathLdPlayer, i))
        print('Open LDPlayer:', i)
        delay(d1)

if __name__ == '__main__':
    q1 = input("Open LDPlayer (y/n)? ")
    if(q1 == 'y' or q1 == ''):
        startLdPlayer(numEmulator)
        q2 = input("Type `ok` when emolator open success. ")

    main()

# print(getRandomPhoneNumber())
