import numpy as np
import matplotlib.pyplot as plt
import matplotlib.lines as mlines
from scipy.stats import chi2

from sklearn.covariance import EmpiricalCovariance, MinCovDet

feature1 = np.array([
    7.83, 8.0, 8.3, 6.89, 8.3, 6.34, 8.33, 6.29, 6.64, 6.98, 8.97, 7.39, 
    8.13, 8.68, 7.62, 0.05, 7.39, 0.14, 8.45, 4.91, 7.88, 7.15, 8.34, 
    6.58, 7.73, 7.58, 8.97, 8.43, 8.42, 9.13, 8.58, 8.1, 8.05, 8.32, 7.51, 
    7.18, 6.62, 7.32, 8.17, 8.16, 9.01, 8.61, 7.61, 7.99, 7.32, 8.03, 7.53, 
    8.94, 8.41, 8.92, 5.76, 7.59, 7.03, 8.79, 8.84, 8.61, 7.65, 7.31, 7.97, 
    7.15, 8.8, 7.76, 4.92, 9.09
])

feature2 = np.array([
    453.4346319025092, 434.45544701171013, 398.4271517437949, 424.7965915530401, 
    125.81597145751662, 235.04798175941468, 462.5468855684683, 325.5689235713545, 
    47.37404052884008, 245.75537250005033, 248.18569903948776, 201.35003312964736, 
    170.50883815520052, 172.9197338714202, 397.20582668554687, 98.34271514169454, 
    340.794001861609, 315.2351413259099, 420.98453928793526, 761.5869484612532, 
    447.29572042646134, 228.2843293351732, 278.2652585805249, 195.62356571458204, 
    652.2834568626012, 100.68460516086968, 230.5411625181776, 322.88290900054875, 
    601.1955879236698, 202.88630430836335, 1004.1276129987051, 113.11302649430277, 
    157.15444392837585, 106.81500300550327, 145.15221664683668, 392.60296056536924, 
    252.83830303508546, 237.9030662710188, 351.95717631314824, 3.203822419267869, 
    433.0486583372871, 376.27196906294193, 219.01395201457584, 387.1670770711274, 
    322.5983262035857, 285.72898358125775, 309.5708510426421, 149.24317968715118, 
    366.3422393572565, 93.49881284344463, 234.1251911286988, 156.09396835852712, 
    152.86251225623707, 585.9198735516437, 277.3022209107388, 157.0931401986817, 
    153.74176260192522, 71.56910969011314, 72.86926169752131, 76.95662751751878, 
    159.3558451768232, 295.3250426319511, 135.52705292643375, 327.3491475556256
])

X = np.column_stack((feature1, feature2))

emp_cov = EmpiricalCovariance().fit(X)
robust_cov = MinCovDet(random_state=0).fit(X)

robust_dist = np.sqrt(robust_cov.mahalanobis(X))

threshold = np.sqrt(chi2.ppf(0.975, df=2))

outlier_mask = robust_dist > threshold

fig, ax = plt.subplots(figsize=(10, 6))

inlier_plot = ax.scatter(
    X[~outlier_mask, 0],
    X[~outlier_mask, 1],
    color="black",
    label="Inliers"
)

outlier_plot = ax.scatter(
    X[outlier_mask, 0],
    X[outlier_mask, 1],
    color="red",
    s=80,
    label="Outliers"
)

xx, yy = np.meshgrid(
    np.linspace(X[:, 0].min()-1, X[:, 0].max()+1, 200),
    np.linspace(X[:, 1].min()-1, X[:, 1].max()+1, 200)
)

zz = np.c_[xx.ravel(), yy.ravel()]

mahal_emp_cov = emp_cov.mahalanobis(zz).reshape(xx.shape)
ax.contour(
    xx, yy,
    np.sqrt(mahal_emp_cov),
    cmap=plt.cm.PuBu_r,
    linestyles="dashed"
)

mahal_robust_cov = robust_cov.mahalanobis(zz).reshape(xx.shape)
ax.contour(
    xx, yy,
    np.sqrt(mahal_robust_cov),
    cmap=plt.cm.YlOrBr_r,
    linestyles="dotted"
)

ax.set_xlabel("Code Quality")
ax.set_ylabel("Modernization Features")

ax.legend(
    [
        mlines.Line2D([], [], color="tab:blue", linestyle="dashed"),
        mlines.Line2D([], [], color="tab:orange", linestyle="dotted"),
        inlier_plot,
        outlier_plot,
    ],
    ["MLE dist", "MCD dist", "Inliers", "Outliers"]
)

plt.show()

print("Detected outliers:")
print(np.where(outlier_mask)[0])