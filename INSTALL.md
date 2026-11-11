# 安装与更新指南

适用版本：`0.1.0-draft.1`。这是一份可移植Skill，不是浏览器扩展、模型或独立软件。

## 1 使用Agent安装

优先复制README中的安装指令给你的Agent。Agent应确认：

1. 你能读取该私有仓库，Agent的运行环境也能读取。使用机构批准的GitHub登录或凭据管理方式；不要把密码或访问令牌贴进对话、URL或仓库。
2. 当前Agent支持哪种Skill安装机制。托管平台优先使用原生安装器；不能读写本地文件的聊天应用，不能靠复制路径完成安装。
3. 安装全部 `skills/optimize-pr-geo` 内容，不能只粘贴 `SKILL.md`。本仓库无需新建插件或MCP。
4. 当前版本文件完整；同名Skill存在时检查差异并备份，不静默覆盖。
5. 安装后能够加载名称 `optimize-pr-geo`，并说明Word生成和版式检查能力是否可用。

## 2 本地Codex或Claude Code安装

适用于在本机或可写工作环境运行的CLI Agent，不等同于ChatGPT或Claude网页账号安装。以下路径根据2026年11月10日读取的官方文档整理；环境有管理策略时，以该Agent当前官方机制为准。

| Agent | 个人全部项目 | 仅指定项目 |
|---|---|---|
| 本地Codex | `~/.agents/skills/optimize-pr-geo/` | `<项目目录>/.agents/skills/optimize-pr-geo/` |
| 本地Claude Code | `~/.claude/skills/optimize-pr-geo/` | `<项目目录>/.claude/skills/optimize-pr-geo/` |

Windows的 `~` 对应当前用户目录；不要使用另一个用户的目录。项目级安装在你的实际内容工作项目内，不一定是本仓库目录。

### 获取仓库

先完成GitHub访问授权，再运行：

```bash
git clone https://github.com/cici-kiterunner/PMI-marketing-skills.git
cd PMI-marketing-skills
```

如果平台提供下载文件夹方式，也可以下载后让Agent安装完整Skill目录。不要将仓库放入已安装Skill自身目录。

### 使用辅助脚本

脚本使用Python 3.9或更新版本的标准库，无网络操作、无包安装。macOS/Linux通常使用 `python3`；Windows可使用 `py -3` 替换示例中的 `python3`。

先预览个人级Codex安装位置：

```bash
python3 scripts/install_skill.py --agent codex --scope user --dry-run
```

执行个人级安装：

```bash
python3 scripts/install_skill.py --agent codex --scope user
```

Claude Code：

```bash
python3 scripts/install_skill.py --agent claude-code --scope user
```

项目级示例（替换为你的真实项目路径）：

```bash
python3 scripts/install_skill.py --agent codex --scope project --project-root "/path/to/your-project"
```

不使用脚本时，复制整个 `skills/optimize-pr-geo` 文件夹到上表所列目录。已有同名Skill时先比较与备份，不只覆盖主文件，否则容易出现旧版参考资料混用。

## 3 安装后验收

让Agent回答：

```text
请读取 optimize-pr-geo，简短告诉我：
1. 改稿前你会先反馈什么？
2. 理念、品牌、增长分别指什么？
3. 最终交付顺序和文档标记是什么？
4. 遇到没有依据的数据、产品介绍或培训招生诉求，你会怎么处理？
先不要修改稿件。
```

合格表现：先预判用户问题与三层传播目标；对照Word新增标黄、删除加删除线；随后给重点建议及下一步动作；不制造事实，不将培训招生等同于PMI考试报名或续证目标。还需用一篇你有权限处理的稿件验证文件交付；“能复述规则”不代表完整功能已测试。

若界面未显示Skill，先用完整名称显式调用或刷新Skill列表；仍未识别时检查安装位置、会话工作目录及宿主管理规则。不要到处重复安装同名副本。Word能力不足时，先补齐宿主文档能力或使用支持文件生成的Agent，不能把纯文本加粗当作黄色高亮。

## 4 更新与回退

查看 `VERSION`，在仓库目录中拉取已审阅版本：

```bash
git pull --ff-only
python3 scripts/install_skill.py --agent codex --scope user --dry-run
python3 scripts/install_skill.py --agent codex --scope user --replace
```

Claude Code或项目安装使用相同参数替换。`--replace`会把旧目录移到用户或项目根目录下的 `.agent-skill-backups/`，不会直接丢弃旧版。回退时先移走当前副本，再把对应备份目录恢复到原安装位置，并重新验收。托管平台按其版本管理机制回退。

## 5 常见问题

| 情况 | 处理 |
|---|---|
| 仓库404或无权限 | 核对地址、已登录账号与仓库授权；不要切换到陌生镜像或公开仓库 |
| 网页能开，Agent不能读 | 需要在Agent实际运行环境配置经批准的读取方式 |
| 只装了主文件 | 重新安装完整文件夹，包含references和版本元数据 |
| 同名版本冲突 | 确认要使用的范围，备份后仅保留正确副本 |
| 没有PMI原始指南 | 使用已附必要摘要并说明“部分可核”；团队另行提供有权限的原文，不能声称全文核验 |
| 没有Word生成或渲染能力 | 如实说明能力缺口，不伪称已生成或检查文档 |

## 官方参考

- [OpenAI本地Skill位置与构建说明](https://learn.chatgpt.com/docs/build-skills)
- [Claude Code Skills说明](https://code.claude.com/docs/en/skills)

未对其他Agent给出未经核验的固定路径；请其按自身官方Skill机制安装。
