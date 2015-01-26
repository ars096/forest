

var myChart = echarts.init(document.getElementById('status-motor-rxrot-gauge'));
myChart.setOption(option_rxrot_gauge);

/*
var spana1 = echarts.init(document.getElementById('status-spana-1'));
var spana2 = echarts.init(document.getElementById('status-spana-2'));
var spana3 = echarts.init(document.getElementById('status-spana-3'));
var spana4 = echarts.init(document.getElementById('status-spana-4'));
spana1.setOption(option_spana1);
spana2.setOption(option_spana2);
spana3.setOption(option_spana3);
spana4.setOption(option_spana4);
*/

var spana1 = echarts.init(document.getElementById('graph'));
spana1.setOption(option_spana1);

refresh();


function refresh() {
    var connection = check_connection();
    if (check_connection == false) { return; }
    
    update_timestamp();
    update_status();
    update_temperature();
    update_loatt();
    update_sis();
    update_rxrot();
    update_slider();
    update_switch();
    update_losg();
    //update_spana();
    
    setTimeout("refresh()", 1000);
}

function check_connection(){
    var req = new XMLHttpRequest();
    req.open("GET", "/database/show_tables/csv", false);
    req.send();
    if (req.readyState == 4 && req.status == 200) { return true; }
    else { return false; }
}

function update_timestamp(){
    var d = new Date();
    var year = d.getFullYear();
    var month = d.getMonth() + 1;
    var day = d.getDate();
    var hour = ("00" + d.getHours()).substr(-2);
    var minute = ("00" + d.getMinutes()).substr(-2);
    var sec = ("00" + d.getSeconds()).substr(-2);
    
    yyyymmdd = "" + year + "/" + month + "/" + day;
    hhmmss = "" + hour + ":" + minute + ":" + sec
    
    document.getElementById("header-timestamp-date").textContent = yyyymmdd;
    document.getElementById("header-timestamp-time").textContent = hhmmss;
}

function set_latest(table, func){
    var req = new XMLHttpRequest();
    req.open("GET", "/database/latest/"+ table +"/1/json");
    req.send();
    
    req.onreadystatechange = function() {
	if (req.readyState == 4 && req.status == 200) {
	    var ret = JSON.parse(req.responseText);
	    func(ret[0]);
	}
    }   
}

function update_status(){
    var set_status = function(d){
	status = "" + d[2]
	action = "" + d[3]
	
	document.getElementById("status-operation").textContent = action;
    }
    
    set_latest("operation_log", set_status);
}

