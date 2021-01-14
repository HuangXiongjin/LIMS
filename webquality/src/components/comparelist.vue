<template>
    <div class="container">
        <div class="fsz14px" style="backgroundColor:#0E2A43;color:#fff;textAlign:center;">原料质检排名及完成情况</div>
        <div style="overflow:hidden;">
            <div style="height:300px;backgroundColor:#0E2A43;" id="box4"></div>
        </div>
    </div>
</template>
<script>
import echarts from '@/assets/js/echarts.js'
export default {
    data(){
            return {
                comparelist:null
            }
    },
    mounted(){
        this.drawpic()
    },
     beforeDestroy(){
            this.comparelist.clear()
            this.comparelist.dispose()
            this.comparelist=null
      },
    methods: {
         drawpic() {
               this.comparelist=echarts.init(document.getElementById('box4'))
               var colorArray = [
                    {
                        top: '#ffa800', //黄
                        bottom: 'rgba(11,42,84,.3)'
                    }, {
                        top: '#1ace4a', //绿
                        bottom: 'rgba(11,42,84, 0.3)'
                    },
                    {
                        top: '#4bf3ff', //蓝
                        bottom: 'rgba(11,42,84,.3)'
                    }, {
                        top: '#4f9aff', //深蓝
                        bottom: 'rgba(11,42,84,.3)'
                    },
                    {
                        top: '#b250ff', //粉
                        bottom: 'rgba(11,42,84,.3)'
                    }
                ];
                var option = {
                    backgroundColor: '#0E2A43',
                    tooltip: {
                        show: true,
                        formatter: "{b}:{c}"
                        },
                grid: {
                        left: '5%',
                        top: '12%',
                        right: '1%',
                        bottom: '8%',
                        containLabel: true
                        },
                
                    xAxis: {
                        type: 'value',
                        show:false,
                        position: 'top',
                        axisTick: {
                            show: false
                        },
                        axisLine: {
                            show: false,
                            lineStyle: {
                                color: '#fff',
                            }
                        },
                        splitLine: {
                            show: false
                        },
                    },
                    yAxis: [{
                            type: 'category',
                            axisTick: {
                                show: false,
                                alignWithLabel: false,
                                length: 5,

                            },
                            "splitLine": { //网格线
                                "show": false
                            },
                            inverse: 'true', //排序
                            axisLine: {
                                show: false,
                                lineStyle: {
                                    color: '#fff',
                                }
                            },
                            data: ['原料A', '原料B', '原料C', '原料D', '原料E']
                        }

                    ],
                    series: [{
                            name: '能耗值',
                            type: 'bar',
                                label: {
                                normal: {
                                show: true,
                                position: 'right',
                                formatter: '{c}',
                                textStyle: {
                                    color: 'white' //color of value
                                }
                                }
                            },
                            itemStyle: {
                                normal: {
                                    show: true,
                                    color: function(params) {
                                        let num = colorArray.length;
                                        return {
                                            type: 'linear',
                                            colorStops: [{
                                                offset: 0,
                                                color: colorArray[params.dataIndex % num].bottom
                                            }, {
                                                offset: 1,
                                                color: colorArray[params.dataIndex % num].top
                                            }, {
                                                offset: 0,
                                                color: colorArray[params.dataIndex % num].bottom
                                            }, {
                                                offset: 1,
                                                color: colorArray[params.dataIndex % num].top
                                            }, {
                                                offset: 0,
                                                color: colorArray[params.dataIndex % num].bottom
                                            }, {
                                                offset: 1,
                                                color: colorArray[params.dataIndex % num].top
                                            }, {
                                                offset: 0,
                                                color: colorArray[params.dataIndex % num].bottom
                                            }, {
                                                offset: 1,
                                                color: colorArray[params.dataIndex % num].top
                                            }, {
                                                offset: 0,
                                                color: colorArray[params.dataIndex % num].bottom
                                            }, {
                                                offset: 1,
                                                color: colorArray[params.dataIndex % num].top
                                            }, {
                                                offset: 0,
                                                color: colorArray[params.dataIndex % num].bottom
                                            }, {
                                                offset: 1,
                                                color: colorArray[params.dataIndex % num].top
                                            }],
                                            //globalCoord: false
                                        }
                                    },
                                    barBorderRadius: 50,
                                    borderWidth: 0,
                                    borderColor: '#333',
                                }
                            },
                            barGap: '0%',
                            barCategoryGap: '60%',
                            data: [60, 132, 89, 134, 60]
                        }

                    ]
                };
               this.comparelist.setOption(option)
          }
    },
}
</script>
<style scoped>

</style>