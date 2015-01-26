

var option_rxrot_gauge = {
    tooltip : {
        formatter: "{a} <br/>{b} : {c}%"
    },
    toolbox: {
        show : false,
    },
    series : [
        {
            name : 'cosmos',
            type : 'gauge',
	    radius : '90%',
	    min : -120,
	    max : 120,
	    startAngle : 210,
	    endAngle : -30,
	    splitNumber : 6,
	    axisLine : {
		show : true,
		lineStyle : {
		    color: [
			[(-110 + 120)/240., '#aaaaaa'],
			[(-100 + 120)/240., '#f44336'],
			[(-90 + 120)/240.,  '#FF9800'],
			[(-80 + 120)/240.,  '#66BB6A'],
			[(0 + 120)/240.,    '#42A5F5'],
			[(80 + 120)/240.,   '#42A5F5'],
			[(90 + 120)/240.,   '#66BB6A'],
			[(100 + 120)/240.,  '#FF9800'],
			[(110 + 120)/240.,  '#f44336'],
			[(120 + 120)/240.,  '#aaaaaa'],
		    ],
		    width : 5,
		},
	    },
	    axisTick :{ splitNumber : 5 },
	    title : { show : false },
	    pointer : {
		width: 4,
		color: '#D7CCC8',
	    },
            detail : {
		formatter:'cosmos: {value}',
		textStyle : { fontSize : 15},
		offsetCenter: [0, '60%'],
	    },
            data:[{value: -0.0, name: 'cosmos'}]
        },
        {
            name : 'prog',
            type : 'gauge',
	    radius : '90%',
	    min : -120,
	    max : 120,
	    startAngle : 210,
	    endAngle : -30,
	    splitNumber : 6,
	    axisLine : {
		show : true,
		lineStyle : {
		    color: [
			[(-110 + 120)/240., '#aaaaaa'],
			[(-100 + 120)/240., '#f44336'],
			[(-90 + 120)/240.,  '#FF9800'],
			[(-80 + 120)/240.,  '#66BB6A'],
			[(0 + 120)/240.,    '#42A5F5'],
			[(80 + 120)/240.,   '#42A5F5'],
			[(90 + 120)/240.,   '#66BB6A'],
			[(100 + 120)/240.,  '#FF9800'],
			[(110 + 120)/240.,  '#f44336'],
			[(120 + 120)/240.,  '#aaaaaa'],
		    ],
		    width : 10,
		},
	    },
	    axisTick :{ splitNumber : 5 },
	    title : { show : false },
	    pointer : {
		width: 4,
		color: '#B0BEC5',
	    },
            detail : {
		formatter:'prog: {value}',
		textStyle : { fontSize : 15},
		offsetCenter: [0, '40%'],
	    },
            data:[{value: -0.0, name: 'prog'}]
        },
        {
            name : 'real',
            type : 'gauge',
	    radius : '90%',
	    min : -120,
	    max : 120,
	    startAngle : 210,
	    endAngle : -30,
	    splitNumber : 6,
	    axisLine : {
		show : true,
		lineStyle : {
		    color: [
			[(-110 + 120)/240., '#aaaaaa'],
			[(-100 + 120)/240., '#f44336'],
			[(-90 + 120)/240.,  '#FF9800'],
			[(-80 + 120)/240.,  '#66BB6A'],
			[(0 + 120)/240.,    '#42A5F5'],
			[(80 + 120)/240.,   '#42A5F5'],
			[(90 + 120)/240.,   '#66BB6A'],
			[(100 + 120)/240.,  '#FF9800'],
			[(110 + 120)/240.,  '#f44336'],
			[(120 + 120)/240.,  '#aaaaaa'],
		    ],
		    width : 10,
		},
	    },
	    axisTick :{ splitNumber : 5 },
	    title : { show : false },
	    pointer : {
		width: 4,
		color: '#424242',
	    },
            detail : {
		formatter:'real: {value}',
		textStyle : { fontSize : 15},
		offsetCenter: [0, '20%'],
	    },
            data:[{value: -0.0, name: 'real'}]
        }
    ]
};


