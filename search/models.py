from __future__ import unicode_literals

from django.db import models

# Create your models here.

class SL_SV_Table(models.Model):
	type = models.CharField(max_length=100)
	gene1_id = models.CharField(max_length=1000)
	gene2_id = models.CharField(max_length=1000)
	gene1_symbol = models.CharField(max_length=1000)
	gene2_symbol = models.CharField(max_length=1000)
	tissue = models.CharField(max_length=1000)
	source = models.CharField(max_length=1000)
	TCGA_result = models.CharField(max_length=100,null=True)
	cancer = models.CharField(max_length=100,null=True)

class SL_SV_Table_detail(models.Model):
	type = models.CharField(max_length=100)
	gene1_id = models.CharField(max_length=1000)
	gene2_id = models.CharField(max_length=1000)
	gene1_symbol = models.CharField(max_length=1000)
	gene2_symbol = models.CharField(max_length=1000)
	score = models.CharField(max_length=1000)
	tissue = models.CharField(max_length=1000)
	source = models.CharField(max_length=1000)
	drug_effect = models.CharField(max_length=100,null=True)


class Gene(models.Model):
	entrez_id = models.CharField(max_length=100,null=False)
	symbol = models.CharField(max_length=100,null=False)
	Synonyms = models.CharField(max_length=1000,null=True)
	chromosome = models.CharField(max_length=1000,null=True)
	map_location = models.CharField(max_length=100,null=True)
	description = models.CharField(max_length=2000,null=True)
	type_of_gene = models.CharField(max_length=100,null=True)
	EsemGeneId = models.CharField(max_length=1000,null=True)
	GeneStartBp = models.CharField(max_length=1000,null=True)
	GeneEndBp = models.CharField(max_length=1000,null=True)
	HGNCID = models.CharField(max_length=1000,null=True)
	EnseProtFami = models.CharField(max_length=1000,null=True)
	UniProtKBSwissProtId = models.CharField(max_length=1000,null=True)
	census = models.CharField(max_length=100, null=True)

class Complex(models.Model):
	type = models.CharField(max_length=100,null=False)
	complex_type = models.CharField(max_length=100,null=False)
	gene_id_1 = models.CharField(max_length=100,null=True)
	gene_symbol_1 = models.CharField(max_length=100,null=True)
	gene_id_2 = models.CharField(max_length=100,null=True)
	gene_symbol_2 = models.CharField(max_length=100,null=True)
	complex_1 = models.CharField(max_length=1000,null=True)
	complex_2 = models.CharField(max_length=1000,null=True)
	complex_p_value = models.CharField(max_length=100,null=True)
	complex_Y = models.CharField(max_length=10,null=True)

class Pathway(models.Model):
	type = models.CharField(max_length=100,null=False)
	pathway_type = models.CharField(max_length=100,null=False)
	gene_id_1 = models.CharField(max_length=100,null=True)
	gene_symbol_1 = models.CharField(max_length=100,null=True)
	gene_id_2 = models.CharField(max_length=100,null=True)
	gene_symbol_2 = models.CharField(max_length=100,null=True)
	Pathway_1 = models.CharField(max_length=1000,null=True)
	Pathway2 = models.CharField(max_length=1000,null=True)
	pathway_p_value = models.CharField(max_length=100,null=True)
	pathway_Y = models.CharField(max_length=10,null=True)

class Chemical(models.Model):
	int_type = models.CharField(max_length=100,null=False)
	gene_id = models.CharField(max_length=100,null=True)
	gene_symbol = models.CharField(max_length=100,null=True)
	chemical = models.CharField(max_length=100,null=True)
	score = models.CharField(max_length=100,null=True)
	source = models.CharField(max_length=100,null=True)
	tissue = models.CharField(max_length=100,null=True)
	chemical_Y = models.CharField(max_length=10,null=True)


class gene_tcga_alter_samples(models.Model):
	entrez_id = models.IntegerField(null=False)
	cancer = models.CharField(max_length=100)
	mutation = models.CharField(max_length=20480)
	amplication = models.CharField(max_length=20480)
	deletion = models.CharField(max_length=20480)


class TCGA_info(models.Model):
	gene1_id = models.IntegerField(null=False)
	gene2_id = models.IntegerField(null=False)
	gene1_symbol = models.CharField(max_length=100,null=True)
	gene2_symbol = models.CharField(max_length=100,null=True)
	cancer = models.CharField(max_length=1000, null=False)
	gene1_change = models.CharField(max_length=100,null=True)
	gene2_change = models.CharField(max_length=100,null=True)
	co_change = models.CharField(max_length=100,null=True)
	pvalue = models.CharField(max_length=100,null=True)
	exp_pvalue = models.CharField(max_length=100,null=True)
	meth_pvalue = models.CharField(max_length=100,null=True)




