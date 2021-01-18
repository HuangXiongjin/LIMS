<template>
    <div class="container is-current" style="backgroundColor:#fff;">
        <div class="box" style="height:180px;backgroundColor:#fff;" id="box9"></div>
    </div>
</template>
<script>
import echarts from '@/assets/js/echarts.js'
export default {
    data(){
            return {
                comparePie:null
            }
    },
    props:['toptitle','comment','startvalue','stopvalue'],
    mounted(){
        this.drawpic(this.comment,this.startvalue,this.stopvalue)
    },
     beforeDestroy(){
            this.comparePie.clear()
            this.comparePie.dispose()
            this.comparePie=null
      },
    methods: {
         drawpic(comment,startvalue,stopvalue) {
               this.comparePie=echarts.init(document.getElementById('box9'))
               let index = 0;
               var colorList = ['#73DDFF', '#73ACFF', '#FDD56A', '#FDB36A', '#FD866A', '#9E87FF', '#58D5FF'];
               var option = {
                    title: {
                        text: '占比分析',
                        x: 'center',
                        y: 'center',
                        textStyle: {
                            fontSize: 16
                        }
                    },
                    tooltip: {
                        trigger: 'item',
                        borderColor: 'rgba(255,255,255,.3)',
                        backgroundColor: 'rgba(13,5,30,.6)',
                        borderWidth: 1,
                        padding: 5,
                        formatter: function(parms) {
                        var str = parms.marker + "" + parms.data.name + "</br>" +
                        "数量：" + parms.data.value + "件</br>" +
                        "占比：" + parms.percent + "%";
                        return str;
                        }
                    },
                    series: [{
                        type: 'pie',
                        center: ['50%', '50%'],
                        radius: ['65%', '90%'],
                        clockwise: true,
                        avoidLabelOverlap: true,
                        hoverOffset: 20,
                        emphasis:{
                            itemStyle:{
                                borderColor: '#f3f3f3',
                                borderWidth: 10
                            }
                        },
                        itemStyle: {
                            normal: {
                                color: function(params) {
                                    return colorList[params.dataIndex]
                                }
                            }
                        },
                        label: {
                            show: false,
                            position: 'inner',
                            formatter: '{a|{b}：{d}%}\n{hr|}',
                            rich: {
                                hr: {
                                    backgroundColor: 't',
                                    borderRadius: 3,
                                    width: 3,
                                    height: 3,
                                    padding: [3, 3, 0, -12]
                                },
                                a: {
                                    padding: [-30, 15, -20, 15]
                                }
                            }
                        },
                        labelLine: {
                            normal: {
                                length: 20,
                                length2: 30,
                                lineStyle: {
                                    width: 1
                                }
                            }
                        },
                        data: [{
                            'name': '物料A',
                            'value': 56
                        }, {
                            'name': '物料B',
                            'value': 36
                        }, {
                            'name': '物料C',
                            'value': 15
                        }, {
                            'name': '物料D',
                            'value': 20
                        }, {
                            'name': '物料E',
                            'value': 89
                        }, {
                            'name': '物料F',
                            'value': 40
                        }],
                    }]
                };
               this.comparePie.setOption(option)
          }
    },
}
</script>
<style scoped>

</style>