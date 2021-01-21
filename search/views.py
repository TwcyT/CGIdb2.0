


import django.conf
from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from .forms import SearchForm
import re, os, json, pandas as pd, numpy as np
from .models import SL_SV_Table, Gene, SL_SV_Table_detail, Complex, Pathway, Chemical, TCGA_info, gene_tcga_alter_samples
from wsgiref.util import FileWrapper
from django.db.models import Q

cancer_samples = {}
with open(os.path.join(django.conf.settings.DATA_DIR,"cancer_samples.txt")) as f:
        for i in f:
                line = i.strip().split("\t")
                cancer_samples[line[0]] = line[1:]
ccle_cellline2tissue = pd.read_table(os.path.join(django.conf.settings.DATA_DIR,"CCLE_cclline_tissue.txt"))
ccle_alter = pd.read_table(os.path.join(django.conf.settings.DATA_DIR,"CCLE_alter_commSam.txt"),index_col=0)
ccle_alter = ccle_alter.astype("int8")
ccle_drugeffect = pd.read_table(os.path.join(django.conf.settings.DATA_DIR,"CCLE_drug_commSam_IC50.txt"))

CGP_cellline2tissue = pd.read_table(os.path.join(django.conf.settings.DATA_DIR,"CGP_cclline_tissue.txt"))
CGP_alter = pd.read_table(os.path.join(django.conf.settings.DATA_DIR,"CGP_alter_commSam.txt"),index_col=0)
CGP_alter = CGP_alter.astype("int8")
CGP_drugeffect_ic50 = pd.read_table(os.path.join(django.conf.settings.DATA_DIR,"CGP_drug_commSam_IC50.txt"))

CTRP_cellline2tissue = pd.read_table(os.path.join(django.conf.settings.DATA_DIR,"CTRP_cclline_tissue.txt"))
CTRP_alter = pd.read_table(os.path.join(django.conf.settings.DATA_DIR,"CTRP_alter_commSam.txt"),index_col=0)
CTRP_alter = CTRP_alter.astype("int8")
CTRP_drugeffect_auc = pd.read_table(os.path.join(django.conf.settings.DATA_DIR,"CTRP_drug_commSam_AUC.txt"))

GDSC1_cellline2tissue = pd.read_table(os.path.join(django.conf.settings.DATA_DIR,"GDSC1_cclline_tissue.txt"))
GDSC1_alter = pd.read_table(os.path.join(django.conf.settings.DATA_DIR,"GDSC1_alter_commSam.txt"),index_col=0)
GDSC1_alter = GDSC1_alter.astype("int8")
GDSC1_drugeffect_auc = pd.read_table(os.path.join(django.conf.settings.DATA_DIR,"GDSC1_drug_commSam_AUC.txt"))
GDSC1_drugeffect_ic50 = pd.read_table(os.path.join(django.conf.settings.DATA_DIR,"GDSC1_drug_commSam_IC50.txt"))
GDSC2_cellline2tissue = pd.read_table(os.path.join(django.conf.settings.DATA_DIR,"GDSC2_cclline_tissue.txt"))
GDSC2_alter = pd.read_table(os.path.join(django.conf.settings.DATA_DIR,"GDSC2_alter_commSam.txt"),index_col=0)
GDSC2_alter = GDSC2_alter.astype("int8")
GDSC2_drugeffect_auc = pd.read_table(os.path.join(django.conf.settings.DATA_DIR,"GDSC2_drug_commSam_AUC.txt"))
GDSC2_drugeffect_ic50 = pd.read_table(os.path.join(django.conf.settings.DATA_DIR,"GDSC2_drug_commSam_IC50.txt"))

significant_drugeffect = pd.read_table(os.path.join(django.conf.settings.DATA_DIR, "significant_drugEffect.txt"))



def home(request):
    return HttpResponse(loader.get_template('CGIdb2.0.html').render({},request))


def contact(request):
    return HttpResponse(loader.get_template('contact.html').render({},request))

def search(request):
    SL_SV_pairs = SL_SV_Table.objects.filter(Q(gene1_symbol__startswith='A') & Q(type='SL'))[:10]
    SL_SV_pairs_length = SL_SV_Table.objects.filter(Q(gene1_symbol__startswith='A') & Q(type='SL')).count()
    for s in SL_SV_pairs:
        s.source = s.source.strip().split(";")
    for s in SL_SV_pairs:
        s.tissue = s.tissue.strip().split(";")
    return HttpResponse(loader.get_template('search.html').render({"letter":'A',"start":1,"browse_pairs":SL_SV_pairs, "browse_length":SL_SV_pairs_length},request))


def statistic_gene(request):
    return HttpResponse(loader.get_template('statistic_gene.html').render({},request))

def statistic_source(request):
    return HttpResponse(loader.get_template('statistic_source.html').render({},request))

def statistic_drug(request):
    return HttpResponse(loader.get_template('statistic_drug.html').render({},request))

def statistic_com_path(request):
    return HttpResponse(loader.get_template('statistic_complex_pathway.html').render({},request))

def FAQ(request):
    return HttpResponse(loader.get_template('FAQ.html').render({},request))

