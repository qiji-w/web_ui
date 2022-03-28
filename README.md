<<<<<<< HEAD
## Framework of web UI

## selenium + pytest + allure + po

### 执行用例
+ 初始化环境并执行用例 `python3 run_all_cases.py  --url http://uat-gdp.growingio.com --project_id WlGk4Daj --mark UI_test_dsitribute_analysis`

**注意:** 
> 第一次执行用例，必须要先执行初始化环境并执行用例操作

> mark为缺省参数，若不填写，默认执行所有测试用例


### 环境搭建

#### [执行用例的jenkins地址](https://release-jenkins.growingio.cn/view/QA-Tools/job/qa-web-ui-op/)

#### [发送通知的jenkins地址](https://release-jenkins.growingio.cn/view/Notify/job/web-ui-notify/)

#### 安装python并安装依赖库
+ 统一使用python3.7以后的版本
+ 下载方式
  + 手动安装，[下载地址](https://www.python.org/downloads/mac-osx/)
  + 自动安装   使用homebrew安装（[安装homebrew](https://growingio.atlassian.net/wiki/spaces/FEW/pages/707331018#id-%E5%BC%80%E5%8F%91%E7%8E%AF%E5%A2%83%E6%90%AD%E5%BB%BA-Homebrew)）
    + 查询python版本`brew search python3`
    + 安装python指定版本`brew install python@3.7`
      
+ 搭建python虚拟环境(可不安装虚拟环境)
  + 使用pip包管理工具安装
    + 安装`pip3 install virtualenv`
    + 安装`pip3 install virtualenvwrapper`
  
  + 配置环境变量
    + 创建目录`mkdir ~/.virtualenvs`
    + 编辑配置文件 `vim ~/.bash_profile`
      文件内添加以下内容
      
      **这里需要注意**：`/Library/Frameworks/Python.framework/Versions/3.7/bin/`要根据你的python安装路径而定
       ```python
       export WORKON_HOME=$HOME/.virtualenvs
 
       export VIRTUALENVWRAPPER_SCRIPT=/Library/Frameworks/Python.framework/Versions/3.7/bin/virtualenvwrapper.sh
       export VIRTUALENVWRAPPER_PYTHON=/Library/Frameworks/Python.framework/Versions/3.7/bin/python3
       export VIRTUALENVWRAPPER_VIRTUALENV=/Library/Frameworks/Python.framework/Versions/3.7/bin/virtualenv
       export VIRTUALENVWRAPPER_VIRTUALENV_ARGS='--no-site-packages'
 
       source /Library/Frameworks/Python.framework/Versions/3.7/bin/virtualenvwrapper.sh
       VIRTUALENVWRAPPER_PYTHON=/usr/local/bin/python3
       ```
       执行命令`source ~/.bash_profile`,使配置生效
  
  + 创建虚拟环境 `mkvirtualenv virtualenv_name`
  
  + 进入虚拟环境 `workon virtualenv_name` 
  
  + 删除虚拟环境 `rmvirtualenv virtualenv_name`
    
+ 使用`mkvirtualenv selenium_env`命令,创建虚拟环境，在虚拟环境中，安装项目requirements.txt中的依赖库`pip3 install -r requirements.txt`

#### 下载安装python编辑器-pycharm
+ [下载地址](https://www.jetbrains.com/pycharm/download/#section=mac)

  下载完成后，傻瓜式安装即可
  
  可以不用安装上一步骤中的虚拟环境，使用pycharm管理虚拟环境也可

#### 浏览器driver

下载并解压好对应浏览器版本的driver，放入path环境变量中，这样在代码中，实例化driver时，不用填写具体的浏览器driver的路径


chrome
+ [driver下载及支持版本](http://npm.taobao.org/mirrors/chromedriver/)

firefox 
+ [driver支持firefox版本对应表](https://firefox-source-docs.mozilla.org/testing/geckodriver/Support.html)
+ [driver下载地址](https://github.com/mozilla/geckodriver/releases)

safari

+ safari浏览器本身已经集成了safaridriver，启用并开启即可:`safaridriver --enable`
[参考](http://www.bubuko.com/infodetail-3624630.html)


#### 执行测试用例

+ 将项目导入pycharm中，具体执行步骤参考`方案设计`中的步骤`5、用例执行及报告展示`

### 一、PageObject 设计模式

#### 1、PO模式

PO是Page Object的缩写，PO模式是自动化测试项目开发实践的最佳设计模式之一。
核心思想是通过对界面元素的封装减少冗余代码，同时在后期维护中，若元素定位发生变化， 只
需要调整页面元素封装的代码，提高测试用例的可维护性、可读性。

#### 2、PO模式分层设计

+ BasePage层：存放对网页的一些基础操作并封装成类，BasePage页适用于整个项目

+ 组件层：工具组件类，继承自BasePage类，封装了对各个组件的常用方法

+ 业务page层：一个页面定义成一个page类并继承组件类，调用组件类中的对各个组件的操作方法（也可以直接使用BasePage中封装的方法），实现当前页面的主要业务功能，并按照业务逻辑，在调用的方法中返回其他页面page类

+ case层：调用业务page层封装的方法，按照业务逻辑，调用业务page层封装好的方法编写case（因为在业务层的方法中返回了其他的页面page类）

### 二、方案设计

#### 1、目录层级划分

`basepage/base_page.py`- 实例化webdriver及webdriver的基础操作，公用的操作
 
`项目分成以下内容：

+ `base_page` - 存放当前项目的特有basepage类，继承公用的basepage类

+ `component` - 存放组件类文件目录，继承BasePage类，页面组件的工具类

+ `page` - 存放页面page文件的目录

+ `testcase/*` - 存放测试case层，可以按照测试模块不同，新建不同的文件夹

`util/util.py` - 用于实现一些额外的功能（原生框架不支持的）

`log` - 存放日志文件的目录

`report` - 存放报告数据的目录

`conf` - 配置文件

`datas` - 数据驱动文件



![](.README_images/863b161c.png)


#### 2、pytest

[pytest介绍](https://blog.csdn.net/lovedingd/article/details/98952868)


1.`fixture` - 初始化测试case或者清除工作 eg: `@pytest.fixture(scope="function", autouse=False)`

a.`scope`被标记方法的作用域，可填写4个参数,与`yield`配合使用，实现与setup和teardown一样的功能
+ `session` 作用于整个session，每个session只运行一次 
+ `module` 作用于整个模块，每个module的所有test只运行一次
+ `class` 作用于整个类，每个class的所有test只运行一次
+ `function` (default)：作用于每个测试方法，每个test都运行一次

b.`fixture`的调用

+ 自动调用：`autouse`缺省为`False`，置为`True`,fixture装饰的函数，会在作用域范围内被自动执行

+ 手动调用：将被fixture装饰的方法名当作函数的传参，传入要调用的函数，当执行到此函数时，fixture会被调用，如果fixture有返回值，返回值会被赋给此处被当做传参的方法名

c.`conftest.py`与`fixture`配合使用

 + 可以跨.py文件调用，有多个.py文件调用时，可让conftest.py只调用了一次fixture，或调用多次fixture
 
 + 不需要import导入 conftest.py，pytest用例会自动识别该文件，放到项目的根目录下就可以全局目录调用了，如果放到某个package下，那就在该package内有效，可有多个conftest.py


#### 3、编写case的一些约定

编码规范遵循[google规范](https://zh-google-styleguide.readthedocs.io/en/latest/google-python-styleguide/python_style_rules/#comments)

1.命名规则：
+ 测试文件必须以test_开头
+ 测试类必须以Test开头，且不能有init方法
+ 测试函数或者方法必须以test_开头

2.给测试case打标签，给测试case增加装饰器 `@pytest.mark.markname`,执行case时候，可以通过参数`-m markname`筛选要执行的测试case

3.给测试类增加装饰器`@allure.feature("description")`,测试方法增加装饰器 `@allure.story("description")`，方便在allure报告中展示测试用例

4.类和方法名的命名要见名知意

测试用例demo
```python
@pytest.mark.op_board
@allure.feature("测试看板模块")
class TestOpBoard:

    @pytest.fixture()
    def board(self, init_driver):
        yield init_driver.jump_to_board_by_url()

    @allure.story("打开board页面成功")
    def test_board_demo(self, board):
        text = board.get_board_assert_text()
        assert '全部看板' == text
```
4.定位方式的选择优先级:
+ 1.id
+ 2.css_selector
+ 3.xpath
+ 4.class_name
+ 5.XXX



#### 4、新增case的流程及断言

1.以页面page为准，若已有case涉及到的页面page，就在对应页面page类中添加的新方法去实现新的业务逻辑；若无页面page，新建页面page文件，新建页面page类，再在类中新增方法


2.在case层新增测试用例

3.将要断言的数据内容提取并返回到用例层进行断言，暂时使用`assert`关键字进行断言

**补充：页面之间跳转通过访问url的方式实现**
+ 新增页面page时，定义好page类，然后先增加类变量`（_path = "/xxx"）`表示当前page的path路径, path在conf文件中维护。其次，在首页page类中增加方法名为：jump_to_XXX，此方法中返回新增页面的page,会自动通过path定位到页面，以jump开头的方法都为通过url跳转的页面。

**新增case**

page页面

```python
from conf.op_conf.conf import board_module_path


class BoardPage(ElementDesign):
  _path = board_module_path

  def input_content_in_input(self, content):
    pass
    return self
```
首页page
```python
    def jump_to_board_by_url(self):
        return BoardPage(self._driver)
```
+ 编写case时，要定一个scope为function级的fixture，执行jump_to_xxx。每个case都以打开这个页面为基准，进行维护。目的：减少case间耦合性。
```python
@allure.feature("测试demo")
class TestDemo:

    @pytest.fixture()
    def demo_fixture(self, init_driver):
        yield init_driver.jump_to_board_by_url()

    @allure.story("demo1")
    def test_demo1(self, board):
        pass
    
    @allure.story("demo2")
    def test_demo2(self, board):
        pass
    
```
#### 5、用例执行及报告展示(allure)


1.本地安装[allure command](https://www.jianshu.com/p/bdd1d6fcc5df)命令行工具

2.安装python依赖库`pip3 install -r requirements.txt`

3.执行测试用例（项目根目录下，终端执行）
+ 1.执行特定标签用例`pytest -m markname`
+ 2.执行项目的所有用例`pytest`

  目前执行用例前，需要在op_conf/conf.py文件中填写自己的用户名和密码，已申请专门用于测试的账号，固定写定

4.终端执行`allure serve report` 会自动调起浏览器展示报告

#### 6、selenium-grid 模式搭建

1.执行项目内`docker-compose.yml`文件，`docker-compose -f docker-compose.yml up -d`,搭建浏览器执行节点（hub、node）

2.执行测试用例，根目录下执行`pytest`

3.通过 VNC viewer查看容器内浏览器执行

#### 7、基础设施建设

##### done

1.basepage通用方法方法封装：（1）切换窗口 （2）切换iframe （3）鼠标事件 （4）键盘事件

2.项目登陆方法实现（op和saas）

3.gio design页面组件方法封装

4.数据库连接

+ 使用records库连接，[相关api](https://github.com/kenreitz42/records)

5.用例读取yaml文件内容，实现参数化的方法封装

6.获取cookie方式改为由api获取

##### todo

1.输入浏览器类型启动对应类型的浏览器，执行测试用例

2.维护自动化case

3.xxx

=======
>>>>>>> 6cf55d52c0f0dd273e8903d1ba195d2e497645df

