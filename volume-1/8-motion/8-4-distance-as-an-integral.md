##### table-8-4
![一个坠落球体的速度表](/assets/volume-1/table-8-4.png)

现在我们讨论一下逆向的问题。如果我们有一个从零开始、在不同时间的速率表。如 Table.8-4 所示的坠落的球体。对于汽车的速度，一个类似的表可以被构建出来，通过车速表记录其每分钟或半分钟的值。如果我们知道一辆汽车在任意时间行驶地有多快，我们是否能够确定它跑得有多远？这个问题就是我们之前解决的逆向；我们给定速度，寻求距离。如果我们知道速率，如何求得距离？如果汽车的速率不是常数，就像一个女士有一刻行驶的速率是 60 英里一小时，然后减速、加速，等等，那么我们该如何知道她跑了多远？这很简单。我们使用相同的点子，把距离描述为无穷小量。让我们说，“在头一秒，她的速率是这样的，通过公式 $\Delta{s}=v\Delta{t}$ 我们可以计算出她以那个速率在一秒中行驶的距离。”她在下一秒的速率几乎相同，但有些细微的差别；我们可以通过新的速率乘以时间计算出她在下一秒行驶的距离。我们一直延续到运动的结束。我们现在有一些微小的距离，总距离就是这些小片儿的和。也就是说，距离是这些速度乘以时间的和，或者 $s=\sum{v\Delta{t}}$ ，其中希腊字符 $\Sigma$ （Sigma）用于表示加法。为了更加精确，我们说它是在特定时间的速度，也就是 i-th time 的，乘以 $\Delta{t}$ 的和。

$$s=\sum_{i}v(t_i)\Delta{t}$$

时间的规则是 $t_{i+1}=t_i+\Delta{t}$ 。然而，这里的距离不正确，因为速度在时间间隔 $\Delta{t}$ 内有变化。如果我们选取的时间足够小，和会很精确，所以我们会让它们越来越小，以达到我们满意的程度。真正的 s 是

$$s=\lim_{\Delta{t} \to 0}\sum_{i}v(t_i)\Delta{t}$$

数学家为这个极限发明了一个符号，类比于微分的符号。 $\Delta$ 转变为 $d$ ，提醒我们时间极小；速度被称之为在时间 $t$ 处的 $v$ ，加法被写作一个大“s”， $\int$ （来自于拉丁文 summa），现在被用作积分符号。因此公式是

$$s=\int{v(t)dt}$$

把这些元素加在一起的过程叫作积分，它是求导的逆向过程。这个积分的导数是 $v$ ，所以操作符（ $d$ ）移除了其他（ $\int$ ）。我们可以通过求导公式的逆运算来获得积分公式。所以可以通过求导各种函数获得自己的积分表。对于每一个微分公式，如果我们把它掉个儿就能得到积分公式。

每一个函数都能求导，也就是，该进程可以以代数的形式实现，进而变成一个确定的函数。但是对于任意的积分不太可能如我们所愿以一种简单的方式写成一个分析的值。你可以计算它，比如说，通过做上面的求和，然后使用更小的时间间隔 $\Delta{t}$ 再做一次，再使用更小的时间间隔做一次，直到它趋近于正确。通常情况下，给出某个函数，不太可能寻得其积分。有人总是想在求导时给出满意的函数，但是他们做不到，或许没有办法表示那些给定名字的函数。