def results(request):
    global node, links
    if request.method == "POST":
        form = SearchForm(request.POST)

        gene_info = ""
        pairs_info = ""

        if form.is_valid():
            search_type = form.cleaned_data["search_type"]
            if search_type == 'Gene':
                gf = form.cleaned_data["filter"]

                if gf:
                    gf = [i for i in re.split("[,;\s]\s*", gf) if not i == ""]
                    tmp = [Gene.objects.filter(Q(entrez_id=i) | Q(symbol=i)) for i in gf]
                    tmp = [i[0] for i in tmp if not len(i) == 0]
                    gene_info = {tmp[i] for i in range(0, len(tmp))}
                    pairs_info_detail = [k for j in [SL_SV_Table_detail.objects.raw(
                        "select search_sl_sv_table_detail.*, a.symbol as gene1_symbol,b.symbol as gene2_symbol from search_sl_sv_table_detail inner join search_gene a on search_sl_sv_table_detail.gene1_id=a.entrez_id inner join search_gene b on search_sl_sv_table_detail.gene2_id=b.entrez_id where gene1_id=" + str(
                            i.entrez_id)) for i in gene_info] for k in j]
                    pairs_info_detail.extend([k for j in [SL_SV_Table_detail.objects.raw(
                        "select search_sl_sv_table_detail.*, a.symbol as gene1_symbol,b.symbol as gene2_symbol from search_sl_sv_table_detail inner join search_gene a on search_sl_sv_table_detail.gene1_id=a.entrez_id inner join search_gene b on search_sl_sv_table_detail.gene2_id=b.entrez_id where gene2_id=" + str(
                            i.entrez_id)) for i in gene_info] for k in j])
                    pairs_info = [k for j in [SL_SV_Table.objects.raw(
                        "select search_sl_sv_table.*, a.symbol as gene1_symbol,b.symbol as gene2_symbol from search_sl_sv_table inner join search_gene a on search_sl_sv_table.gene1_id=a.entrez_id inner join search_gene b on search_sl_sv_table.gene2_id=b.entrez_id where gene1_id=" + str(
                            i.entrez_id)) for i in gene_info] for k in j]
                    pairs_info.extend([k for j in [SL_SV_Table.objects.raw(
                        "select search_sl_sv_table.*, a.symbol as gene1_symbol,b.symbol as gene2_symbol from search_sl_sv_table inner join search_gene a on search_sl_sv_table.gene1_id=a.entrez_id inner join search_gene b on search_sl_sv_table.gene2_id=b.entrez_id where gene2_id=" + str(
                            i.entrez_id)) for i in gene_info] for k in j])
            # pairs_info = [j for i in pairs_info for j in i]
                    gene_heat = [i.gene1_symbol for i in pairs_info_detail]
                    gene_heat.extend([i.gene2_symbol for i in pairs_info_detail])
                    gene_info_1 = [Gene.objects.filter(Q(symbol=i.gene1_symbol)) for i in pairs_info]
                    gene_info_1.extend([Gene.objects.filter(Q(symbol=i.gene2_symbol)) for i in pairs_info])
                    pairs_info_1 = [SL_SV_Table.objects.filter(Q(gene1_symbol=i.symbol) | Q(gene2_symbol=i.symbol)) for i in tmp]
                    links_1 = []
                    SL_node = []
                    SV_node = []
                    gene_heat_list = list(set(gene_heat))
                    search_symbol = [i.symbol for i in gene_info]
                    search_symbol = list(set(search_symbol))
                    gene_heat_detail = []

                    for w in gene_heat_list:
                        if w not in search_symbol:
                            numbers = gene_heat.count(w)
                            gene_heat_detail.extend([{'value':numbers, 'name':w}])
                    for h in pairs_info_1:
                        for k in h:
                            if k.type == 'SL' and k.gene1_symbol not in search_symbol:
                                SL_node.extend([k.gene1_symbol])
                                links_1.extend([{ 'id': k.id,'from': k.gene1_symbol, 'to': k.gene2_symbol, 'label':'SL', 'length':'150'}])
                            elif k.type == 'SL' and k.gene2_symbol not in search_symbol:
                                SL_node.extend([k.gene2_symbol])
                                links_1.extend([{ 'id': k.id, 'from': k.gene1_symbol, 'to': k.gene2_symbol, 'label':'SL', 'length':'150'}])
                            elif k.type == 'SV' and k.gene2_symbol not in search_symbol:
                                SV_node.extend([k.gene2_symbol])
                                links_1.extend([{ 'id': k.id, 'from': k.gene1_symbol, 'to': k.gene2_symbol, 'label':'SV', 'length':'150'}])
                            elif k.type == 'SV' and k.gene1_symbol not in search_symbol:
                                SV_node.extend([k.gene1_symbol])
                                links_1.extend([{ 'id': k.id, 'from': k.gene1_symbol, 'to': k.gene2_symbol, 'label':'SV', 'length':'150'}])
                    SL_node = list(set(SL_node))
                    SV_node = list(set(SV_node))

                    node_1 = []
                    for h in search_symbol:
                        node_1.extend([{'id': h, 'label': h, 'image':'/static/CGIdb2/static/image/Searching_gene.gif'}])
                    for h in SL_node:
                        if h not in SV_node:
                            node_1.extend([{'id': h, 'label': h, 'image':'/static/CGIdb2/static/image/SL_gene.gif'}])
                        else:
                            node_1.extend([{'id': h, 'label': h, 'image': '/static/CGIdb2/static/image/SL_SV_gene.gif'}])
                    for h in SV_node:
                        if h not in SL_node:
                            node_1.extend([{'id': h, 'label': h, 'image':'/static/CGIdb2/static/image/SV_gene.gif'}])
                        else:
                            node_1.extend([{'id': h, 'label': h, 'image': '/static/CGIdb2/static/image/SL_SV_gene.gif'}])
                    seen = set()
                    node = []
                    for d in node_1:
                        t = tuple(d.items())
                        if t not in seen:
                            seen.add(t)
                            node.append(d)
                    seen = set()
                    links = []
                    for d in links_1:
                        t = tuple(d.items())
                        if t not in seen:
                            seen.add(t)
                            links.append(d)
                    tmp_complex = [Complex.objects.filter(Q(gene_id_1=i) | Q(gene_id_2=i) | Q(gene_symbol_2=i) | Q(gene_symbol_1=i)) for i in gf]
                    tmp_complex = [i[0] for i in tmp_complex if not len(i) == 0]
                    complex_result = {tmp_complex[i] for i in range(0, len(tmp_complex))}
                    tmp_pathway = [Pathway.objects.filter(Q(gene_id_1=i) | Q(gene_id_2=i) | Q(gene_symbol_2=i) | Q(gene_symbol_1=i)) for i in gf]
                    tmp_pathway = [i[0] for i in tmp_pathway if not len(i) == 0]
                    pathway_result = {tmp_pathway[i] for i in range(0, len(tmp_pathway))}
                    tmp_chemical = [Chemical.objects.filter(Q(gene_id=i) | Q(gene_symbol=i)) for i in gf]
                    tmp_chemical = [i[0] for i in tmp_chemical if not len(i) == 0]
                    chemical_result = {tmp_chemical[i] for i in range(0, len(tmp_chemical))}
                    for s in pairs_info_detail:
                        s.source = s.source.strip().split(";")
                    for s in pairs_info_detail:
                        s.drug_effect = s.drug_effect.strip()
                    for r in pairs_info:
                        r.TCGA_result = r.TCGA_result.strip()
                    for f in pairs_info:
                        f.cancer = f.cancer.strip().split(";")
                    for r in complex_result:
                        r.complex_Y = r.complex_Y.strip()
                    for r in pathway_result:
                        r.pathway_Y = r.pathway_Y.strip()
                    for r in chemical_result:
                        r.chemical_Y = r.chemical_Y.strip()
                return render(request, 'results.html',{
                    "result": 1,
                    "gene_info": gene_info,
                    "pairs_info": pairs_info,
                    "pairs_info_detail":pairs_info_detail,
                    "gene_heat_detail":json.dumps(gene_heat_detail),
                    "node": json.dumps(node),
                    "links": json.dumps(links),
                    "complex_result": complex_result,
                    "pathway_result": pathway_result,
                    "chemical_result":chemical_result,
                    })
    else:
        form = SearchForm()

    # return HttpResponse(loader.get_template('GI/search.html').render({"form":form},request))
    return render(request, "results.html", {'form': form})




