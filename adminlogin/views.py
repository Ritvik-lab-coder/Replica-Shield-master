from django.shortcuts import render
from responses.models import Response
from django.contrib.auth.decorators import login_required
from . import utils
from collections import defaultdict
from sklearn.cluster import DBSCAN

@login_required
def profile_view(request):

    return render(request, 'profile.html')


@login_required
def database_view(request):

    responses = Response.objects.all()

    return render(request, 'dataview.html', {'responses': responses})

@login_required
def gen_duplicates(request):

    abstract_list = Response.objects.values_list('abstract', flat=True)
    
    proj_vec = utils.create_tfidf_vectors(abstract_list)
    doc_filename_pairs = list(zip(range(len(abstract_list)), proj_vec))

    plagiarism_results = utils.find_similarity(doc_filename_pairs)

    all_files = list(set(file1 for result in plagiarism_results for file1 in result[:2]))
    similarity_matrix = utils.create_similarity_matrix(plagiarism_results, all_files)

    distance_matrix = abs(1 - similarity_matrix)

    epsilon = 0.5 
    min_samples = 1  
    dbscan = DBSCAN(eps=epsilon, min_samples=min_samples, metric='precomputed')
    clusters = dbscan.fit_predict(distance_matrix)

    titles = Response.objects.values_list('title', flat=True)

    cluster_project_lists = defaultdict(list)
    for i, cluster_label in enumerate(clusters):
        project_title = titles[i]
        cluster_project_lists[cluster_label].append(project_title)

    cluster_data = [{'cluster_label': label, 'projects': projects} for label, projects in cluster_project_lists.items()]


    return render(request, 'nlp.html', {'cluster_data': cluster_data})