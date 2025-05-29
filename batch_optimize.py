#!/usr/bin/env python3
"""
批量优化逻辑学导论书籍的视觉样式
将统一的专业设计系统应用到所有章节文件中
"""

import os
import re
import glob

def optimize_file(file_path):
    """优化单个文件的视觉样式"""
    print(f"正在优化: {file_path}")

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # 备份原文件
        backup_path = file_path + '.backup'
        with open(backup_path, 'w', encoding='utf-8') as f:
            f.write(content)

        # 应用优化规则
        content = apply_optimizations(content)

        # 写入优化后的内容
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)

        print(f"✅ 优化完成: {file_path}")

    except Exception as e:
        print(f"❌ 优化失败: {file_path} - {e}")

def apply_optimizations(content):
    """应用视觉优化规则"""

    # 1. 替换引言部分
    content = re.sub(
        r'\\begin\{quotation\}\s*\\textit\{([^}]+)\}\s*\\end\{quotation\}',
        r'\\begin{logicbox}[title=引言]\n\\textit{\1}\n\\end{logicbox}',
        content,
        flags=re.MULTILINE | re.DOTALL
    )

    # 2. 替换章节导读
    content = re.sub(
        r'\\begin\{quote\}\s*\\textit\{([^}]+)\}\s*\\end\{quote\}',
        r'\\begin{logicbox}[title=章节导读]\n\\textit{\1}\n\\end{logicbox}',
        content,
        flags=re.MULTILINE | re.DOTALL
    )

    # 3. 标记重要术语
    important_terms = [
        '逻辑学', '命题', '论证', '前提', '结论', '推理', '演绎', '归纳',
        '有效性', '可靠性', '真值', '谬误', '定义', '概念', '判断',
        '三段论', '直言命题', '复合命题', '条件命题', '析取命题', '合取命题',
        '否定', '矛盾', '反对', '下反对', '差等', '换位', '换质', '对当',
        '归纳推理', '演绎推理', '类比推理', '因果推理', '统计推理',
        '假设', '理论', '证明', '反驳', '批判性思维', '或然性', '必然性',
        '解析', '图示', '结论指示词', '前提指示词', '省略三段论',
        '信念歧见', '态度歧见', '一致', '歧见', '语境', '反诘问句',
        '演绎论证', '归纳论证', '有效', '无效', '古典逻辑', '现代符号逻辑'
    ]

    for term in important_terms:
        # 只替换加粗的术语
        content = re.sub(
            rf'\\textbf\{{{re.escape(term)}\}}',
            rf'\\logicterm{{{term}}}',
            content
        )

    # 4. 标记强调内容
    emphasis_words = [
        '正确', '错误', '真的', '假的', '有效', '无效', '可靠', '不可靠',
        '必然', '可能', '或然', '确定', '不确定', '一致', '矛盾',
        '决定性地', '绝对必然地', '或然性地', '充分一致', '完全对立',
        '分立性支持', '托架线', '隐含前提', '单独论证', '串联式论证',
        '浓缩论证', '交织式论证', '多重复合论证'
    ]

    for word in emphasis_words:
        content = re.sub(
            rf'\\textbf\{{{re.escape(word)}\}}',
            rf'\\logicemph{{{word}}}',
            content
        )

    # 5. 标记警告内容
    warning_words = [
        '注意', '警告', '错误', '谬误', '陷阱', '误区', '问题', '无效的'
    ]

    for word in warning_words:
        content = re.sub(
            rf'\\textbf\{{{re.escape(word)}\}}',
            rf'\\logicwarn{{{word}}}',
            content
        )

    # 6. 替换总结框 - 更全面的模式匹配
    patterns = [
        # 标准总结框
        (r'\\begin\{center\}\s*\\fbox\{\\parbox\{[^}]+\}\{\s*\\centering\s*\\textbf\{([^}]+)\}\\\\([^}]+)\}\}\s*\\end\{center\}',
         r'\\chaptersummary{\n\2\n}'),
        # 简单总结框
        (r'\\begin\{center\}\s*\\fbox\{\\parbox\{[^}]+\}\{\s*\\centering\s*([^}]+)\}\}\s*\\end\{center\}',
         r'\\chaptersummary{\n\1\n}'),
        # 其他格式的总结框
        (r'\\begin\{center\}\s*\\textbf\{([^}]+)\}\s*\\end\{center\}',
         r'\\chaptersummary{\n\1\n}')
    ]

    for pattern, replacement in patterns:
        content = re.sub(pattern, replacement, content, flags=re.MULTILINE | re.DOTALL)

    # 7. 优化例题框
    content = re.sub(
        r'\\begin\{displayquote\}\s*\\textbf\{例([^}]+)\}([^\\]+)\\end\{displayquote\}',
        r'\\begin{examplebox}[title=例\1]\n\2\n\\end{examplebox}',
        content,
        flags=re.MULTILINE | re.DOTALL
    )

    # 8. 优化定义框
    content = re.sub(
        r'\\begin\{displayquote\}\s*\\textbf\{定义[：:]([^}]+)\}([^\\]+)\\end\{displayquote\}',
        r'\\begin{theorembox}[title=定义：\1]\n\2\n\\end{theorembox}',
        content,
        flags=re.MULTILINE | re.DOTALL
    )

    # 9. 优化定理框
    content = re.sub(
        r'\\begin\{displayquote\}\s*\\textbf\{定理[：:]([^}]+)\}([^\\]+)\\end\{displayquote\}',
        r'\\begin{theorembox}[title=定理：\1]\n\2\n\\end{theorembox}',
        content,
        flags=re.MULTILINE | re.DOTALL
    )

    return content

def main():
    """主函数"""
    print("🚀 开始批量优化逻辑学导论书籍...")

    # 获取所有需要优化的文件
    files_to_optimize = []

    # 章节文件
    for i in range(1, 15):  # chapter1 到 chapter14
        chapter_files = glob.glob(f'chapter{i}/*.tex')
        files_to_optimize.extend(chapter_files)

    # summary文件
    summary_files = glob.glob('chapter*/summary.tex')
    files_to_optimize.extend(summary_files)

    # part文件
    part_files = glob.glob('part*.tex')
    files_to_optimize.extend(part_files)

    print(f"📁 找到 {len(files_to_optimize)} 个文件需要优化")

    # 优化每个文件
    for file_path in files_to_optimize:
        optimize_file(file_path)

    print("🎉 批量优化完成！")
    print("📝 所有原文件已备份为 .backup 文件")
    print("🔧 建议运行 xelatex main.tex 来编译查看效果")

if __name__ == "__main__":
    main()