#def gene_info(request, geneid):
#    gene_info_detail = Gene_Info.objects.filter(Q(GeneID=geneid))
#    return HttpResponse(loader.get_template('gene_info.html').render({
#            'gene_info_detail': gene_info_detail[0],
#    },request))





def drug_effect(request, gene1id, gene2id, tissue):
    gene1_info = Gene.objects.filter(Q(entrez_id=gene1id))
    gene2_info = Gene.objects.filter(Q(entrez_id=gene2id))
    ###### drug effect

    drug_effect = {}
    for t in set(ccle_cellline2tissue.tissue):
        current_celllines = ccle_cellline2tissue.loc[ccle_cellline2tissue.tissue==t,"cell_line_name"]
        if int(gene2id) in ccle_alter.index:
                gene2_alter = ccle_alter.loc[int(gene2id),current_celllines]
                gene2_alter = gene2_alter[gene2_alter.notnull()]
                change_group = ccle_drugeffect[gene2_alter.index[gene2_alter!=0]]
                change_group.index = ccle_drugeffect.drug
                unchange_group = ccle_drugeffect[gene2_alter.index[gene2_alter==0]]
                unchange_group.index = ccle_drugeffect.drug

        else:
                change_group = []
                unchange_group = []

        current_drug_name = significant_drugeffect.loc[significant_drugeffect.database == "CCLE_IC50", :]
        current_drug_name = current_drug_name.drop_duplicates(['drug','geneid1','geneid2'])
        current_drug_name = current_drug_name.loc[(current_drug_name.geneid2 == int(gene2id)) & (current_drug_name.geneid1 == int(gene1id)), "drug"]
        current_drug_name_1 = [i for i in current_drug_name]
        infor_1 = significant_drugeffect.loc[significant_drugeffect.database == "CCLE_IC50", :]
        infor_1 = infor_1.drop_duplicates(['drug','geneid1','geneid2'])
        pvalue_1 = infor_1.loc[(infor_1.geneid2 == int(gene2id)) & (infor_1.geneid1 == int(gene1id)), "p_value"]
        index_1 = [i for i in range(0,len(current_drug_name_1))]
        change_group_1=[json.dumps(filter(lambda x: not np.isnan(x), change_group.loc[i, :].values)) for i in current_drug_name_1]
        unchange_group_1=[json.dumps(filter(lambda x: not np.isnan(x), unchange_group.loc[i, :].values)) for i in current_drug_name_1]

    for y in set(CGP_cellline2tissue.tissue):
        current_celllines = CGP_cellline2tissue.loc[CGP_cellline2tissue.tissue==y,"cell_line_name"]
        if int(gene2id) in CGP_alter.index:
                gene2_alter = CGP_alter.loc[int(gene2id),current_celllines]
                gene2_alter = gene2_alter[gene2_alter.notnull()]
                change_group = CGP_drugeffect_ic50[gene2_alter.index[gene2_alter!=0]]
                change_group.index = CGP_drugeffect_ic50.drug
                unchange_group = CGP_drugeffect_ic50[gene2_alter.index[gene2_alter==0]]
                unchange_group.index = CGP_drugeffect_ic50.drug

        else:
                change_group = []
                unchange_group = []
        current_drug_name = significant_drugeffect.loc[significant_drugeffect.database == "CGP_IC50", :]
        current_drug_name = current_drug_name.drop_duplicates(['drug','geneid1','geneid2'])
        current_drug_name = current_drug_name.loc[(current_drug_name.geneid2 == int(gene2id)) & (current_drug_name.geneid1 == int(gene1id)), "drug"]
        current_drug_name_CGP_ic50 = [i for i in current_drug_name]
        infor_2 = significant_drugeffect.loc[significant_drugeffect.database == "CGP_IC50", :]
        infor_2 = infor_2.drop_duplicates(['drug','geneid1','geneid2'])
        pvalue_2 = infor_2.loc[(infor_2.geneid2 == int(gene2id)) & (infor_2.geneid1 == int(gene1id)), "p_value"]
        index_2 = [i for i in range(0,len(current_drug_name_CGP_ic50))]

        change_group_CGP_ic50=[json.dumps(filter(lambda x: not np.isnan(x), change_group.loc[i, :].values)) for i in current_drug_name_CGP_ic50]
        unchange_group_CGP_ic50=[json.dumps(filter(lambda x: not np.isnan(x), unchange_group.loc[i, :].values)) for i in current_drug_name_CGP_ic50]

    for h in set(CTRP_cellline2tissue.tissue):
        current_celllines = CTRP_cellline2tissue.loc[CTRP_cellline2tissue.tissue==h,"cell_line_name"]
        if int(gene2id) in CTRP_alter.index:
                gene2_alter = CTRP_alter.loc[int(gene2id),current_celllines]
                gene2_alter = gene2_alter[gene2_alter.notnull()]
                change_group = CTRP_drugeffect_auc[gene2_alter.index[gene2_alter!=0]]
                change_group.index = CTRP_drugeffect_auc.drug
                unchange_group = CTRP_drugeffect_auc[gene2_alter.index[gene2_alter==0]]
                unchange_group.index = CTRP_drugeffect_auc.drug
        else:
                change_group = []
                unchange_group = []
        current_drug_name = significant_drugeffect.loc[significant_drugeffect.database == "CTRP_AUC", :]
        current_drug_name = current_drug_name.drop_duplicates(['drug','geneid1','geneid2'])
        current_drug_name = current_drug_name.loc[(current_drug_name.geneid2 == int(gene2id)) & (current_drug_name.geneid1 == int(gene1id)), "drug"]
        current_drug_name_CTRP_auc = [i for i in current_drug_name]
        infor_3 = significant_drugeffect.loc[significant_drugeffect.database == "CTRP_AUC", :]
        infor_3 = infor_3.drop_duplicates(['drug','geneid1','geneid2'])
        pvalue_3 = infor_3.loc[(infor_3.geneid2 == int(gene2id)) & (infor_3.geneid1 == int(gene1id)), "p_value"]
        index_3 = [i for i in range(0,len(current_drug_name_CTRP_auc))]

        change_group_CTRP_auc=[json.dumps(filter(lambda x: not np.isnan(x), change_group.loc[i, :].values)) for i in current_drug_name_CTRP_auc]
        unchange_group_CTRP_auc=[json.dumps(filter(lambda x: not np.isnan(x), unchange_group.loc[i, :].values)) for i in current_drug_name_CTRP_auc]



    for q in set(GDSC1_cellline2tissue.tissue):
        current_celllines = GDSC1_cellline2tissue.loc[GDSC1_cellline2tissue.tissue==q,"cell_line_name"]
        if int(gene2id) in GDSC1_alter.index:
                gene2_alter = GDSC1_alter.loc[int(gene2id),current_celllines]
                gene2_alter = gene2_alter[gene2_alter.notnull()]
                change_group = GDSC1_drugeffect_ic50[gene2_alter.index[gene2_alter!=0]]
                change_group.index = GDSC1_drugeffect_ic50.drug
                unchange_group = GDSC1_drugeffect_ic50[gene2_alter.index[gene2_alter==0]]
                unchange_group.index = GDSC1_drugeffect_ic50.drug

        else:
                change_group = []
                unchange_group = []
        current_drug_name = significant_drugeffect.loc[significant_drugeffect.database == "GDSC1_IC50", :]
        current_drug_name = current_drug_name.drop_duplicates(['drug','geneid1','geneid2'])
        current_drug_name = current_drug_name.loc[(current_drug_name.geneid2 == int(gene2id)) & (current_drug_name.geneid1 == int(gene1id)), "drug"]
        current_drug_name_GDSC1_ic50 = [i for i in current_drug_name]
        infor_4 = significant_drugeffect.loc[significant_drugeffect.database == "GDSC1_IC50", :]
        infor_4 = infor_4.drop_duplicates(['drug','geneid1','geneid2'])
        pvalue_4 = infor_4.loc[(infor_4.geneid2 == int(gene2id)) & (infor_4.geneid1 == int(gene1id)), "p_value"]
        index_4 = [i for i in range(0,len(current_drug_name_GDSC1_ic50))]

        change_group_GDSC1_ic50=[json.dumps(filter(lambda x: not np.isnan(x), change_group.loc[i, :].values)) for i in current_drug_name_GDSC1_ic50]
        unchange_group_GDSC1_ic50=[json.dumps(filter(lambda x: not np.isnan(x), unchange_group.loc[i, :].values)) for i in current_drug_name_GDSC1_ic50]

    for q in set(GDSC1_cellline2tissue.tissue):
        current_celllines = GDSC1_cellline2tissue.loc[GDSC1_cellline2tissue.tissue == q, "cell_line_name"]
        if int(gene2id) in GDSC1_alter.index:
            gene2_alter = GDSC1_alter.loc[int(gene2id), current_celllines]
            gene2_alter = gene2_alter[gene2_alter.notnull()]
            change_group = GDSC1_drugeffect_auc[gene2_alter.index[gene2_alter != 0]]
            change_group.index = GDSC1_drugeffect_auc.drug
            unchange_group = GDSC1_drugeffect_auc[gene2_alter.index[gene2_alter == 0]]
            unchange_group.index = GDSC1_drugeffect_auc.drug

        else:
            change_group = []
            unchange_group = []
        current_drug_name = significant_drugeffect.loc[significant_drugeffect.database == "GDSC1_AUC", :]
        current_drug_name = current_drug_name.drop_duplicates(['drug', 'geneid1', 'geneid2'])
        current_drug_name = current_drug_name.loc[
            (current_drug_name.geneid2 == int(gene2id)) & (current_drug_name.geneid1 == int(gene1id)), "drug"]
        current_drug_name_GDSC1_auc = [i for i in current_drug_name]
        infor_5 = significant_drugeffect.loc[significant_drugeffect.database == "GDSC1_AUC", :]
        infor_5 = infor_5.drop_duplicates(['drug', 'geneid1', 'geneid2'])
        pvalue_5 = infor_5.loc[(infor_5.geneid2 == int(gene2id)) & (infor_5.geneid1 == int(gene1id)), "p_value"]
        index_5 = [i for i in range(0, len(current_drug_name_GDSC1_auc))]

        change_group_GDSC1_auc = [json.dumps(filter(lambda x: not np.isnan(x), change_group.loc[i, :].values)) for i in
                              current_drug_name_GDSC1_auc]
        unchange_group_GDSC1_auc = [json.dumps(filter(lambda x: not np.isnan(x), unchange_group.loc[i, :].values)) for i
                                in current_drug_name_GDSC1_auc]

    for q in set(GDSC2_cellline2tissue.tissue):
        current_celllines = GDSC2_cellline2tissue.loc[GDSC2_cellline2tissue.tissue == q, "cell_line_name"]
        if int(gene2id) in GDSC2_alter.index:
            gene2_alter = GDSC2_alter.loc[int(gene2id), current_celllines]
            gene2_alter = gene2_alter[gene2_alter.notnull()]
            change_group = GDSC2_drugeffect_ic50[gene2_alter.index[gene2_alter != 0]]
            change_group.index = GDSC2_drugeffect_ic50.drug
            unchange_group = GDSC2_drugeffect_ic50[gene2_alter.index[gene2_alter == 0]]
            unchange_group.index = GDSC2_drugeffect_ic50.drug

        else:
            change_group = []
            unchange_group = []
        current_drug_name = significant_drugeffect.loc[significant_drugeffect.database == "GDSC2_IC50", :]
        current_drug_name = current_drug_name.drop_duplicates(['drug', 'geneid1', 'geneid2'])
        current_drug_name = current_drug_name.loc[
            (current_drug_name.geneid2 == int(gene2id)) & (current_drug_name.geneid1 == int(gene1id)), "drug"]
        current_drug_name_GDSC2_ic50 = [i for i in current_drug_name]
        infor_6 = significant_drugeffect.loc[significant_drugeffect.database == "GDSC2_IC50", :]
        infor_6 = infor_6.drop_duplicates(['drug', 'geneid1', 'geneid2'])
        pvalue_6 = infor_6.loc[(infor_6.geneid2 == int(gene2id)) & (infor_6.geneid1 == int(gene1id)), "p_value"]
        index_6 = [i for i in range(0, len(current_drug_name_GDSC2_ic50))]

        change_group_GDSC2_ic50 = [json.dumps(filter(lambda x: not np.isnan(x), change_group.loc[i, :].values)) for i in
                              current_drug_name_GDSC2_ic50]
        unchange_group_GDSC2_ic50 = [json.dumps(filter(lambda x: not np.isnan(x), unchange_group.loc[i, :].values)) for i
                                in current_drug_name_GDSC2_ic50]

    for q in set(GDSC2_cellline2tissue.tissue):
        current_celllines = GDSC2_cellline2tissue.loc[GDSC2_cellline2tissue.tissue == q, "cell_line_name"]
        if int(gene2id) in GDSC2_alter.index:
            gene2_alter = GDSC2_alter.loc[int(gene2id), current_celllines]
            gene2_alter = gene2_alter[gene2_alter.notnull()]
            change_group = GDSC2_drugeffect_auc[gene2_alter.index[gene2_alter != 0]]
            change_group.index = GDSC2_drugeffect_auc.drug
            unchange_group = GDSC2_drugeffect_auc[gene2_alter.index[gene2_alter == 0]]
            unchange_group.index = GDSC2_drugeffect_auc.drug

        else:
            change_group = []
            unchange_group = []
        current_drug_name = significant_drugeffect.loc[significant_drugeffect.database == "GDSC2_AUC", :]
        current_drug_name = current_drug_name.drop_duplicates(['drug', 'geneid1', 'geneid2'])
        current_drug_name = current_drug_name.loc[(current_drug_name.geneid2 == int(gene2id)) & (current_drug_name.geneid1 == int(gene1id)), "drug"]
        current_drug_name_GDSC2_auc = [i for i in current_drug_name]
        infor_7 = significant_drugeffect.loc[significant_drugeffect.database == "GDSC2_AUC", :]
        infor_7 = infor_7.drop_duplicates(['drug', 'geneid1', 'geneid2'])
        pvalue_7 = infor_7.loc[(infor_7.geneid2 == int(gene2id)) & (infor_7.geneid1 == int(gene1id)), "p_value"]
        index_7 = [i for i in range(0, len(current_drug_name_GDSC2_auc))]

        change_group_GDSC2_auc = [json.dumps(filter(lambda x: not np.isnan(x), change_group.loc[i, :].values)) for i in
                              current_drug_name_GDSC2_auc]
        unchange_group_GDSC2_auc = [json.dumps(filter(lambda x: not np.isnan(x), unchange_group.loc[i, :].values)) for i
                                in current_drug_name_GDSC2_auc]

        #print abcd
    return HttpResponse(loader.get_template('drug_effect_boxplot.html').render({
            'gene1_info': gene1_info[0],
            'gene2_info': gene2_info[0],
            'drug_effect': drug_effect,
            'drug_name':current_drug_name_1,
            'change_group':change_group_1,
            'unchange_group':unchange_group_1,
            'index_1':index_1,
            'p_1':pvalue_1,
            'drug_name_cgp_ic50':current_drug_name_CGP_ic50,
            'change_group_cgp_ic50': change_group_CGP_ic50,
            'unchange_group_cgp_ic50': unchange_group_CGP_ic50,
            'index_2': index_2,
            'p_2': pvalue_2,
            'drug_name_ctrp_auc': current_drug_name_CTRP_auc,
            'change_group_ctrp_auc': change_group_CTRP_auc,
            'unchange_group_ctrp_auc': unchange_group_CTRP_auc,
            'index_3': index_3,
            'p_3': pvalue_3,
            'drug_name_gdsc1_ic50': current_drug_name_GDSC1_ic50,
            'change_group_gdsc1_ic50': change_group_GDSC1_ic50,
            'unchange_group_gdsc1_ic50': unchange_group_GDSC1_ic50,
            'index_4': index_4,
            'p_4': pvalue_4,
            'drug_name_gdsc1_auc': current_drug_name_GDSC1_auc,
            'change_group_gdsc1_auc': change_group_GDSC1_auc,
            'unchange_group_gdsc1_auc': unchange_group_GDSC1_auc,
            'index_5': index_5,
            'p_5': pvalue_5,
            'drug_name_gdsc2_ic50': current_drug_name_GDSC2_ic50,
            'change_group_gdsc2_ic50': change_group_GDSC2_ic50,
            'unchange_group_gdsc2_ic50': unchange_group_GDSC2_ic50,
            'index_6': index_6,
            'p_6': pvalue_6,
            'drug_name_gdsc2_auc': current_drug_name_GDSC2_auc,
            'change_group_gdsc2_auc': change_group_GDSC2_auc,
            'unchange_group_gdsc2_auc': unchange_group_GDSC2_auc,
            'index_7': index_7,
            'p_7': pvalue_7,

    },request))



