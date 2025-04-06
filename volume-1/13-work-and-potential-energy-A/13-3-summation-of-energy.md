现在让我们看看更加通用的情况，当存在大量的物体时会发生什么。我们的问题很复杂，把它们标记为 i=1, 2, 3, ...，物体会在彼此之间施加引力的拉力。然后呢？我们需要证明如果我们把所有粒子的动能相加，再加上所有结对的粒子，它们相互之间的引力势能， $-GMm/r_{ij}$ ，结果是一个常数：

##### eq-13-14

$$\sum_i\frac{1}{2}m_iv_i^2+\sum_{(pairs\: ij)}-\frac{Gm_im_j}{r_{ij}}=const$$

我们该如何证明它？我们相对于时间求导它们，结果是零。当我们求导 $\frac{1}{2}m_iv_i^2$ ，其导数是速度、作用力，如同等式 [13-5](/volume-1/13-work-and-potential-energy-A/13-1-energy-of-a-falling-body.md#eq-13-5)。我们通过牛顿的引力定律替换这些作用力，接下来剩下的是 

$$\sum_{pairs}-\frac{Gm_im_j}{r_{ij}}$$

负的时间导数。

动能的时间导数是

##### eq-13-15

$$\frac{d}{dt}\sum_i\frac{1}{2}m_iv_i^2=\sum_im\frac{\boldsymbol{v}_i}{dt}\cdot \boldsymbol{v}_i=\sum_i\boldsymbol{F}_i\cdot \boldsymbol{v}_i=\sum_i(\sum_j-\frac{Gm_im_j\boldsymbol{r}_{ij}}{r_{ij}^3})\cdot \boldsymbol{v}_i$$

势能的时间导数是

$$\frac{d}{dt}\sum_{pairs}-\frac{Gm_im_j}{r_{ij}}=\sum_{pairs}(+\frac{Gm_im_j}{r_{ij}^2})(\frac{dr_{ij}}{dt})$$

由于

$$r_{ij}=\sqrt{(x_i-x_j)^2+(y_i-y_j)^2+(z_i-z_j)^2}$$

所以

$$\frac{dr_{ij}}{dt}=\frac{1}{2r_{ij}}[2(x_i-x_j)(\frac{dx_i}{dt}-\frac{dx_j}{dt})+2(y_i-y_j)(\frac{dy_i}{dt}-\frac{dy_j}{dt})+2(z_i-z_j)(\frac{dz_i}{dt}-\frac{dz_j}{dt})]=\boldsymbol{r}_{ij}\cdot \frac{\boldsymbol{v}_i-\boldsymbol{v}_j}{r_{ij}}=\boldsymbol{r}_{ij}\cdot \frac{\boldsymbol{v}_i}{r_{ij}}+\boldsymbol{r}_{ji}\cdot \frac{\boldsymbol{v}_j}{r_{ji}}$$

因为 $\boldsymbol{r}_{ij}=-\boldsymbol{r}_{ji}$ ，当 $r_{ij}=r_{ji}$ 。因此

##### eq-13-16

$$\frac{d}{dt}\sum_{pairs}-\frac{Gm_im_j}{r_{ij}}=\sum_{pairs}[\frac{Gm_im_j\boldsymbol{r}_{ij}}{r_{ij}^3}\cdot \boldsymbol{v}_i+\frac{Gm_jm_i\boldsymbol{r}_{ji}}{r_{ji}^3}\cdot \boldsymbol{v}_j]$$

现在我们需要搞清楚 $\sum_i\{\sum_j\}$ 和 $\sum_{pairs}$ 的含义。在等式 [13.15](/volume-1/13-work-and-potential-energy-A/13-3-summation-of-energy.md#eq-13-15)中， $\sum_i\{\sum_j\}$ 表示 i 取所有的值，i=1, 2, 3, ...，按照顺序，对于每一个 i 的值，索引 j 取所有的值，除了 i。也就是如果 i=3，j 的取值是 1, 2, 4, ...

在等式 [13.16](/volume-1/13-work-and-potential-energy-A/13-3-summation-of-energy.md#eq-13-16)中， $\sum_{pairs}$ 表示给定的 i 与 j 的值仅会出现一次。因此粒子对 1 和 3 在求和中仅仅贡献一个元素。为了继续追踪，我们或许会让 i 遍历所有的值 1, 2, 3, ...，对于每一个 i ，让 j 仅仅遍历大于 i 的值。因此如果 i=3，那么 j 的取值是 4, 5, 6, ...但是我们留意到，对于每个 i, j 的值，在求和中有两次贡献，一次包含 $\boldsymbol{v}_i$ ，另一次 $\boldsymbol{v}_j$ ，这些元素看起来跟等式 [13.15](/volume-1/13-work-and-potential-energy-A/13-3-summation-of-energy.md#eq-13-15) 中的相同，所有 i 与 j 的值（除了 i=j）都被包含在求和中（等式 13.15）。因此，通过一个一个地比对，我们发现等式 [13.16](/volume-1/13-work-and-potential-energy-A/13-3-summation-of-energy.md#eq-13-16) 与 [13.15](/volume-1/13-work-and-potential-energy-A/13-3-summation-of-energy.md#eq-13-15) 完全相等，但是符号相反，所以动能的导数加上势能的绝对是零。因此我们看到，对于许多物体，动能是所有单独的物体的贡献之和，势能也是如此，它是所有的结对之间的能量之和。我们想要知道为什么是每一个结对的能量：假设我们想要获得把这些物体从它们彼此带到特定距离所做的功的整体大小。我们或许会采取几步，把它们从无限带来，那里没有作用力，一个接一个。首先我们带来第一个，没有功，因为没有其它物体在它上面施加作用力。接下来是第二个，确实有一些功，也就是， $W_{12}=-Gm_1m_2/r_{12}$ 。现在很重要，我们把下一个物体带到位置 3。在任意时刻 3 号上的作用力可以被写作两个作用力之和——在 1 号上施加的作用力和在 2 号上的作用力。因此做的功是每个做功之和，因为如果 $\boldsymbol{F}_3$ 可以被拆分为

$$\boldsymbol{F}_3=\boldsymbol{F}_{13}+\boldsymbol{F}_{23}$$

那么功是

$$\int \boldsymbol{F}_3\cdot d\boldsymbol{s}=\int \boldsymbol{F}_{13}\cdot d\boldsymbol{s}+\int \boldsymbol{F}_{23}\cdot d\boldsymbol{s}=W_{13}+W_{23}$$

也就是，做的功是第一个作用力做的功和第二个的和，就像每个单独地作用。沿用这种方式，我们看到，把给定的部分组合起来，功的大小与等式 [13.14](/volume-1/13-work-and-potential-energy-A/13-3-summation-of-energy.md#eq-13-14) 中的值完全相等。那是因为引力遵从作用力的叠加原理，我们可以把势能写作每一个粒子对的和。
