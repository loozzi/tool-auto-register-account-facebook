import random

from initial import *


def removeAccents(input_str):
    s1 = u'ÀÁÂÃÈÉÊÌÍÒÓÔÕÙÚÝàáâãèéêìíòóôõùúýĂăĐđĨĩŨũƠơƯưẠạẢảẤấẦầẨẩẪẫẬậẮắẰằẲẳẴẵẶặẸẹẺẻẼẽẾếỀềỂểỄễỆệỈỉỊịỌọỎỏỐốỒồỔổỖỗỘộỚớỜờỞởỠỡỢợỤụỦủỨứỪừỬửỮữỰựỲỳỴỵỶỷỸỹ'
    s0 = u'AAAAEEEIIOOOOUUYaaaaeeeiioooouuyAaDdIiUuOoUuAaAaAaAaAaAaAaAaAaAaAaAaEeEeEeEeEeEeEeEeIiIiOoOoOoOoOoOoOoOoOoOoOoOoUuUuUuUuUuUuUuYyYyYyYy'
    result = ''
    for c in input_str:
        if c in s1:
            result += s0[s1.index(c)]
        else:
            result += c
    return result


def cmd(commands):
    os.system(commands)


def getRandomPhoneNumber():
    result = firstPhoneNumber
    for i in range(12 - len(firstPhoneNumber)):
        result += str(random.randint(0, 9))
    return result


def getRandomName(lang):
    firstName = removeAccents(random.choice(listName[lang]['firstName']))
    lastName = removeAccents(random.choice(listName[lang]['lastName']))
    return {
        'fn': firstName,
        'ln': lastName,
        'fullName': "{0} {1}".format(firstName, lastName)
    }


def getRandomDate():
    day = random.randint(10, 28)
    month = random.randint(10, 12)
    year = random.randint(1970, 2003)
    return [day, month, year]


def getRandomPassword(length):
    s = 'zxcvbnmasdfghjklqwertyuiopZXCVBNMASDFGHJKLQWERTYUIOP1234567890'
    result = ""
    for i in range(length):
        result += random.choice(s)

    return result


def randomAllInformation():
    randomName = getRandomName(language)
    randomPhoneNumber = getRandomPhoneNumber()
    randomDate = getRandomDate()
    randomPassword = getRandomPassword(passwordLength)
    return {
        'randomName': randomName,
        'randomPhoneNumber': randomPhoneNumber,
        'randomPassword': randomPassword,
        'randomDate': randomDate
    }


def getToken(device):
    fileName = '{0}.txt'.format(getRandomPassword(20))
    device.pull('/data/data/com.facebook.lite/files/PropertiesStore_v02', './trashs/{0}'.format(fileName))
    try:
        with open('./trashs/{0}'.format(fileName), 'r', errors='ignore') as f:
            token = f.read().split('access_token":"')[1].split(('"'))[0]
            uid = f.read().split('uid":"')[1].split(('"'))[0]
            return {
                'uid': uid,
                'token': token
            }
    except:
        return 'die'




def delay(s):
    time.sleep(s)


def touchScreen(device, x, y):
    device.shell("input tap {0} {1}".format(x, y))


def inputText(device, content):
    for i in content:
        device.shell("input text '{0}'".format(i))
        delay(0.2)


def inputDate(device, value):
    for element in value:
        for i in str(element):
            touchScreen(device, pointsKeyboardNumber[int(i)]['x'], pointsKeyboardNumber[int(i)]['y'])
            delay(0.5)


def installAppication(device, path):
    # Facebook Lite
    if device.is_installed(packageLite):
        device.shell(f'pm clear {packageLite}')
        device.uninstall(packageLite)

    device.install(f"{path}/lite.apk")

    # 1.1.1.1
    if device.is_installed(packageWarp):
        device.shell(f'pm clear {packageWarp}')
        device.uninstall(packageWarp)

    device.install(f"{path}/1111.apk")


def grantPermissions(device):
    # Facebook Lite
    device.shell(f'pm grant {packageLite} android.permission.MANAGE_EXTERNAL_STORAGE')
    device.shell(f'pm grant {packageLite} android.permission.READ_CONTACTS')
    device.shell(f'pm grant {packageLite} android.permission.READ_CALENDAR')
    device.shell(f'pm grant {packageLite} android.permission.READ_PHONE_STATE')

    # 1.1.1.1
    device.shell(f'pm grant {packageWarp} android.permission.MANAGE_EXTERNAL_STORAGE')


def openApplication(device, packageName):
    # print(device.shell(f'dumpsys package | grep {packageName} |grep Activity'))
    device.shell(f'monkey -p {packageName} -c android.intent.category.LAUNCHER 1')


def startWarp(device):
    openApplication(device, packageWarp)
    delay(d1)
    for i in range(len(pointsWarp)):
        touchScreen(device, pointsWarp[i]['x'], pointsWarp[i]['y'])
        delay(d1)
        # getScreenShot(device)


def startLite(device):
    openApplication(device, packageLite)
    delay(d1)
    data = randomAllInformation()
    print(data)
    for i in range(2):
        touchScreen(device, pointsLite[i]['x'], pointsLite[i]['y'])
        delay(d1)
    randomName = data['randomName']
    inputText(device, randomName['fn'])
    # Tab
    device.shell('input keyevent 61')
    delay(d3)
    inputText(device, randomName['ln'])
    delay(d3)
    touchScreen(device, pointsLite[2]['x'], pointsLite[2]['y'])
    delay(d1)
    randomPhoneNumber = data['randomPhoneNumber']
    touchScreen(device, pointsLite[3]['x'], pointsLite[3]['y'])
    inputText(device, randomPhoneNumber)

    delay(d3)
    touchScreen(device, pointsLite[4]['x'], pointsLite[4]['y'])
    delay(d1)

    # Date
    randomDate = data['randomDate']
    inputDate(device, randomDate)
    delay(d3)

    touchScreen(device, pointsLite[5]['x'], pointsLite[5]['y'])
    delay(d1)
    touchScreen(device, pointsLite[6]['x'], pointsLite[6]['y'])
    delay(d1)

    # Input password
    touchScreen(device, pointsLite[7]['x'], pointsLite[7]['y'])
    delay(d3)
    randomPassword = data['randomPassword']
    inputText(device, randomPassword)
    delay(d3)
    touchScreen(device, pointsLite[8]['x'], pointsLite[8]['y'])
    delay(d1)

    touchScreen(device, pointsLite[9]['x'], pointsLite[9]['y'])
    delay(d4)
    touchScreen(device, pointsLite[10]['x'], pointsLite[10]['y'])
    delay(d1)
    token = getToken(device)
    print(token)


def getScreenShot(device):
    result = device.screencap()
    with open(f'../screenshots/screenshot_{datetime.now().strftime("%Y%m%d%H%M%S")}.png', 'wb') as f:
        f.write(result)


def resetAllData(device):
    pass
