#!/usr/bin/env python3
from pathlib import Path
import json, re

root = Path('/workspace/doubaoWork')
path = root / 'guide-data.js'
raw = path.read_text(encoding='utf-8')
data = json.loads(re.sub(r';\s*$', '', re.sub(r'^window\.BOOK_DATA\s*=\s*', '', raw, count=1)))

META = {
    'c01': {
        'group': 'base', 'core': True, 'en': 'Artificial Intelligence',
        'aka': 'AI',
        'aliases': ['AI', 'Artificial Intelligence', 'A.I.', '人工智慧'],
        'related': ['c02', 'c03', 'c04'],
        'text': '泛指让计算机完成识别、生成、预测、规划等任务的技术集合。书中的AI不是具有统一意图的“人”，不同模型、工具和产品必须分别核验。'
    },
    'c02': {
        'group': 'base', 'core': True, 'en': 'Generative AI',
        'aka': '',
        'aliases': ['Generative AI', 'AIGC', '生成式人工智能', '文生图', '文生视频'],
        'related': ['c01', 'c03', 'c07'],
        'text': '根据输入和既有模式生成文字、图像、音频、视频或代码的系统。它擅长形成候选内容，但输出流畅不等于事实正确。'
    },
    'c03': {
        'group': 'base', 'core': True, 'en': 'Large Model',
        'aka': 'LLM',
        'aliases': ['LLM', 'Large Language Model', '大语言模型', '基础模型'],
        'related': ['c01', 'c02', 'c04'],
        'text': '通过大规模数据和计算训练、能处理多类语言或内容任务的基础模型。它提供理解与生成能力，但不是实时更新的事实数据库，也不能替代来源核验。'
    },
    'c04': {
        'group': 'base', 'core': True, 'en': 'Agent',
        'aka': 'Agent',
        'aliases': ['Agent', '代理', '智能代理', '自主代理'],
        'related': ['c05', 'c08', 'c06'],
        'text': '围绕目标规划步骤，并在条件允许时调用工具推进任务的系统。能执行多步操作不等于可以独立承担判断和责任。'
    },
    'c05': {
        'group': 'base', 'core': True, 'en': 'Office Agent',
        'aka': '',
        'aliases': ['办公智能体', '办公代理', 'Office Agent', '豆包工作'],
        'related': ['c04', 'c11', 'c12'],
        'text': '本书对面向办公任务、能读取材料、调用办公工具并形成交付物的一类智能体系统的统称。强调任务链，而不是某一个按钮或模型。'
    },
    'c06': {
        'group': 'task', 'core': True, 'en': 'Context',
        'aka': 'Context',
        'aliases': ['Context', '背景信息', '企业上下文', '任务上下文'],
        'related': ['c11', 'c05', 'c18'],
        'text': '系统理解当前任务所需的背景，包括指令、材料、身份、历史状态和组织规则。上下文越多不一定越好，错误、过期或越权材料会把任务带偏。'
    },
    'c07': {
        'group': 'base', 'core': True, 'en': 'Multimodal',
        'aka': '',
        'aliases': ['Multimodal', '多模态生成', '图文', '音视频'],
        'related': ['c02', 'c25'],
        'text': '能够处理文字之外的图片、语音、音频或视频。支持某种格式只说明系统能够读取或生成，并不保证识别、事实和版权状态自动正确。'
    },
    'c08': {
        'group': 'run', 'core': True, 'en': 'Tool Use',
        'aka': '',
        'aliases': ['Tool Use', 'Function Calling', 'function calling', '调用工具', '工具使用'],
        'related': ['c04', 'c10', 'c21'],
        'text': '系统使用搜索、计算、文件、浏览器或其他软件完成动作。每次调用仍受产品能力、授权和任务边界限制。'
    },
    'c09': {
        'group': 'run', 'core': True, 'en': 'Workflow',
        'aka': '',
        'aliases': ['Workflow', '流程', '业务流程', '协作流程'],
        'related': ['c13', 'c26', 'c27'],
        'text': '为完成一项工作而组织起来的步骤、交接关系和检查规则。它不只是一串操作，还要说明输入、异常、责任和交付标准。'
    },
    'c10': {
        'group': 'run', 'core': True, 'en': 'Runtime',
        'aka': '',
        'aliases': ['Runtime', '运行环境', '本地', '云端', '浏览器'],
        'related': ['c08', 'c21', 'c15'],
        'text': '任务实际运行并接触文件或系统的位置，例如本地电脑、云端或浏览器。环境不同，可访问的数据、持续时间和风险也不同。'
    },
    'c11': {
        'group': 'task', 'core': True, 'en': 'Instruction',
        'aka': '',
        'aliases': ['Prompt', 'prompt', '提示词', '指令模板', '任务说明'],
        'related': ['c06', 'c12', 'c05'],
        'text': '用户对一次任务的说明，至少交代目标、材料和期望结果；长任务还要补充边界、检查点和失败处理。指令不是免除核验责任的“口令”。'
    },
    'c12': {
        'group': 'task', 'core': True, 'en': 'Acceptance Criteria',
        'aka': '',
        'aliases': ['Acceptance Criteria', '验收', '完成标准', '核对标准'],
        'related': ['c11', 'c13', 'c23'],
        'text': '判断成果是否可以采用的一组可观察条件，例如数字能复算、文档无遗漏、格式正确、外发对象已确认。标准越具体，返工和争议越容易定位。'
    },
    'c13': {
        'group': 'run', 'core': True, 'en': 'Checkpoint',
        'aka': '',
        'aliases': ['Checkpoint', '检查节点', '确认点', '中间检查'],
        'related': ['c14', 'c15', 'c12'],
        'text': '任务推进到关键位置时保存状态并确认的节点。便于在错误扩大前暂停，也为失败后继续执行提供起点。'
    },
    'c14': {
        'group': 'run', 'core': True, 'en': 'Human Takeover',
        'aka': 'HITL',
        'aliases': ['HITL', 'Human-in-the-loop', '人工确认', '接管', '人机协同'],
        'related': ['c13', 'c15', 'c21'],
        'text': '系统遇到登录验证、歧义、异常或高影响决定时，把控制交回给人。接管不是自动化失败，而是受控流程的一部分。'
    },
    'c15': {
        'group': 'run', 'core': True, 'en': 'Rollback and Recovery',
        'aka': '',
        'aliases': ['Rollback', '回滚', '恢复', '还原', 'undo'],
        'related': ['c13', 'c14', 'c22'],
        'text': '回滚是退回到此前状态；恢复是让业务在异常后重新可用。发送和公开发布未必能完全回滚，因此执行前仍需确认。'
    },
    'c16': {
        'group': 'extend', 'core': True, 'en': 'Skill',
        'aka': 'Skill',
        'aliases': ['Skill', 'SKILL.md', '自定义技能', '技能包'],
        'related': ['c11', 'c12', 'c17'],
        'text': '把验证过的输入条件、处理步骤、异常分支和验收标准封装为可复用方法。一次偶然成功的指令还不能称为稳定技能。'
    },
    'c17': {
        'group': 'extend', 'core': True, 'en': 'Connector',
        'aka': '',
        'aliases': ['Connector', '连接', '外部系统', '系统接入'],
        'related': ['c18', 'c21', 'c16'],
        'text': '让任务在授权范围内读取或写入外部系统的连接能力。连接器缩短数据搬运，却同时引入账号、权限、接口变化和退出管理问题。'
    },
    'c18': {
        'group': 'extend', 'core': True, 'en': 'Model Context Protocol',
        'aka': 'MCP',
        'aliases': ['MCP', 'Model Context Protocol', '模型上下文协议'],
        'related': ['c17', 'c08', 'c21'],
        'text': '让AI应用以相对统一的方式发现和使用外部工具或数据源的协议。协议解决连接方式，不会自动解决认证、权限和合规。'
    },
    'c19': {
        'group': 'extend', 'core': True, 'en': 'Work Partner',
        'aka': '',
        'aliases': ['Partner', '伙伴', '专业角色', '角色化智能体'],
        'related': ['c20', 'c16', 'c05'],
        'text': '围绕研究、分析、开发或设计等专业角色组织的能力入口。角色名称不能代替对工具、输入和交付质量的核验。'
    },
    'c20': {
        'group': 'extend', 'core': True, 'en': 'Work Squad',
        'aka': '',
        'aliases': ['Squad', '多智能体', '工作队', '协作智能体'],
        'related': ['c19', 'c09', 'c12'],
        'text': '多个智能体围绕同一成果分担子任务的协作方式。只有分工清楚、可独立验收且整合成本可控时才可能有价值。'
    },
    'c21': {
        'group': 'govern', 'core': True, 'en': 'Least Privilege',
        'aka': '',
        'aliases': ['Least Privilege', '最小授权', '权限最小化', '授权范围'],
        'related': ['c10', 'c22', 'c17'],
        'text': '只授予完成当前任务所必需的账号、目录、数据和操作能力，并限定范围与时间。权限越大并不代表任务越容易成功。'
    },
    'c22': {
        'group': 'govern', 'core': True, 'en': 'Audit Trail',
        'aka': '',
        'aliases': ['Audit', '审计', '操作留痕', '日志', '追溯'],
        'related': ['c21', 'c15', 'c12'],
        'text': '记录谁在何时使用了什么输入、执行了哪些关键动作、产生了什么结果以及由谁确认，以便事后还原过程。'
    },
    'c23': {
        'group': 'govern', 'core': True, 'en': 'Evidence Chain',
        'aka': '',
        'aliases': ['Evidence', '证据', '来源追溯', '可追溯', '交叉核验'],
        'related': ['c12', 'c24', 'c02'],
        'text': '从结论回到原始来源、提取内容、处理步骤和判断依据的可追溯关系。多个网页重复同一消息不等于独立证据。'
    },
    'c24': {
        'group': 'govern', 'core': True, 'en': 'Metric Definition',
        'aka': '',
        'aliases': ['口径', '指标定义', '统计口径', '数据定义'],
        'related': ['c23', 'c12'],
        'text': '一个指标的定义、时间范围、统计对象、计算方法和排除规则。名称相同但口径不同的数字不能直接比较或合并。'
    },
    'c25': {
        'group': 'deliver', 'core': False, 'en': 'Presentation',
        'aka': 'PPT',
        'aliases': ['PPT', 'PowerPoint', '幻灯片', '演示稿', '汇报材料'],
        'related': ['c07', 'c12'],
        'text': '服务于一次具体沟通的页面系统。页数不是目标；叙事是否清楚、证据是否可靠、视觉是否帮助理解，才决定质量。'
    },
    'c26': {
        'group': 'run', 'core': False, 'en': 'Scheduled Task',
        'aka': '',
        'aliases': ['Cron', '自动化', '周期任务', '定时', '调度'],
        'related': ['c09', 'c14', 'c21'],
        'text': '按稳定周期和规则持续运行的工作。人的角色从逐次操作转向规则设计、结果检查和异常处理。'
    },
    'c27': {
        'group': 'deliver', 'core': False, 'en': 'Job Workflow',
        'aka': '',
        'aliases': ['流程卡', '岗位工作流', '岗位卡片', '业务场景'],
        'related': ['c09', 'c12', 'c16'],
        'text': '把高频工作拆成输入、执行、检查和交付，并标明AI职责、人工责任与效果基线。工具能力只有进入具体岗位才形成可衡量价值。'
    },
}

for c in data['concepts']:
    extra = META[c['id']]
    c.update(extra)

path.write_text('window.BOOK_DATA = ' + json.dumps(data, ensure_ascii=False, indent=2) + ';\n', encoding='utf-8')
print(json.dumps({
    'concepts': len(data['concepts']),
    'core': sum(1 for c in data['concepts'] if c.get('core')),
    'groups': sorted({c['group'] for c in data['concepts']}),
}, ensure_ascii=False))
