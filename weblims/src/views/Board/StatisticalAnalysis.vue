<template>
    <el-row :gutter="20" class="container" :style="conheight">
        <el-col :span='12' style="height:45%;" class="mgb24"><div class="box" id='box'></div></el-col>
        <el-col :span='12' style="height:45%;" class="mgb24"><div class="box">2</div></el-col>
        <el-col :span='12' style="height:50%;"><div class="box">2</div></el-col>
        <el-col :span='12' style="height:50%;"><div class="box">2</div></el-col>
    </el-row>
</template>
<script>
import echarts from '@/assets/js/echarts.js'
export default {
    data(){

        return {
           msg:'12',
           conheight:{
               height:''
           }
        }
    },
    created(){
        window.addEventListener('resize', this.getHeight);
        this.getInitHeight()
    },
    mounted(){
        this.drawpic()
    },
    beforeDestroy(){
        if(this.myecharts){
            this.myecharts.clear()
            this.myecharts.dispose()
            this.myecharts=null
        }
    },
    methods: {
        getInitHeight(){
            this.conheight.height=(window.innerHeight-160)+'px'
        },
         drawpic(){
            if(this.myecharts){
                this.myecharts.clear()
                this.myecharts.dispose()
                this.myecharts=null
            }
            this.myecharts=echarts.init(document.getElementById('box'))
            var xData = ["取样", "审核", "质检","质检审核"];
            var yData = [22, 30, 45,20];
            var option = {
                backgroundColor: '#061326',
                "grid": {
                    "top": "15%",
                    "left": "-5%",
                    "bottom": "5%",
                    "right": "5%",
                    "containLabel": true
                },
                tooltip:{
                show:true 
                },
                animation: false,
                "xAxis": [{
                    "type": "category",
                    "data": xData,
                    "axisTick": {
                        "alignWithLabel": true
                    },
                    "nameTextStyle": {
                        "color": "#82b0ec"
                    },
                    "axisLine": {
                        show: false,
                        "lineStyle": {
                            "color": "#82b0ec"
                        }
                    },
                    "axisLabel": {
                        "textStyle": {
                            "color": "#fff"
                        },
                        margin: 30
                    }
                }],
                "yAxis": [{
                    show: false,
                    "type": "value",
                    "axisLabel": {
                        "textStyle": {
                            "color": "#fff"
                        },
                    },
                    "splitLine": {
                        "lineStyle": {
                            "color": "#0c2c5a"
                        }
                    },
                    "axisLine": {
                        "show": false
                    }
                }],
                "series": [{
                        "name": "",
                        type: 'pictorialBar',
                        symbolSize: [40, 10],
                        symbolOffset: [0, -6],
                        symbolPosition: 'end',
                        z: 12,
                        // "barWidth": "0",
                        "label": {
                            "normal": {
                                "show": true,
                                "position": "top",
                                // "formatter": "{c}%"
                                fontSize: 25,
                                fontWeight: 'bold',
                                color: '#34DCFF'
                            }
                        },
                        color: "#2DB1EF",
                        data: yData
                    },
                    {
                        name: '',
                        type: 'pictorialBar',
                        symbolSize: [40, 10],
                        symbolOffset: [0, 7],
                        // "barWidth": "20",
                        z: 12,
                        "color": "#2DB1EF",
                        "data": yData
                    },
                    {
                        name: '',
                        type: 'pictorialBar',
                        symbolSize: [50, 15],
                        symbolOffset: [0, 12],
                        z: 10,
                        itemStyle: {
                            normal: {
                                color: 'transparent',
                                borderColor: '#2EA9E5',
                                borderType: 'solid',
                                borderWidth: 1
                            }
                        },
                        data: yData
                    },
                    {
                        name: '',
                        type: 'pictorialBar',
                        symbolSize: [70, 20],
                        symbolOffset: [0, 18],
                        z: 10,
                        itemStyle: {
                            normal: {
                                color: 'transparent',
                                borderColor: '#19465D',
                                borderType: 'solid',
                                borderWidth: 2
                            }
                        },
                        data: yData
                    },
                    {
                        type: 'bar',
                        //silent: true,
                        "barWidth": "40",
                        barGap: '10%', // Make series be overlap
                        barCateGoryGap: '10%',
                        itemStyle: {
                            normal: {
                                color: new echarts.graphic.LinearGradient(0, 0, 0, 0.7, [{
                                        offset: 0,
                                        color: "#38B2E6"
                                    },
                                    {
                                        offset: 1,
                                        color: "#0B3147"
                                    }
                                ]),
                                opacity: .8
                            },
                        },
                        data: yData
                    }
                ]
            };
            this.myecharts.setOption(option)
        }
    },
}
</script>
<style scoped>
  .box{
      background-color:#ccc;
      height: 100%;
  }
</style>