def SL_SV_tissue(request):

    filename = "/alidata/database/CGIdb2/data/download/SL_SV_tissue.csv" # Select your file here.
    wrapper = FileWrapper(open(filename, 'rb'))
    response = HttpResponse(wrapper, content_type='application/octet-stream')
    response['Content-Length'] = os.path.getsize(filename)
    response['Content-Disposition'] = 'attachment;filename="{0}"'.format("CGIdb2_SL_SV_tissue.csv")

    return response

def SL_tissue(request):

    filename = "/alidata/database/CGIdb2/data/download/SL_tissue.csv" # Select your file here.
    wrapper = FileWrapper(open(filename, 'rb'))
    response = HttpResponse(wrapper, content_type='application/octet-stream')
    response['Content-Length'] = os.path.getsize(filename)
    response['Content-Disposition'] = 'attachment;filename="{0}"'.format("CGIdb2_SL_tissue.csv")

    return response

def SV_tissue(request):

    filename = "/alidata/database/CGIdb2/data/download/SV_tissue.csv" # Select your file here.
    wrapper = FileWrapper(open(filename, 'rb'))
    response = HttpResponse(wrapper, content_type='application/octet-stream')
    response['Content-Length'] = os.path.getsize(filename)
    response['Content-Disposition'] = 'attachment;filename="{0}"'.format("CGIdb2_SV_tissue.csv")

    return response

