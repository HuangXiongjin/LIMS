<template>
    <div class="container" style="position:relative;">
        <div class="fsz14px" style="backgroundColor:#fff;color:#666;textAlign:center;">排名环比</div>
        <div style="overflow:hidden;">
            <div style="height:300px;backgroundColor:#fff;" id="box2"></div>
        </div>
        <div class="mydateclass">
            <el-select v-model="weekdate">
                <el-option
                v-for="item in options"
                :key="item.value"
                :label="item.label"
                :value="item.value">
                </el-option> 
            </el-select>
        </div>
    </div>
</template>
<script>
import echarts from '@/assets/js/echarts.js'
let _ = require('lodash')
export default {
    data(){
            return {
                weekbar:null,
                weekdate:'周',
                options:[{ value: '年',label: '年'}, {value: '月',label: '月'},{value: '周',label: '周'}]
            }
    },
    props:['res1','res2'],
    mounted(){
        this.drawpic()
    },
     beforeDestroy(){
            this.weekbar.clear()
            this.weekbar.dispose()
            this.weekbar=null
      },
    methods: {
         drawpic() {
               this.weekbar=echarts.init(document.getElementById('box2'))
                var data1 =this.res1

                var data2 = this.res2
                // data = data.sort((a, b) => {
                //     return b.value - a.value
                // });
                var getArrByKey = (data, k) => {
                    let key = k || "value";
                    let res = [];
                    if (data) {
                        data.forEach(function(t) {
                            res.push(t[key]);
                        });
                    }
                    return res;
                };
                var opt = {
                    index: 0
                }
                // [起始最深颜色,结束的浅颜色]
                // colorLeft = ['#0CEBEA', '#368BFF'];
                var colorLeft = ['#00B0E2', '#00B0E2']
                var colorRight = ['#6BC616', '#6BC616']

                var option = {
                    legend : {
                                top: '1%',
                                left : '2%',
                                itemWidth : 18,
                                itemHeight : 10,
                                itemGap: 16,
                                orient: 'horizontal',
                                // icon : 'circle',
                                textStyle : {
                                    color : '#666',
                                    fontSize : 14,
                                },
                                data: ['本周', '上周']
                            },
                    grid: [{
                        show: false,
                        left: '2%',
                        top: '10%',
                        bottom: '8%',
                        width: '40%',

                    }, {
                        show: false,
                        left: '50%',
                        top: '10%',
                        bottom: '8%',
                        width: '0%',

                    }, {
                        show: false,
                        right: '2%',
                        top: '10%',
                        bottom: '8%',
                        width: '40%',
                    }],
                    tooltip: {
                        show: true,
                        // 设置  是否百分比
                        formatter: '{b} : {c}'
                    },
                    xAxis: [{
                            type: 'value',
                            inverse: true,
                            axisLine: {
                                show: true
                            },
                            axisTick: {
                                show: true
                            },
                            position: 'bottom',
                            axisLabel: {
                                show: true,
                                textStyle: {
                                    color: '#666'
                                }
                            },
                            splitLine: {
                                show: false
                            }
                        }, {
                            gridIndex: 1,
                            show: false,
                        },
                        {
                            gridIndex: 2,
                            show: true,
                            type: 'value',
                            inverse: false,
                            axisLine: {
                                show: true
                            },
                            axisTick: {
                                show: true
                            },
                            position: 'bottom',
                            axisLabel: {
                                show: true,
                                textStyle: {
                                    color: '#666'
                                }
                            },
                            splitLine: {
                                show: false
                            }
                        }
                    ],
                    yAxis: [{
                            gridIndex: 0,
                            triggerEvent: true,
                            show: true,
                            inverse: true,
                            data: getArrByKey(data1, 'name'),
                            axisLine: {
                                show: false
                            },
                            splitLine: {
                                show: false
                            },
                            axisTick: {
                                show: false
                            },
                            axisLabel: {
                                show: false
                            }
                        },
                        {
                            gridIndex: 1,
                            type: 'category',
                            inverse: true,
                            position: 'left',
                            axisLine: {
                                show: false
                            },
                            axisTick: {
                                show: false
                            },
                            axisLabel: {
                                show: true,
                                interval: 0,
                                align: 'auto',
                                verticalAlign: 'middle',
                                textStyle: {
                                    color: '#666',
                                    fontSize: 12,
                                    align: 'center',

                                },

                            },
                            data: getArrByKey(data1, 'name'),
                        },
                        {
                            gridIndex: 2,
                            triggerEvent: true,
                            show: true,
                            inverse: true,
                            data: getArrByKey(data2, 'name'),
                            axisLine: {
                                show: false
                            },
                            splitLine: {
                                show: false
                            },
                            axisTick: {
                                show: false
                            },
                            axisLabel: {
                                show: false,
                            }
                        }
                    ],
                    series: [

                        {
                            name: '本周',
                            type: 'bar',
                            gridIndex: 0,
                            showBackground: true,
                            backgroundStyle: {
                                barBorderRadius: 20,
                            },
                            xAxisIndex: 0,
                            yAxisIndex: 0,
                            data: data1,
                            barWidth: 15,
                            // barCategoryGap: '40%',
                            itemStyle: {
                                normal: {
                                    show: true,
                                    color: new echarts.graphic.LinearGradient(0, 0, 1, 0, [{
                                        offset: 0,
                                        color: colorLeft[0] //指0%处的颜色
                                    }, {
                                        offset: 1,
                                        color: colorLeft[1] //指100%处的颜色
                                    }], false),
                                    barBorderRadius: [10,0,0,10],

                                },
                            },

                            label: {
                                normal: {
                                    show: true,
                                    position: 'insideRight',
                                    textStyle: {
                                        color: '#ffffff',
                                        fontSize: '12'
                                    }
                                }
                            }
                        },
                        {
                            name: '上周',
                            type: 'bar',
                            xAxisIndex: 2,
                            yAxisIndex: 2,
                            gridIndex: 2,
                            showBackground: true,
                            backgroundStyle: {
                                barBorderRadius: 20,
                            },
                            data: data2,
                            barWidth: 15,
                            // barCategoryGap: '40%',
                            itemStyle: {
                                normal: {
                                    show: true,
                                    color: new echarts.graphic.LinearGradient(0, 0, 1, 0, [{
                                        offset: 0,
                                        color: colorRight[0] //指0%处的颜色
                                    }, {
                                        offset: 1,
                                        color: colorRight[1] //指100%处的颜色
                                    }], false),
                                    barBorderRadius: [0,5,5,0],

                                },
                            },
                            label: {
                                normal: {
                                    show: true,
                                    position: 'insideLeft',
                                    textStyle: {
                                        color: '#ffffff',
                                        fontSize: '12'
                                    }
                                }
                            }
                        }
                    ]
                };
               this.weekbar.setOption(option)
          }
    },
}
</script>
<style scoped>

</style>