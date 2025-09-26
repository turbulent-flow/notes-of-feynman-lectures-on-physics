---
layout: default
title: 11-6 Newton's Laws in Vector Notation
parent: 11. Vectors
nav_order: 6
---
为了以向量的形式书写牛顿定律，我们还要再走一步，定义加速度向量。它是速度向量的时间导数，可以被简单地阐释为它的部分是 x、y 和 z 相对于 t 的二阶导数：

##### eq-11-11

$$a=\frac{d\boldsymbol{v}}{dt}=(\frac{d}{dt})(\frac{d\boldsymbol{r}}{dt})=\frac{d^2\boldsymbol{r}}{dt^2}$$

##### eq-11-12

$$a_x=\frac{dv_x}{dt}=\frac{d^2x}{dt^2}$$

$$a_y=\frac{dv_y}{dt}=\frac{d^2y}{dt^2}$$

$$a_z=\frac{dv_z}{dt}=\frac{d^2z}{dt^2}$$

基于这个定义，牛顿定律可以写作：

##### eq-11-13

$$m\boldsymbol{a}=\boldsymbol{F}$$

##### eq-11-14

$$m(d^2\boldsymbol{r}/dt^2)=\boldsymbol{F}$$

现在的问题是证明牛顿定律在坐标旋转中保持不变：证明 $\boldsymbol{a}$ 是一个向量；我们已经做过。证明 $\boldsymbol{F}$ 是一个向量；我们假定如此。所以如果作用力是一个向量，我们知道加速度是一个向量，那么等式 [11.13](/volume-1/11-vectors/11-6-newton's-laws-in-vector-notation.md#eq-11-13) 在任意的坐标系中看起来相同。以这种形式（不直接包含 x 的、 y 的以及 z 的）书写等式的好处是每次我们书写牛顿等式或者其他物理定律，不用再写三条。我们所写的看起来好像是一条定律，但实际上，对任意一组坐标而言，它是三条定律，因为任意的向量等式包含一则陈述：彼此的部分相等。

![一个弯曲的轨迹](/notes-of-feynman-lectures-on-physics/assets/volume-1/fig-11-7.png)

![计算加速度的图解](/notes-of-feynman-lectures-on-physics/assets/volume-1/fig-11-8.png)

加速度是向量速度的变化率的事实帮助我们在某些相当复杂的情况中计算加速度。例如，一个粒子在某个复杂的曲线上移动（Fig.11-7），在一个瞬间 $t$ ，它拥有确定的速度 $\boldsymbol{v}_1$ ，在稍后的另一个瞬间 $t_2$ ，它有一个不同的速度 $\boldsymbol{v}_2$ 。加速度是什么？答案是：加速度是速度之间的差，除以微小的时间间隔，所以我们需要两个速度的差值。我们该如何得到速度的差值呢？把两个向量相减，我们把向量放在 $\boldsymbol{v}_2$ 和 $\boldsymbol{v}_1$ 的末端；我们划出 $\Delta{\boldsymbol{v}}$ ，它是两个向量的差。对吗？No！只有在向量的末尾处于相同的地方时，它才会奏效！如果我们把向量移到其他的某个地方，然后再画一条线，没有任何意义，所以请注意！我们需要画一个新的图解，做向量减法。在 Fig.11-8 中， $\boldsymbol{v}_1$ 和 $\boldsymbol{v}_2$ 与 Fig.11-7 中的部分平行且相等，现在我们能讨论加速度了。加速度是 $\Delta{\boldsymbol{v}}/\Delta{t}$ 。值得注意的是我们可以从两个部分组成速度差值；我们认为加速度拥有两个部分： 

$$\Delta{\boldsymbol{v}}_{\parallel}$$ ，

沿着路径的切线方向，以及 $\Delta{\boldsymbol{v}}_{\perp}$ ，垂直于路径，如图 Fig.11-8 所示。相切于路径的加速度是，向量长度的改变，也就是，速率 $v$ 的改变：

##### eq-11-15

$$a_{\parallel}=dv/dt$$

加速度的另一个部分，垂直于曲线，很容易计算出来，运用 Fig.11-7 和 Fig.11-8 。在很短的时间 $\Delta{t}$ 中，把 $\boldsymbol{v}_1$ 和 $\boldsymbol{v}_2$ 之间的夹角的变化设为 $\Delta{\theta}$ 。如果速度的数值是 $v$ ，那么


$$\Delta{v}_{\perp}=v\Delta{\theta}$$

加速度 $a$ 是

$$a_{\perp}=v(\Delta{\theta}/\Delta{t})$$

现在我们需要知道 $\Delta{\theta}/\Delta{t}$ ，可以通过这种方式求得：如果，在一个给定的时刻，曲线近似于一个圆，它的半径是 $R$ ，然后在一个时间 $\Delta{t}$ 中，距离 $s$ 是， $v\Delta{t}$ ，其中 $v$ 是速率。

$$\Delta{\theta}=(v\Delta{t})/R \quad or \quad \Delta{\theta}/\Delta{t}=v/R $$

因此我们发现

$$a_{\perp}=v^2/R$$

正如我们之前所看到的那样。
