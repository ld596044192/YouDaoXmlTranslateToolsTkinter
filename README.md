## **[YouDaoXmlTranslateToolsTkinter](https://gitee.com/ld596044192/you-dao-xml-translate-tools-tkinter)**

### 介绍（前言）
#### 工具简介

此工具以有道翻译引擎为主的安卓开发xml多语言翻译工具，该工具仅适用于安卓开发在多语言翻译时辅助使用；主要包含xml批量翻译以及单文件批量翻译，其他均为定制功能（不一定适合你们使用）；

该工具原本只是帮助安卓开发的辅助工具，现单独开源分享，并把部分开发时的调试功能屏蔽，以免影响正常功能

#### 为什么要开发此工具？

这是因为安卓开发时，在进行多语言开发时，如果仅一两个语言还好，但需要翻译的语言一旦过多，花费的时间可能几天甚至一周时间，时间成本过大（虽然可以借助某些工具，但也不是很智能，需要花费的时间也是比较大）；

本人使用python3.8开发的xml批量翻译工具，以原生tkinter GUI库快速开发，虽然如今本人转战使用移植Flutter的python第三库flet进行GUI开发，但并不打算把该工具的功能进行移植，主要本人没时间，而且该工具以tkinter开发已足够稳定，以 V1.1.3 版本作为最终版进行开源分布！！！

使用的翻译引擎目前仅有有道翻译，目前并未打算使用其他翻译引擎，如自己需要其他引擎，请自行编写使用，如有问题可联系 596044192@qq.com 

#### 本工具优点：

（一）比其他翻译网站和工具更加智能：

1. 根据项目res翻译文件夹结构进行识别，没有对应xml文件会自动创建并输入格式
2. 已翻译的符合命名规则的文件夹会自动跳过，翻译没有翻译过的文件夹
3. 只要你的翻译文件夹符合命名规则，那么工具就会进行批量翻译，你需要的只是等待工具翻译完成
4. 工具翻译时自动写入文件，如果避免误操作，建议你先备份需要翻译的xml文件夹，以免无法还原
5. 翻译时出现的异常操作都能更好的以简体中文进行提示
6. 批量翻译功能（主界面），翻译过程可以暂停和继续，也可以直接停止翻译，满足你的需求

（二）单文件（单个xml文件）翻译语言更加多

只要是有道翻译引擎支持的语言，都能进行翻译，翻译结果的精确度参考有道翻译

### 安装教程

（1）该工具可以在release版本发布页面，使用本人自行打包的最终版，无需安装python环境，即可在电脑环境进行使用，注意，电脑系统版本建议使用Win10版本及以上，使用Win7系统可能报错；

如果需要使用Win7系统，就不能使用本人发布提供的release版本，你需要下载源代码，然后使用Python3.6 ~ Python3.8版本进行打包，高版本的Python编译器不再支持Win7系统的运行，强行运行会导致缺少插件...

（2）源代码使用步骤：

1.下载该工具的源代码并解压

2.使用Pycharm等开发工具进行加载，推荐使用Python 3.8及以上

3.找到requirements.txt并执行以下命令

```python
cd <前面文件夹省略>\YouDao_XML_Translate\xml_translate_tool
```

```python
pip install -r requirements.txt
```

4.等待本项目所需要的库安装完毕后，打开 youdao_gui.py 运行即可

5.如想要自行打包，请使用控制台cd .. 返回到与 YouDao_XML_Translate 文件夹同级位置，再使用控制台执行：

```
pyinstaller .\xml批量翻译工具.spec
```

或

```
pyinstaller <前面文件夹省略>\xml批量翻译工具.spec
```

6.若想要更改工具名称，最简单打包后直接更改工具名称，或者如下：

首先把“xml批量翻译工具.spec”命名为其他你想要的名称，再使用记事本打开spec文件夹

![image-20240312213147057](C:\Users\59604\AppData\Roaming\Typora\typora-user-images\image-20240312213147057.png)

这样直接使用命令打包后生成的工具名称就是你想要的，不用每次都自行更改名称

### 使用说明

（1）该工具需要有道翻译的id和key，如果没有需要自行到 http://ai.youdao.com/ 进行注册

![image-20240312213352914](C:\Users\59604\AppData\Roaming\Typora\typora-user-images\image-20240312213352914.png)

成功注册并进行个人实名认证后，即可获得可以免费使用的50体验金，一旦体验金使用完毕需要自行充值才能继续使用有道翻译功能

（2）创建应用库后即可获得id和key

![image-20240312213605774](C:\Users\59604\AppData\Roaming\Typora\typora-user-images\image-20240312213605774.png)

（3）然后把复制的ID和Key，填入下面方框，并点击保存

![image-20240312213641292](C:\Users\59604\AppData\Roaming\Typora\typora-user-images\image-20240312213641292.png)

（4）必须输入可用的ID和Key，否则翻译功能不可用

下面这个为工具的主界面，属于“xml批量翻译”的主要功能