def SL_SV_source(request):

    filename = "/alidata/database/CGIdb2/data/download/SL_SV_source.csv" # Select your file here.
    wrapper = FileWrapper(open(filename, 'rb'))
    response = HttpResponse(wrapper, content_type='application/octet-stream')
    response['Content-Length'] = os.path.getsize(filename)
    response['Content-Disposition'] = 'attachment;filename="{0}"'.format("CGIdb2_SL_SV_source.csv")

    return response

def SL_source(request):

    filename = "/alidata/database/CGIdb2/data/download/SL_source.csv" # Select your file here.
    wrapper = FileWrapper(open(filename, 'rb'))
    response = HttpResponse(wrapper, content_type='application/octet-stream')
    response['Content-Length'] = os.path.getsize(filename)
    response['Content-Disposition'] = 'attachment;filename="{0}"'.format("CGIdb2_SL_source.csv")

    return response

def SV_source(request):

    filename = "/alidata/database/CGIdb2/data/download/SV_source.csv" # Select your file here.
    wrapper = FileWrapper(open(filename, 'rb'))
    response = HttpResponse(wrapper, content_type='application/octet-stream')
    response['Content-Length'] = os.path.getsize(filename)
    response['Content-Disposition'] = 'attachment;filename="{0}"'.format("CGIdb2_SV_source.csv")

    return response

