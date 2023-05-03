# 空间处理方面知识

本项目主要汇聚有关于空间位置处理方面的知识信息，通过各类实战项目出发进行相关知识的积累、分享以及建模。
帮助快速进行商业化。

## 1. Shapely

shapely是基于笛卡尔坐标的几何对象操作和分析Python库。底层基于GEOS和JTS库。shapely无法读取和
写数据文件，但可以基于应用广泛的一些格式和协议进行序列化(serialize)和去序列化(deserialize)操
作。而且shapely不关注数据格式和坐标系统，但shapely的整合性很强，可以和GIS之类的工具协同工作。
这种黏性类似python。

#### 1.1 几何类型
实际的各类空间信息需要对应类型去封装，为此需要通过下述各类对象进行封装。其中学习过GeoJson的
开发者可以熟悉的发现其几何类型如出一辙。

|         类型         |               说明               |
|:------------------:|:------------------------------:|
|       Point        |  表示具有 x、y 和可能的 z 值的单个坐标的几何类型   |
|     LineString     |        由一个或多个线段组成的几何类型         |
|     LinearRing     |    一种几何类型，由一条或多条线段组成，形成一个闭环    |
|      Polygon       |        表示由线性环包围的区域的几何类型        |
|     MultiPoint     |        一个或多个Point对象的集合         |
|  MultiLineString   |       一个或多个LineString的集合       |
|    MultiPolygon    |        一个或多个Polygon的集合。        |
| GeometryCollection | 一个或多个几何图形的集合，其中可能包含不止一种类型的几何图形 |

上述几何类型如均可以支持`pickle`库的序列化以及反序列化，对应我们也可以通过其自带的属性进行序列化
以及反序列化操作，比如下述示例代码中的那样。  

```python
pickled = pickle.dumps(Point(1, 1))
pt = pickle.loads(pickled)
```

其中`pickle`对类型`linearrings`序列化后在进行反序列化会导致类型变回`linestrings`，对应的也可以使用
其自带的属性进行序列化以及反序列化操作。  

```python
pt = Point(1, 2)
print(pt.wkt)
print(to_wkt(pt))

print(pt.wkb)
print(to_wkb(pt))

print(from_wkt(pt.wkt))
print(from_wkb(pt.wkb))
```

使用对象本身的`wkt`与`wkb`属性可以获取，对应的通过`to_wkt`与`to_wkb`也可以起到一样的效果，对应的反序列化
操作则使用`from_wkt`与`from_wkb`即可，如果希望转换为GeoJson对象则可以通过`to_geojson`与`from_geojson`实现。  

#### 1.2 常用属性

* area
计算对应多边形的面积尺寸。
```python
geome = Polygon([(0, 0), (0, 2), (2, 0), (4, 4)])
print(geome.area)
print(area(geome))
```

* bounds
代表几何体的minx, miny, maxx, maxy值。
```python
geome = Polygon([(0, 0), (0, 2), (2, 0), (4, 4)])
print(geome.bounds)
print(bounds(geome))
```

* geom_type
返回多边形的类型，主要返回如上表1.1中的几何类型。

* distance
计算两个多边形之间的最短距离。

* minumum_clearance
返回可以移动节点以生成无效几何体的最小距离。
```python
geome = Polygon([(0, 0), (0, 2), (2, 0), (4, 4)])
print(geome.minimum_clearance)
print(minimum_clearance(geome))
```

* hausdorff_distance(豪斯多夫距离)  
一个集合到另一个集合中最近点的最大距离，具体公式如H(A,B)=max(h(A,B),h(B,A))，代表集合A中各个点到B的最短距离，并
在排序中选择最长距离，对应的h(B, A)则相反。

* representative_point
返回位于GeoSeries每一个元素中的坐标点，该点不会是几何中心。
```python
geome = Point(0, 0).buffer(2.0).difference(Point(0,0).buffer(1.0))
print(geome.centroid)
print(geome.representative_point())
```

#### 1.3 几何操作

* difference
计算参数1中不构成参数B中的几何形状。
```python
def difference_test():
    line1 = LineString([(0, 0), (2, 2)])
    line2 = LineString([(1, 1), (3, 3)])
    dif = difference(line1, line2)
    gLine1 = geopandas.GeoSeries(line1)
    gLine2 = geopandas.GeoSeries(line2)
    gDif = geopandas.GeoSeries(dif)
    ax = plt.subplot(111)
    gLine1.plot(ax=ax, edgecolor='blue')
    gLine2.plot(ax=ax, edgecolor="grey")
    gDif.plot(ax=ax, edgecolor="red")
    plt.show()
```

* intersection
返回几何图形中相交的部分,示例只需要修改上述代码中`difference`部分为`intersection`即可。
该方法还有另一个针对多个几何类型的操作方式`intersection_all`。  

* symmetric_difference
与`difference`相反，返回两个几何类型中不重叠的部分几何部分，对应也有针对多个几何类
型的`symmetric_difference_all`对象。  
```python
# ..
line2 = LineString([(1, 1), (3, 3)])
dif = symmetric_difference(line1, line2)
gLine1 = geopandas.GeoSeries(line1)
# ..
```

* union
返回两个几何类型的并集部分，对应的也有针对多个几何类型的`union_all`方法。
```python
line2 = LineString([(1, 1), (3, 3)])
dif = union(line1, line2)
gLine1 = geopandas.GeoSeries(line1)
```



#### 1.4 常用操作

* 多边形可视化
为了能够让我们操作的图表以可视化的方式进行呈现，我们需要经过以下操作通过`matplotlib`进行可视化呈现。  
```python
from shapely import Polygon
import matplotlib.pyplot as plt
import geopandas as gpd

if __name__ == '__main__':
    geome = Polygon([(0, 0), (0, 2), (2, 2), (2, 0)])
    p = gpd.GeoSeries(geome)
    p.plot(facecolor='grey', edgecolor='black')
    plt.show()
```

#### 参考文献
* [Shapely官方文档](https://shapely.readthedocs.io/en/stable/index.html)  
* [Shapely 1.8中文文档](https://www.osgeo.cn/shapely/manual.html)