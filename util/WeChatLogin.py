from appium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from appium.webdriver.common.mobileby import MobileBy as MB

import time

"""
1\识别
2、开启调试：
针对微信版本在7.0+，微信有对H5开关做了调整，需要在聊天窗口输入如下：
http://debugmm.qq.com/?forcex5=true
http://debugx5.qq.com

3、appium代码当中：
   #支持X5内核应用自动化配置  desired_caps["recreateChromeDriverSessions"] = True
   # desired_caps["chromeOptions"] = {"androidProcess":"com.tencent.mm:appbrand0"}  # 小程序在哪个进程 
   获取小程序所在的进程：
 adb shell dumpsys activity top | findstr ACTIVITY
   
4、注意:进入小程序之后，获取当前所有的上下文，切换进最后一个webview
   chromedriver版本要与微信x5版本号匹配，而不是原生的webview（uc-devtools查看微信x5版本号）

5、获取小程序当中所有的窗口。
   遍历所有窗口，并切入窗口的html中，查找有代表性的元素。
   driver.find_element
   driver.page_source.find("") != -1:
      break
"""

# 启动appium时，需要指定chromedriver.exe的目录。使用appium默认目录下的会报错。
# 在切换到小程序webview时，会去匹配chrome内核的39的驱动。在切换完成之后，在打印所有的窗口时，会使用x5内核的版本。
# 所以指定一个非默认目录下面的chromedriver.exe(X5内核对应的版本)，此问题就不会出现 。
# 在appium server上设置chromedriver的路径：D:\ChromeDrivers\chromedriver.exe
desired_caps = {}
# 支持X5内核应用自动化配置
desired_caps["recreateChromeDriverSessions"] = True
# android 4.4以下的版本通过Selendroid来切换到webview
desired_caps["automationName"] = "UiAutomator2"
desired_caps["platformName"] = "Android"
# desired_caps["platformVersion"] = "8.1"
desired_caps["deviceName"] = "69ef8797"
desired_caps["appPackage"] = "com.tencent.mm"
desired_caps["appActivity"] = "com.tencent.mm.ui.LauncherUI"
# chromedriverExecutableDir：在chromedriver文件夹中自动匹配对应的chromedriver.exe来进行使用
desired_caps["chromedriverExecutableDir"] = 'E:\chromedriver_win32\chromedriver.exe'
desired_caps["showChromedriverLog"] = True
desired_caps["noReset"] = True
desired_caps["unicodeKeyboard"] = True
# desired_caps["resetKeyboard"] = True


# ChromeOptions使用来定制启动选项，因为在appium中切换context识别webview的时候,
# 把com.tencent.mm:toolsmp的webview识别成com.tencent.mm的webview.
# 所以为了避免这个问题，加上androidProcess: com.tencent.mm:toolsm
desired_caps["chromeOptions"] = {"androidProcess": "tencent.mm:appbrand0"}
# desired_caps["browserName"] = ""

driver = webdriver.Remote('http://127.0.0.1:4723/wd/hub', desired_caps)


# 进入微信小程序并获取所有的上下文
def mini_context(driver, el):
    """

    :param driver: webdriver.Remote
    :param el: 小程序的id元素
    :return:
    """
    # 打开微信下拉列表
    wait = WebDriverWait(driver, timeout=20, poll_frequency=0.1)
    loc = (MB.ID, el)
    wait.until(EC.visibility_of_all_elements_located(loc))
    time.sleep(3)
    size = driver.get_window_size()
    driver.swipe(size["width"] * 0.5, size["height"] * 0.2, size["width"] * 0.5, size["height"] * 0.9, 100)

    # 点击小程序
    locs = (MB.ID, el)
    WebDriverWait(driver, 30).until(EC.visibility_of_element_located(loc))
    driver.find_element(*locs).click()
    time.sleep(3)

    # 获取所有的上下文
    cons = driver.contexts
    return "当前所有的上下文为：", cons


if __name__ == '__main__':
    mini_context(driver, el='com.tencent.mm:id/dt5')
    # 切换到小程序webview
    driver.switch_to.context('WEBVIEW_com.tencent.mm:appbrand0')
    time.sleep(5)
