# Gemini Cookie 配置说明

## 📋 目录
- [快速开始（推荐）](#快速开始推荐)
- [手动配置（备选）](#手动配置备选)
- [工作原理](#工作原理)
- [常见问题](#常见问题)

---

## 🚀 快速开始（推荐）

### 方法1: 自动解析 Cookie（最简单）

1. **访问 Gemini 并登录**
   - 打开 https://gemini.google.com
   - 使用你的 Google 账号登录

2. **获取完整 Cookie**
   - 按 `F12` 打开开发者工具
   - 切换到 `Network` 标签
   - 在 Gemini 中发送一条消息（任意内容）
   - 找到任意一个请求（如 `StreamGenerate`），点击查看
   - 在 `Request Headers` 中找到 `Cookie` 字段
   - 复制完整的 Cookie 内容（可能很长，包含多个键值对）

3. **粘贴到配置文件**
   - 打开 `config/gemini_cookies.json`
   - 将复制的 Cookie 粘贴到 `cookies_raw` 字段
   - 保存文件

4. **完成！**
   - 重启 ComfyUI 或重新加载节点
   - 系统会自动：
     - 提取 `__Secure-1PSID` 和 `__Secure-1PSIDTS`
     - 访问 Gemini 页面
     - 自动获取 `SNlM0e` 和 `PUSH_ID`
     - 更新配置文件

### Cookie 示例格式

```
__Secure-1PSID=xxxxxxxxxx; __Secure-1PSIDTS=xxxxxxxxxx; SAPISID=xxxxxxxxxx; APISID=xxxxxxxxxx; ...
```

---

## 🔧 手动配置（备选）

如果自动解析失败，可以手动填写各字段：

### 1. 获取 __Secure-1PSID 和 __Secure-1PSIDTS

1. F12 → `Application` → `Cookies` → `https://gemini.google.com`
2. 找到并复制 `__Secure-1PSID` 的值
3. 找到并复制 `__Secure-1PSIDTS` 的值
4. 粘贴到配置文件对应字段

### 2. 获取 SNlM0e（AT Token）

**方法A：从 Network 获取**
1. F12 → `Network` → 发送消息
2. 找到 `StreamGenerate` 请求
3. 查看 `Form Data` 中的 `at` 字段
4. 复制值粘贴到配置文件的 `snlm0e` 字段

**方法B：从页面源码获取**
1. 按 `Ctrl+U` 查看页面源代码
2. 按 `Ctrl+F` 搜索 `SNlM0e`
3. 找到类似 `"SNlM0e":"xxxxxxxxxx"` 的内容
4. 复制引号内的值

### 3. 获取 PUSH_ID

1. F12 → `Network` → 发送一条消息
2. 找到上传图片相关的请求（如果有）
3. 查看请求头中的 `push-id` 字段
4. 格式为 `feeds/xxxxxxxxxxxxx`
5. 复制到配置文件的 `push_id` 字段

---

## ⚙️ 工作原理

### 自动解析流程

```
粘贴 cookies_raw
    ↓
系统检测到内容
    ↓
步骤1: 解析 Cookie 字符串
    → 提取 __Secure-1PSID
    → 提取 __Secure-1PSIDTS
    ↓
步骤2: 使用 Cookie 访问 Gemini 页面
    → 从 HTML 提取 SNlM0e
    → 从 HTML 提取 PUSH_ID
    ↓
步骤3: 更新配置文件
    → 填充所有字段
    → 保存到 gemini_cookies.json
    ↓
完成！后续直接使用
```

### 配置文件结构

```json
{
  "cookies_raw": "粘贴完整Cookie",  // 自动解析源
  "secure_1psid": "自动填充",      // 从 cookies_raw 提取
  "secure_1psidts": "自动填充",    // 从 cookies_raw 提取
  "snlm0e": "自动填充",            // 从页面获取
  "push_id": "自动填充",           // 从页面获取
  "model_ids": { ... }              // 模型 ID 映射
}
```

---

## ❓ 常见问题

### Q1: Cookie 过期了怎么办？

**答**：重新获取并粘贴到 `cookies_raw` 字段即可。Cookie 通常几周后会过期。

### Q2: 自动解析失败怎么办？

**答**：
1. 检查网络连接
2. 确认 Cookie 是否完整（包含 `__Secure-1PSID`）
3. 查看控制台日志查找错误信息
4. 使用手动配置方式

### Q3: 需要填写所有字段吗？

**答**：
- 使用自动解析：只需填写 `cookies_raw`
- 手动配置：必须填写 `secure_1psid`、`snlm0e`、`push_id`
- `secure_1psidts` 推荐但非必需

### Q4: 为什么需要 PUSH_ID？

**答**：`push_id` 用于上传图片到 Gemini 服务器。如果不使用图片功能，可以不填。

### Q5: 配置文件安全吗？

**答**：
- ⚠️ **重要**：配置文件包含你的 Google 账号 Cookie，属于敏感信息
- 不要分享给他人
- 不要提交到公开的代码仓库
- 建议将 `config/gemini_cookies.json` 添加到 `.gitignore`

### Q6: 多次运行会重复解析吗？

**答**：不会。系统只在检测到 `cookies_raw` 有内容且其他字段为空时才自动解析。解析后会保存结果，后续直接使用。

### Q7: 可以同时使用多个账号吗？

**答**：目前不支持。如需切换账号，重新粘贴新账号的 Cookie 即可。

---

## 📝 配置示例

### 自动解析配置（推荐）

```json
{
  "cookies_raw": "__Secure-1PSID=abcd1234...; __Secure-1PSIDTS=efgh5678...; SAPISID=...",
  "secure_1psid": "",
  "secure_1psidts": "",
  "snlm0e": "",
  "push_id": ""
}
```

保存后系统自动填充：

```json
{
  "cookies_raw": "__Secure-1PSID=abcd1234...; __Secure-1PSIDTS=efgh5678...; SAPISID=...",
  "secure_1psid": "abcd1234...",
  "secure_1psidts": "efgh5678...",
  "snlm0e": "AUTO_EXTRACTED_TOKEN",
  "push_id": "feeds/auto_extracted_id"
}
```

### 手动配置

```json
{
  "cookies_raw": "",
  "secure_1psid": "手动复制的值",
  "secure_1psidts": "手动复制的值",
  "snlm0e": "手动复制的值",
  "push_id": "feeds/手动复制的ID"
}
```

---

## 🎯 快速检查清单

使用前确认：
- [ ] `secure_1psid` 不为空
- [ ] `snlm0e` 不为空
- [ ] `push_id` 不为空（如果需要使用图片功能）
- [ ] `push_id` 格式为 `feeds/xxxxxx`

如果自动解析后某些字段仍为空，请使用手动配置方式补充。

---

**提示**：配置完成后，在 ComfyUI 中使用 "JM Gemini Reverse Engineering" 节点即可开始生成图片！
