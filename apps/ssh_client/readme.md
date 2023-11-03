## APP说明

> SSH Linux 服务器执行远程命令，用户、密码或认证文件都已经上传到mytools/ssh_clients/config.ini，只需要填写ip和命令即可

## 动作列表
* execute:通过输入参数使指定host执行命令，并返回执行结果 
### 执行命令

**参数：**

|  参数   | 类型  |  必填   |  备注  |
|  ----  | ----  |  ----  |  ----  |
| **host**  | text | `是` | 主机地址 |
| **shell**  | text | `是` | 执行命令 |

**返回值：**

```
执行命令的返回结果
```