def drug_effect_download(request):

    filename = "/alidata/database/CGIdb2/data/download/significant_drugEffect.csv" # Select your file here.
    wrapper = FileWrapper(open(filename, 'rb'))
    response = HttpResponse(wrapper, content_type='application/octet-stream')
    response['Content-Length'] = os.path.getsize(filename)
    response['Content-Disposition'] = 'attachment;filename="{0}"'.format("CGIdb2_significant_drugEffect.csv")

    return response

def complex_download(request):

    filename = "/alidata/database/CGIdb2/data/download/SL_SV_complex.csv" # Select your file here.
    wrapper = FileWrapper(open(filename, 'rb'))
    response = HttpResponse(wrapper, content_type='application/octet-stream')
    response['Content-Length'] = os.path.getsize(filename)
    response['Content-Disposition'] = 'attachment;filename="{0}"'.format("CGIdb2_SL_SV_complex.csv")

    return response

def pathway_download(request):

    filename = "/alidata/database/CGIdb2/data/download/SL_SV_pathway.csv" # Select your file here.
    wrapper = FileWrapper(open(filename, 'rb'))
    response = HttpResponse(wrapper, content_type='application/octet-stream')
    response['Content-Length'] = os.path.getsize(filename)
    response['Content-Disposition'] = 'attachment;filename="{0}"'.format("CGIdb2_SL_SV_pathway.csv")

    return response

