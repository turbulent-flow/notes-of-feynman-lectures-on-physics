## 项目简介
Feynman Lectures On Physics[^1] 的学习笔记，站点[链接](https://turbulent-flow.github.io/notes-of-feynman-lectures-on-physics/)。

## 关于 AI 的应用
项目部署到 Github Pages[^1] 之后，我遇到了引用链接失效的问题，比如，原本仓库的一个图片链接为`/docs/assets/volume-1/fig-15-1.png`，部署之后应该变为`/{baseurl}/assets/volume-1/fig-15-1.png`。我重新梳理了一遍笔记整理的流程，假设一个大章节为一个单元：
1. 首先把一个章节通篇阅读一遍，搞清楚它讲的内容。
2. 然后再落笔，为了保持书写的连贯性，保持引用的原始路径。所有的引用分为三类：
   1. 图片的插入，比如，`![text](/docs/assets/volume-1/fig-15-1.png)`。
   2. 段落的引用，比如，`[text](/docs/volume-1/15-the-special-theory-of-relativity/15-1-the-principle-of-relativity.md#eq-15-1)`。
   3. 脚注的引用。
3. 在发布项目之前，需要对上述的第一小点与第二小点进行更正，写完章节后还需要更新对应的目录信息，便于导航：
   1. 图片的插入需要改为`![text]({{ "/assets/volume-1/fig-15-1.png" | relative_url }})`，这里使用了 Liquid Filter[^3]。
   2. 段落的引用需要改为`[text]({{ "/volume-1/15-the-special-theory-of-relativity/15-1-the-principle-of-relativity.html#eq-15-1" | relative_url }})`。
   3. 目录的信息涉及四类文件，除了下面的第一小点与第二小点，其余的需要更新：
      1. 主目录。
      2. 卷目录。
      3. 大章节目录，比如，`/docs/volume-1/15-the-special-theory-of-relativity/index.md`（这里使用了 YAML Front Matter[^4]和 Just the Docs 主题的导航[^5]），内容为：
        ```markdown
        ---
        layout: default
        title: 15. The Special Theory of Relativity
        parent: Volume 1
        nav_order: 15
        has_children: true
        ---
        ## 15. The Special Theory of Relativity
        ```
      4. 各小节目录，比如，`/docs/volume-1/15-the-special-theory-of-relativity/15-1-the-principle-of-relativity.md`的头部，内容为：
        ```markdown
        ---
        layout: default
        title: 15-1 The Principle of Relativity
        parent: 15. The Special Theory of Relativity
        nav_order: 1
        ---
        ```

AI 特别适合处理第三点的任务，换言之，我们可以通过使用生成式 AI ，比如，ChatGPT，生成满足要求的脚本，再把它加入到 git 钩子的自动化进程里（这里使用的是 git hooks 中的 pre-commit[^6]）。在安装钩子之后（具体可以参考[如何安装钩子](/readme.md#如何安装钩子)），在每次提交之前，可以做到如下三点：
   1. 自动修正失效的引用链接。
   2. 自动更新目录信息。
   3. 如果有新的`index.md`文件或者有修改的`.md`文件，自动把它们加入到 git 的暂存区[^7]。

## 如何安装钩子
若尚未安装钩子，请执行以下命令：
```shell
chmod +x utilities/install_git_hooks.sh
bash utilities/install_git_hooks.sh
chmod +x .git/hooks/pre-commit
```

[^1]: https://www.feynmanlectures.caltech.edu/
[^2]: https://docs.github.com/en/pages/getting-started-with-github-pages/what-is-github-pages#title-h1
[^3]: https://jekyllrb.com/docs/liquid/filters/
[^4]: https://jekyllrb.com/docs/front-matter/
[^5]: https://just-the-docs.com/docs/navigation/
[^6]: https://git-scm.com/book/en/v2/Customizing-Git-Git-Hooks#_committing_workflow_hooks
[^7]: https://git-scm.com/about/staging-area