function update_sis(){
    var set_sis = function(d){
	v1 = ("" + d[2]).substr(0, 4) + " mV"
	i1 = ("" + d[3]).substr(0, 5) + " uA"
	v2 = ("" + d[4]).substr(0, 4) + " mV"
	i2 = ("" + d[5]).substr(0, 5) + " uA"
	v3 = ("" + d[6]).substr(0, 4) + " mV"
	i3 = ("" + d[7]).substr(0, 5) + " uA"
	v4 = ("" + d[8]).substr(0, 4) + " mV"
	i4 = ("" + d[9]).substr(0, 5) + " uA"
	v5 = ("" + d[10]).substr(0, 4) + " mV"
	i5 = ("" + d[11]).substr(0, 5) + " uA"
	v6 = ("" + d[12]).substr(0, 4) + " mV"
	i6 = ("" + d[13]).substr(0, 5) + " uA"
	v7 = ("" + d[14]).substr(0, 4) + " mV"
	i7 = ("" + d[15]).substr(0, 5) + " uA"
	v8 = ("" + d[16]).substr(0, 4) + " mV"
	i8 = ("" + d[17]).substr(0, 5) + " uA"
	v9 = ("" + d[18]).substr(0, 4) + " mV"
	i9 = ("" + d[19]).substr(0, 5) + " uA"
	v10 = ("" + d[20]).substr(0, 4) + " mV"
	i10 = ("" + d[21]).substr(0, 5) + " uA"
	v11 = ("" + d[22]).substr(0, 4) + " mV"
	i11 = ("" + d[23]).substr(0, 5) + " uA"
	v12 = ("" + d[24]).substr(0, 4) + " mV"
	i12 = ("" + d[25]).substr(0, 5) + " uA"
	v13 = ("" + d[26]).substr(0, 4) + " mV"
	i13 = ("" + d[27]).substr(0, 5) + " uA"
	v14 = ("" + d[28]).substr(0, 4) + " mV"
	i14 = ("" + d[29]).substr(0, 5) + " uA"
	v15 = ("" + d[30]).substr(0, 4) + " mV"
	i15 = ("" + d[31]).substr(0, 5) + " uA"
	v16 = ("" + d[32]).substr(0, 4) + " mV"
	i16 = ("" + d[33]).substr(0, 5) + " uA"

	document.getElementById("status-sis-v1").textContent = v1;
	document.getElementById("status-sis-i1").textContent = i1;
	document.getElementById("status-sis-v2").textContent = v2;
	document.getElementById("status-sis-i2").textContent = i2;
	document.getElementById("status-sis-v3").textContent = v3;
	document.getElementById("status-sis-i3").textContent = i3;
	document.getElementById("status-sis-v4").textContent = v4;
	document.getElementById("status-sis-i4").textContent = i4;
	document.getElementById("status-sis-v5").textContent = v5;
	document.getElementById("status-sis-i5").textContent = i5;
	document.getElementById("status-sis-v6").textContent = v6;
	document.getElementById("status-sis-i6").textContent = i6;
	document.getElementById("status-sis-v7").textContent = v7;
	document.getElementById("status-sis-i7").textContent = i7;
	document.getElementById("status-sis-v8").textContent = v8;
	document.getElementById("status-sis-i8").textContent = i8;
	document.getElementById("status-sis-v9").textContent = v9;
	document.getElementById("status-sis-i9").textContent = i9;
	document.getElementById("status-sis-v10").textContent = v10;
	document.getElementById("status-sis-i10").textContent = i10;
	document.getElementById("status-sis-v11").textContent = v11;
	document.getElementById("status-sis-i11").textContent = i11;
	document.getElementById("status-sis-v12").textContent = v12;
	document.getElementById("status-sis-i12").textContent = i12;
	document.getElementById("status-sis-v13").textContent = v13;
	document.getElementById("status-sis-i13").textContent = i13;
	document.getElementById("status-sis-v14").textContent = v14;
	document.getElementById("status-sis-i14").textContent = i14;
	document.getElementById("status-sis-v15").textContent = v15;
	document.getElementById("status-sis-i15").textContent = i15;
	document.getElementById("status-sis-v16").textContent = v16;
	document.getElementById("status-sis-i16").textContent = i16;
    }
    
    set_latest("sis_bias", set_sis);
}

function update_loatt(){
    var set_att = function(d){
	att1 = ("" + d[2]).substr(0,5) + " mA"
	att2 = ("" + d[3]).substr(0,5) + " mA"
	att3 = ("" + d[4]).substr(0,5) + " mA"
	att4 = ("" + d[5]).substr(0,5) + " mA"
	att5 = ("" + d[6]).substr(0,5) + " mA"
	att6 = ("" + d[7]).substr(0,5) + " mA"
	att7 = ("" + d[8]).substr(0,5) + " mA"
	att8 = ("" + d[9]).substr(0,5) + " mA"
	att9 = ("" + d[10]).substr(0,5) + " mA"
	
	document.getElementById("status-loatt-1").textContent = att1;
	document.getElementById("status-loatt-2").textContent = att2;
	document.getElementById("status-loatt-3").textContent = att3;
	document.getElementById("status-loatt-4").textContent = att4;
	document.getElementById("status-loatt-5").textContent = att5;
	document.getElementById("status-loatt-6").textContent = att6;
	document.getElementById("status-loatt-7").textContent = att7;
	document.getElementById("status-loatt-8").textContent = att8;
	document.getElementById("status-loatt-9").textContent = att9;
    }
    
    set_latest("lo_att", set_att);
}