def browse_gene_SL(request, letter, page, pageLength):
    template = loader.get_template("browse_gene_sub_SL.html")
    SL_SV_pairs = SL_SV_Table.objects.filter(Q(gene1_symbol__startswith=letter) & Q(type='SL'))[int(pageLength)*(int(page)-1):int(pageLength)*int(page)]
    SL_SV_pairs_length = SL_SV_Table.objects.filter(Q(gene1_symbol__startswith=letter) & Q(type='SL')).count()
    if int(pageLength)*int(page)>SL_SV_pairs_length:
        end = SL_SV_pairs_length
    else:
        end = int(pageLength)*int(page)
    for s in SL_SV_pairs:
        s.source = s.source.strip().split(";")
    for s in SL_SV_pairs:
        s.tissue = s.tissue.strip().split(";")
    return HttpResponse(template.render({"letter":letter,"start":int(pageLength)*(int(page)-1)+1,"end":end, "browse_pairs":SL_SV_pairs, "browse_length":SL_SV_pairs_length}, request))

def browse_gene_SL_orgin(request, letter):
    template = loader.get_template("browse_gene_SL.html")
    SL_SV_pairs = SL_SV_Table.objects.filter(Q(gene1_symbol__startswith=letter) & Q(type='SL'))[:10]
    SL_SV_pairs_length = SL_SV_Table.objects.filter(Q(gene1_symbol__startswith=letter) & Q(type='SL')).count()
    for s in SL_SV_pairs:
        s.source = s.source.strip().split(";")
    for s in SL_SV_pairs:
        s.tissue = s.tissue.strip().split(";")
    return HttpResponse(template.render({"letter":letter,"start":1, "browse_pairs":SL_SV_pairs, "browse_length":SL_SV_pairs_length}, request))


def browse_gene_SV(request, letter, page, pageLength):
    template = loader.get_template("browse_gene_sub_SV.html")
    SL_SV_pairs = SL_SV_Table.objects.filter(Q(gene1_symbol__startswith=letter) & Q(type='SV'))[int(pageLength)*(int(page)-1):int(pageLength)*int(page)]
    SL_SV_pairs_length = SL_SV_Table.objects.filter(Q(gene1_symbol__startswith=letter) & Q(type='SV')).count()
    if int(pageLength)*int(page)>SL_SV_pairs_length:
        end = SL_SV_pairs_length
    else:
        end = int(pageLength)*int(page)
    for s in SL_SV_pairs:
        s.source = s.source.strip().split(";")
    for s in SL_SV_pairs:
        s.tissue = s.tissue.strip().split(";")
    return HttpResponse(template.render({"letter":letter,"start":int(pageLength)*(int(page)-1)+1,"end":end, "browse_pairs":SL_SV_pairs, "browse_length":SL_SV_pairs_length}, request))

def browse_gene_SV_orgin(request, letter):
    template = loader.get_template("browse_gene_SV.html")
    SL_SV_pairs = SL_SV_Table.objects.filter(Q(gene1_symbol__startswith=letter) & Q(type='SV'))[:10]
    SL_SV_pairs_length = SL_SV_Table.objects.filter(Q(gene1_symbol__startswith=letter) & Q(type='SV')).count()
    for s in SL_SV_pairs:
        s.source = s.source.strip().split(";")
    for s in SL_SV_pairs:
        s.tissue = s.tissue.strip().split(";")
    return HttpResponse(template.render({"letter":letter,"start":1, "browse_pairs":SL_SV_pairs, "browse_length":SL_SV_pairs_length}, request))

