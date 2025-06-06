不仅仅是牛顿定律，迄今为止我们所了解的其他的物理定律，有两个属性，它们在坐标轴的平移和旋转里是不变的（或是对称的）。这些属性非常重要，数学技术通过它们在书写和使用物理定律方面得到进步。

上一个分析包含了过多的数学工作。为了减到最少去分析这类问题，一个非常强力的数学方法被发明出来。这个系统，被称之为向量分析，包含这一章的抬头；严格来说，这是一个有关物理定律对称的章节。通过之前的分析方法，我们可以获得搜寻的结果，但是在实践中我们喜欢更加简单、迅速地做事儿，所以我们采用向量技术。

我们注意到两种数值的某些特征，它们在物理中很重要。（实际上不止两个，但是让我们从它们开始。）其中之一，像一袋土豆的数量，我们称它为普通数值，或者没有方向的数值，亦或标量。温度就是这样的一个数值。其他的在物理中的重要数值都有方向，比如速度：我们不仅要记录一个物体的速率，还要持续追踪它的走向。动量和作用力也有方向，就像位移：当某人从空间中的一个地方走到另一个地方，我们可以持续记录他走了多远，但是如果我们也想知道他走到哪里，我们就得指明一个方向。

所有的数值都有方向，像空间中的一步，被称之为向量。

一个向量是三个数字。为了表示空间中的一步，从原点到某个特定的 P 点，它的位置是 (x, y, z)，我们真地需要三个数字，但是我们将发明一个单独的数学符号， $r$ ，它不同于我们迄今为止所使用的其他数学符号。它不是一个单独的数字，它表示三个数字：x、y 和 z。但是它表示的不仅仅是这三个数字，因为如果我们使用了不同的坐标系，这三个数字会变为 $x^{'}$ 、 $y^{'}$ 和 $z^{'}$ 。我们想要保持简洁，所以我们采用相同的标记去表示数字 $(x, y, z)$ 和 $(x^{'}, y^{'}, z^{'})$ 。也就是说，我们使用相同的标记表示第一组数字，它们位于一个坐标系中，如果我们使用了其他的坐标系，也可以用它表示第二组数字。这样做的好处是当我们改变了坐标系，我们无须改变等式的字母。如果我们使用 $x,y,z$ 写一个等式，然后使用另一个系统，我们就不得不变为 $x^{'},y^{'},z^{'}$ ，现在只需写作 $r$ ，如果我们使用一组坐标，它可以表示 $(x,y,z)$ ，或者如果我们使用另一组坐标，它可以表示 $(x^{'},y^{'},z^{'})$ ，等等。这三个数字可以描述在一个给定的坐标系中的数值，它们被称之为在那个系统的坐标轴的方向上的向量部分。也就是说，我们使用相同的符号表示三个字母，它们对应同一个对象，就像从不同的坐标轴上所看到的。我们可以说“这个相同的对象”蕴含了一个物理直觉，关于空间中一步的事实，它独立于我们测量的部分。所以符号 $r$ 将表示相同的事物，不管我们怎么转动坐标轴。

现在假设有另外一个带有方向的物理数值，任意的其他数值，也会关联三个数字，像作用力，这三个数字通过一个特定的数学规则变为另外三个数字，如果我们改变了坐标轴的话。那么从 $(x,y,z)$ 变为 $(x^{'},y^{'},z^{'})$ 必然是相同的规则。换句话说，任意关联三个数字的物理数值，它们的转换如同在空间中一步的部分，那么它就是一个向量。下面的等式

$$\boldsymbol{F}=\boldsymbol{r}$$

在任意的坐标系中是正确的，如果它在一个坐标系中是正确的话。当然，这个等式表示的是三个等式：

$$F_x=x,\quad F_y=y,\quad F_z=z$$

或则

$$F_{x^{'}}=x^{'},\quad F_{y^{'}}=y^{'},\quad F_{z^{'}}=z^{'}$$

物理关系可以被表示为向量等式的事实，让我们确信仅仅是坐标系的旋转，关系不会改变。这就是为什么向量在物理中如此有用。

现在让我们学习向量的一些属性。在向量的例子中，我们也许会提到速度、动量、作用力和加速度。出于方便的目的，我们通过一个箭头表示一个向量数值，这个箭头指明它作用的方向。为什么我们可以通过一个箭头表示作用力？因为它跟“空间中的一步”一样拥有相同的数学转换的属性。我们因此可以在一个图解中表示它，就像它是一步，使用一个尺寸，譬如一单位的作用力，或一牛顿，对应一个特定地便捷的长度。一旦我们这样做了，所有的作用力都可以被表示成长度，就像下面的等式：

$$\boldsymbol{F}=k\boldsymbol{r}$$

其中 $k$ 是某个常数，这是一个完美适用的等式。因此我们总是可以用线表示作用力，这真的很方便，因为一旦我们划出线，就不再需要坐标轴。当然，我们可以迅速地计算出三个部分，哪怕它们随着旋转的坐标轴改变，因为这仅仅是一个几何问题。
