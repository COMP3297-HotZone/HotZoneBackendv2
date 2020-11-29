import numpy as np
from sklearn.cluster import DBSCAN
import math
from datetime import datetime, timedelta
from addLocation.models import *
from addLocation.serializers import *
from viewCases.models import *
from .serializers import *

def fetchData():
    dataArr = []
    allVisit = VisitedLocation.objects.all()
    visitSerializer = ClusteringDataSerializer(allVisit,many=True)

    for visit in visitSerializer.data:
        if visit['dateFrom'] == visit['dateTo']:
            locationID = visit['location']['id']
            x = visit['location']['xcoord']
            y = visit['location']['ycoord']
            dateOfVisit = visit['dateFrom']
            dateOfVisit = (datetime.fromisoformat(dateOfVisit)-datetime.fromisoformat("2020-01-01")).days
            caseID = visit['caseRecord']['id']
            dataArr.append([x,y,dateOfVisit,caseID,locationID])
    return dataArr

    
def performCluster(D, T, C):
    dataArr = fetchData()
    if not dataArr:
        return {'Total clusters':'0','Total un-clustered':'0'}
    npDataArr = np.array(dataArr)
    # print(npDataArr.shape)
    # D = int(input("Inter-location distance threshold: ") or 200)
    # T = int(input("Proximity in time threshold: ") or 3)
    # C = int(input("Minimum Cluster size: ") or 2)
    return cluster(npDataArr, D, T, C)

def cluster(vector_4d, distance, time, minimum_cluster):
    ret = ""
    retDict = {}

    params = {"space_eps": distance, "time_eps":time}
    db = DBSCAN(eps=1, min_samples=minimum_cluster-1,metric=custom_metric, metric_params=params).fit_predict(vector_4d)
    
    # print(vector_4d.shape)
    # print(len(db))
    # Extract total clusters from them (for sanity checks)
    unique_labels = set(db)
    total_clusters = len(unique_labels) if -1 not in unique_labels else len(unique_labels) -1
    # print("Total clusters: ", total_clusters)
    ret += f'Total clusters: {total_clusters}\n'
    retDict['Total clusters']=total_clusters

    # Extract total un-clustered data (for sanity checks)
    total_noise = list(db).count(-1)
    # print("Total un-clustered:", total_noise)
    ret += f'Total un-clustered: {total_noise}\n'
    retDict['Total un-clustered']=total_noise

    clusterArr = []
    for k in unique_labels:
        if k!=-1:
            labels_k = db == k
            cluster_k = vector_4d[labels_k]
            # print("Cluster",k," size:", len(cluster_k))
            ret += f'Cluster {k} size:{len(cluster_k)}\n'
            
            cases = []
            for pt in cluster_k:
                # print(f"(x:{pt[0]}, y:{pt[1]}, day:{pt[2]}, caseNo:{pt[3]})")
                ret += f"(x:{pt[0]}, y:{pt[1]}, day:{pt[2]}, caseNo:{pt[3]})\n"
                day = (datetime.fromisoformat("2020-01-01")+ timedelta(days=int(pt[2]))).strftime("%Y-%m-%d")
                location = getattr(Location.objects.get(pk=pt[4]),"name")
                cases.append({"x":pt[0], "y":pt[1], "day":day, "caseNo":int(pt[3]), "locationName": location})
            clusterArr.append(cases)
    retDict['cluster']=clusterArr
            
    return retDict

def custom_metric(q,p,space_eps,time_eps):
    dist = 0
    for i in range(2):
        dist += (q[i]-p[i])**2
    spatial_dist = math.sqrt(dist)

    time_dist = math.sqrt((q[2]-p[2])**2)

    if time_dist/time_eps <= 1 and spatial_dist/space_eps <= 1 and p[3] != q[3]:
        return 1
    else:
        return 2