function update_temperature(){
    var set_temp = function(d){
	t1 = ("" + d[3]).substr(0,5) + " K"
	t2 = ("" + d[6]).substr(0,5) + " K"
	t3 = ("" + d[9]).substr(0,5) + " K"
	t4 = ("" + d[12]).substr(0,5) + " K"
	t5 = ("" + d[15]).substr(0,5) + " K"
	t6 = ("" + d[18]).substr(0,5) + " K"
	document.getElementById("status-temp-1").textContent = t1;
	document.getElementById("status-temp-2").textContent = t2;
	document.getElementById("status-temp-3").textContent = t3;
	document.getElementById("status-temp-4").textContent = t4;
	document.getElementById("status-temp-5").textContent = t5;
	document.getElementById("status-temp-6").textContent = t6;
    }
    
    set_latest("dewar_temp", set_temp);
}


function update_rxrot(){
    var set_rxrot = function(d){
	real = "" + d[2]
	prog = "" + d[4]
	cosmos = "" + d[5]
	document.getElementById("status-rxrot-real").textContent = real;
	document.getElementById("status-rxrot-prog").textContent = prog;
	document.getElementById("status-rxrot-cosmos").textContent = cosmos;
	
	option_rxrot_gauge.series[0].data[0].value = 0.0 + cosmos
	option_rxrot_gauge.series[1].data[0].value = 0.0 + prog
	option_rxrot_gauge.series[2].data[0].value = 0.0 + real
	
	myChart.setOption(option_rxrot_gauge);

    }
    
    set_latest("rxrot_status", set_rxrot);
}

function update_slider(){
    var set_slider = function(d){
	position = "" + d[2]
	count = "" + d[3]
	document.getElementById("status-slider-position").textContent = position;
	document.getElementById("status-slider-count").textContent = count;	
    }
    
    set_latest("slider_status", set_slider);
}

function update_switch(){
    var set_switch = function(d){
	ch1 = "" + d[2]
	ch2 = "" + d[3]
	ch3 = "" + d[4]
	ch4 = "" + d[5]
	document.getElementById("status-switch-1").textContent = ch1;
	document.getElementById("status-switch-2").textContent = ch2;
	document.getElementById("status-switch-3").textContent = ch3;
	document.getElementById("status-switch-4").textContent = ch4;
    }
    
    set_latest("IF_switch", set_switch);
}

function update_losg(){
    var set_losg = function(d){
	freq1 = "" + ((0.0 + d[2]) / 1e9) + " GHz"
	power1 = "" + d[3] + " dBm"
	if (d[4] == 1){ output1 = "ON"; }
	else{ output1 = "OFF"; }
	freq2 = "" + ((0.0 + d[5]) / 1e9) + " GHz"
	power2 = "" + d[6] + " dBm"
	if (d[7] == 1){ output2 = "ON"; }
	else{ output2 = "OFF"; }
	document.getElementById("status-losg1-freq").textContent = freq1;
	document.getElementById("status-losg1-power").textContent = power1;
	document.getElementById("status-losg1-output").textContent = output1;
	document.getElementById("status-losg2-freq").textContent = freq2;
	document.getElementById("status-losg2-power").textContent = power2;
	document.getElementById("status-losg2-output").textContent = output2;
    }
    
    set_latest("lo_sg", set_losg);
}

function update_spana(){
    var set_spana = function(d){
	ch1 = "" + d[2]
	ch2 = "" + d[3]
	ch3 = "" + d[4]
	ch4 = "" + d[5]
	
	option_spana.series[0].data = ch1;
	spana1.setOption(option_spana)
	
	option_spana.series[0].data = ch2;
	spana2.setOption(option_spana)
	
	option_spana.series[0].data = ch3;
	spana3.setOption(option_spana)
	
	option_spana.series[0].data = ch4;
	spana4.setOption(option_spana)
    }
    
    set_latest("spana", set_spana);
}

