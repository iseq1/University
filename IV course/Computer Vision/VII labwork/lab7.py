from image_clustering_class import ImageClustering

if __name__ == '__main__':
    img_clust_obj = ImageClustering()
    img_clust_obj.get_clasterization()
    img_clust_obj.get_evaluation_results()
    img_clust_obj.get_metrics()
    img_clust_obj.get_best_metrics()
    img_clust_obj.get_roc_curves()