![image-20240312213815455](C:\Users\59604\AppData\Roaming\Typora\typora-user-images\image-20240312213815455.png)

（5）可以点击“模块说明”查看具体的使用说明

![image-20240312214025274](C:\Users\59604\AppData\Roaming\Typora\typora-user-images\image-20240312214025274.png)

（6）本工具也提供了模版作为参考，如果你的项目翻译文件夹不是这个结构，那么直接在本模版上进行操作

![image-20240312214231698](C:\Users\59604\AppData\Roaming\Typora\typora-user-images\image-20240312214231698.png)

![image-20240312214313755](C:\Users\59604\AppData\Roaming\Typora\typora-user-images\image-20240312214313755.png)

![image-20240312214410324](C:\Users\59604\AppData\Roaming\Typora\typora-user-images\image-20240312214410324.png)

注：values文件夹里的xml文件名称必须为strings.xml，否则提示出错

![image-20240312221309330](C:\Users\59604\AppData\Roaming\Typora\typora-user-images\image-20240312221309330.png)

（7）需要翻译的xml文件内容格式如下

![image-20240312214720953](C:\Users\59604\AppData\Roaming\Typora\typora-user-images\image-20240312214720953.png)

（8）点击翻译，将会自动把中文翻译为英文，点击“复制”按钮也可直接把带xml格式的内容复制到你想要的位置上

![image-20240312214838512](C:\Users\59604\AppData\Roaming\Typora\typora-user-images\image-20240312214838512.png)

![image-20240312215132939](C:\Users\59604\AppData\Roaming\Typora\typora-user-images\image-20240312215132939.png)

（9）如果需要批量翻译多种语言，可以直接复制文件夹并修改如下

![image-20240312215556266](C:\Users\59604\AppData\Roaming\Typora\typora-user-images\image-20240312215556266.png)

文件夹命名规则：values- 后面跟的是有道翻译引擎支持的语言代码，文件夹可为空

（10）批量翻译效果

![image-20240312215828811](C:\Users\59604\AppData\Roaming\Typora\typora-user-images\image-20240312215828811.png)

![image-20240312215903806](C:\Users\59604\AppData\Roaming\Typora\typora-user-images\image-20240312215903806.png)

文件过多就不再展示，具体自行体验

（11）单文件翻译

![image-20240312220142765](C:\Users\59604\AppData\Roaming\Typora\typora-user-images\image-20240312220142765.png)

![image-20240312220224929](C:\Users\59604\AppData\Roaming\Typora\typora-user-images\image-20240312220224929.png)

![image-20240312220247579](C:\Users\59604\AppData\Roaming\Typora\typora-user-images\image-20240312220247579.png)

（12）定制功能（仅保留，但不一定适合所有人）

![image-20240312220334510](C:\Users\59604\AppData\Roaming\Typora\typora-user-images\image-20240312220334510.png)

（13）也可以支持直接复制内容进行翻译，复制的内容同样需要符合xml文件的格式

![image-20240312220722576](C:\Users\59604\AppData\Roaming\Typora\typora-user-images\image-20240312220722576.png)

![image-20240312220813264](C:\Users\59604\AppData\Roaming\Typora\typora-user-images\image-20240312220813264.png)

这个直接添加内容翻译，批量功能会优先翻译这个，并且翻译出来的内容不会覆盖xml文件，而是追加原有的xml文件中，这是为了xml翻译的安全而考虑，注意如果没有xml文件会自动创建xml文件并写入！！！

（如果想要批量你的values文件夹中的xml文件，请清空直接复制的内容）

### 注意事项

1、该工具因使用tkinter原生GUI库，因此功能比较受限，可能部分考虑到但无法优化，因此建议你使用本工具时，请勿一直最小化，否则还原窗口时可能导致窗口卡顿；同时建议不用时就关闭本工具

2、该工具启动时间可能根据电脑配置有关，配置不好的电脑启动时间稍长，请耐心等待，切勿重复启动，受限于tkinter框架，启动时需要初始化的东西无法进行优化

3、批量翻译功能上下滚动，需要把鼠标放在滚动条时才会生效，受限于tkinter框架只能如此，无法优化

4、本工具不建议作为暴力测试对象，暴力测试导致的Bug非重要本人不会进行修改，由于最终版本工具属于稳定版本，但难免有Bug，不影响使用暂时不会再修改

5、关于本工具的图标设置，可修改如下几处：

![image-20240312222138133](C:\Users\59604\AppData\Roaming\Typora\typora-user-images\image-20240312222138133.png)

打包后的工具图标，修改spec文件：

![image-20240312222238924](C:\Users\59604\AppData\Roaming\Typora\typora-user-images\image-20240312222238924.png)

然后把打包后的工具移到其他位置刷新，图标即可更新，如果不行就需要按照pyinstaller.txt重新运行打包命令，再修改spec，最终再次打包即可成功！！！

### 声明

本工具均由本人一人开发使用，仅作开源分享免费使用，最终解释权归本人所有！！！
