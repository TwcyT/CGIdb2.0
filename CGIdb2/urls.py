"""CGIdb2 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from search import views as view

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', view.home),
    url(r'^contact/', view.contact),
    url(r'^search/', view.search),
    url(r'^results/', view.results),
    url(r'^drug_effect/(?P<gene1id>\d+)/(?P<gene2id>\d+)/(?P<tissue>\w+)/$', view.drug_effect),
    url(r'^TCGA_result/(?P<gene1id>\d+)/(?P<gene2id>\d+)/(?P<cancer>\w+)/$', view.TCGA_result),
    #url(r'^gene_info/(?P<geneid>\d+)/', view.gene_info),
    url(r'^statistic_gene/', view.statistic_gene),
    url(r'^statistic_source/', view.statistic_source),
    url(r'^statistic_drug/', view.statistic_drug),
    url(r'^statistic_com_path/', view.statistic_com_path),
    url(r'^FAQ/', view.FAQ),
    url(r'^data/SL_SV_tissue', view.SL_SV_tissue),
    url(r'^data/SL_tissue', view.SL_tissue),
    url(r'^data/SV_tissue', view.SV_tissue),
    url(r'^data/SL_SV_source', view.SL_SV_source),
    url(r'^data/SL_source', view.SL_source),
    url(r'^data/SV_source', view.SV_source),
    url(r'^data/drug_effect_download', view.drug_effect_download),
    url(r'^data/complex_download', view.complex_download),
    url(r'^data/pathway_download', view.pathway_download),
    url(r'^browse_gene/SL/(?P<letter>[A-Z])/(?P<page>\d+)/(?P<pageLength>\d+)/$', view.browse_gene_SL),
    url(r'^browse_gene/SL/(?P<letter>[A-Z])/$', view.browse_gene_SL_orgin),
    url(r'^browse_gene/SV/(?P<letter>[A-Z])/(?P<page>\d+)/(?P<pageLength>\d+)/$', view.browse_gene_SV),
    url(r'^browse_gene/SV/(?P<letter>[A-Z])/$', view.browse_gene_SV_orgin),
    url(r'^browse_gene/tissues/(?P<tissue>\w+)/$', view.browse_tissue_orgin),
    url(r'^browse_gene/tissues/(?P<tissue>\w+)/(?P<page>\d+)/(?P<pageLength>\d+)/$', view.browse_tissue),

]

