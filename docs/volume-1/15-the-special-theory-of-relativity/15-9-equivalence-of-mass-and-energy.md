---
layout: default
title: 15-9 Equivalence of Mass and Energy
parent: 15. The Special Theory of Relativity
nav_order: 9
---
上面的观测让爱因斯坦提出一个物体的质量可以表示地更加简单，相比公式 [15.1](/volume-1/15-the-special-theory-of-relativity/15-1-the-principle-of-relativity.md#eq-15-1) ，如果我们说质量等于整体的能量除以 $c^2$ 。如果等式 [15.11](/volume-1/15-the-special-theory-of-relativity/15-8-relativistic-dynamics.md#eq-15-11) 乘以 $c^2$ ，结果是

##### eq-15-12

$$mc^2=m_0c^2+\frac{1}{2}m_0v^2+\cdots$$

左边的元素表示物体的整体能量，我们意识到最后一个元素是普通的动能。爱因斯坦说这个很大的常数元素， $m_0c^2$ 是物体整体能量的一部分，一个非常重要的能量，被称为“静止能量”。

让我们与爱因斯坦一起遵循假定的结果，一个物体的能量总是等于 $mc^2$ 。很有趣的是，我们会得到公式 [15.1](/volume-1/15-the-special-theory-of-relativity/15-1-the-principle-of-relativity.md#eq-15-1) ，质量会随着速率发生变化，这就是截止目前我们所假设的。我们从静止开始，此时能量是 $m_0c^2$ 。然后我们应用一个作用力到该物体，使它移动，带来了动能。因为能量增加，所以质量会增加——它隐含在原始的假设中。只要作用力一直持续，能量和质量都会持续增加。我们已经看到（第 [13](/volume-1/13-work-and-potential-energy-A/) 章）能量相对时间的变化率等于作用力乘以速度，或者

##### eq-15-13

$$\frac{dE}{dt}=\boldsymbol{F} \cdot \boldsymbol{v}$$

我们也有（第 [9](/volume-1/9-newton's-laws-of-dynamics/) 章，等式 [9.1](/volume-1/9-newton's-laws-of-dynamics/9-1-momentum-and-force.md#eq-9-1)）， $F=d(mv)/dt$ 。当我们把这些关联与 $E$ 的定义放在一起，等式 [15.13](/volume-1/15-the-special-theory-of-relativity/15-9-equivalence-of-mass-and-energy.md#eq-15-13) 变为

##### eq-15-14

$$\frac{d(mc^2)}{dt}=\boldsymbol{v} \cdot \frac{d(m\boldsymbol{v})}{dt}$$

我们想求得这个等式中 $m$ 的解。我们首先运用数学技巧，在两边乘以 $2m$ ，等式变为

##### eq-15-15

$$c^2(2m)\frac{dm}{dt}=2m\boldsymbol{v} \cdot \frac{d(m\boldsymbol{v})}{dt}$$

为了避免求导，我们可以在等式两边积分。我们注意到 $(2m)dm/dt$ 是 $m^2$ 的时间导数， $(2m\boldsymbol{v}) \cdot d(m\boldsymbol{v})/dt$ 是 $(mv)^2$ 的时间导数。所以等式 [15.15](/volume-1/15-the-special-theory-of-relativity/15-9-equivalence-of-mass-and-energy.md#eq-15-15) 变为

##### eq-15-16

$$c^2\frac{d(m^2)}{dt}=\frac{dm^2v^2}{dt}$$

如果两个数值的导数相等，那么它们本身顶多相差一个常数，我们说是 $C$ 。于是我们写作

##### eq-15-17

$$m^2c^2=m^2v^2+C$$

我们需要更加清晰地定义常数 $C$ 。因为等式 [15.17](/volume-1/15-the-special-theory-of-relativity/15-9-equivalence-of-mass-and-energy.md#eq-15-17) 对于所有的速度都是正确的，我们选择一个特殊的情况，当 $v=0$ ，在该情况下质量是 $m_0$ ，我们得到

$$m_0^2c^2=0+C$$

我们可以在等式 [15.17](/volume-1/15-the-special-theory-of-relativity/15-9-equivalence-of-mass-and-energy.md#eq-15-17) 中使用 $C$ 的值，它变为

##### eq-15-18

$$m^2c^2=m^2v^2+m_0^2c^2$$

除以 $c^2$ ，再重新组织元素得到

$$m^2(1-v^2/c^2)=m_0^2$$

从中我们得到

##### eq-15-19

$$m=m_0/\sqrt{1-v^2/c^2}$$

这就是公式 [15.1](/volume-1/15-the-special-theory-of-relativity/15-1-the-principle-of-relativity.md#eq-15-1) ，它是达成等式 [15.12](/volume-1/15-the-special-theory-of-relativity/15-9-equivalence-of-mass-and-energy.md#eq-15-12) 中质量与能量统一的必要条件。

正常情况下，这些能量的变化表示在质量中微乎其微的改变，在大多数时间，我们没法从一些材料中生成太多的能量；但是在原子弹爆炸中，爆炸当量为 2 万吨 TNT ，比如，在爆炸之后的尘土要比最初参与爆炸的材料的质量轻 1 克，因为能量被释放了，也就是，释放的能量有 1 克的质量，根据关系式 $\Delta{E}=\Delta (mc^2)$ 。这个质量与能量相等的理论被实验完美地验证，物质湮灭——全都转换成能量：一个电子和一个反电子在静止时相遇，每一个的静止质量为 $m_0$ 。当它们相遇时会消解[^1]，并生成两束伽马射线，经测量，每一束的能量为 $m_0c^2$ 。这个实验直接佐证了，能量与一个粒子的静止质量有关。

[^1]: 「消解」是一个不稳定的原子核通过放射丢失能量的过程。参考资料：[wiki](https://en.wikipedia.org/wiki/Radioactive_decay)。
