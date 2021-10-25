# DuelEditor

[![Build Status](https://github.com/Wind2009-Louse/DuelEditor/actions/workflows/main.yml/badge.svg?branch=master)](https://travis-ci.com/Wind2009-Louse/DuelEditor)

决构工具

## 基本操作

1. **卡片搜索**中输入卡名创建卡片，添加到**操作对象**列表中。
2. 设置移动区域，**移动对象**。
3. 对场上的卡片，可以通过双击，将其添加到**操作对象**列表中。
4. 重复2. 

## 糖

1. 快捷操作。
- 1.1. Ctrl+N/O/S快捷创建/打开/保存。
- 1.2. 卡片搜索/注释栏支持回车。
- 1.3. 操作列表支持Del键。
- 1.4. 卡片搜素双击可以补全卡名；操作列表双击可以进行复制。
  - 1.4.1. 支持多关键词进行卡片搜索，每个关键词前加上“-”则说明排除该关键词。
2. 支持cdb，将**cards.cdb**和项目放在同一目录中，项目可以读取卡片内容，进行卡名补全、效果快查、简易伤害计算等操作。
3. 按住Shift点击场上的卡片，可以进行效果快查。
- 3.1. 快查中，**狮子男巫**、**狮子男巫1**和**狮子男巫k**均可以查到**狮子男巫**，建议创建卡片时按照格式（卡名+0~1位序号）命名，方便快查。
4. 创建卡名的搜索框同样可以用来搜索场上的卡片，若在场上搜索到前缀相同的卡片，将会被标红。