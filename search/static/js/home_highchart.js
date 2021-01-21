var chart = Highcharts.chart('home_highchart', {
	chart: {
		type: 'bar'
	},
	title: {
		text: 'SL/SV Number'
	},
	xAxis: {
		categories: ['Bile Duct', 'Bladder', 'Blood', 'Bone', 'Bone Marrow', 'Brain', 'Breast', 'Cervix', 'Colorectal', 'Esophagus', 'Head and Neck', 'kidney', 'Liver', 'Lung', 'Lymph Nodes', 'Nervous System', 'Ovary', 'Pancreas', 'Pleura', 'Prostate', 'Skin', 'Soft Tissue', 'Stomach', 'Thyroid', 'Uterus']
	},
	yAxis: {
		min: 0,
		title: {
			text: 'SL/SV'
		}
	},
	legend: {
		/* 图例显示顺序反转
         * 这是因为堆叠的顺序默认是反转的，可以设置
         * yAxis.reversedStacks = false 来达到类似的效果
         */
		reversed: true
	},
	plotOptions: {
		series: {
			stacking: 'normal'
		}
	},
	series: [{
		name: 'SL',
		data: [11, 238, 166, 229, 13, 2, 2195, 109, 1672, 338, 12, 310, 216, 861, 979, 2310, 469, 288, 8, 31, 505, 96, 347, 81, 257]
	}, {
		name: 'SV',
		data: [0, 451, 81, 62, 0, 0, 1193, 0, 2215, 542, 0, 847, 225, 2286, 1880, 1298, 856, 658, 18, 0, 1233, 190, 1054, 80, 239]
	}]
});