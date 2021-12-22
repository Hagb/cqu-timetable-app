# 重庆大学课程表 APP（非官方）

WIP。目前仅实现简陋的考表显示及考表日历导出（Android 特有功能）。[Release](https://github.com/Hagb/cqu-timetable-app/releases) 中有预编译的 apk。

使用 [BeeWare](https://beeware.org) 项目，以 Python 和 Java 写成，可在多个平台上运行。

[BeeWare](https://beeware.org) 目前较为实验性，所以这里使用我们自定义（魔改和/或改进）的版本。同时本项目亦是高度实验性的，为作者用 Python 写 Android 的尝试（~~实际上为了填 BeeWare 的坑，也写了很多 Java 和修补~~ 当然 BeeWare 还是挺好的）。

对于使用该项目可能造成的一切风险，用户自负。

## 运行（PC）

```bash
pip install briefcase
briefcase dev
```

## Android 编译

```bash
git submodule update --init
./create-android-project.sh
briefcase build android
# 或用 briefcase run android --update 通过 adb 安装并运行
```

## TODO

- [ ] Android 端上实现使用 Calendar Sync Adapter 定时自动更新系统日历中的课表、考表。（目前使用的是 [Calendar Provider](https://developer.android.com/guide/topics/providers/calendar-provider)，只能打开 APP 来更新，没法后台自动更新）
- [ ] PC 端上实现导出 ics 并唤起系统打开方式打开 ics
- [x] 考表获取、显示、（Android）导出
- [ ] 课表获取、显示、（Android）导出
