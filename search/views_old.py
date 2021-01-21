


from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from .forms import SearchForm
import re, os, json, pandas as pd, numpy as np
from .models import SL_SV_Table, Gene
from django.db.models import Q

def home(request):
	return HttpResponse(loader.get_template('CGIdb2.0.html').render({},request))


def contact(request):
	return HttpResponse(loader.get_template('contact.html').render({},request))

def search(request):
	return HttpResponse(loader.get_template('search.html').render({},request))


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
					pairs_info = [k for j in [SL_SV_Table.objects.raw(
						"select search_sl_sv_table.*, a.symbol as gene1_symbol,b.symbol as gene2_symbol from search_sl_sv_table inner join search_gene a on search_sl_sv_table.gene1_id=a.entrez_id inner join search_gene b on search_sl_sv_table.gene2_id=b.entrez_id where gene1_id=" + str(
							i.entrez_id)) for i in gene_info] for k in j]
					pairs_info.extend([k for j in [SL_SV_Table.objects.raw(
						"select search_sl_sv_table.*, a.symbol as gene1_symbol,b.symbol as gene2_symbol from search_sl_sv_table inner join search_gene a on search_sl_sv_table.gene1_id=a.entrez_id inner join search_gene b on search_sl_sv_table.gene2_id=b.entrez_id where gene2_id=" + str(
							i.entrez_id)) for i in gene_info] for k in j])
			# pairs_info = [j for i in pairs_info for j in i]
					gene_info_1 = [Gene.objects.filter(Q(symbol=i.gene1_symbol)) for i in pairs_info]
					gene_info_1.extend([Gene.objects.filter(Q(symbol=i.gene2_symbol)) for i in pairs_info])
					pairs_info_1 = [SL_SV_Table.objects.filter(Q(gene1_symbol=i.symbol) | Q(gene2_symbol=i.symbol)) for i in tmp]
					links_1 = []
					SL_node = []
					SV_node = []
					search_symbol = [i.symbol for i in gene_info]
					search_symbol = list(set(search_symbol))
					for h in pairs_info_1:
						for k in h:
							links_1.extend([{ 'source': k.gene1_symbol, 'target': k.gene2_symbol, 'name': k.type}])
							if k.type == 'SL' and k.gene1_symbol not in search_symbol:
								SL_node.extend([k.gene1_symbol])
							elif k.type == 'SL' and k.gene2_symbol not in search_symbol:
								SL_node.extend([k.gene2_symbol])
							elif k.type == 'SV' and k.gene2_symbol not in search_symbol:
								SV_node.extend([k.gene2_symbol])
							elif k.type == 'SV' and k.gene1_symbol not in search_symbol:
								SV_node.extend([k.gene1_symbol])

					SL_node = list(set(SL_node))
					SV_node = list(set(SV_node))

					node_1 = []
					for h in gene_info_1:
						for k in h:
							if k.symbol in search_symbol:
								node_1.extend([{'id': k.id, 'label': k.symbol, 'category': 0}])
							elif k.symbol in SL_node:
								node_1.extend([{'name': k.symbol, 'des': k.description, 'category': 1}])
							elif k.symbol in SV_node:
								node_1.extend([{'name': k.symbol, 'des': k.description, 'category': 2}])
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
				return render(request, 'results.html',{
					"result": 1,
					"gene_info": gene_info,
					"pairs_info": pairs_info,
					"node": json.dumps(node),
					"links": json.dumps(links)
					})
	else:
		form = SearchForm()

	# return HttpResponse(loader.get_template('GI/search.html').render({"form":form},request))
	return render(request, "results.html", {'form': form})

