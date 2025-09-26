---
layout: default
title: 11-7 Scalar Product of Vectors
parent: 11. Vectors
nav_order: 7
---
让我们更进一步学习向量的属性。很容易看出在空间中一步的长度在任何坐标系中都是相同的。如果一个步长 $\boldsymbol{r}$ 在一个坐标系中由 $x, y, z$ 表示，在另一个坐标系中由 $x^{'}, y^{'}, z^{'}$ 表示，那么距离 $r=|\boldsymbol{r}|$ 在两者中都是一样的。等式如下：

$$r=\sqrt{x^2+y^2+z^2}$$

$$r^{'}=\sqrt{x^{'2}+y^{'2}+z^{'2}}$$

我们想验证这两个值相等。不采用平方根会更加方便，所以让我们讨论下距离的平方；也就是，论证：

##### eq-11-17

$$x^2+y^2+z^2=x^{'2}+y^{'2}+z^{'2}$$

如果我们替换等式 [11.5](/volume-1/11-vectors/11-3-rotations.html#eq-11-5)，我们会发现确实如此。我们看到存在着其他类型的等式，对于任意两个坐标系，它们是成立的。

某种新的东西被包含在内。我们可以生成一个新的数值，一个 x、y 和 z 的函数，被称之为标量函数，它没有方向，但在两个系统中都是一样的。我们可以从一个向量中产生一个标量。我们发现了一个通用的规则。很明显就是我们刚刚提到的：把部分的平方相加。现在让我们定义一个新的东西，我们称它为 $\boldsymbol{a} \cdot \boldsymbol{a}$ 。它不是一个向量，而是一个标量；它是一个数字，在所有的坐标系中都是相同的，它被定义为向量的三个部分的平方之和：

##### eq-11-18

$$\boldsymbol{a} \cdot \boldsymbol{a}=a_x^2+a_y^2+a_z^2$$

你问道，“那它的坐标是什么？”它不依赖于坐标，在每一组坐标中，答案都是相同的。所以我们有了一个新的数值，一个新的不可变量或一个标量，它是由一个向量“平方后”产生的。对于任意两个向量 $\boldsymbol{a}$ 和 $\boldsymbol{b}$，我们可以定义下面的数值：

##### eq-11-19

$$\boldsymbol{a} \cdot \boldsymbol{b}=a_xb_x+a_yb_y+a_zb_z$$

这个系统不太像数学示例，在其中（数学的示例）一切都能被定义，然后我们不知道我们在谈论什么。实际上，数学的荣光在于我们不需要涉及我们讨论的是什么。定律、论述以及逻辑，它们都独立于“它是什么”。如果我们有其他的 objects，只要它们遵从相同的公理系统，就像欧几里得几何那样，然后如果我们产生了新的定义，并施以正确的逻辑，那么所有的结论都是正确的，无论对象是什么，没有任何差别。然而，在现实中，当我们划一条线，或者使用光束和经纬仪构建一条线段，就像我们在测绘中做的那样，我们会如欧几里得度量线段吗？不，我们会做近似；准星有宽度，但是几何线条没有，因此，欧几里得几何是否能用于测绘是一个物理问题，不是数学问题。站在一个实验的立场，而不是数学的立场，我们需要知道欧几里得定律能否应用于我们在测量陆地中所使用的那种几何；我们假设它可以，并且它做的很好；但是不够精确，因为我们的测绘线段不是真正的几何线段。欧几里得的那些线条，它们真的很抽象，能否应用到真实是一个跟经验相关的问题，bu shi yi ge
我们发现该数值，在主系统与非主系统中计算出的，同样保持一致。为了证明它，我们留意到 $\boldsymbol{a} \cdot \boldsymbol{a}, \boldsymbol{b} \cdot \boldsymbol{b}$ 和 $\boldsymbol{c} \cdot \boldsymbol{c}$ 是成立的，其中 $\boldsymbol{c}=\boldsymbol{a}+\boldsymbol{b}$ 。因此平方之和 $(a_x+b_x)^2+(a_y+b_y)^2+(a_z+b_z)^2$ 不会改变：

##### eq-11-20

$$(a_x+b_x)^2+(a_y+b_y)^2+(a_z+b_z)^2=(a_{x^{'}}+b_{x^{'}})^2+(a_{y^{'}}+b_{y^{'}})^2+(a_{z^{'}}+b_{z^{'}})^2$$

如果等式的两边都展开的话，会有等式 [11.19](/volume-1/11-vectors/11-7-scalar-product-of-vectors.html#eq-11-19) 中出现的叉积，也会有 $\boldsymbol{a}$ 和 $\boldsymbol{b}$ 部分的平方之和。等式 [11.18](/volume-1/11-vectors/11-7-scalar-product-of-vectors.html#eq-11-18) 中的元素不会改变，剩下的叉积元素（[11.19](/volume-1/11-vectors/11-7-scalar-product-of-vectors.html#eq-11-19)）也不会改变。

数值 $\boldsymbol{a} \cdot \boldsymbol{b}$ 被称之为两个向量的标量乘积，它拥有蛮多好玩且有用的属性。譬如，很容易证明：

##### ea-11-21

$$\boldsymbol{a} \cdot (\boldsymbol{b}+\boldsymbol{c})=\boldsymbol{a} \cdot \boldsymbol{b}+\boldsymbol{a} \cdot \boldsymbol{c}$$

同样地，有一个简单的几何方式去计算 $\boldsymbol{a} \cdot \boldsymbol{b}$ ，而不用计算 $\boldsymbol{a}$ 和 $\boldsymbol{b}$ 的部分： $\boldsymbol{a} \cdot \boldsymbol{b}$ 是 $\boldsymbol{a}$ 的长度与 $\boldsymbol{b}$ 的长度的乘积乘以它们之间夹角的余弦。为什么？假设我们选择了一个特别的坐标系，其中 x-轴坐落在 $\boldsymbol{a}$ 上；在那些情形中，仅有的 $\boldsymbol{a}$ 的部分是 $a_x$ ，那么它的长度当然是整个 $\boldsymbol{a}$ 的。因此等式 [11.19](/volume-1/11-vectors/11-7-scalar-product-of-vectors.html#eq-11-19) 简化为 $\boldsymbol{a} \cdot \boldsymbol{b}=a_xb_x$ ，也就是， $\boldsymbol{a}$ 的长度乘以 $\boldsymbol{b}$ 在 $\boldsymbol{a}$ 的方向上的部分， $b\cos{\theta}$ :

$$\boldsymbol{a} \cdot \boldsymbol{b}=ab\cos{\theta}$$

因此，在那个特别的坐标系中，我们证明了 $\boldsymbol{a} \cdot \boldsymbol{b}$ 是 $\boldsymbol{a}$ 的长度乘以 $\boldsymbol{b}$ 的长度乘以 $\cos{\theta}$ 。如果它在一个坐标系成立，那么它在所有的都成立，因为 $\boldsymbol{a} \cdot \boldsymbol{b}$ 独立于坐标系；这是我们的论证。

点积好在哪？在物理中有哪些示例是我们可以用到它的？在第四章中动能被称为 $\frac{1}{2}mv^2$ ，但是如果物体在空间中运动，速度应该在 x-方向上、y-方向上和z-方向上平方，所以依照向量分析，动能公式为：

##### eq-11-22

$$K.E.=\frac{1}{2}mv^2=\frac{1}{2}m(\boldsymbol{v} \cdot \boldsymbol{v})=\frac{1}{2}m(v_x^2+v_y^2+v_z^2)$$

能量没有方向。动量拥有方向；它是一个向量，它是质量乘以速度向量。

点积的另一个例子是由一个作用力做的功，当某物从一个地方被推到其他地方。我们还没有定义做功，但是它等价于能量的改变，重量被举起，当一个作用力 $\boldsymbol{F}$ 作用在一段位移的距离 $\boldsymbol{s}$ 上：

##### eq-11-23

$$Work=\boldsymbol{F} \cdot \boldsymbol{s}$$

有些时候在特定的方向上谈论一个向量的部分会非常方便（比如垂直方向，因为那是引力的方向）。出于这样的目的，在我们想要研究的方向上发明一个单位向量变得很有用。单位向量的意思是它与自身的点积是 unity 。我们称其为 $\boldsymbol{i}$ ； $\boldsymbol{i} \cdot \boldsymbol{i}=1$ 。如果我们想要某个向量在 $\boldsymbol{i}$ 的方向上的部分，我们发现点积 $\boldsymbol{a} \cdot \boldsymbol{i}$ 是 $a\cos{\theta}$ ，也就是， $\boldsymbol{a}$ 在 $\boldsymbol{i}$ 的方向上的部分。这是一个很棒的方式获取部分；实际上，我们可以得到所有的部分并写出一个相当有趣的公式。假设在一个给定的坐标系， x、y 和 z 中，我们发明了三个向量： $\boldsymbol{i}$ ，一个在 x 方向上的单位向量； $\boldsymbol{j}$ ，一个在 y 方向上的单位向量； $\boldsymbol{k}$ ，一个在 z 方向上的单位向量。 $\boldsymbol{i} \cdot \boldsymbol{i}=1$ 。 $\boldsymbol{i} \cdot \boldsymbol{j}$ 呢？当两个向量垂直，它们的点积是零。因此：

##### eq-11-24

$$\boldsymbol{i} \cdot \boldsymbol{i}=1$$

$$\boldsymbol{i} \cdot \boldsymbol{j}=0 \quad \boldsymbol{j} \cdot \boldsymbol{j}=1$$

$$\boldsymbol{i} \cdot \boldsymbol{k}=0 \quad \boldsymbol{j} \cdot \boldsymbol{k}=0 \quad \boldsymbol{k} \cdot \boldsymbol{k}=1$$

现在任意的向量都能写作：

##### eq-11-25

$$\boldsymbol{a}=a_xi+a_yj+a_zk$$

这就意味着我们可以从一个向量的部分过渡到向量本身。

向量的讨论并没有终结，我们现在可以去往更深的地方，我们应该首先在物理情景中运用迄今为止所讨论的一些想法。然后，当我们正确地掌握了基础的部分，我们会更加容易地深入其中，而不会过于困扰。我们稍后会定义另一种两个向量的乘积，叫作向量乘积，写作 $\boldsymbol{a} \times \boldsymbol{b}$ 。我们在后面的章节会展开讨论。
