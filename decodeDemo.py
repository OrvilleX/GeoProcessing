from shapely import LineString, union
import matplotlib.pyplot as plt
import geopandas


def difference_test():
    line1 = LineString([(0, 0), (2, 2)])
    line2 = LineString([(1, 1), (3, 3)])
    dif = union(line1, line2)
    gLine1 = geopandas.GeoSeries(line1)
    gLine2 = geopandas.GeoSeries(line2)
    gDif = geopandas.GeoSeries(dif)
    ax = plt.subplot(111)
    gLine1.plot(ax=ax, edgecolor='blue')
    gLine2.plot(ax=ax, edgecolor="grey")
    gDif.plot(ax=ax, edgecolor="red")
    plt.show()


if __name__ == '__main__':
    difference_test()
