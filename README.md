# utm-generator-dev

[![GitHub Stars](https://img.shields.io/github/stars/XiaomingX/utm-generator-dev.svg)](https://github.com/XiaomingX/utm-generator-dev/stargazers)
[![GitHub License](https://img.shields.io/github/license/XiaomingX/utm-generator-dev.svg)](https://github.com/XiaomingX/utm-generator-dev/blob/main/LICENSE)

一个轻量实用的UTM参数生成工具，帮助开发者快速为链接添加标准化UTM参数，便于通过Google Analytics、百度统计、Bing Analytics等工具追踪不同渠道的引流效果，精准分析流量来源质量。


## 项目地址
[GitHub仓库](https://github.com/XiaomingX/utm-generator-dev)


## 功能简介
UTM（Urchin Tracking Module）参数是用于标记网络营销活动的核心标签，本工具专注于解决"链接来源追踪"的痛点：
- 自动从来源链接提取域名作为`utm_source`（如从`https://mp.jobleap4u.com/`提取`mp_jobleap4u`）
- 为目标链接批量添加固定的`utm_medium`（媒介类型）和`utm_campaign`（活动名称）
- 智能保留目标链接原有的查询参数（如`?page=1&sort=desc`），避免参数冲突
- 输出符合URL规范的最终链接，支持带路径、端口、哈希值的复杂链接格式


## 安装方法
### 直接使用源码
```bash
# 克隆仓库
git clone https://github.com/XiaomingX/utm-generator-dev.git
cd utm-generator-dev

# 环境要求：Python 3.6+（依赖Python标准库，无需额外安装第三方包）
```

### 作为模块引入
可直接将`utm_generator.py`文件复制到你的项目中，通过`import`调用：
```python
from utm_generator import add_utm_params
```


## 快速使用
### 基础示例
```python
from utm_generator import add_utm_params

# 来源链接（流量源头页面）
from_url = "https://mp.jobleap4u.com/"
# 目标链接（需要添加UTM参数的页面）
to_url = "https://jobleap.cn/"

# 生成带UTM参数的链接
trackable_url = add_utm_params(from_url, to_url)
print(trackable_url)
# 输出：
# https://jobleap.cn/?utm_source=mp_jobleap4u&utm_medium=discover_page&utm_campaign=content_cta
```

### 复杂链接示例（含原有参数）
```python
from_url = "https://blog.jobleap4u.com/articles/123"
to_url = "https://jobleap.cn/jobs?type=remote&experience=3+"

trackable_url = add_utm_params(from_url, to_url)
print(trackable_url)
# 输出（保留原有参数，追加UTM标签）：
# https://jobleap.cn/jobs?type=remote&experience=3+&utm_source=blog_jobleap4u&utm_medium=discover_page&utm_campaign=content_cta
```


## 核心参数说明
### 函数参数
| 参数名      | 类型   | 说明                          | 示例                          |
|-------------|--------|-------------------------------|-------------------------------|
| `from_url`  | `str`  | 流量来源链接（如推广页面URL） | `https://mp.jobleap4u.com/`   |
| `to_url`    | `str`  | 需要添加UTM参数的目标链接     | `https://jobleap.cn/`         |

### 生成的UTM标签
| UTM参数         | 含义                          | 生成规则                          |
|-----------------|-------------------------------|-----------------------------------|
| `utm_source`    | 标识流量来源平台              | 自动从`from_url`域名提取（替换`.`为`_`） |
| `utm_medium`    | 标识流量媒介类型              | 固定为`discover_page`（可根据需求修改源码） |
| `utm_campaign`  | 标识具体营销活动名称          | 固定为`content_cta`（可根据需求修改源码） |


## 功能亮点
- **零依赖**：仅使用Python标准库`urllib`，无需额外安装依赖包，轻量易集成
- **智能兼容**：自动处理目标链接中已有的查询参数，避免重复或冲突
- **标准化输出**：严格遵循URL编码规范，确保生成的链接在所有浏览器和统计工具中正常生效
- **灵活扩展**：可通过修改源码中的`utm_medium`和`utm_campaign`默认值，适配不同业务场景


## 测试
项目包含基础测试用例，可直接运行验证功能：
```bash
python test_utm_generator.py
```


## 贡献指南
欢迎参与项目改进！流程如下：
1.  Fork 本仓库（[https://github.com/XiaomingX/utm-generator-dev/fork](https://github.com/XiaomingX/utm-generator-dev/fork)）
2.  创建特性分支（`git checkout -b feature/your-feature`）
3.  提交修改（`git commit -m 'Add your feature'`）
4.  推送到分支（`git push origin feature/your-feature`）
5.  提交 Pull Request


## 许可证
本项目基于 [MIT 许可证](https://github.com/XiaomingX/utm-generator-dev/blob/main/LICENSE) 开源，允许自由使用、修改和分发。


## 联系作者
如有问题或建议，可通过以下方式联系：
- GitHub Issues：[https://github.com/XiaomingX/utm-generator-dev/issues](https://github.com/XiaomingX/utm-generator-dev/issues)