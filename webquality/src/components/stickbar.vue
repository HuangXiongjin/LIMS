<template>
    <div class="container">
        <div class="fsz14px" style="backgroundColor:#fff;color:#666;textAlign:center;">{{res3}}质检数量对比</div>
        <div style="overflow:hidden;">
            <div style="height:300px;backgroundColor:#fff;" id="box3"></div>
        </div>
    </div>
</template>
<script>
import echarts from '@/assets/js/echarts.js'
export default {
    data(){
            return {
                stickbar:null
            }
    },
    props:['res1','res2','xdate','res3'],
    mounted(){
        this.drawpic()
    },
     beforeDestroy(){
            this.stickbar.clear()
            this.stickbar.dispose()
            this.stickbar=null
      },
    methods: {
         drawpic() {
               this.stickbar=echarts.init(document.getElementById('box3'))
               var option = {
                    backgroundColor: '#fff',
                    tooltip: { //提示框组件
                        trigger: 'axis',
                        formatter: '{b}<br />{a0}: {c0}<br />{a1}: {c1}',
                        axisPointer: {
                            type: 'shadow',
                            label: {
                                backgroundColor: '#6a7985'
                            }
                        },
                        textStyle: {
                            color: '#fff',
                            fontStyle: 'normal',
                            fontFamily: '微软雅黑',
                            fontSize: 12,
                        }
                    },
                    grid: {
                        left: '10%',
                        right: '10%',
                        bottom: '10%',
                        top:'15%',
                    //	padding:'0 0 10 0',
                        containLabel: true,
                    },
                    legend: {//图例组件，颜色和名字
                        right:'10%',
                        top:'5%',
                        itemGap: 16,
                        itemWidth: 18,
                        itemHeight: 10,
                        data:[{
                            name:'物料A',
                            //icon:'image://../wwwroot/js/url2.png', //路径
                        },
                        {
                            name:'物料B',
                        }],
                        textStyle: {
                            color: '#a8aab0',
                            fontStyle: 'normal',
                            fontFamily: '微软雅黑',
                            fontSize: 12,            
                        }
                    },
                    xAxis: [
                        {
                            type: 'category',
                        //	boundaryGap: true,//坐标轴两边留白
                            data: this.xdate,
                            axisLabel: { //坐标轴刻度标签的相关设置。
                        //		interval: 0,//设置为 1，表示『隔一个标签显示一个标签』
                            //	margin:15,
                                textStyle: {
                                    color: '#078ceb',
                                    fontStyle: 'normal',
                                    fontFamily: '微软雅黑',
                                    fontSize: 12,
                                },
                                // rotate:50,
                            },
                            axisTick:{//坐标轴刻度相关设置。
                                show: false,
                            },
                            axisLine:{//坐标轴轴线相关设置
                                lineStyle:{
                                    color:'#fff',
                                    opacity:0.2
                                }
                            },
                            splitLine: { //坐标轴在 grid 区域中的分隔线。
                                show: false,
                            }
                        }
                    ],
                    yAxis: [
                        {
                            type: 'value',
                            splitNumber: 5,
                            axisLabel: {
                                textStyle: {
                                    color: 'skyblue',
                                    fontStyle: 'normal',
                                    fontFamily: '微软雅黑',
                                    fontSize: 12,
                                }
                            },
                            axisLine:{
                                show: false
                            },
                            axisTick:{
                                show: false
                            },
                            splitLine: {
                                show: true,
                                lineStyle: {
                                    color: ['#fff'],
                                    opacity:0.3
                                }
                            }
                        }
                    ],
                    series : [
                        {
                            name:'物料A',
                            type:'bar',
                            data:this.res1,
                            barWidth: 10,
                            barGap:0,//柱间距离
                            itemStyle: {
                                    normal: {
                                        show: true,
                                        color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [{
                                            offset: 0,
                                            color: '#5768EF'
                                        }, {
                                            offset: 1,
                                            color: '#5768EF'
                                        }]),
                                        barBorderRadius: 50,
                                        borderWidth: 0,
                                    }
                                },
                            },
                            {
                            name:'物料B',
                            type:'bar',
                            data:this.res2,
                            barWidth: 10,
                            barGap:0,//柱间距离
                            itemStyle: {
                                normal: {
                                    show: true,
                                    color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [{
                                        offset: 0,
                                        color: '#69CBF2'
                                    }, {
                                        offset: 1,
                                        color: '#69CBF2'
                                    }]),
                                    barBorderRadius: 50,
                                    borderWidth: 0,
                                }
                            },
                        }
                    ]
                };
               this.stickbar.setOption(option)
          }
    },
}
</script>
<style scoped>
    
</style>