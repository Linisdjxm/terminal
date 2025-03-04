# 网络演示系统终端
---

## 环境依赖
由 Anaconda 构筑 Python 环境
**TBD**

## 部署步骤
1. **TBD**
2. **TBD**
3. **TBD**

## 目录结构描述
```
NETTERMINAL
├── Document                    // 文档
│
├── Forms                       // 界面设计
│   ├── MainWindowMin.ui
│   ├── MainWindowPro.ui
│   ├── Ui_MainWindowMin.py
│   └── Ui_MainWindowPro.py
│
├── Sources                     // 核心组成
│   ├── Component                   // 功能组件(提供功能)
│       ├── Component1                  // 功能1
│       └── Component2                  // 功能2
│   ├── Device                      // 设备模块(提供模型)
│       ├── Device1                     // 模块1
│       └── Device2                     // 模块2
│   ├── Driver                      // 硬件驱动(提供途径)
│       ├── Driver1                     // 驱动1
│       ├── Driver2                     // 驱动2
│       └── Driver3                     // 驱动3
│   ├── MainWindowMin.py            // 移动终端入口(控制逻辑)
│   └── MainWindowPro.py            // 地面站终端入口(控制逻辑)
│
├── Main.py                     // 启动程序
├── Main3.py                     // 测试程序2
└── README.md                   // 帮助文档
```

## 测试
1. 在适当的Conda环境下分别运行Main.py, Main3.py

## 项目架构
![项目架构图](./Document/fig_architecture.png "项目架构图")

## V1.0.0 版本内容更新
1. **TBD**