def browse_tissue_orgin(request,tissue):
    template = loader.get_template("browse_tissue_orgin.html")
    if SL_SV_Table_detail.objects.filter(Q(tissue=tissue)).count()>9:
        SL_SV_pairs = SL_SV_Table_detail.objects.filter(Q(tissue=tissue))[:10]
    else:
        SL_SV_pairs = SL_SV_Table_detail.objects.filter(Q(tissue=tissue))
    SL_SV_pairs_length = SL_SV_Table_detail.objects.filter(Q(tissue=tissue)).count()
    for s in SL_SV_pairs:
        s.source = s.source.strip().split(";")
    for s in SL_SV_pairs:
        s.tissue = s.tissue.strip().split(";")
    return HttpResponse(template.render({"tissue":tissue,"start":1, "browse_pairs":SL_SV_pairs, "browse_length":SL_SV_pairs_length}, request))


def browse_tissue(request, tissue, page, pageLength):
    template = loader.get_template("browse_tissue_sub.html")
    SL_SV_pairs = SL_SV_Table_detail.objects.filter(Q(tissue=tissue))[int(pageLength)*(int(page)-1):int(pageLength)*int(page)]
    SL_SV_pairs_length = SL_SV_Table_detail.objects.filter(Q(tissue=tissue)).count()
    if int(pageLength)*int(page)>SL_SV_pairs_length:
        end = SL_SV_pairs_length
    else:
        end = int(pageLength)*int(page)
    for s in SL_SV_pairs:
        s.source = s.source.strip().split(";")
    for s in SL_SV_pairs:
        s.tissue = s.tissue.strip().split(";")
    return HttpResponse(template.render({"tissue":tissue,"start":int(pageLength)*(int(page)-1)+1,"end":end, "browse_pairs":SL_SV_pairs, "browse_length":SL_SV_pairs_length}, request))


def TCGA_result(request, gene1id, gene2id, cancer):
    ####### oncoprint
    predicted_info = TCGA_info.objects.filter(Q(gene1_id=gene1id) & Q(gene2_id=gene2id) & Q(cancer=cancer))
    # if cancer in gene_tcga_alter_samples.objects.values_list("cancer",flat=True):
    if predicted_info[0].pvalue != '':
        gene1_samples = gene_tcga_alter_samples.objects.filter(Q(entrez_id=gene1id) & Q(cancer=cancer))[0]
        mut1 = gene1_samples.mutation.strip().split(";")
        amp1 = gene1_samples.amplication.strip().split(";")
        del1 = gene1_samples.deletion.strip().split(";")
        gene2_samples = gene_tcga_alter_samples.objects.filter(Q(entrez_id=gene2id) & Q(cancer=cancer))[0]
        mut2 = gene2_samples.mutation.strip().split(";")
        amp2 = gene2_samples.amplication.strip().split(";")
        del2 = gene2_samples.deletion.strip().split(";")
        overlap_samples = set(mut1 + amp1 + del1).intersection(set(mut2 + amp2 + del2))
        sorted_samples = [i for i in mut1 + amp1 + del1 if i not in overlap_samples]
        overlap_samples_new = [i for i in mut1 if i in overlap_samples]
        overlap_samples_new_1 = [i for i in mut2 if i in overlap_samples_new]
        overlap_samples_new_1.extend([i for i in amp2 if i in overlap_samples_new])
        overlap_samples_new_1.extend([i for i in del2 if i in overlap_samples_new])
        overlap_samples_new = [i for i in amp1 if i in overlap_samples]
        overlap_samples_new_2 = [i for i in mut2 if i in overlap_samples_new]
        overlap_samples_new_2.extend([i for i in amp2 if i in overlap_samples_new])
        overlap_samples_new_2.extend([i for i in del2 if i in overlap_samples_new])
        overlap_samples_new = [i for i in del1 if i in overlap_samples]
        overlap_samples_new_3 = [i for i in mut2 if i in overlap_samples_new]
        overlap_samples_new_3.extend([i for i in amp2 if i in overlap_samples_new])
        overlap_samples_new_3.extend([i for i in del2 if i in overlap_samples_new])
        overlap_samples_new = overlap_samples_new_1
        overlap_samples_new.extend(overlap_samples_new_2)
        overlap_samples_new.extend(overlap_samples_new_3)
        sorted_samples.extend(overlap_samples_new)
        sorted_samples.extend([i for i in mut2 + amp2 + del2 if i not in overlap_samples])
        sorted_samples.extend(set(cancer_samples[cancer]).difference(sorted_samples))
        if "" in sorted_samples:
            sorted_samples.remove("")
        gene2_samples = [[i, 0, 0] for i in range(0, len(sorted_samples))]
        gene1_samples = [[i, 1, 0] for i in range(0, len(sorted_samples))]
        for i in range(0, len(sorted_samples)):
            if sorted_samples[i] in mut1:
                gene1_samples[i][2] = 1
            if sorted_samples[i] in amp1:
                gene1_samples[i][2] = 2
            if sorted_samples[i] in del1:
                gene1_samples[i][2] = 3
            if sorted_samples[i] in mut2:
                gene2_samples[i][2] = 1
            if sorted_samples[i] in amp2:
                gene2_samples[i][2] = 2
            if sorted_samples[i] in del2:
                gene2_samples[i][2] = 3
        gene1_samples.extend(gene2_samples)
    else:
        gene1_samples = []
        sorted_samples = []
    for s in predicted_info:
        s.gene2_symbol = s.gene2_symbol.strip()
    # print abcd
    return HttpResponse(loader.get_template('TCGA_results.html').render({
        'cancer_samples': json.dumps(sorted_samples),
        'gene_samples': json.dumps(gene1_samples),
        'predicted_info': predicted_info[0],

    }, request))

